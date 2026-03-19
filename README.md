# School Management System | Django

A full-stack web application built using Django to manage school operations including student management, teacher workflows, and assignment handling.

---

## Overview

This project simulates a real-world school management system where students, teachers, and administrators interact through role-based dashboards. It focuses on backend development, structured system design, and data handling using Django.

---

## Key Features

### Authentication and Authorization
- User registration and login system
- Role-based access control (Admin, Teacher, Student)
- JWT-based authentication support

### Teacher Module
- Create and manage assignments
- View student submissions
- Update scores and feedback

### Student Module
- Submit assignments with file upload support
- View submitted work and results
- Access assigned tasks

### Admin Module
- Manage students and teachers
- Monitor system data
- Update user details

### File Handling
- Upload and manage assignment files
- Organized submission tracking

---

## Tech Stack

- Backend: Django, Django REST Framework
- Authentication: JWT (SimpleJWT)
- Frontend: HTML, CSS, Bootstrap
- Database: SQLite (development)
- Tools: Git, GitHub

---

## Project Structure

## Project Structure
```
school-management-system-django/
│
├── manage.py
├── requirements.txt
├── .gitignore
│
├── school_system/
│   ├── __init__.py
│   ├── asgi.py
│   ├── middleware.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
│
├── school_system_app/
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── custom_auth.py
│   ├── forms.py
│   ├── models.py
│   ├── signals.py
│   ├── tests.py
│   ├── urls.py
│   ├── utils.py
│   ├── views.py
│   │
│   ├── controllers/
│   │   ├── admin.py
│   │   ├── students.py
│   │   ├── teachers.py
│   │   └── users.py
│   │
│   ├── migrations/
│   │   └── __init__.py
│   │
│   └── templates/
│       ├── admin_page.html
│       ├── admin_update.html
│       ├── assignment.html
│       ├── intro_video.html
│       ├── list_submissions.html
│       ├── login.html
│       ├── permission_denied.html
│       ├── profiles.html
│       ├── register.html
│       ├── score_update.html
│       ├── student_list.html
│       ├── student_register.html
│       ├── student_update.html
│       ├── submission.html
│       ├── teacher_list.html
│       ├── teacher_register.html
│       ├── teacher_update.html
│       ├── update_assignment.html
│       ├── view_assignments.html
│       ├── view_file.html
│       ├── view_file_teacher.html
│       ├── view_submits.html
│       │
│       └── passwords/
│           ├── password_reset_complete.html
│           ├── password_reset_confirm.html
│           ├── password_reset_done.html
│           ├── password_reset_email.html
│           └── password_reset_form.htmlschool_system/  
---

## Setup Instructions

### Clone the Repository
git clone https://github.com/yourusername/school-management-system-django.git  
cd school-management-system-django  

### Create Virtual Environment
python -m venv venv  
venv\Scripts\activate  

### Install Dependencies
pip install -r requirements.txt  

### Apply Migrations
python manage.py migrate  

### Run Server
python manage.py runserver  

---

## What This Project Demonstrates

- Strong understanding of Django architecture
- Role-based system design
- Backend and frontend integration using templates
- File handling and validation
- Modular code structure using controllers and utilities

---

## Notes

- .env file is excluded for security
- SQLite is used for development purposes only

---

## Future Improvements

- Deployment on cloud platforms such as AWS or Render
- REST API expansion for frontend integration
- UI improvements using modern frameworks
- Performance optimization and pagination

---

## Author

Thrisha Reddy Kumbam  
Master’s in Computer Science  
SUNY Polytechnic Institute  
