"""User router module for managing user-related API endpoints.

This module defines routes for creating users, retrieving multiple users,
and fetching a specific user by ID. It utilizes FastAPI and depends on
external service and schema layers for business logic and validation.
"""

import uuid
from typing import Annotated

from fastapi import APIRouter, HTTPException, Query

from app import dependencies, exceptions
from app.schemas import user as user_schemas

router = APIRouter(prefix="/users", tags=["users"])


@router.post("/", response_model=user_schemas.UserPublic)
def create_user(
    user: user_schemas.UserCreate,
    user_service: dependencies.UserServiceDep,
):
    """Create a new user account."""
    try:
        created_user = user_service.create_user_in_db(user)
    except exceptions.ExistingEmailError:
        raise HTTPException(
            status_code=400,
            detail="Email already registered",
        ) from None
    return created_user


@router.get("/", response_model=list[user_schemas.UserPublic])
def read_users(
    user_service: dependencies.UserServiceDep,
    offset: int = 0,
    limit: Annotated[int, Query(le=100)] = 100,
    username: str | None = None,
    email: str | None = None,
):
    """Retrieve a list of users with optional filters."""
    return user_service.get_users_from_db(
        offset,
        limit,
        username,
        email,
    )


@router.get("/{user_id}", response_model=user_schemas.UserPublic)
def read_user(
    user_id: uuid.UUID,
    user_service: dependencies.UserServiceDep,
):
    """Retrieve a single user by their unique ID."""
    user = user_service.get_user_by_id(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user
