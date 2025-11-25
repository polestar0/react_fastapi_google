from datetime import datetime, timedelta, timezone
from jose import jwt
from fastapi import HTTPException
from google.oauth2 import id_token
from google.auth.transport import requests as grequests

# Note: Assuming '4' in the original text was a stray character and removing it.
from .config import GOOGLE_CLIENT_ID, JWT_SECRET, ACCESS_EXPIRE_MINUTES, REFRESH_EXPIRE_DAYS

ALGORITHM = "HS256"

def verify_google_token(token: str):
    """Verifies a Google ID token and returns the payload (idinfo)."""
    try:
        # grequests.Request() is used for the transport mechanism
        idinfo = id_token.verify_oauth2_token(token, grequests.Request(), GOOGLE_CLIENT_ID)
        # idinfo contains email, name, picture, sub, etc.
        return idinfo
    except Exception as e:
        # Raise an HTTPException if the token is invalid or verification fails
        raise HTTPException(status_code=401, detail="Invalid Google token")

def create_access_token(subject: str):
    """Creates a JWT access token for a given subject (e.g., user ID)."""
    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_EXPIRE_MINUTES)
    payload = {"sub": subject, "exp": expire}
    
    # Encode the payload into a JWT
    token = jwt.encode(payload, JWT_SECRET, algorithm=ALGORITHM)
    
    # Return the token and its remaining lifetime in seconds
    return token, int((expire - datetime.now(timezone.utc)).total_seconds())

def create_refresh_token(subject: str):
    """Creates a JWT refresh token for a given subject (e.g., user ID)."""
    expire = datetime.now(timezone.utc) + timedelta(days=REFRESH_EXPIRE_DAYS)
    payload = {"sub": subject, "exp": expire}
    
    # Encode the payload into a JWT
    token = jwt.encode(payload, JWT_SECRET, algorithm=ALGORITHM)
    return token

def verify_local_token(token: str):
    """Decodes and verifies a locally issued JWT (access or refresh token)."""
    try:
        # Decode the token using the secret and algorithm
        payload = jwt.decode(token, JWT_SECRET, algorithms=[ALGORITHM])
        return payload
    except Exception:
        # Raise an HTTPException if the token is invalid, expired, or corrupted
        raise HTTPException(status_code=401, detail="Invalid token")