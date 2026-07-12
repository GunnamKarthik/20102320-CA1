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
