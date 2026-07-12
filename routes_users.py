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


@users_bp.route('/api/users/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    """Update an existing user record."""
    data = request.get_json()

    if not data.get('name') or not data.get('email'):
        return jsonify({'error': 'Name and email are required'}), 400

    db = get_db()

    # Check if another user already has this email (not the current user)
    existing_user = db.execute('SELECT id FROM users WHERE email = ? AND id != ?', (data['email'], user_id)).fetchone()
    if existing_user:
        db.close()
        return jsonify({'error': 'Another user with this email already exists'}), 409

    # Update the user's details
    db.execute(
        'UPDATE users SET name = ?, email = ?, department = ?, role = ? WHERE id = ?',
        (data['name'], data['email'], data.get('department', ''), data.get('role', ''), user_id)
    )
    db.commit()

    # Return the updated user
    updated_user = db.execute('SELECT * FROM users WHERE id = ?', (user_id,)).fetchone()
    db.close()

    if not updated_user:
        return jsonify({'error': 'User not found'}), 404

    return jsonify(dict(updated_user))


@users_bp.route('/api/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    """Delete a user. Any license assignments will be removed automatically (CASCADE)."""
    db = get_db()
    db.execute('DELETE FROM users WHERE id = ?', (user_id,))
    db.commit()
    db.close()
    return jsonify({'message': 'User deleted successfully'})
