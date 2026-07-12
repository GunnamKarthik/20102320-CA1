# test_licenses.py - Unit tests for License CRUD operations

import json


def test_create_license(client):
    """Test that we can create a new license."""
    client.post('/api/vendors', json={'company_name': 'TestVendor', 'default_currency': 'USD'})
    response = client.post('/api/licenses', json={
        'software_name': 'Office 365',
        'license_key': 'XXXX-YYYY',
        'purchase_date': '2025-01-01',
        'expiry_date': '2026-01-01',
        'seats': 5,
        'cost': 299.99,
        'vendor_id': 1
    })
    data = response.get_json()
    assert response.status_code == 201
    assert data['software_name'] == 'Office 365'


def test_get_licenses_with_search(client):
    """Test that we can search licenses by software name."""
    client.post('/api/vendors', json={'company_name': 'TestVendor', 'default_currency': 'USD'})
    client.post('/api/licenses', json={'software_name': 'Office 365', 'license_key': 'AAA', 'purchase_date': '2025-01-01', 'expiry_date': '2028-01-01', 'vendor_id': 1})
    client.post('/api/licenses', json={'software_name': 'Photoshop', 'license_key': 'BBB', 'purchase_date': '2025-01-01', 'expiry_date': '2028-01-01', 'vendor_id': 1})
    response = client.get('/api/licenses?search=Office')
    data = response.get_json()
    assert len(data) == 1


def test_update_license(client):
    """Test that we can update a license."""
    client.post('/api/vendors', json={'company_name': 'TestVendor', 'default_currency': 'USD'})
    client.post('/api/licenses', json={'software_name': 'Office 365', 'license_key': 'XXXX', 'purchase_date': '2025-01-01', 'expiry_date': '2026-01-01', 'seats': 5, 'vendor_id': 1})
    response = client.put('/api/licenses/1', json={
        'software_name': 'Office 365 Pro',
        'license_key': 'XXXX',
        'purchase_date': '2025-01-01',
        'expiry_date': '2027-01-01',
        'seats': 10,
        'vendor_id': 1
    })
    data = response.get_json()
    assert data['software_name'] == 'Office 365 Pro'


def test_delete_license(client):
    """Test that we can delete a license."""
    client.post('/api/vendors', json={'company_name': 'TestVendor', 'default_currency': 'USD'})
    client.post('/api/licenses', json={'software_name': 'Office 365', 'license_key': 'XXXX', 'purchase_date': '2025-01-01', 'expiry_date': '2026-01-01', 'vendor_id': 1})
    response = client.delete('/api/licenses/1')
    assert response.status_code == 200
