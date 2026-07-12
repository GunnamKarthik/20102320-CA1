# routes_assignments.py - CRUD API endpoints for License Assignments
# Handles assigning licenses to users, with seat availability checking

from flask import Blueprint, request, jsonify
from db import get_db

# Create a blueprint for assignment routes
assignments_bp = Blueprint('assignments', __name__)


@assignments_bp.route('/api/assignments', methods=['GET'])
def get_all_assignments():
    """Get all license assignments, joined with license and user names for display."""
    db = get_db()
    # Join with licenses and users tables to get readable names
    assignments = db.execute("""
        SELECT a.*, l.software_name, u.name as user_name, u.email as user_email
        FROM license_assignments a
        LEFT JOIN licenses l ON a.license_id = l.id
        LEFT JOIN users u ON a.user_id = u.id
        ORDER BY a.assignment_date DESC
    """).fetchall()
    db.close()
    result = [dict(row) for row in assignments]
    return jsonify(result)


@assignments_bp.route('/api/assignments', methods=['POST'])
def create_assignment():
    """Assign a license to a user. Checks if there are available seats first."""
    data = request.get_json()

    # Validate required fields
    if not data.get('license_id') or not data.get('user_id'):
        return jsonify({'error': 'License and user are required'}), 400

    db = get_db()

    # Get the license to check how many seats it has
    license_row = db.execute('SELECT seats FROM licenses WHERE id = ?', (data['license_id'],)).fetchone()
    if not license_row:
        db.close()
        return jsonify({'error': 'License not found'}), 400

    # Count how many users are already assigned to this license
    assigned_count = db.execute(
        'SELECT COUNT(*) as count FROM license_assignments WHERE license_id = ?',
        (data['license_id'],)
    ).fetchone()['count']

    # Check if there are any seats left
    if assigned_count >= license_row['seats']:
        db.close()
        return jsonify({'error': 'No available seats for this license'}), 400

    # Try to create the assignment (will fail if user is already assigned due to UNIQUE constraint)
    try:
        cursor = db.execute(
            'INSERT INTO license_assignments (license_id, user_id, assignment_date, notes) VALUES (?, ?, ?, ?)',
            (data['license_id'], data['user_id'], data.get('assignment_date', ''), data.get('notes', ''))
        )
        db.commit()
    except Exception:
        db.close()
        return jsonify({'error': 'This user is already assigned to this license'}), 409

    # Return the newly created assignment
    new_assignment = db.execute('SELECT * FROM license_assignments WHERE id = ?', (cursor.lastrowid,)).fetchone()
    db.close()
    return jsonify(dict(new_assignment)), 201


@assignments_bp.route('/api/assignments/<int:assignment_id>', methods=['PUT'])
def update_assignment(assignment_id):
    """Update an assignment's date or notes."""
    data = request.get_json()

    db = get_db()
    # Only update the assignment date and notes (not the license or user link)
    db.execute(
        'UPDATE license_assignments SET assignment_date = ?, notes = ? WHERE id = ?',
        (data.get('assignment_date', ''), data.get('notes', ''), assignment_id)
    )
    db.commit()

    # Return the updated assignment
    updated_assignment = db.execute('SELECT * FROM license_assignments WHERE id = ?', (assignment_id,)).fetchone()
    db.close()

    if not updated_assignment:
        return jsonify({'error': 'Assignment not found'}), 404

    return jsonify(dict(updated_assignment))


@assignments_bp.route('/api/assignments/<int:assignment_id>', methods=['DELETE'])
def delete_assignment(assignment_id):
    """Remove an assignment (unassign a user from a license, freeing up a seat)."""
    db = get_db()
    db.execute('DELETE FROM license_assignments WHERE id = ?', (assignment_id,))
    db.commit()
    db.close()
    return jsonify({'message': 'Assignment removed successfully'})
