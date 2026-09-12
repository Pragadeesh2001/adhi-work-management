# Adhi Work Management System

A role-based work management web application built with Django to manage customers, tenders, projects, progress updates, materials, issues, and workers in a structured workflow.

## Overview

The Adhi Work Management System helps management and team leaders track project execution from project assignment through completion.

The application provides different access levels based on user roles:

* **Management** can view all projects, create projects, assign projects to Team Leaders, and manage project status.
* **Team Leaders** can view their assigned projects and manage progress, materials, issues, and workers.

## Features

### Management

* Management dashboard
* View all projects
* Create projects
* Assign projects to Team Leaders
* Change project status
* View project reports
* View project progress
* View materials used
* View project issues
* Filter projects by status

### Team Leader

* Team Leader dashboard
* View assigned projects only
* View project details
* Add, edit, and delete progress updates
* Add, edit, and delete materials
* Add, edit, and delete issues
* Add, edit, and delete workers
* Update project progress through progress entries

### Authentication & Authorization

* Custom Django user model
* Email-based login
* Role-based access control
* Management and Team Leader roles
* Protected project access
* Users can only access functionality permitted by their role

## Project Workflow

```text
Customer
  |
  v
Tender
  |
  v
Project
  |
  v
Team Leader
  |-- Progress
  |-- Materials
  |-- Issues
  `-- Workers
```

A customer can have multiple tenders, and a tender can contain multiple projects.

Progress entries are associated with individual projects. The system calculates the project's completed quantity from its progress records and automatically updates the project status based on completion.

## Technology Stack

* **Python**
* **Django 5.1.7**
* **Django ORM**
* **Django Forms / ModelForms**
* **Django Templates**
* **Django Authentication**
* **HTML**
* **CSS**
* **SQLite**
* **Django Admin**
* **Git & GitHub**

## Database Relationships

```text
User
  `-- Team Leader
       `-- Projects

Customer
  `-- Tenders
       `-- Projects

Project
  |-- Progress
  |-- Materials
  |-- Issues
  `-- Workers
```

The application uses Django model relationships and foreign keys to maintain connections between customers, tenders, projects, and project-related records.

## Project Structure

```text
adhi-work-management/
|
|-- config/
|   |-- settings.py
|   |-- urls.py
|   |-- asgi.py
|   `-- wsgi.py
|
|-- customers/
|-- tenders/
|-- projects/
|-- progress/
|-- materials/
|-- issues/
|-- workers/
|-- users/
|
|-- templates/
|
|-- manage.py
|-- requirements.txt
|-- .gitignore
`-- README.md
```

## Local Setup

### 1. Clone the repository

```bash
git clone https://github.com/Pragadeesh2001/adhi-work-management.git
cd adhi-work-management
```

### 2. Create a virtual environment

```bash
python -m venv venv
```

### 3. Activate the virtual environment

#### Windows PowerShell

```powershell
.\venv\Scripts\Activate.ps1
```

### 4. Install dependencies

```bash
pip install -r requirements.txt
```

### 5. Apply migrations

```bash
python manage.py migrate
```

### 6. Create a superuser

```bash
python manage.py createsuperuser
```

### 7. Start the development server

```bash
python manage.py runserver
```

Open the application at:

```text
http://127.0.0.1:8000/
```

## Validation & Business Logic

The application includes validation and business logic for:

* Planned quantity must be greater than zero.
* Project end date cannot be earlier than the start date.
* Project progress is recalculated from stored progress entries.
* Project status changes automatically according to completion.
* Team Leaders can only access projects assigned to them.
* Management can access all projects.

## Current Version

The current version is a **Django-based application** using server-rendered templates.

The project focuses on implementing the core work-management workflow before introducing additional technologies.

## Future Improvements

Planned improvements include:

* Django REST Framework APIs
* React frontend
* Improved dashboard UI
* PostgreSQL database
* Production deployment
* Additional reporting and analytics
* API-based frontend integration

## Author

**Pragadeeshwaran Sivaraj**

GitHub: https://github.com/Pragadeesh2001
