# routes_licenses.py - CRUD API endpoints for Licenses
# Handles creating, reading, updating, and deleting license records
# Also supports search by software name and filter by status

from flask import Blueprint, request, jsonify
from db import get_db
from datetime import date, timedelta

# Create a blueprint for license routes
licenses_bp = Blueprint('licenses', __name__)


def auto_update_statuses(db):
    """Automatically update license statuses based on expiry dates.
    - If expiry_date is in the past -> status becomes 'expired'
    - If expiry_date is within 30 days -> status becomes 'expiring'
    """
    today = date.today().isoformat()
    expiring_threshold = (date.today() + timedelta(days=30)).isoformat()

    # Mark expired licenses
    db.execute("UPDATE licenses SET status = 'expired' WHERE expiry_date < ? AND status != 'expired'", (today,))
    # Mark expiring-soon licenses
    db.execute("UPDATE licenses SET status = 'expiring' WHERE expiry_date >= ? AND expiry_date <= ? AND status = 'active'", (today, expiring_threshold))
    db.commit()


@licenses_bp.route('/api/licenses', methods=['GET'])
def get_all_licenses():
    """Get all licenses, with optional search and status filter.
    Query params: ?status=active&search=Office"""
    db = get_db()

    # Auto-update statuses before returning results
    auto_update_statuses(db)

    # Build the query with optional filters
    query = """SELECT l.*, v.company_name as vendor_name,
               (SELECT COUNT(*) FROM license_assignments WHERE license_id = l.id) as assigned_count
               FROM licenses l
               LEFT JOIN vendors v ON l.vendor_id = v.id
               WHERE 1=1"""
    params = []

    # Filter by status if provided
    status_filter = request.args.get('status')
    if status_filter:
        query += " AND l.status = ?"
        params.append(status_filter)

    # Search by software name if provided
    search_term = request.args.get('search')
    if search_term:
        query += " AND l.software_name LIKE ?"
        params.append(f"%{search_term}%")

    query += " ORDER BY l.software_name"

    licenses = db.execute(query, params).fetchall()
    db.close()
    result = [dict(row) for row in licenses]
    return jsonify(result)
