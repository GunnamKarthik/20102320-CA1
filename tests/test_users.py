# test_users.py - Unit tests for User CRUD operations

import json


def test_create_user(client):
    """Test that we can create a new user."""
    response = client.post('/api/users', json={
        'name': 'Alice Smith',
        'email': 'alice@karthikit.com',
        'department': 'Engineering',
        'role': 'Developer'
    })
    data = response.get_json()
    assert response.status_code == 201
    assert data['name'] == 'Alice Smith'


def test_get_all_users(client):
    """Test that we can retrieve all users."""
    client.post('/api/users', json={'name': 'Alice', 'email': 'alice@test.com'})
    client.post('/api/users', json={'name': 'Bob', 'email': 'bob@test.com'})
    response = client.get('/api/users')
    data = response.get_json()
    assert len(data) == 2


def test_update_user(client):
    """Test that we can update a user."""
    client.post('/api/users', json={'name': 'Alice', 'email': 'alice@test.com', 'department': 'Engineering', 'role': 'Developer'})
    response = client.put('/api/users/1', json={
        'name': 'Alice Smith',
        'email': 'alice@test.com',
        'department': 'Management',
        'role': 'Team Lead'
    })
    data = response.get_json()
    assert data['department'] == 'Management'


def test_delete_user(client):
    """Test that we can delete a user."""
    client.post('/api/users', json={'name': 'Alice', 'email': 'alice@test.com'})
    response = client.delete('/api/users/1')
    assert response.status_code == 200
