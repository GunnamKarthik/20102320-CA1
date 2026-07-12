# routes_users.py - CRUD API endpoints for Users
# Handles creating, reading, updating, and deleting user records

from flask import Blueprint, request, jsonify
from db import get_db

# Create a blueprint for user routes
users_bp = Blueprint('users', __name__)


@users_bp.route('/api/users', methods=['GET'])
def get_all_users():
    """Get a list of all users from the database."""
    db = get_db()
    # Fetch all users ordered by name
    users = db.execute('SELECT * FROM users ORDER BY name').fetchall()
    db.close()
    result = [dict(row) for row in users]
    return jsonify(result)
