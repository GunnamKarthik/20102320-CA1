# db.py - Database connection and schema for the License Manager
# This file handles all database setup and provides a helper to get a connection

import sqlite3
import os

# Path to the SQLite database file
DATABASE = os.path.join(os.path.dirname(__file__), 'license_manager.db')

# SQL schema to create all 4 tables
SCHEMA = """
-- Vendors table: stores software vendor/supplier information
CREATE TABLE IF NOT EXISTS vendors (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    company_name TEXT NOT NULL,
    contact_email TEXT,
    website TEXT,
    country TEXT,
    default_currency TEXT NOT NULL DEFAULT 'USD'
);

-- Licenses table: stores software license details, linked to a vendor
CREATE TABLE IF NOT EXISTS licenses (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    software_name TEXT NOT NULL,
    license_key TEXT NOT NULL,
    purchase_date TEXT NOT NULL,
    expiry_date TEXT NOT NULL,
    seats INTEGER NOT NULL DEFAULT 1,
    cost REAL NOT NULL DEFAULT 0.0,
    currency TEXT NOT NULL DEFAULT 'USD',
    status TEXT NOT NULL DEFAULT 'active' CHECK(status IN ('active', 'expiring', 'expired')),
    vendor_id INTEGER NOT NULL,
    FOREIGN KEY (vendor_id) REFERENCES vendors(id) ON DELETE RESTRICT
);

-- Users table: stores employee/user information
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    email TEXT NOT NULL UNIQUE,
    department TEXT,
    role TEXT
);

-- License assignments table: links users to licenses (many-to-many)
CREATE TABLE IF NOT EXISTS license_assignments (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    license_id INTEGER NOT NULL,
    user_id INTEGER NOT NULL,
    assignment_date TEXT NOT NULL,
    notes TEXT DEFAULT '',
    FOREIGN KEY (license_id) REFERENCES licenses(id) ON DELETE CASCADE,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    UNIQUE(license_id, user_id)
);
"""
