# Freelancer Gigs & Invoicing API

A backend API built with **FastAPI**, **SQLAlchemy**, and **Pydantic** to help freelancers manage **clients**, **gigs**, and **invoices** in a clean, real‑world–oriented way.

This project focuses on **correct data modeling**, **business rules**, and **production‑style API design**, rather than just basic CRUD.

This backend serves the following frontend https://github.com/TrangLe265/freelancer-hub

---

## ✨ Features

* Manage **Clients**, **Gigs**, and **Invoices**
* Status‑based lifecycle management (no unsafe hard deletes)
* Automatic invoice dates (issue date + 15‑day due date)
* Computed invoice totals based on gig wage
* Flexible filtering (by client, gig, status)
* Realistic seed data for demos and testing
* OpenAPI / Swagger documentation out of the box

---

## 🧱 Tech Stack

* **Python 3.9+**
* **FastAPI** – API framework
* **SQLAlchemy** – ORM
* **Pydantic** – data validation & serialization
* **SQLite / PostgreSQL** (configurable)
* **Uvicorn** – ASGI server

---

## 🧠 Domain Model

### Client

* Represents a freelancer’s customer
* Uses **soft‑delete via status** instead of hard deletion

Statuses:

* `active`
* `inactive`
* `archived`

---

### Gig

* Represents a freelance job or contract
* Each gig belongs to a client
* A gig may have **at most one invoice**

Statuses:

* `pending`
* `completed`
* `cancelled`

> Cancelling a gig automatically voids its associated invoice (if any).

---

### Invoice

* Represents a financial document for a gig
* Invoice totals are **computed dynamically** from the gig wage
* Invoices are never deleted

Statuses:

* `draft`
* `created`
* `sent`
* `paid`
* `void`

---

## 📐 Design Decisions

### ❌ No Hard Deletes

To preserve auditability and data integrity:

| Entity  | Strategy                 |
| ------- | ------------------------ |
| Client  | Status‑based (archived)  |
| Gig     | Status‑based (cancelled) |
| Invoice | Status‑based (void)      |

This reflects real‑world accounting and compliance practices.

---

### 📄 Invoice Defaults

* `issue_date` defaults to **today**
* `due_date` defaults to **15 days after issue date**

Handled using `default_factory` to ensure values are calculated **at request time**, not import time.

---

### 🧮 Computed Fields

* `Invoice.total_amount` is derived from `Gig.wage`
* Prevents duplication and ensures consistency

---

## 🔌 API Endpoints (Overview)

### Clients

* `POST /clients`
* `GET /clients`
* `GET /clients/{id}`
* `PATCH /clients/{id}` (update / archive)

### Gigs

* `POST /gigs`
* `GET /gigs`
* `GET /gigs/{id}`
* `PATCH /gigs/{id}` (update / cancel)

### Invoices

* `POST /invoices`
* `GET /invoices`
* `GET /invoices/{id}`
* `PATCH /invoices/{id}` (status updates)

Filtering invoices:

```
GET /invoices?client_id=1&status=paid
```

---

## 🌱 Seed Data

The project includes realistic seed data:

* Multiple clients
* Multiple gigs per client
* Invoices in different lifecycle stages

This makes it easy to:

* Test filtering
* Demonstrate business logic
* Showcase the API in interviews

Run the seed script:

```bash
python3 -m app.seed
```
If you need to clear the database and start from scratch: 

```bash
python3 -m app.reset_db
```
---

## 🚀 Getting Started

### 1. Clone the repository

```bash
git clone <repo-url>
cd freelancer-invoicing-api
```

### 2. Create a virtual environment

```bash
python3 -m venv venv
source venv/bin/activate
```
Now your terminal should start working with the (venv) prefix

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Run the API

```bash
uvicorn app.main:app --reload
```

### 5. Open API docs

* Swagger UI: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
* ReDoc: [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)

---

## 🧪 Development Notes

* Uses **Pydantic schemas** to separate create/update/response concerns
* Uses **PATCH** for partial updates
* Enum‑based state transitions enforce business rules
* Designed for easy extension (auth, payments, exports)

---

## 📌 Future Improvements

* Authentication & user accounts
* Pagination for list endpoints
* PDF invoice generation
* Payment provider integration
* Background tasks for reminders

---

## 📄 License

This project is for learning and portfolio purposes.

---

## 👤 Author

Built by **Trang Thuy Le**

