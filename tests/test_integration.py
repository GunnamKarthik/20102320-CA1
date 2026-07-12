# test_integration.py - Integration test for the full application
# Tests a complete business workflow from start to finish:
# Create vendor -> license -> users -> assign -> convert currency -> unassign -> delete

from unittest.mock import patch, MagicMock


def test_full_workflow(client):
    """Integration test: walk through a complete business workflow.
    This test verifies that the frontend-to-backend chain works end-to-end."""

    # Step 1: Create a vendor
    response = client.post('/api/vendors', json={
        'company_name': 'Microsoft',
        'contact_email': 'sales@microsoft.com',
        'website': 'https://microsoft.com',
        'country': 'USA',
        'default_currency': 'USD'
    })
    assert response.status_code == 201
    vendor = response.get_json()
    assert vendor['company_name'] == 'Microsoft'

    # Step 2: Create a license linked to the vendor (3 seats)
    response = client.post('/api/licenses', json={
        'software_name': 'Office 365',
        'license_key': 'XXXX-YYYY-ZZZZ',
        'purchase_date': '2025-01-01',
        'expiry_date': '2026-12-31',
        'seats': 3,
        'cost': 299.99,
        'currency': 'USD',
        'vendor_id': vendor['id']
    })
    assert response.status_code == 201
    license_data = response.get_json()
    assert license_data['software_name'] == 'Office 365'

    # Step 3: Create two users
    response = client.post('/api/users', json={
        'name': 'Alice Smith',
        'email': 'alice@karthikit.com',
        'department': 'Engineering',
        'role': 'Developer'
    })
    assert response.status_code == 201
    alice = response.get_json()

    response = client.post('/api/users', json={
        'name': 'Bob Jones',
        'email': 'bob@karthikit.com',
        'department': 'Design',
        'role': 'Designer'
    })
    assert response.status_code == 201
    bob = response.get_json()

    # Step 4: Assign the license to both users
    response = client.post('/api/assignments', json={
        'license_id': license_data['id'],
        'user_id': alice['id'],
        'assignment_date': '2025-06-01',
        'notes': 'Primary developer'
    })
    assert response.status_code == 201

    response = client.post('/api/assignments', json={
        'license_id': license_data['id'],
        'user_id': bob['id'],
        'assignment_date': '2025-06-01',
        'notes': 'Design team'
    })
    assert response.status_code == 201

    # Step 5: Check seat count - should show 2 assigned out of 3
    response = client.get('/api/licenses')
    licenses = response.get_json()
    assert licenses[0]['assigned_count'] == 2
    assert licenses[0]['seats'] == 3

    # Step 6: Test currency conversion (mock the external API)
    mock_response = MagicMock()
    mock_response.json.return_value = {
        'result': 'success',
        'rates': {'EUR': 0.92, 'GBP': 0.79}
    }
    with patch('routes_convert.requests.get', return_value=mock_response):
        response = client.get('/api/convert?amount=299.99&from=USD&to=EUR')
        data = response.get_json()
        assert data['converted'] == 275.99
        assert data['rate'] == 0.92

    # Step 7: Remove Bob's assignment (free up a seat)
    response = client.delete('/api/assignments/2')
    assert response.status_code == 200

    # Verify seat count dropped back to 1
    response = client.get('/api/licenses')
    licenses = response.get_json()
    assert licenses[0]['assigned_count'] == 1

    # Step 8: Delete Alice (should cascade-delete her assignment)
    response = client.delete('/api/users/' + str(alice['id']))
    assert response.status_code == 200

    # Verify all assignments are gone
    response = client.get('/api/assignments')
    assignments = response.get_json()
    assert len(assignments) == 0

    # Step 9: Delete the license
    response = client.delete('/api/licenses/' + str(license_data['id']))
    assert response.status_code == 200

    # Step 10: Now we can delete the vendor (no licenses left)
    response = client.delete('/api/vendors/' + str(vendor['id']))
    assert response.status_code == 200

    # Final check: everything is clean
    assert len(client.get('/api/vendors').get_json()) == 0
    assert len(client.get('/api/licenses').get_json()) == 0
    assert len(client.get('/api/users').get_json()) == 1  # Bob is still there
    assert len(client.get('/api/assignments').get_json()) == 0
