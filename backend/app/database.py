from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from typing import Generator # Added for type hinting the generator function
from .config import DATABASE_URL


## ⚙️ Database Setup

# 1. Create the SQLAlchemy Engine
# The engine manages the connection to the database specified by DATABASE_URL.
engine = create_engine(DATABASE_URL)

# 2. Create a configured Session class
# SessionLocal is used to create individual database sessions.
SessionLocal = sessionmaker(
    autocommit=False,  # Don't commit automatically after every change
    autoflush=False,   # Don't flush changes to the DB automatically before every query
    bind=engine        # Bind the session to the created engine
)

# 3. Define the Declarative Base
# Base is the base class for all your SQLAlchemy models (classes/tables).
Base = declarative_base()


## 🛠️ Dependency Helper

def get_db() -> Generator[SessionLocal, None, None]:
    """
    A dependency injection function to manage database sessions.
    
    It creates a new session, yields it to the calling function, 
    and ensures the session is closed afterward, even if errors occur.
    
    This is typically used in FastAPI dependencies.
    """
    db = SessionLocal()
    try:
        # Yield the database session object
        yield db
    finally:
        # Close the session after the request is finished
        db.close()