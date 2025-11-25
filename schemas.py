from pydantic import BaseModel
from typing import Optional


## 🔐 Authentication Models
class TokenResponse(BaseModel):
    """
    Response model for authentication, containing the access token.
    """
    access: str
    expires_in: int


class GoogleToken(BaseModel):
    """
    Model for receiving the Google OAuth token from the client.
    """
    token: str


## 👤 User Data Model
class UserOut(BaseModel):
    """
    Model for outputting basic user data (used for responses).
    """
    email: str
    name: Optional[str] = None
    picture: Optional[str] = None