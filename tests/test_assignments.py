# test_assignments.py - Unit tests for License Assignment CRUD operations

import json


def setup_test_data(client):
    """Helper: create a vendor, license, and users for assignment tests."""
    client.post('/api/vendors', json={'company_name': 'TestVendor', 'default_currency': 'USD'})
    client.post('/api/licenses', json={'software_name': 'TestApp', 'license_key': 'XXXX', 'purchase_date': '2025-01-01', 'expiry_date': '2028-01-01', 'seats': 2, 'vendor_id': 1})
    client.post('/api/users', json={'name': 'Alice', 'email': 'alice@test.com'})
    client.post('/api/users', json={'name': 'Bob', 'email': 'bob@test.com'})


def test_create_assignment(client):
    """Test that we can assign a license to a user."""
    setup_test_data(client)
    response = client.post('/api/assignments', json={
        'license_id': 1, 'user_id': 1, 'assignment_date': '2025-06-01', 'notes': 'Primary user'
    })
    assert response.status_code == 201


def test_get_all_assignments(client):
    """Test that we can retrieve all assignments with joined names."""
    setup_test_data(client)
    client.post('/api/assignments', json={'license_id': 1, 'user_id': 1, 'assignment_date': '2025-06-01'})
    response = client.get('/api/assignments')
    data = response.get_json()
    assert len(data) == 1
    assert data[0]['software_name'] == 'TestApp'
    assert data[0]['user_name'] == 'Alice'


def test_update_assignment(client):
    """Test that we can update an assignment's notes."""
    setup_test_data(client)
    client.post('/api/assignments', json={'license_id': 1, 'user_id': 1, 'assignment_date': '2025-06-01'})
    response = client.put('/api/assignments/1', json={'assignment_date': '2025-07-01', 'notes': 'Updated'})
    data = response.get_json()
    assert data['notes'] == 'Updated'


def test_delete_assignment(client):
    """Test that we can remove an assignment."""
    setup_test_data(client)
    client.post('/api/assignments', json={'license_id': 1, 'user_id': 1, 'assignment_date': '2025-06-01'})
    response = client.delete('/api/assignments/1')
    assert response.status_code == 200
