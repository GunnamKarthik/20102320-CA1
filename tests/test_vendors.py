# test_vendors.py - Unit tests for Vendor CRUD operations

import json


def test_create_vendor(client):
    """Test that we can create a new vendor with valid data."""
    response = client.post('/api/vendors', json={
        'company_name': 'Microsoft',
        'contact_email': 'sales@microsoft.com',
        'website': 'https://microsoft.com',
        'country': 'USA',
        'default_currency': 'USD'
    })
    data = response.get_json()
    assert response.status_code == 201
    assert data['company_name'] == 'Microsoft'


def test_get_all_vendors(client):
    """Test that we can retrieve all vendors."""
    client.post('/api/vendors', json={'company_name': 'Microsoft', 'default_currency': 'USD'})
    client.post('/api/vendors', json={'company_name': 'Adobe', 'default_currency': 'USD'})
    response = client.get('/api/vendors')
    data = response.get_json()
    assert len(data) == 2


def test_update_vendor(client):
    """Test that we can update a vendor's details."""
    client.post('/api/vendors', json={'company_name': 'Microsoft', 'default_currency': 'USD'})
    response = client.put('/api/vendors/1', json={
        'company_name': 'Microsoft Corp',
        'default_currency': 'EUR'
    })
    data = response.get_json()
    assert data['company_name'] == 'Microsoft Corp'


def test_delete_vendor(client):
    """Test that we can delete a vendor with no licenses."""
    client.post('/api/vendors', json={'company_name': 'TestVendor', 'default_currency': 'USD'})
    response = client.delete('/api/vendors/1')
    assert response.status_code == 200
