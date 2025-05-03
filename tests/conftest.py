import uuid

import pydantic
import pytest

from app.schemas import user as user_schemas


class _ExampleUser(pydantic.BaseModel):
    id: uuid.UUID = uuid.UUID("11111111-2222-3333-4444-555566667777")
    username: str = "johndoe"
    password: str = "secret"
    full_name: str = "John Doe"
    phone_number: str = "+34 123 456 789"
    email: pydantic.EmailStr = "johndoe@example.com"


TEST_USER = _ExampleUser()


@pytest.fixture
def user_create() -> user_schemas.UserCreate:
    return user_schemas.UserCreate(
        username=TEST_USER.username,
        full_name=TEST_USER.full_name,
        email=TEST_USER.email,
        password=TEST_USER.password,
        phone_number=TEST_USER.phone_number,
    )
