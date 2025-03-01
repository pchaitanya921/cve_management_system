import sys
import os
import pytest
from backend import create_app
from backend.database import db

@pytest.fixture
def app():
    """Creates a test Flask application"""
    app = create_app()
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'  # In-memory database for tests
    with app.app_context():
        db.create_all()
    yield app

@pytest.fixture
def client(app):
    """Creates a test client"""
    return app.test_client()

def test_home_route(client):
    """Test if the home route is working"""
    response = client.get('/')
    assert response.status_code == 200

def test_filter_route(client):
    """Test filter API"""
    response = client.get('/api/filter')  # Adjust endpoint as per your route
    assert response.status_code == 200
    assert isinstance(response.json, dict)  # Assuming JSON response

def test_create_cve_entry(client):
    """Test creating a new CVE entry"""
    data = {
        "cve_id": "CVE-2024-1234",
        "description": "Test vulnerability",
        "severity": "High"
    }
    response = client.post('/api/cve', json=data)  # Adjust endpoint
    assert response.status_code == 201
    assert response.json["message"] == "CVE entry created successfully"

def test_get_cve_list(client):
    """Test fetching CVE list"""
    response = client.get('/api/cve')  # Adjust endpoint
    assert response.status_code == 200
    assert isinstance(response.json, list)

def test_invalid_route(client):
    """Test 404 error for invalid routes"""
    response = client.get('/invalid-route')
    assert response.status_code == 404
