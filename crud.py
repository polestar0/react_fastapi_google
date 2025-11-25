from sqlalchemy.orm import Session
from . import models
from typing import Optional # Added Optional for clarity in function signature

def get_user_by_email(db: Session, email: str) -> Optional[models.User]:
    """
    Retrieves a user from the database based on their email address.

    Args:
        db: The SQLAlchemy database session.
        email: The email address of the user to retrieve.

    Returns:
        The User object if found, otherwise None.
    """
    return db.query(models.User).filter(models.User.email == email).first()


def create_or_update_user(db: Session, email: str, name: str, picture: str, refresh_token: str) -> models.User:
    """
    Creates a new user if they don't exist, or updates an existing user's 
    name, picture, and refresh token.

    Args:
        db: The SQLAlchemy database session.
        email: The user's unique email (used for lookup).
        name: The user's name.
        picture: The URL of the user's profile picture.
        refresh_token: The new JWT refresh token.

    Returns:
        The created or updated User object.
    """
    # 1. Try to find the user by email
    user = get_user_by_email(db, email)

    if not user:
        # 2a. Create a new user if not found
        user = models.User(
            email=email,
            name=name,
            picture=picture,
            refresh_token=refresh_token
        )
        db.add(user)
    else:
        # 2b. Update the existing user's details
        user.name = name
        user.picture = picture
        user.refresh_token = refresh_token
        
    # 3. Commit changes (new user or update) and refresh the object
    db.commit()
    db.refresh(user)
    
    return user