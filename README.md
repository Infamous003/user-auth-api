# User Authentication API

A simple and secure User Authentication API built with FastAPI and Python.  
This API lets you create, update, delete, and retrieve user records, with JWT-based authentication.

---

## Features

- Register new users
- Log in with username and password (JWT token returned)
- Fetch all users
- Fetch a user by ID
- Update user details (protected)
- Delete a user (protected)

---

## Tech Stack

- FastAPI  
- Python  
- JWT (JSON Web Tokens)  
- SQLModel / SQLAlchemy  
- bcrypt (for password hashing)

---

## Authentication Flow

1. Users authenticate by sending valid credentials to the `/login` endpoint.
2. On success, a JWT token is issued.
3. Protected routes require this token in the `Authorization` header as a Bearer token.

---

## API Endpoints

| Method | Endpoint            | Description                         | Auth Required |
|--------|---------------------|-------------------------------------|---------------|
| POST   | `/register`         | Register a new user                 | No            |
| POST   | `/login`            | Log in and get JWT token            | No            |
| GET    | `/users`            | Get all users                       | No            |
| GET    | `/users/{id}`       | Get user by ID                      | No            |
| PUT    | `/users/{id}`       | Update user (must be same user)     | Yes           |
| DELETE | `/users/{id}`       | Delete user (must be same user)     | Yes           |

---

## Quick Start

1. Clone the repository.
2. Create a virtual environment and activate it.
3. Install dependencies:
```bash
pip install -r requirements.txt
```

Enjoy :p