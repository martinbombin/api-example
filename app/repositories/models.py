"""SQLAlchemy ORM models for database schema definitions.

This module defines the `User` model and a declarative `Base` class used to
construct database tables. It includes field definitions and constraints for
user-related data.
"""

import uuid

from sqlalchemy import Column, String
from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    """Declarative base class for all ORM models.

    This is used by SQLAlchemy to track and map model classes to database tables.
    """


class User(Base):
    """ORM model representing a user in the system.

    Attributes:
        id (str): Unique identifier for the user (UUID string).
        username (str): The user's login username.
        full_name (str | None): The user's full name (optional).
        phone_number (str | None): The user's phone number (optional).
        email (str): The user's email address (must be unique).
        password (str): Hashed password for the user.

    """

    __tablename__ = "user"

    id = Column(
        String(36),
        primary_key=True,
        default=lambda: str(uuid.uuid4()),
    )
    username = Column(String(100), index=True)
    full_name = Column(String(100), nullable=True, default=None)
    phone_number = Column(String(30), nullable=True, default=None)
    email = Column(String(100), unique=True)
    password = Column(String(100))
