# app.py - Main Flask application for Karthik IT Solutions License Manager
# This file creates the Flask app, registers all route blueprints, and serves the main page

from flask import Flask, render_template
from db import init_db

# Import all route blueprints
from routes_vendors import vendors_bp
from routes_licenses import licenses_bp
from routes_users import users_bp
from routes_assignments import assignments_bp
from routes_convert import convert_bp

# Create the Flask application
app = Flask(__name__)


@app.route('/')
def home():
    """Serve the main single-page application."""
    return render_template('index.html')


# Register all blueprints (each handles CRUD for one entity)
app.register_blueprint(vendors_bp)
app.register_blueprint(licenses_bp)
app.register_blueprint(users_bp)
app.register_blueprint(assignments_bp)
app.register_blueprint(convert_bp)


# Run the app
if __name__ == '__main__':
    # Create all database tables on first run
    init_db()
    # Start the Flask development server
    app.run(debug=True, port=5000)
