# FastAPI User Management System

A FastAPI application implementing JWT Authentication, User Profile Management, Education Details, and Personal Details using a layered architecture.

---

## Features

* JWT Authentication
* User Registration and Login
* Protected Routes
* User CRUD Operations
* Education CRUD Operations
* Personal Details CRUD Operations
* PUT and PATCH Support
* MySQL Database Integration
* Environment Variables with `.env`
* Service Layer Architecture
* Clean and Modular Project Structure

---

# Tech Stack

* Python
* FastAPI
* MySQL
* Pydantic
* JWT Authentication
* Passlib (bcrypt)
* python-jose
* python-dotenv

---

# Project Structure

```text
project
│
├── main.py
├── auth.py
├── database.py
├── config.py
├── .env
│
├── models
│   ├── user_model.py
│   ├── education_model.py
│   └── personal_detail_model.py
│
├── schemas
│   ├── user_schema.py
│   ├── education_schema.py
│   └── personalDetail_schema.py
│
├── routers
│   ├── auth.py
│   ├── users.py
│   ├── education.py
│   └── personal_details.py
│
├── services
│   ├── users_service.py
│   ├── education_service.py
│   └── personal_details_service.py
│
├── utils
│   ├── user_mapper.py
│   ├── user_details_mapper.py
│   ├── education_mapper.py
│   └── personal_details_mapper.py
│
└── requirements.txt
```

---

# Architecture

This project follows the Service Layer Pattern.

```text
Client
   ↓
Router
   ↓
Schema Validation
   ↓
Service Layer
   ↓
Database
   ↑
Service Layer
   ↓
Utils (Tuple → Dictionary)
   ↓
JSON Response
```

---

# Installation

## Clone Repository

```bash
git clone <repository-url>
cd project
```

## Create Virtual Environment

```bash
python -m venv venv
```

### Windows

```bash
venv\Scripts\activate
```

### Linux / Mac

```bash
source venv/bin/activate
```

---

## Install Dependencies

```bash
pip install -r requirements.txt
```

---

# Environment Variables

Create a `.env` file:

```env
SECRET_KEY=""
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

DB_HOST=localhost
DB_USER="your_DB_user"
DB_PASSWORD="your_DB_password"
DB_NAME="your_DB_name"
```

---

# Running the Application

```bash
uvicorn main:app --reload
```

Application URL:

```text
http://127.0.0.1:8000
```

---

# API Documentation

Swagger UI

```text
http://127.0.0.1:8000/docs
```

ReDoc

```text
http://127.0.0.1:8000/redoc
```

---

# Authentication APIs

| Method | Endpoint       |
| ------ | -------------- |
| POST   | /auth/register |
| POST   | /auth/login    |
| GET    | /auth/profile  |

---

# User APIs

| Method | Endpoint            |
| ------ | ------------------- |
| GET    | /users              |
| GET    | /users/me           |
| GET    | /users/{id}         |
| GET    | /users/details/all  |
| GET    | /users/{id}/details |
| PUT    | /users/me           |
| PATCH  | /users/me           |
| DELETE | /users/me           |

---

# Education APIs

| Method | Endpoint            |
| ------ | ------------------- |
| POST   | /education          |
| GET    | /education          |
| GET    | /education/{edu_id} |
| PUT    | /education/{edu_id} |
| PATCH  | /education/{edu_id} |
| DELETE | /education/{edu_id} |

---

# Personal Details APIs

| Method | Endpoint               |
| ------ | ---------------------- |
| POST   | /personal-details      |
| GET    | /personal-details      |
| GET    | /personal-details/{id} |
| PUT    | /personal-details/{id} |
| PATCH  | /personal-details/{id} |
| DELETE | /personal-details/{id} |

---

# Security

* Password hashing using bcrypt
* JWT Authentication
* Bearer Token Authorization
* Protected APIs using Depends()
* Token Verification using HTTPBearer

---

# Database Tables

## Users

* id
* name
* email
* password
* age
* phone
* gender
* address
* city
* state
* country
* pincode

## Education

* edu_id
* user_id
* degree
* college_name
* specialization
* passing_year
* percentage

## Personal Details

* id
* user_id
* father_name
* mother_name
* date_of_birth
* marital_status
* nationality
* blood_group
* emergency_contact
* alternate_email

---

# Future Improvements

* SQLAlchemy ORM
* Repository Layer Pattern
* Alembic Migrations
* Docker Support
* Redis Caching
* Pagination
* Role-Based Access Control (RBAC)
* Logging
* Unit Testing with Pytest
* CI/CD Pipeline
* Kubernetes Deployment

---

# Author

Developed with FastAPI and MySQL following production-level layered architecture principles.
