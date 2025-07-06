# 📚 SBA24070 Book Catalogue App

**Database Flexibility Note:**
- You do **not** have to use the database provided by default.
- By default, the app uses SQLite, which requires no setup—just clone and run.
- You can switch to PostgreSQL (or another supported DB) by updating `settings.py` (or your `.env` for Docker) and running migrations.
- See [Quickstart Guide](docs/QUICKSTART.md) for setup instructions for both local and Docker environments.

You can use the provided scripts for setup:
- `./run_django.sh`: Sets HOST to 'localhost', installs requirements, runs migrations, and starts the Django server.
- `./run_docker.sh`: Sets HOST to 'db', builds and starts Docker containers, runs migrations, and starts the app.
- `./setup.sh`: Interactive setup for both modes, ensures correct HOST is set and all requirements are met.

---

## 📄 Documentation & Examples

- [Quickstart Guide](docs/QUICKSTART.md): Step-by-step setup and usage instructions
- [API Documentation](API_DOCUMENTATION.md): Full REST API reference and usage
- [API Example (JavaScript)](static/js/api-example.js): Example code for using the API with JavaScript

---

## 🛠️ Tech Stack

- **Backend**: Django (Python 3.8+)
- **Database**: SQLite (default), PostgreSQL ready
- **Frontend**: HTML + Bootstrap + Custom CSS
- **External API**: [Open Library](https://openlibrary.org/developers/api)
- **Version Control**: Git + GitHub
- **Authentication**: Custom user model with password hashing

---

## 👨‍💻 Author

**James Scott**  
Student ID: SBA24070  
Email: jamesdeanscott19@gmail.com  
GitHub: [github.com/Jamesscott34](https://github.com/Jamesscott34)

---

## 🚀 How It Works

- **Login Page** is the default landing page when you visit the application.
- **User Registration** allows new users to sign up with a username, email, and password.
- **Home Page** (after login) shows all saved books in a table with reading progress.
- **Manual Add** lets you enter title, author, published date, description, and an auto-generated ISBN (starting with `JS`).
- **Open Library Search** lets you search external books, view results, and import selected ones into your library.
- **Admin Dashboard**: If you log in as `admin`, you get a special admin dashboard page with user management and statistics. Admin can view any user's books and set a referral book for any user.
- **Books are saved in SQLite DB** using Django's ORM by default.
- **Books can be edited, deleted, and marked read/unread**.
- **Notification System** allows admins to send personalized messages and book recommendations to users.
- **User/Admin Book Separation**: Users and admin see only their own books on `/home/`. Admin can view any user's books from the dashboard.
- **Admin Referral Feature**: Admin can set a referral book for any user; users can add the referral to their collection from their profile.
- **User Notes**: Users can add/edit personal notes in their profile.

---

## ✅ Features So Far

- [x] Login Page as Default Landing Page
- [x] Manual Book Entry Form with Description and JS-ISBN
- [x] Editable Book Entries
- [x] Delete and Toggle Status
- [x] Open Library Integration with Search + Import
- [x] Book Table with Description Column
- [x] Bootstrap Styling with Custom Color Theme
- [x] User Registration (Sign Up)
- [x] User Login/Logout with Session Management
- [x] Personalized Welcome Message
- [x] Admin User and Dashboard
- [x] Admin User Management Script
- [x] User Deletion from Admin Dashboard
- [x] User Profile Editing and Password Reset
- [x] Profile Deletion with Confirmation
- [x] Comprehensive Notification System
- [x] Book Statistics and Reading Progress Tracking
- [x] Admin Restrictions (can only change own email, cannot notify self)
- [x] Book View Tracking and Attribution
- [x] Automatic Book Saving from Notifications
- [x] Complete REST API with Authentication, CRUD Operations, and Statistics
- [x] Add search and filter options to local book list
- [x] Improve validation and error handling
- [x] Implement cover image upload for manually added books
- [x] Add book categories and tags
- [x] User/admin book separation (users and admin see only their own books on `/home/`)
- [x] Admin can view any user's books from the admin dashboard
- [x] Admin referral feature: admin can set a referral book for any user, and users can add it to their collection
- [x] User notes: users can add/edit personal notes in their profile

---

## ️ What To Do Next

- [ ] Implement email notification functionality
- [ ] Add book import/export (CSV, JSON)
- [ ] Add analytics/dashboard for users (reading stats, most read authors, etc.)
- [ ] Enhance book cover image support (drag-and-drop, cropping)
- [ ] Add user profile picture/avatar
- [ ] Improve mobile responsiveness and accessibility
- [ ] Add Kubernetes manifests for deployment, service, ingress, and config
- [ ] Create a Helm chart for easy deployment and configuration
- [ ] Set up CI/CD pipeline for automated testing, building, and deployment to Kubernetes

---

## ✅ REST API

A complete REST API is available for integration with JavaScript frontends, mobile apps, and other services. See [API Documentation](API_DOCUMENTATION.md) for all endpoints, authentication, and usage examples.

---