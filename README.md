# 📚 SBA24070 Book Catalogue App

**Database Flexibility Note:**
- By default, the app uses SQLite, which requires no setup—just clone and run.
- You can switch to PostgreSQL (or another supported DB) by updating `settings.py` (or your `.env` for Docker) and running migrations.
- See [Quickstart Guide](docs/QUICKSTART.md) for setup instructions for both local and Docker environments.

You can use the provided scripts for setup:
- `./run_django.sh`: Local Django setup
- `./run_docker.sh`: Docker Compose setup
- `./setup.sh`: Interactive setup for both modes

---

## 📄 Documentation & Examples
- [Quickstart Guide](docs/QUICKSTART.md)
- [API Documentation](API_DOCUMENTATION.md)
- [API Example (JavaScript)](static/js/api-example.js)

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
- **Login Page** is the default landing page.
- **User Registration** for new users.
- **Home Page** shows your saved books and reading progress.
- **Manual Add**: Enter book details and auto-generate ISBN.
- **Open Library Search**: Search/import books from Open Library.
- **Admin Dashboard**: Admin can view/manage users, see stats, view any user's books, and set referral books.
- **Books**: Edit, delete, mark read/unread.
- **Notifications**: Admins can send messages and book recommendations.
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

## 🚢 Deploying with Helm & Kubernetes

See [HELM_DEPLOYMENT.md](HELM_DEPLOYMENT.md) for full instructions on using the Helm chart in `book-catalogue/` to deploy this app to Kubernetes.

---

## ✅ REST API
A complete REST API is available for integration with JavaScript frontends, mobile apps, and other services. See [API Documentation](API_DOCUMENTATION.md) for all endpoints, authentication, and usage examples.

---

## 👤 Author & License
**James Scott**  
Student ID: SBA24070  
Email: jamesdeanscott19@gmail.com  
GitHub: [github.com/Jamesscott34](https://github.com/Jamesscott34)

This project is part of the SBA24070 coursework and is for educational purposes.

=======

## 📋 Notification System Support

For issues and questions:
1. Check the troubleshooting section
2. Review the admin management script documentation
3. Check Django documentation for framework-specific issues

---
