"""Pydantic schemas for user-related API models.

These models are used for data validation and serialization of user data in FastAPI endpoints.
Includes base schema, input (creation), and output (public-facing) models, with examples for OpenAPI docs.
"""

import uuid

import pydantic


class _ExampleUser(pydantic.BaseModel):
    """Example user data used for schema documentation and OpenAPI examples."""

    id: uuid.UUID = uuid.UUID("11111111-2222-3333-4444-555566667777")
    username: str = "johndoe"
    password: str = "secret"
    full_name: str = "John Doe"
    phone_number: str = "+34 123 456 789"
    email: pydantic.EmailStr = "johndoe@example.com"


DEFAULT_USER = _ExampleUser()


class UserBase(pydantic.BaseModel):
    """Base schema for user data.

    Includes shared fields for both input and output models, such as:
    - `username`: The user's unique login name.
    - `full_name`: The user's full name (optional).
    - `phone_number`: Contact number (optional).
    - `email`: The user's email address.
    """

    username: str = pydantic.Field(examples=[DEFAULT_USER.username])
    full_name: str | None = pydantic.Field(
        default=None,
        examples=[DEFAULT_USER.full_name],
    )
    phone_number: str | None = pydantic.Field(
        default=None,
        examples=[DEFAULT_USER.phone_number],
    )
    email: pydantic.EmailStr = pydantic.Field(
        examples=[DEFAULT_USER.email],
    )


class UserCreate(UserBase):
    """Schema for creating a new user.

    Inherits from `UserBase` and adds:
    - `password`: The user's password for authentication.
    """

    password: str = pydantic.Field(examples=[DEFAULT_USER.password])


class UserPublic(UserBase):
    """Public-facing schema for returning user data via API.

    Inherits from `UserBase` and adds:
    - `id`: The user's unique identifier (UUID).
    """

    id: uuid.UUID = pydantic.Field(examples=[DEFAULT_USER.id])
