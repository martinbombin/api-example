"""User repository module for handling database interactions related to the User model.

This module provides the `UserRepository` class, which abstracts CRUD operations
and query utilities for users in a SQLAlchemy-backed database.
"""

import uuid

from sqlalchemy import exists, select
from sqlalchemy.orm import Session

from app.repositories import models
from app.schemas import user as user_schema


class UserRepository:
    """Repository class for performing database operations on User objects.

    Attributes:
        session (Session): SQLAlchemy session used for database interactions.

    """

    def __init__(self, session: Session) -> None:
        """Initialize the UserRepository with a database session.

        Args:
            session (Session): The SQLAlchemy session to use.

        """
        self.session = session

    def _create_schema_to_model(
        self,
        user: user_schema.UserCreate,
    ) -> models.User:
        return models.User(**user.model_dump())

    def _model_to_public_schema(
        self,
        user: models.User,
    ) -> user_schema.UserPublic:
        return user_schema.UserPublic(**user.__dict__)

    def user_exists(self, email: str) -> bool:
        """Check whether a user with the given email exists in the database.

        Args:
            email (str): The email address to check.

        Returns:
            bool: True if a user with the email exists, False otherwise.

        """
        return self.session.query(
            exists().where(models.User.email == email),
        ).scalar()

    def create_user(
        self,
        user: user_schema.UserCreate,
    ) -> user_schema.UserPublic:
        """Create a new user in the database.

        Args:
            user (models.User): The User object to add.

        Returns:
            user_schema.UserPublic: The newly created User.

        """
        model_user = self._create_schema_to_model(user=user)
        self.session.add(model_user)
        self.session.commit()
        self.session.refresh(model_user)

        return self._model_to_public_schema(user=model_user)

    def get_users(
        self,
        offset: int = 0,
        limit: int = 100,
        username: str | None = None,
        email: str | None = None,
    ) -> list[user_schema.UserPublic]:
        """Retrieve a list of users from the database, with optional filters.

        Args:
            offset (int): The starting index for pagination. Default is 0.
            limit (int): The maximum number of users to return. Default is 100.
            username (str | None): Optional filter by username.
            email (str | None): Optional filter by email.

        Returns:
            list[user_schema.UserPublic]: A list of Users matching the criteria.

        """
        stmt = select(models.User)

        if username:
            stmt = stmt.where(models.User.username == username)
        if email:
            stmt = stmt.where(models.User.email == email)

        stmt = stmt.offset(offset).limit(limit)
        model_users = list(self.session.scalars(stmt).all())

        return [
            self._model_to_public_schema(user=model_user)
            for model_user in model_users
        ]

    def get_user_by_id(
        self,
        user_id: uuid.UUID,
    ) -> user_schema.UserPublic | None:
        """Retrieve a user by their unique identifier.

        Args:
            user_id (uuid.UUID): The UUID of the user to retrieve.

        Returns:
            models.User | None: The User if found, or None if not found.

        """
        model_user = self.session.get(models.User, str(user_id))
        if model_user is None:
            return None

        return self._model_to_public_schema(user=model_user)
