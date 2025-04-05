# 💸 Mini Payment Gateway API

A minimal FastAPI-based backend that allows you to create customers and process payments using SQLAlchemy ORM with support for PostgreSQL, MySQL, or SQLite.

---

## 🚀 Features

- Create customer with name and email
- Make payments using customer ID, amount, currency, and method
- SQLAlchemy ORM with PostgreSQL/MySQL support
- Environment-based database configuration
- Swagger UI for interactive API testing

---

## 📁 Project Structure

app/ ├── api/ │ └── routes.py # API endpoints ├── db/ │ ├── session.py # DB engine and session │ ├── base.py # SQLAlchemy base class │ └── init_db.py # DB initializer ├── models/ │ ├── customer.py # Customer model │ └── payment.py # Payment model ├── schemas/ │ ├── customer.py # Customer Pydantic schema │ └── payment.py # Payment Pydantic schema ├── main.py # FastAPI app entry point run.py # Run file for launching the app .env # Environment variables


---

## 🛠 Setup Instructions

### 1. Clone the repository

```bash
git clone https://github.com/your-username/mini-payment-gateway.git
cd mini-payment-gateway
