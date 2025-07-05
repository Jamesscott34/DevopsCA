# 📚 SBA24070 Book Catalogue App

This is a Django-based book catalogue system developed as part of a DevOps assignment. It allows users to manage personal book collections with the ability to:

- Add/edit/delete books manually
- Browse and import books from the Open Library API
- Toggle read/unread status
- Store descriptions and auto-generate ISBNs
- **Register, log in, and log out as a user**
- **Admin user with special dashboard and user management**
- **Beautiful, modern color theme and UI**

---

## 🚀 How It Works

- **Home Page** shows all saved books in a table.
- **Manual Add** lets you enter title, author, published date, description, and an auto-generated ISBN (starting with `JS`).
- **Open Library Search** lets you search external books, view results, and import selected ones into your library with auto-generated ISBNs.
- **User Registration** allows new users to sign up with a username, email, and password.
- **Login/Logout** for all users.
- **Admin Dashboard**: If you log in as `admin`, you get a special admin dashboard page with user management capabilities.
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
- [x] Admin User Management Script
- [x] User Deletion from Admin Dashboard
- [x] User Profile Editing and Password Reset
- [x] Profile Deletion with Confirmation
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
- **User Management**: Admin users can delete other users from the admin dashboard.

### Profile Management Features

#### **Password Change**
- **Location**: Profile dropdown → "Change Password" or `/profile/change-password/`
- **Security**: Requires current password verification
- **Validation**: New password must be entered twice for confirmation
- **Requirements**: New password must be different from current password
- **Security Tips**: Includes password strength recommendations

#### **Profile Editing**
- **Location**: Profile dropdown → "Edit Profile" or `/profile/edit/`
- **Fields**: Username and email address
- **Validation**: Ensures uniqueness and prevents conflicts
- **Session Updates**: Automatically updates user session after changes
- **Real-time**: Changes take effect immediately

#### **Profile Deletion**
- **Location**: Profile dropdown → "Delete Profile" or `/profile/delete/`
- **Protection**: Admin users cannot delete themselves
- **Confirmation**: Multiple confirmation dialogs with clear warnings
- **Information**: Shows exactly what data will be deleted
- **Alternatives**: Suggests other options before deletion
- **Cleanup**: Completely removes user and all associated data

### Admin User Setup
The application includes an automated admin user setup script that creates the admin user with default credentials.

### Admin Dashboard Features
- **User Management**: View all users with emails (passwords hidden for security)
- **User Deletion**: Delete regular users (admin users are protected)
- **System Statistics**: Total books, users, read/unread counts
- **Reading Progress**: Visual progress tracking
- **System Health**: Database and application status monitoring

---

## 👨‍💻 Author

**James Scott**  
Student ID: SBA24070  
Email: jamesdeanscott19@gmail.com  
GitHub: [github.com/Jamesscott34](https://github.com/Jamesscott34)

---

## 🧪 Setup Instructions

### Quick Setup (Recommended)
```bash
# 1. Clone the repo
git clone https://github.com/Jamesscott34/DevopsCA.git
cd DevopsCA

# 2. Run the automated setup script
./setup.sh
```

The setup script will:
- Prompt you for a virtual environment name (default: `devops`)
- Create and activate the virtual environment
- Install Django and requirements
- Create Django project and books app (if needed)
- Run database migrations
- Set up admin user automatically
- Start the Django development server

### Manual Setup
```bash
# 1. Clone the repo
git clone https://github.com/Jamesscott34/DevopsCA.git
cd DevopsCA

# 2. Create virtual environment
python3 -m venv devops
source devops/bin/activate

# 3. Install requirements
pip install -r requirements.txt

# 4. Run migrations
python manage.py makemigrations
python manage.py migrate

# 5. Create admin user (IMPORTANT: Run this script!)
python admin_manager.py

# 6. Start the dev server
python manage.py runserver
```

### Admin User Management Script

The `admin_manager.py` script automatically creates and configures the admin user:

```bash
# Run the full setup (creates admin user, verifies, tests authentication)
python admin_manager.py

# Or run specific commands:
python admin_manager.py create    # Create admin user only
python admin_manager.py verify    # Verify admin user exists
python admin_manager.py test      # Test password authentication
python admin_manager.py stats     # Show user statistics
python admin_manager.py reset     # Reset admin password to 'admin'
```

**Default Admin Credentials:**
- Username: `admin`
- Password: `admin`

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
- `/admin-dashboard/delete-user/<id>/` — Delete user (admin only)
- `/profile/edit/` — Edit user profile
- `/profile/change-password/` — Change user password
- `/profile/delete/` — Delete user profile
- `/add/` — Add book manually
- `/open-library/` — Browse Open Library

---

## 🔧 Admin Dashboard Features

The admin dashboard provides:
- System statistics (total books, users, read/unread counts)
- User management (view all users, delete users)
- Quick access to book management functions
- Reading progress tracking
- System health monitoring

---

## 🚨 Important Notes

1. **Always run `python admin_manager.py` after setup** to create the admin user
2. The admin user has special privileges including user deletion
3. Regular users can only manage their own book catalogs
4. The application uses SQLite by default for development

---
