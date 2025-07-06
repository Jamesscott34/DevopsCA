'''
README for SBA24070 Book Catalogue App

IMPORTANT DATABASE HOST NOTE:
- If running locally (not in Docker), set DATABASES['default']['HOST'] = 'localhost' in sba24070_book_catalogue/settings.py
- If running with Docker, set DATABASES['default']['HOST'] = 'db' in sba24070_book_catalogue/settings.py

**Database Flexibility Note:**
- You do **not** have to use the database provided by default.
- By default, the app uses SQLite, which requires no setup—just clone and run.
- You can switch to PostgreSQL (or another supported DB) by updating `settings.py` (or your `.env` for Docker) and running migrations.
- See below for setup instructions for both local and Docker environments.

You can use the provided scripts for setup:
- ./run_django.sh: Sets HOST to 'localhost', installs requirements, runs migrations, and starts the Django server.
- ./run_docker.sh: Sets HOST to 'db', builds and starts Docker containers, runs migrations, and starts the app.
- ./setup.sh: Interactive setup for both modes, ensures correct HOST is set and all requirements are met.

See below for detailed instructions.
'''

# 📚 SBA24070 Book Catalogue App

This is a Django-based book catalogue system developed as part of a DevOps assignment. It allows users to manage personal book collections with the ability to:

- Add/edit/delete books manually
- Browse and import books from the Open Library API
- Toggle read/unread status
- Store descriptions and auto-generate ISBNs
- **Register, log in, and log out as a user**
- **Admin user with special dashboard and user management**
- **Beautiful, modern color theme and UI**
- **Comprehensive notification system**
- **User profile management and password reset**
- **Book statistics and reading progress tracking**

---

## 🚀 How It Works

- **Login Page** is the default landing page when you visit the application.
- **User Registration** allows new users to sign up with a username, email, and password.
- **Home Page** (after login) shows all saved books in a table with reading progress.
- **Manual Add** lets you enter title, author, published date, description, and an auto-generated ISBN (starting with `JS`).
- **Open Library Search** lets you search external books, view results, and import selected ones into your library with auto-generated ISBNs.
- **Admin Dashboard**: If you log in as `admin`, you get a special admin dashboard page with comprehensive user management capabilities.
- **Books are saved in SQLite DB** using Django's ORM.
- **Books can be edited, deleted, and marked read/unread**.
- **Modern, colorful UI** with custom CSS and Bootstrap.
- **Notification System** allows admins to send personalized messages and book recommendations to users.

---

## ️ What To Do Next

- [ ] Implement email notification functionality

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

---

## �� REST API

The Book Catalog application now includes a complete REST API that allows integration with JavaScript frontends, mobile applications, and other services.

### 🔗 API Base URL
```
http://127.0.0.1:8000/api/
```

### 📋 Available Endpoints

#### 🔑 Authentication Endpoints
- `POST /api/auth/register/` - Register new user
- `POST /api/auth/login/` - User login
- `POST /api/auth/logout/` - User logout
- `POST /api/auth/change_password/` - Change password

#### 📚 Book Endpoints
- `GET /api/books/` - Get all books (with filtering and search)
- `GET /api/books/{id}/` - Get single book
- `POST /api/books/` - Create new book
- `PUT /api/books/{id}/` - Update book
- `DELETE /api/books/{id}/` - Delete book
- `POST /api/books/{id}/toggle_read/` - Toggle read status
- `GET /api/books/read_books/` - Get read books only
- `GET /api/books/unread_books/` - Get unread books only
- `GET /api/books/statistics/` - Get book statistics

#### 👥 User Endpoints (Admin Only)
- `GET /api/users/` - Get all users
- `GET /api/users/{id}/` - Get single user
- `POST /api/users/` - Create new user
- `PUT /api/users/{id}/` - Update user
- `DELETE /api/users/{id}/` - Delete user
- `GET /api/users/statistics/` - Get user statistics

#### 🔔 Notification Endpoints
- `GET /api/notifications/` - Get all notifications
- `GET /api/notifications/{id}/` - Get single notification
- `POST /api/notifications/` - Create notification
- `PUT /api/notifications/{id}/` - Update notification
- `DELETE /api/notifications/{id}/` - Delete notification
- `POST /api/notifications/{id}/mark_read/` - Mark as read
- `POST /api/notifications/mark_all_read/` - Mark all as read
- `GET /api/notifications/unread_count/` - Get unread count

#### 📊 System Statistics (Admin Only)
- `GET /api/statistics/` - Get comprehensive system statistics

### 🔧 API Features

#### Authentication & Security
- **Session-based authentication** for secure user sessions
- **Role-based access control** (admin vs regular users)
- **Password hashing** and validation
- **CSRF protection** and secure headers

#### Data Operations
- **Full CRUD operations** for all models
- **Filtering and searching** capabilities
- **Pagination** for large datasets
- **Data validation** and error handling

#### Advanced Features
- **Book statistics** and reading progress tracking
- **User management** for admin users
- **Notification system** with read/unread tracking
- **System-wide statistics** for monitoring

### 📖 Usage Examples

#### JavaScript/Fetch API
```javascript
// Login
const loginResponse = await fetch('http://127.0.0.1:8000/api/auth/login/', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ username: 'admin', password: 'admin' }),
    credentials: 'include'
});

// Get books
const booksResponse = await fetch('http://127.0.0.1:8000/api/books/', {
    credentials: 'include'
});

// Create book
const newBook = await fetch('http://127.0.0.1:8000/api/books/', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
        title: 'The Hobbit',
        author: 'J.R.R. Tolkien',
        description: 'A fantasy novel about a hobbit\'s journey.',
        published_date: '1937-09-21',
        isbn: '978-0547928241',
        is_read: false
    }),
    credentials: 'include'
});
```

#### Python/Requests
```python
import requests

session = requests.Session()

# Login
login_data = {'username': 'admin', 'password': 'admin'}
login_response = session.post('http://127.0.0.1:8000/api/auth/login/', json=login_data)

# Get books
books_response = session.get('http://127.0.0.1:8000/api/books/')
books_data = books_response.json()
```

### 🛠️ API Testing

#### Browsable API Interface
Visit any API endpoint in your browser to access the interactive Django REST Framework interface:
- `http://127.0.0.1:8000/api/` - API root
- `http://127.0.0.1:8000/api/books/` - Books endpoint
- `http://127.0.0.1:8000/api/auth/login/` - Login endpoint

#### JavaScript Example File
A complete JavaScript example is available at `static/js/api-example.js` that demonstrates all API operations.

#### API Documentation
Comprehensive API documentation is available in `API_DOCUMENTATION.md` with detailed examples and usage instructions.

### 🔍 Filtering & Searching

#### Book Filtering
- `GET /api/books/?is_read=true` - Get only read books
- `GET /api/books/?is_read=false` - Get only unread books
- `GET /api/books/?search=fantasy` - Search in title, author, or description

#### Pagination
- `GET /api/books/?page=2` - Get second page
- `GET /api/books/?page_size=10` - 10 items per page

### 📊 Response Format

All API responses follow a consistent JSON format with proper HTTP status codes and error handling.

### 🚀 Getting Started with API

1. **Start the server:**
   ```bash
   python manage.py runserver
   ```

2. **Access the API:**
   ```
   http://127.0.0.1:8000/api/
   ```

3. **Test authentication:**
   ```bash
   curl -X POST http://127.0.0.1:8000/api/auth/login/ \
        -H "Content-Type: application/json" \
        -d '{"username":"admin","password":"admin"}' \
        -c cookies.txt
   ```

4. **Get books:**
   ```bash
   curl http://127.0.0.1:8000/api/books/ -b cookies.txt
   ```

---

## 📦 Tech Stack

- **Backend**: Django (Python 3.8+)  
- **Database**: SQLite (default), PostgreSQL ready  
- **Frontend**: HTML + Bootstrap + Custom CSS  
- **External API**: [Open Library](https://openlibrary.org/developers/api)  
- **Version Control**: Git + GitHub  
- **Authentication**: Custom user model with password hashing

---

## 🎯 Default Landing Page

**Login Page is the Default**: When you start the server and visit `http://127.0.0.1:8000/`, the login page appears automatically. This ensures users must authenticate before accessing the book catalog.

---

## 👤 User Management

- **Default Landing**: Visit `http://127.0.0.1:8000/` to see the login page
- **Register**: Go to `/register/` to create a new user account
- **Login**: Go to `/login/` to log in with your username and password
- **Logout**: Click the logout button in the navigation or go to `/logout/`
- **Admin User**: If you log in as `admin`, you will be redirected to a special admin dashboard at `/admin-dashboard/`
- **Personalized Welcome**: After login, the homepage will greet you by your username
- **User Management**: Admin users can manage other users from the admin dashboard

### Profile Management Features

#### **Password Change**
- **Location**: Profile dropdown → "Change Password" or `/profile/change-password/`
- **Security**: Requires current password verification
- **Validation**: New password must be entered twice for confirmation
- **Requirements**: New password must be different from current password

#### **Profile Editing**
- **Location**: Profile dropdown → "Edit Profile" or `/profile/edit/`
- **Fields**: Username and email address
- **Validation**: Ensures uniqueness and prevents conflicts
- **Session Updates**: Automatically updates user session after changes

#### **Profile Deletion**
- **Location**: Profile dropdown → "Delete Profile" or `/profile/delete/`
- **Protection**: Admin users cannot delete themselves
- **Confirmation**: Multiple confirmation dialogs with clear warnings
- **Cleanup**: Completely removes user and all associated data

### Admin User Setup
The application includes an automated admin user setup script that creates the admin user with default credentials.

### Admin Dashboard Features
- **User Management**: View all users with emails (passwords hidden for security)
- **User Deletion**: Delete regular users (admin users are protected)
- **System Statistics**: Total books, users, read/unread counts
- **Reading Progress**: Visual progress tracking
- **System Health**: Database and application status monitoring
- **Book Statistics**: Most read and most viewed books
- **Notification Management**: Send individual or bulk notifications
- **Email Management**: Change user email addresses (admin can only change their own)

### Admin Features
- **User Management**: View all users, delete users, and manage permissions
- **Book Statistics**: View most read and most viewed books with view counts
- **Notification System**: Send individual or bulk notifications to users
- **Book Recommendations**: Recommend books to users with automatic saving to reading lists
- **Email Management**: Change user email addresses with validation
- **System Statistics**: Monitor user activity and book engagement
- **Admin Restrictions**: Admin can only change their own email and cannot send notifications to themselves

---

## 👨‍💻 Author

**James Scott**  
Student ID: SBA24070  
Email: jamesdeanscott19@gmail.com  
GitHub: [github.com/Jamesscott34](https://github.com/Jamesscott34)

---

## 🚀 Quickstart

See [docs/QUICKSTART.md](docs/QUICKSTART.md) for a step-by-step guide.

## 🛠️ Setup Instructions

### Using setup.sh (Recommended)

```sh
./setup.sh
```
- This will install dependencies, run migrations, collect static files, create the admin user, and start the server.
- Visit: [http://127.0.0.1:8000](http://127.0.0.1:8000)
- Log in as admin: Username: `admin`, Password: `admin`

### Manual Setup

1. Install dependencies:
   ```sh
   pip install -r requirements.txt
   ```
2. Run migrations:
   ```sh
   python manage.py makemigrations
   python manage.py migrate
   ```
3. Collect static files:
   ```sh
   python manage.py collectstatic --noinput
   ```
4. Create the admin user:
   ```sh
   python manage.py create_admin
   ```
5. Start the server:
   ```sh
   python manage.py runserver
   ```
6. Visit: [http://127.0.0.1:8000](http://127.0.0.1:8000)

### Docker

1. **Add your database credentials to a `.env` file** in your project root (see Docker Compose for required variables).
2. **Build and start the containers:**
   ```sh
   docker compose up --build
   ```
3. **Run migrations and collect static files:**
   ```sh
   docker compose exec web python manage.py migrate
   docker compose exec web python manage.py collectstatic --noinput
   docker compose exec web python manage.py create_admin
   ```
4. **Visit the app:**
   - [http://localhost:8000](http://localhost:8000)
   - Log in as admin: `admin` / `admin`