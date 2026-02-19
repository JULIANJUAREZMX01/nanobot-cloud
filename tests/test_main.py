"""Tests for main application"""

import pytest
from fastapi.testclient import TestClient
from app.main import app


@pytest.fixture
def client():
    """Test client"""
    return TestClient(app)


def test_health_check(client):
    """Test health check endpoint"""
    response = client.get("/api/status")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_root_endpoint(client):
    """Test root endpoint"""
    response = client.get("/")
    assert response.status_code in [200, 404]  # 404 if dashboard not found


def test_get_sessions(client):
    """Test get sessions endpoint"""
    response = client.get("/api/sessions")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
