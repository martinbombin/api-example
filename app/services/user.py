"""User service layer for encapsulating business logic related to user operations.

This module acts as a bridge between the API layer and the repository layer,
handling application-specific concerns like checking for existing users.

Key components:
- `UserService`: Class encapsulating user-related operations.
"""

import uuid

from passlib.context import CryptContext

from app import exceptions
from app.repositories.user import UserRepository
from app.schemas import user as schemas_user

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class UserService:
    """Service class responsible for user-related business logic."""

    def __init__(self, user_repo: UserRepository) -> None:
        """Initialize the UserService.

        Args:
            user_repo (UserRepository): The user repository instance used for persistance operations.

        """
        self.user_repo = user_repo

    def _hash_password(self, password: str) -> str:
        return pwd_context.hash(password)

    def create_user_in_db(
        self,
        user_create: schemas_user.UserCreate,
    ) -> schemas_user.UserPublic:
        """Create a new user in after validating uniqueness.

        Args:
            user_create (UserCreate): The user creation schema with input data.

        Raises:
            ExistingEmailError: If a user with the same email already exists.

        Returns:
            schemas_user.UserPublic: The newly created User.

        """
        if self.user_repo.user_exists(user_create.email):
            raise exceptions.ExistingEmailError

        hashed_password = self._hash_password(
            user_create.password,
        )
        user_create.password = hashed_password

        return self.user_repo.create_user(user_create)

    def get_users_from_db(
        self,
        offset: int = 0,
        limit: int = 100,
        username: str | None = None,
        email: str | None = None,
    ) -> list[schemas_user.UserPublic]:
        """Retrieve a list of users with optional filters.

        Args:
            offset (int): Pagination offset. Default is 0.
            limit (int): Maximum number of users to return. Default is 100.
            username (str | None): Optional filter by username.
            email (str | None): Optional filter by email.

        Returns:
            list[schemas_user.UserPublic]: A list of Users matching the query.

        """
        return self.user_repo.get_users(
            offset=offset,
            limit=limit,
            username=username,
            email=email,
        )

    def get_user_by_id(
        self,
        user_id: uuid.UUID,
    ) -> schemas_user.UserPublic | None:
        """Retrieve a single user by their UUID.

        Args:
            user_id (uuid.UUID): The unique identifier of the user.

        Returns:
            schemas_user.UserPublic | None: The user if found, or None if not found.

        """
        return self.user_repo.get_user_by_id(user_id)
