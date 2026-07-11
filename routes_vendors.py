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
