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


@users_bp.route('/api/users', methods=['POST'])
def create_user():
    """Create a new user record."""
    data = request.get_json()

    # Validate required fields
    if not data.get('name') or not data.get('email'):
        return jsonify({'error': 'Name and email are required'}), 400

    db = get_db()

    # Check if a user with this email already exists
    existing_user = db.execute('SELECT id FROM users WHERE email = ?', (data['email'],)).fetchone()
    if existing_user:
        db.close()
        return jsonify({'error': 'A user with this email already exists'}), 409

    # Insert the new user
    cursor = db.execute(
        'INSERT INTO users (name, email, department, role) VALUES (?, ?, ?, ?)',
        (data['name'], data['email'], data.get('department', ''), data.get('role', ''))
    )
    db.commit()

    # Return the newly created user
    new_user = db.execute('SELECT * FROM users WHERE id = ?', (cursor.lastrowid,)).fetchone()
    db.close()
    return jsonify(dict(new_user)), 201
