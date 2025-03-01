import pytest
from backend.database import get_db, init_db
from backend import create_app

@pytest.fixture
def app():
    """Create and configure a new app instance for testing."""
    app = create_app(testing=True)  # Ensure your create_app function supports testing mode
    with app.app_context():
        init_db()  # Initialize the test database
    yield app

@pytest.fixture
def client(app):
    """Return a test client for the app."""
    return app.test_client()

def test_database_connection(client):
    """Test if the database connection is successful."""
    with get_db() as db:
        result = db.execute("SELECT 1").fetchone()
        assert result is not None
