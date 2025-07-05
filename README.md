# 📚 SBA24070 Book Catalogue App

This is a Django-based book catalogue system developed as part of a DevOps assignment. It allows users to manage personal book collections with the ability to:

- Add/edit/delete books manually
- Browse and import books from the Open Library API
- Toggle read/unread status
- Store descriptions and auto-generate ISBNs
- **Register, log in, and log out as a user**
- **Admin user with special dashboard**
- **Beautiful, modern color theme and UI**

---

## 🚀 How It Works

- **Home Page** shows all saved books in a table.
- **Manual Add** lets you enter title, author, published date, description, and an auto-generated ISBN (starting with `JS`).
- **Open Library Search** lets you search external books, view results, and import selected ones into your library with auto-generated ISBNs.
- **User Registration** allows new users to sign up with a username, email, and password.
- **Login/Logout** for all users.
- **Admin Dashboard**: If you log in as `admin`, you get a special admin dashboard page.
- **Books are saved in a PostgreSQL/SQLite DB** using Django's ORM.
- **Books can be edited, deleted, and marked read/unread**.
- **Modern, colorful UI** with custom CSS and Bootstrap.

---

## 🛠️ What To Do Next

- [ ] Add search and filter options to local book list  
- [ ] Improve validation and error handling  
- [ ] Implement cover image upload for manually added books  
- [ ] Deploy to cloud with Docker + Kubernetes (DevOps stage)  
- [ ] Add REST API endpoints for integration with JavaScript frontends  
- [ ] Add user profile editing and password reset  

---

## ✅ Features So Far

- [x] Manual Book Entry Form with Description and JS-ISBN
- [x] Editable Book Entries
- [x] Delete and Toggle Status
- [x] Open Library Integration with Search + Import
- [x] Book Table with Description Column
- [x] Bootstrap Styling
- [x] Beautiful Custom Color Theme
- [x] User Registration (Sign Up)
- [x] User Login/Logout
- [x] Personalized Welcome Message
- [x] Admin User and Dashboard
- [x] Branching + Merging with Git (open-library-integration → master → api-js-bridge)

---

## 📦 Tech Stack

- **Backend**: Django (Python 3.13)  
- **Database**: SQLite (default), PostgreSQL ready  
- **Frontend**: HTML + Bootstrap + Custom CSS  
- **External API**: [Open Library](https://openlibrary.org/developers/api)  
- **Version Control**: Git + GitHub  
- **Deployment**: Docker & Kubernetes (coming soon)

---

## 👤 User Management

- **Register**: Go to `/register/` to create a new user account.
- **Login**: Go to `/login/` to log in with your username and password.
- **Logout**: Click the logout button in the navigation or go to `/logout/`.
- **Admin User**: If you log in as `admin`, you will be redirected to a special admin dashboard at `/admin-dashboard/`.
- **Personalized Welcome**: After login, the homepage will greet you by your username.

### Creating an Admin User
- Register a user with the username `admin` (case-sensitive) via the registration page, or add one via the Django admin interface.
- The admin user will have access to the admin dashboard and can be extended with more features.

---

## 👨‍💻 Author

**James Scott**  
Student ID: SBA24070  
Email: jamesdeanscott19@gmail.com  
GitHub: [github.com/Jamesscott34](https://github.com/Jamesscott34)

---

## 🧪 Setup Instructions

```bash
# 1. Clone the repo
https://github.com/Jamesscott34/DevopsCA.git
cd DevopsCA

# 2. Create virtual environment
python3 -m venv devops
source devops/bin/activate

# 3. Install requirements
pip install -r requirements.txt

# 4. Run migrations
python manage.py makemigrations
python manage.py migrate

# 5. (Optional) Create a superuser for Django admin
python manage.py createsuperuser

# 6. Start the dev server
python manage.py runserver
```

---

## 🌈 UI & Styling
- The app uses a beautiful, modern color theme with gradients, custom buttons, and responsive design.
- All pages are styled with Bootstrap and custom CSS for a professional look.

---

## 🗝️ Default URLs
- `/` — Home (book list)
- `/register/` — Register new user
- `/login/` — User login
- `/logout/` — User logout
- `/admin-dashboard/` — Admin dashboard (for admin user)
- `/add/` — Add book manually
- `/open-library/` — Browse Open Library

---
