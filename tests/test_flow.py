from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from main import app, get_db
import models
import database
import pytest

# Setup test database
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)

@pytest.fixture(autouse=True)
def setup_db():
    models.Base.metadata.create_all(bind=engine)
    yield
    models.Base.metadata.drop_all(bind=engine)

def test_auth_flow():
    # Try to access admin without login
    response = client.get("/", follow_redirects=False)
    assert response.status_code == 303
    assert response.headers["location"] == "/login"
    
    # Login with wrong password
    response = client.post("/login", data={"password": "wrong"})
    assert "Senha incorreta" in response.text
    
    # Login with correct password
    response = client.post("/login", data={"password": "admin"}, follow_redirects=False)
    assert response.status_code == 303
    assert response.headers["location"] == "/"
    
    # Access admin with session
    # TestClient cookie handling is automatic
    response = client.get("/")
    assert response.status_code == 200
    assert "Painel do Administrador" in response.text

def test_draw_flow_authenticated():
    # Login first
    client.post("/login", data={"password": "admin"})
    
    # Add 3 participants
    client.post("/participants", data={"name": "Alice"})
    client.post("/participants", data={"name": "Bob"})
    client.post("/participants", data={"name": "Charlie"})
    
    # Draw
    client.post("/draw")
    
    # Check if links are generated
    response = client.get("/")
    assert "Link Mágico" in response.text
    
    # Get tokens from DB to test reveal
    db = TestingSessionLocal()
    alice = db.query(models.Participant).filter_by(name="Alice").first()
    
    # Reveal should be public
    response = client.get(f"/reveal/{alice.token}")
    assert response.status_code == 200
    assert "Seu amigo secreto é..." in response.text
    
    # Logout
    response = client.get("/logout", follow_redirects=False)
    assert response.status_code == 303
    assert response.headers["location"] == "/login"
    
    # Verify access denied after logout
    response = client.get("/", follow_redirects=False)
    assert response.status_code == 303
