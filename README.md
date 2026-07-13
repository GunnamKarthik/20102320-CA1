# Karthik IT Solutions - Software License Manager


---

## Overview

This is a web-based Software License Manager built for **Karthik IT Solutions**, a small IT consultancy. The application helps the company track its software licenses, manage vendors, assign licenses to employees, and monitor costs across different currencies.

The system is built as a **proof-of-concept** CRUD (Create, Read, Update, Delete) application using Python Flask, SQLite, and JavaScript.

---


---

## Organisation

**Karthik IT Solutions** is a small IT consultancy that manages multiple software licenses for its team and clients. The company works with various software vendors (Microsoft, Adobe, etc.) across different countries and currencies. They need a central system to:

- Track which software licenses they own
- Know when licenses are expiring
- See who is using which license
- Monitor software costs across different currencies
- Manage vendor relationships

---


---

## System Requirements

### Data Requirements

The system manages four main entities:

1. **Vendors** - Software suppliers (e.g., Microsoft, Adobe)
   - Company name, contact email, website, country, default currency

2. **Licenses** - Software licenses owned by the company
   - Software name, license key, purchase/expiry dates, number of seats, cost, currency, status, linked vendor

3. **Users** - Employees who use the software
   - Name, email, department, role

4. **License Assignments** - Links between users and licenses
   - Which user has which license, assignment date, notes

### CRUD Operations

Each entity supports full CRUD:
- **Create**: Add new records via forms
- **Read**: View all records in tables, with search and filter for licenses
- **Update**: Edit existing records (form pre-fills with current data)
- **Delete**: Remove records with confirmation dialog

### Additional Features

- **Search and Filter**: Search licenses by software name, filter by status (Active/Expiring/Expired)
- **Seat Tracking**: Shows how many seats are used vs. available for each license
- **Auto Status Updates**: Automatically marks licenses as "expired" or "expiring" based on dates
- **Currency Conversion**: Convert license costs between currencies using the ExchangeRate API
- **Validation**: Required fields enforced on both client and server side
- **Delete Protection**: Cannot delete a vendor that still has licenses linked to it
- **Cascading Deletes**: Removing a user or license automatically removes their assignments

---


---

## Architecture

```
Browser (JavaScript)  <--->  Flask API (Python)  <--->  SQLite Database
```

- **Frontend**: Single HTML page with inline CSS and JavaScript. Uses `fetch()` to make API calls.
- **Backend**: Python Flask with Blueprint-based route modules. Returns JSON responses.
- **Database**: SQLite with 4 tables and foreign key relationships.
- **External API**: ExchangeRate API (open.er-api.com) for currency conversion.

The system follows an **API-based architecture** — the frontend communicates with the backend exclusively through API calls. No page refreshes occur; all updates happen on the same page using JavaScript DOM manipulation.

---


---

## Database Schema

### Entity Relationship

```
vendors (1) ----< (many) licenses (1) ----< (many) license_assignments >---- (1) users
```

- A vendor can have many licenses
- A license can be assigned to many users (limited by seat count)
- A user can have many license assignments

### Tables

**vendors**
| Column | Type | Notes |
|--------|------|-------|
| id | INTEGER | Primary key, auto-increment |
| company_name | TEXT | Required |
| contact_email | TEXT | |
| website | TEXT | |
| country | TEXT | |
| default_currency | TEXT | Default: USD |

**licenses**
| Column | Type | Notes |
|--------|------|-------|
| id | INTEGER | Primary key, auto-increment |
| software_name | TEXT | Required |
| license_key | TEXT | Required |
| purchase_date | TEXT | ISO date format |
| expiry_date | TEXT | ISO date format |
| seats | INTEGER | Default: 1 |
| cost | REAL | Default: 0.0 |
| currency | TEXT | Default: USD |
| status | TEXT | active / expiring / expired |
| vendor_id | INTEGER | Foreign key to vendors |

**users**
| Column | Type | Notes |
|--------|------|-------|
| id | INTEGER | Primary key, auto-increment |
| name | TEXT | Required |
| email | TEXT | Required, unique |
| department | TEXT | |
| role | TEXT | |

**license_assignments**
| Column | Type | Notes |
|--------|------|-------|
| id | INTEGER | Primary key, auto-increment |
| license_id | INTEGER | Foreign key to licenses |
| user_id | INTEGER | Foreign key to users |
| assignment_date | TEXT | ISO date format |
| notes | TEXT | |

---


---

## API Documentation

### Vendor Endpoints

| Method | URL | Description |
|--------|-----|-------------|
| GET | `/api/vendors` | Get all vendors |
| POST | `/api/vendors` | Create a new vendor |
| PUT | `/api/vendors/<id>` | Update a vendor |
| DELETE | `/api/vendors/<id>` | Delete a vendor |

### License Endpoints

| Method | URL | Description |
|--------|-----|-------------|
| GET | `/api/licenses?status=active&search=Office` | Get licenses (with optional filter/search) |
| POST | `/api/licenses` | Create a new license |
| PUT | `/api/licenses/<id>` | Update a license |
| DELETE | `/api/licenses/<id>` | Delete a license |

### User Endpoints

| Method | URL | Description |
|--------|-----|-------------|
| GET | `/api/users` | Get all users |
| POST | `/api/users` | Create a new user |
| PUT | `/api/users/<id>` | Update a user |
| DELETE | `/api/users/<id>` | Delete a user |

### Assignment Endpoints

| Method | URL | Description |
|--------|-----|-------------|
| GET | `/api/assignments` | Get all assignments (with joined names) |
| POST | `/api/assignments` | Create an assignment (checks seat availability) |
| PUT | `/api/assignments/<id>` | Update an assignment |
| DELETE | `/api/assignments/<id>` | Delete an assignment |

### Currency Conversion

| Method | URL | Description |
|--------|-----|-------------|
| GET | `/api/convert?amount=100&from=USD&to=EUR` | Convert currency using ExchangeRate API |

---


---

## Setup and Installation

### Prerequisites
- Python 3.x installed
- pip (Python package manager)

### Steps

1. Clone the repository:
   ```
   git clone <repository-url>
   cd Karthik
   ```

2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

3. Run the application:
   ```
   python app.py
   ```

4. Open your browser and go to:
   ```
   http://localhost:5000
   ```

The database file (`license_manager.db`) is created automatically on first run.

---

