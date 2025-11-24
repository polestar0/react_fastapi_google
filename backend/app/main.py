import os # Add import for os, as it's often needed in FastAPI apps, even if not explicitly used here
from fastapi import FastAPI, Depends, Request, Response, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from . import config, schemas, crud, auth
from .database import get_db # Assuming get_db is in .database, based on previous context
from app import models
from app.database import engine

# Initialize the FastAPI application
app = FastAPI()

# --- CORS Middleware Setup ---
app.add_middleware(
    CORSMiddleware,
    # Allow requests from the specified frontend origin
    allow_origins=[config.FRONTEND_ORIGIN],
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods
    allow_headers=["*"],  # Allow all headers
)

# Constant for the refresh token cookie name
REFRESH_COOKIE_NAME = "refresh_token"

models.Base.metadata.create_all(bind=engine)

@app.post("/api/google-login", response_model=schemas.TokenResponse)
def google_login(
    payload: schemas.GoogleToken, 
    response: Response, 
    db: Session = Depends(get_db)
):
    """
    Handles Google OAuth login: verifies the token, creates/updates the user, 
    and sets access/refresh tokens.
    """
    try:
        # 1. Verify the incoming Google ID token
        idinfo = auth.verify_google_token(payload.token)
    except HTTPException as e:
        # Re-raise the exception if token verification failed
        raise e
        
    email = idinfo.get("email")
    name = idinfo.get("name")
    picture = idinfo.get("picture")

    # 2. Create a local refresh token and store it in the database
    refresh = auth.create_refresh_token(email)
    user = crud.create_or_update_user(
        db, 
        email=email, 
        name=name, 
        picture=picture, 
        refresh_token=refresh
    )

    # 3. Create a short-lived access token
    access, expires_in = auth.create_access_token(email)

    # 4. Set the HTTP-only cookie for the refresh token (secure storage)
    response.set_cookie(
        key=REFRESH_COOKIE_NAME,
        value=refresh,
        httponly=True,  # Prevents client-side JavaScript access
        max_age=60 * 60 * 24 * config.REFRESH_EXPIRE_DAYS, # Max age in seconds
        samesite="lax", # Good default for cross-site cookie behavior
        secure=False,   # Set to True in production with HTTPS
    )

    # 5. Return the short-lived access token to the client
    return {"access": access, "expires_in": expires_in}


@app.post("/api/refresh", response_model=schemas.TokenResponse)
def refresh_token(request: Request, response: Response, db: Session = Depends(get_db)):
    """
    Refreshes the access token using the refresh token stored in an HTTP-only cookie.
    """
    # 1. Get the refresh token from the cookie
    token = request.cookies.get(REFRESH_COOKIE_NAME)
    if not token:
        raise HTTPException(status_code=401, detail="No refresh token found in cookies")

    # 2. Decode the refresh token locally
    try:
        payload = auth.verify_local_token(token)
    except HTTPException:
        raise HTTPException(status_code=401, detail="Invalid refresh token format or expiration")

    email = payload.get("sub")

    # 3. Cross-check the token with the one stored in the database for validity
    user = crud.get_user_by_email(db, email)
    if not user or user.refresh_token != token:
        # Invalidate if user doesn't exist or token doesn't match DB (stale token)
        raise HTTPException(status_code=401, detail="Invalid or revoked refresh token")

    # 4. If valid, issue a new short-lived access token
    access, expires_in = auth.create_access_token(email)
    return {"access": access, "expires_in": expires_in}


@app.get("/api/me", response_model=schemas.UserOut)
def get_current_user_details(request: Request, db: Session = Depends(get_db)):
    """
    Retrieves the current authenticated user's details using the Access Token
    from the Authorization header.
    """
    # 1. Extract the Authorization header
    auth_header = request.headers.get("authorization")
    if not auth_header:
        raise HTTPException(status_code=401, detail="Missing Authorization header")
        
    # 2. Parse the Bearer scheme and token
    scheme, _, token = auth_header.partition(" ")
    if scheme.lower() != "bearer" or not token:
        raise HTTPException(status_code=401, detail="Invalid Authorization header format (must be 'Bearer <token>')")

    # 3. Verify the access token
    try:
        payload = auth.verify_local_token(token)
    except HTTPException:
        # This handles token expiration or invalid signature
        raise HTTPException(status_code=401, detail="Invalid or expired access token")
        
    email = payload.get("sub")
    
    # 4. Fetch user details from the database
    user = crud.get_user_by_email(db, email)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
        
    # 5. Return safe user data
    return {"email": user.email, "name": user.name, "picture": user.picture}