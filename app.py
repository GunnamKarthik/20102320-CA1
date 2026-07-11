# app.py - Main Flask application for Karthik IT Solutions License Manager
# This file creates the Flask app and serves the main page

from flask import Flask, render_template

# Create the Flask application
app = Flask(__name__)


@app.route('/')
def home():
    """Serve the main single-page application."""
    return render_template('index.html')


# Run the app
if __name__ == '__main__':
    # Start the Flask development server
    app.run(debug=True, port=5000)
