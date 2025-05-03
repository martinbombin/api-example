import uuid

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import Engine
from sqlalchemy.orm import Session, sessionmaker

from app import main
from app.repositories import models
from app.repositories.user import UserRepository
from app.schemas import user as user_schema


@pytest.fixture(scope="session")
def engine():
    with TestClient(main.app) as client:
        test_engine = client.app.state.db_engine  # type: ignore
        yield test_engine
        models.Base.metadata.drop_all(test_engine)


@pytest.fixture
def db_session(engine: Engine):
    Session = sessionmaker(bind=engine)
    connection = engine.connect()
    transaction = connection.begin()
    session = Session(bind=connection)

    yield session

    session.close()
    transaction.rollback()
    connection.close()


@pytest.fixture
def user_repo(db_session: Session) -> UserRepository:
    return UserRepository(session=db_session)


@pytest.mark.integration
def test_user_exists(user_repo, db_session):
    user = models.User(
        username="existsuser",
        email="exists@example.com",
        password="secret",
    )
    db_session.add(user)
    db_session.commit()

    assert user_repo.user_exists("exists@example.com") is True
    assert user_repo.user_exists("notfound@example.com") is False


@pytest.mark.integration
def test_create_user(user_repo):
    user = user_schema.UserCreate(
        username="newuser",
        email="new@example.com",
        password="secret",
    )
    result = user_repo.create_user(user)

    assert result.id is not None
    assert result.email == "new@example.com"
    assert result.username == "newuser"


@pytest.mark.integration
def test_get_users_default(user_repo, db_session):
    users = [
        models.User(
            username="user1",
            email="u1@example.com",
            password="secret",
        ),
        models.User(
            username="user2",
            email="u2@example.com",
            password="secret",
        ),
    ]
    db_session.add_all(users)
    db_session.commit()

    retrieved_users = user_repo.get_users()
    assert len(retrieved_users) == len(users)


@pytest.mark.integration
def test_get_users_with_filters(user_repo, db_session):
    user = models.User(
        username="filterme",
        email="filter@example.com",
        password="secret",
    )
    db_session.add(user)
    db_session.commit()

    result = user_repo.get_users(username="filterme")
    assert len(result) == 1
    assert result[0].username == "filterme"

    result = user_repo.get_users(email="filter@example.com")
    assert len(result) == 1
    assert result[0].email == "filter@example.com"

    result = user_repo.get_users(email="notfound@example.com")
    assert len(result) == 0


@pytest.mark.integration
def test_get_user_by_id(user_repo, db_session):
    user = models.User(
        username="byid",
        email="byid@example.com",
        password="secret",
    )
    db_session.add(user)
    db_session.commit()

    result = user_repo.get_user_by_id(uuid.UUID(user.id))  # type: ignore
    assert result is not None
    assert result.email == "byid@example.com"


@pytest.mark.integration
def test_get_user_by_id_not_found(user_repo):
    random_id = uuid.uuid4()
    result = user_repo.get_user_by_id(random_id)
    assert result is None
