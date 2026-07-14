# Karthik IT Solutions - Software License Manager

## Overview

This is a web-based Software License Manager built for **Karthik IT Solutions**, a small IT consultancy. The application helps the company track its software licenses, manage vendors, assign licenses to employees, and monitor costs across different currencies.

The system is built as a **proof-of-concept** CRUD (Create, Read, Update, Delete) application using Python Flask, SQLite, and JavaScript.

---

## Organisation

**Karthik IT Solutions** is a small IT consultancy that manages multiple software licenses for its team and clients. The company works with various software vendors (Microsoft, Adobe, etc.) across different countries and currencies. They need a central system to:

- Track which software licenses they own
- Know when licenses are expiring
- See who is using which license
- Monitor software costs across different currencies
- Manage vendor relationships

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

## How to Use

### Workflow

1. **Start with Vendors**: Add your software vendors first (e.g., Microsoft, Adobe)
2. **Add Licenses**: Create licenses and link them to vendors
3. **Add Users**: Add employees who will use the software
4. **Assign Licenses**: Go to the Assignments tab to assign licenses to users

### Using Each Tab

- **Vendors Tab**: Add/edit/delete vendor companies. You cannot delete a vendor that still has licenses.
- **Licenses Tab**: Add/edit/delete licenses. Use the search box and status filter to find specific licenses. Use the "Convert" button to see costs in different currencies.
- **Users Tab**: Add/edit/delete employees. Deleting a user removes their license assignments.
- **Assignments Tab**: Assign licenses to users. The dropdown shows available seats. You cannot assign more users than the license allows.

### Editing a Record
1. Click the "Edit" button on any row
2. The form fills with the current data
3. Make your changes
4. Click "Save Changes"
5. Click "Cancel" to discard changes

---

## External API Integration

### ExchangeRate API

The application uses the **Open ExchangeRate API** (https://open.er-api.com) to convert license costs between currencies. This is a free API that requires no API key.

**How it works:**
1. On the Licenses tab, select a target currency from the "Convert costs to" dropdown
2. Click "Convert"
3. Each license's cost is converted and displayed in the "Converted" column

**Why this matters:** Karthik IT Solutions works with vendors in different countries and currencies. Being able to see all costs in one currency helps the company evaluate total software spending and make budget decisions.

The conversion is handled server-side (through Flask) rather than directly from JavaScript, following the API-based architecture requirement.

---

## Testing

### Running Tests

```
pytest tests/ -v
```

### Test Coverage

**Unit Tests (20 tests across 4 files):**

- `test_vendors.py` - Tests vendor CRUD, validation, and delete protection
- `test_licenses.py` - Tests license CRUD, search, filter, and vendor validation
- `test_users.py` - Tests user CRUD, validation, and duplicate email check
- `test_assignments.py` - Tests assignment CRUD, seat limits, and cascade deletes

**Integration Test (1 comprehensive workflow):**

- `test_integration.py` - Tests a complete business workflow end-to-end:
  1. Creates a vendor, license, and users
  2. Assigns licenses and checks seat counts
  3. Tests currency conversion (with mocked external API)
  4. Tests unassigning and cascade deletes
  5. Verifies clean state at the end

### Test Results

All 25 tests pass successfully:
```
25 passed in 0.78s
```

---

## Project Structure

```
D:/Karthik/
├── app.py                  # Main Flask app (~30 lines)
├── db.py                   # Database connection and schema (~60 lines)
├── routes_vendors.py       # Vendor CRUD endpoints (~65 lines)
├── routes_licenses.py      # License CRUD endpoints (~100 lines)
├── routes_users.py         # User CRUD endpoints (~75 lines)
├── routes_assignments.py   # Assignment CRUD endpoints (~80 lines)
├── routes_convert.py       # Currency conversion endpoint (~40 lines)
├── templates/
│   └── index.html          # Single-page frontend (~550 lines)
├── tests/
│   ├── conftest.py         # Shared test fixtures
│   ├── test_vendors.py     # Vendor unit tests
│   ├── test_licenses.py    # License unit tests
│   ├── test_users.py       # User unit tests
│   ├── test_assignments.py # Assignment unit tests
│   └── test_integration.py # Integration test
├── requirements.txt        # Python dependencies
└── README.md               # This file
```

---

## Technologies Used

- **Python 3.11** - Backend programming language
- **Flask 3.0** - Web framework for building the API
- **SQLite** - Lightweight database for data storage
- **JavaScript** - Frontend logic (fetch API calls, DOM manipulation)
- **HTML/CSS** - Page structure and styling (inline, within Flask template)
- **ExchangeRate API** - External API for currency conversion
- **pytest** - Testing framework

---

## Deployment (Ubuntu Server - GCP)

### Server Details

- **Server IP:** 34.140.56.119
- **OS:** Ubuntu 24.04 LTS
- **Platform:** Google Cloud Platform (Compute Engine)
- **WSGI Server:** Gunicorn

### Prerequisites

- SSH key (`id_ed25519`) with access to the server
- Python 3, pip, git installed on the server

### Connect to Server

```bash
ssh -i id_ed25519 ubuntu@34.140.56.119
```

### First-Time Setup

```bash
sudo apt update && sudo apt install python3 python3-pip python3-venv git -y
cd ~
git clone https://github.com/GunnamKarthik/20102320-CA1.git
cd 20102320-CA1
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
pip install gunicorn
```

### Start the Application

```bash
cd ~/20102320-CA1
source venv/bin/activate
pkill gunicorn
python3 -c "from db import init_db; init_db()"
gunicorn --bind 0.0.0.0:5000 app:app
```

### Access the Application

Open in browser: `http://34.140.56.119:5000`

### Useful Commands

| Command | Description |
|---------|-------------|
| `pkill gunicorn` | Stop the application |
| `gunicorn --bind 0.0.0.0:5000 app:app` | Start the application |
| `cd ~/20102320-CA1 && git pull` | Pull latest code from GitHub |

### Firewall

If the application is not reachable, ensure port 5000 is open in the GCP firewall:
- Go to VPC Network > Firewall Rules
- Create a rule allowing TCP port 5000 from 0.0.0.0/0

---

## Attributions

- **Flask** - Web framework (https://flask.palletsprojects.com/) - BSD License
- **ExchangeRate API** - Free currency conversion API (https://open.er-api.com)
- **pytest** - Testing framework (https://pytest.org/) - MIT License
- **requests** - HTTP library for Python (https://requests.readthedocs.io/) - Apache 2.0 License
