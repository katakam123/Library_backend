# Library Management Backend API

A complete 'Library Management Backend API' built using 'FastAPI, SQLAlchemy, and MySQL'.

This project provides REST APIs for managing library categories, books, members, and borrowing/return transactions. It includes data validation, database relationships, CRUD operations, and email validation.

---

# Project Overview

The Library Backend is a RESTful API developed with Python and FastAPI.

The main purpose of this project is to provide backend functionality for a library management system.

The system can be used to:
* Manage library categories
* Manage books
* Manage library members
* Manage book borrowing records
* Manage book returns
* Store data permanently in MySQL
* Validate user input
* Handle database relationships
* Provide interactive API documentation

---

# Technologies Used

* Python 3.9+
* FastAPI
* Uvicorn
* SQLAlchemy
* MySQL
* PyMySQL
* Pydantic
* Pydantic Settings
* python-dotenv
* email-validator

---

# Project Structure

Library_backend/
│
├── app/
│   ├── main.py
│   ├── database.py
│   │
│   ├── models/
│   │   ├── __init__.py
│   │   ├── category.py
│   │   ├── book.py
│   │   ├── member.py
│   │   └── borrow_record.py
│   │
│   ├── schemas/
│   │   ├── __init__.py
│   │   ├── category.py
│   │   ├── book.py
│   │   ├── member.py
│   │   └── borrow_record.py
│   │
│   ├── routers/
│   │   ├── __init__.py
│   │   ├── categories.py
│   │   ├── books.py
│   │   ├── members.py
│   │   └── borrow_records.py
│   │
│   └── services/
│       ├── __init__.py
│       └── borrow_service.py
│
├── .env
├── .gitignore
├── requirements.txt
└── README.md

---

# Database

This project uses 'MySQL' as the database and 'SQLAlchemy' as the ORM.

The database connection details are stored in the .env file instead of directly inside the Python code.

Example:
env
DATABASE_URL=mysql+pymysql://username:password@localhost/library_db


Replace:

* 'username' with MySQL username
* 'password' with MySQL password

---

# Database Relationships

The project uses relationships between different library entities.

# Category → Books

One category can contain multiple books.

Category
   │
   └─── Book
   └─── Book
   └─── Book

# Member → Borrow Records

One member can have multiple borrowing records.

Member
   │
   └─── Borrow Record
   └─── Borrow Record

These relationships are implemented using SQLAlchemy.

---

# Installation

# Create a Virtual Environment
Windows:
python -m venv venv

Activate the virtual environment:
venv\Scripts\activate

# Install Dependencies
Install all required packages:
pip install -r requirements.txt

The project dependencies include FastAPI, Uvicorn, SQLAlchemy, PyMySQL, Pydantic, python-dotenv, pydantic-settings, and email-validator.

---

# MySQL Setup

Open MySQL and create the database:
CREATE DATABASE library_db;

Select the database:
USE library_db;

The application uses SQLAlchemy to create and manage the required database tables.

Make sure your MySQL server is running before starting the FastAPI application.

---

# Running the Application

Start the FastAPI server using:
uvicorn app.main:app --reload

The application will normally run at:
http://127.0.0.1:8000

---

# API Documentation

FastAPI automatically provides interactive API documentation.

# Swagger UI

Open:
http://127.0.0.1:8000/docs

Swagger UI allows you to:

* View available APIs
* Enter request data
* Send API requests
* Test POST requests
* Test GET requests
* Test PUT requests
* Test DELETE requests
* View response status codes
* View validation errors

# ReDoc
Alternative API documentation is available at:
http://127.0.0.1:8000/redoc

---

# Main API Modules

##  Category Management

Categories are used to organize books.

### Create Category
POST /categories

### Get Categories
GET /categories

### Get Category by ID
GET /categories/{category_id}

### Update Category
PUT /categories/{category_id}

### Delete Category
DELETE /categories/{category_id}

The category name is unique, so duplicate category names are not allowed.

---

# Book Management

Books can be associated with a particular category.

Typical book operations include:
POST /books
GET /books
GET /books/{book_id}
PUT /books/{book_id}
DELETE /books/{book_id}

---

# Member Management

Members represent people who use the library.

Typical operations include:
POST /members
GET /members
GET /members/{member_id}
PUT /members/{member_id}
DELETE /members/{member_id}

Email addresses are validated using email validation support.

---

# Borrow and Return Management

The borrowing module manages the relationship between members and books.

A borrowing record can contain information such as:
* Member
* Book
* Borrow date
* Return date
* Borrow/return status

 Workflow:

Member
   ↓
Selects Book
   ↓
Borrow Record Created
   ↓
Book Borrowed
   ↓
Book Returned
   ↓
Return Date Updated

---

# Validation

The application uses Pydantic schemas for request validation.

Validation can be used to ensure:
* Required fields are provided
* Email addresses have a valid format
* Data types are correct
* Duplicate category names are prevented
* Invalid IDs are handled
* Invalid database operations return appropriate errors


The API can return a validation error instead of accepting invalid data.

---

#  Error Handling

The API handles common errors such as:

* Resource not found
* Duplicate data
* Invalid input
* Database errors
* Invalid IDs
* Validation errors

FastAPI provides appropriate HTTP status codes and error responses.

---

#  Architecture
The project follows a structured backend architecture.

Client
  ↓
FastAPI
  ↓
Router
  ↓
Schema Validation
  ↓
Service / Business Logic
  ↓
SQLAlchemy ORM
  ↓
MySQL Database

###  main.py
The main entry point of the FastAPI application.
It creates the FastAPI application and includes the API routers.

### database.py
Responsible for the database connection and SQLAlchemy configuration.

### models/
Contains SQLAlchemy database models.
Models represent database tables.

### schemas/
Contains Pydantic schemas.

Schemas are used for:

* Request validation
* Response validation
* Data serialization

### routers/
Contains API endpoints.
Routers handle HTTP requests such as:
* POST
* GET
* PUT
* DELETE

### services/
Contains business logic that can be separated from the API route functions.

---

# Testing the API
The API can be tested using:
* Swagger UI
* Postman
* Browser for GET requests
* Other API testing tools

For example, open:
http://127.0.0.1:8000/docs

Then select an endpoint and click:
Try it out

Enter the required information and click:
Execute

---

# HTTP Methods Used

| Method | Purpose              |
| ------ | -------------------- |
| POST   | Create new data      |
| GET    | Retrieve data        |
| PUT    | Update existing data |
| DELETE | Delete data          |

---

#  Example API Flow

A typical library operation can work as follows:

1. Create Category
        ↓
2. Add Book
        ↓
3. Register Member
        ↓
4. Member Borrows Book
        ↓
5. Borrow Record Created
        ↓
6. Member Returns Book
        ↓
7. Return Information Updated

---

# 🔐 Security

Database credentials should be stored in environment variables.

Example:
DATABASE_URL=your_database_connection

The .env file should not be committed to GitHub.

.gitignore:
.env
venv/
__pycache__/
*.pyc

---

#  Project Objectives

The main objectives of this project are:
* Build a RESTful backend using FastAPI
* Connect FastAPI with MySQL
* Use SQLAlchemy ORM
* Implement CRUD operations
* Implement database relationships
* Validate API input
* Handle errors
* Separate models, schemas, routers, and services
* Provide interactive API documentation

---

# Features
* FastAPI REST API
* MySQL database
* SQLAlchemy ORM
* CRUD operations
* Category management
* Book management
* Member management
* Borrow/return management
* Database relationships
* Pydantic validation
* Email validation
* Environment-based configuration
* Swagger API documentation
* ReDoc documentation
* Error handling

---

# Requirements
The project requires:
fastapi
uvicorn[standard]
sqlalchemy
pymysql
python-dotenv
pydantic
pydantic-settings
email-validator

All dependencies can be installed using:
pip install -r requirements.txt
