from sqlalchemy import create_engine, StaticPool, text
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from ..database import Base
from ..main import app
from ..routers.todos import get_db,get_current_user
import pytest
from ..models import Todos, Users
from fastapi.testclient import TestClient
from ..routers.auth import bcrypt_context

SQLALCHEMY_DATABASE_URI="sqlite:///./test.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URI,connect_args={'check_same_thread': False},
    poolclass=StaticPool,
)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)

def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

def override_get_current_user():
    return {"username":"test1","id":1, "user_role":"admin"}

# app.dependency_overrides[get_db]= override_get_db
# app.dependency_overrides[get_current_user]= override_get_current_user

client = TestClient(app)

@pytest.fixture
def test_todo():
    todo = Todos(
        title = "Learn to code!",
        description = "Learn Python!",
        priority = 5,
        complete = False,
        owner_id = 1,
    )
    db = TestingSessionLocal()
    db.add(todo)
    db.commit()
    yield todo
    with engine.connect() as connection:
        connection.execute(text("DELETE FROM todos;"))
        connection.commit()

@pytest.fixture
def test_user():
    user = Users(
        username="test2",
        email="test2@test2.com",
        first_name="test2",
        last_name="test2",
        hashed_password=bcrypt_context.hash("test2"),
        role="admin",
        phone_number="111-1111-1111",
    )
    db=TestingSessionLocal()
    db.add(user)
    db.commit()
    yield user
    with engine.connect() as connection:
        connection.execute(text("DELETE FROM users;"))
        connection.commit()