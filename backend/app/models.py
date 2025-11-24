from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql import func
from .database import Base


class User(Base):
    """
    SQLAlchemy model for the 'users' table.
    """
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    name = Column(String, nullable=True)
    picture = Column(String, nullable=True)
    refresh_token = Column(String, nullable=True)
    last_login = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now()
    )