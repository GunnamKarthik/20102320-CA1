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

