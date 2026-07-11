# routes_vendors.py - CRUD API endpoints for Vendors
# Handles creating, reading, updating, and deleting vendor records

from flask import Blueprint, request, jsonify
from db import get_db

# Create a blueprint for vendor routes
vendors_bp = Blueprint('vendors', __name__)


@vendors_bp.route('/api/vendors', methods=['GET'])
def get_all_vendors():
    """Get a list of all vendors from the database."""
    db = get_db()
    # Fetch all vendors ordered by company name
    vendors = db.execute('SELECT * FROM vendors ORDER BY company_name').fetchall()
    db.close()
    # Convert each row to a dictionary so it can be returned as JSON
    result = [dict(row) for row in vendors]
    return jsonify(result)


@vendors_bp.route('/api/vendors', methods=['POST'])
def create_vendor():
    """Create a new vendor record."""
    data = request.get_json()

    # Check that the required field is provided
    if not data.get('company_name'):
        return jsonify({'error': 'Company name is required'}), 400

    db = get_db()
    # Insert the new vendor into the database
    cursor = db.execute(
        'INSERT INTO vendors (company_name, contact_email, website, country, default_currency) VALUES (?, ?, ?, ?, ?)',
        (data['company_name'], data.get('contact_email', ''), data.get('website', ''),
         data.get('country', ''), data.get('default_currency', 'USD'))
    )
    db.commit()

    # Fetch the newly created vendor to return it
    new_vendor = db.execute('SELECT * FROM vendors WHERE id = ?', (cursor.lastrowid,)).fetchone()
    db.close()
    return jsonify(dict(new_vendor)), 201
