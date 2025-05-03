import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app import main
from app.repositories import models
from app.schemas.user import UserCreate


@pytest.fixture
def client():
    def _clear_database(engine):
        with Session(engine) as session:
            for table in reversed(models.Base.metadata.sorted_tables):
                session.execute(table.delete())
            session.commit()

    with TestClient(main.app) as client:
        yield client
        db_engine = client.app.state.db_engine  # type: ignore
        _clear_database(engine=db_engine)


@pytest.mark.integration
def test_create_user(
    client: TestClient,
    user_create: UserCreate,
):
    response = client.post(
        "/users/",
        json=user_create.model_dump(),
    )
    data = response.json()

    assert response.status_code == 200
    assert data["id"] is not None
    assert data["username"] == user_create.username
    assert data["full_name"] == user_create.full_name
    assert data["email"] == user_create.email
    assert data["phone_number"] == user_create.phone_number
    assert "password" not in data


@pytest.mark.integration
def test_create_user_incomplete(
    client: TestClient,
    user_create: UserCreate,
):
    user_without_passwd = user_create.model_dump(exclude={"password"})
    response = client.post(
        "/users/",
        json=user_without_passwd,
    )
    assert response.status_code == 422


@pytest.mark.integration
def test_create_user_invalid(
    client: TestClient,
    user_create: UserCreate,
):
    wrong_user = user_create.model_dump()
    wrong_user["full_name"] = {"invalid": "full_name format"}
    response = client.post(
        "/users/",
        json=wrong_user,
    )
    assert response.status_code == 422


@pytest.mark.integration
def test_read_user(
    client: TestClient,
    user_create: UserCreate,
):
    response_1 = client.post(
        "/users/",
        json=user_create.model_dump(),
    )
    inserted_data = response_1.json()

    response_2 = client.get(f"/users/{inserted_data['id']}")
    retrieved_data = response_2.json()

    assert response_2.status_code == 200
    assert inserted_data["username"] == retrieved_data["username"]
    assert inserted_data["full_name"] == retrieved_data["full_name"]
    assert inserted_data["email"] == retrieved_data["email"]
    assert inserted_data["id"] == str(retrieved_data["id"])
    assert (
        inserted_data["phone_number"] == retrieved_data["phone_number"]
    )
    assert "password" not in retrieved_data


@pytest.mark.integration
def test_read_users(
    client: TestClient,
    user_create: UserCreate,
):
    def _get_user_from_list(
        retrieved_data: list[dict],
        username: str,
    ):
        return next(
            item
            for item in retrieved_data
            if item["username"] == username
        )

    response_1 = client.post(
        "/users/",
        json=user_create.model_dump(),
    )
    inserted_data_1 = response_1.json()

    user_2 = UserCreate(
        username="anotheruser",
        email="another@example.com",
        password="secret",
    )
    response_2 = client.post(
        "/users/",
        json=user_2.model_dump(),
    )
    inserted_data_2 = response_2.json()

    response_3 = client.get("/users/")
    retrieved_data = response_3.json()

    assert response_3.status_code == 200
    assert len(retrieved_data) == 2

    retrieved_user_1 = _get_user_from_list(
        retrieved_data,
        username=user_create.username,
    )
    retrieved_user_2 = _get_user_from_list(
        retrieved_data,
        username=user_2.username,
    )

    assert response_3.status_code == 200
    assert inserted_data_1["username"] == retrieved_user_1["username"]
    assert inserted_data_1["full_name"] == retrieved_user_1["full_name"]
    assert inserted_data_1["email"] == retrieved_user_1["email"]
    assert inserted_data_1["id"] == str(retrieved_user_1["id"])
    assert (
        inserted_data_1["phone_number"]
        == retrieved_user_1["phone_number"]
    )
    assert "password" not in retrieved_user_1

    assert inserted_data_2["username"] == retrieved_user_2["username"]
    assert inserted_data_2["email"] == retrieved_user_2["email"]
    assert inserted_data_2["id"] == str(retrieved_user_2["id"])
    assert "password" not in retrieved_user_2
    assert retrieved_user_2["full_name"] is None
