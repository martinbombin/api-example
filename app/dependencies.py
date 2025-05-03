"""Dependency injection utilities for application services and database sessions.

This module defines reusable FastAPI dependency functions to provide database
sessions and service instances to route handlers.

Key components:
- `get_session`: Yields a SQLAlchemy session tied to the app lifecycle.
- `get_user_service`: Provides a fully initialized UserService instance.
- `UserServiceDep`: Typed annotation for injecting UserService as a dependency.
"""

from typing import Annotated

from fastapi import Depends, Request
from sqlalchemy.orm import Session

from app.repositories.user import UserRepository
from app.services.user import UserService


def get_session(request: Request):
    """Provide a SQLAlchemy session tied to the current request lifecycle.

    Args:
        request (Request): The incoming FastAPI request object.

    Yields:
        Session: A SQLAlchemy session instance.

    This function ensures the session is properly closed after the request.

    """
    SessionLocal = request.app.state.SessionLocal
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()


def get_user_service(
    session: Session = Depends(get_session),
) -> UserService:
    """Provide a UserService instance with an attached repository.

    Args:
        session (Session): Injected SQLAlchemy session.

    Returns:
        UserService: A fully initialized user service.

    """
    repo = UserRepository(session)
    return UserService(repo)


# Annotated type alias for injecting the user service
UserServiceDep = Annotated[UserService, Depends(get_user_service)]
