'''
README for SBA24070 Book Catalogue App

IMPORTANT DATABASE HOST NOTE:
- If running locally (not in Docker), set DATABASES['default']['HOST'] = 'localhost' in sba24070_book_catalogue/settings.py
- If running with Docker, set DATABASES['default']['HOST'] = 'db' in sba24070_book_catalogue/settings.py

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
- [ ] Add book categories and tags

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

---

## 🚀 REST API

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

**Note:**
- The `web` service runs Django with Gunicorn for production-like serving.
- The `db` service uses PostgreSQL and persists data in a Docker volume.
- The `.env` file is required for environment variables and should not be committed to version control.

## 🔑 Admin Login

- The admin user (`admin`/`admin`) can log in via the main login page at `/login/`.
- The admin dashboard is accessible after login.

---

## 🌈 UI & Styling
- The app uses a beautiful, modern color theme with gradients, custom buttons, and responsive design.
- All pages are styled with Bootstrap and custom CSS for a professional look.
- Admin dashboard features comprehensive statistics and management tools.

---

## 🗝️ Default URLs
- `/` — Login page (default landing page)
- `/register/` — Register new user
- `/login/` — User login
- `/logout/` — User logout
- `/home/` — Home page with book catalog (requires login)
- `/admin-dashboard/` — Admin dashboard (for admin user)
- `/admin-dashboard/delete-user/<id>/` — Delete user (admin only)
- `/profile/edit/` — Edit user profile
- `/profile/change-password/` — Change user password
- `/profile/delete/` — Delete user profile
- `/add/` — Add book manually
- `/open-library/` — Browse Open Library
- `/notifications/` — View user notifications
- `/send-notification/` — Send individual notification (admin)
- `/send-bulk-notification/` — Send bulk notification (admin)

---

## 🔧 Admin Dashboard Features

The admin dashboard provides:
- System statistics (total books, users, read/unread counts)
- User management (view all users, delete users, change emails)
- Quick access to book management functions
- Reading progress tracking
- System health monitoring
- Book statistics (most read and most viewed)
- Notification management system
- Email management tools

---

## 🚨 Important Notes

1. **Always run `python admin_manager.py` after setup** to create the admin user
2. **Login page is the default landing page** - users must authenticate first
3. The admin user has special privileges including user deletion and notification management
4. Regular users can only manage their own book catalogs
5. The application uses SQLite by default for development
6. Admin cannot send notifications to themselves or change other users' emails

---

## 📋 Notification System

The application includes a comprehensive notification system that allows admins to communicate with users:

#### Individual Notifications
- Send personalized notifications to specific users
- Include book recommendations with automatic saving to user reading lists
- Add custom email content for enhanced communication
- Track notification read status

#### Bulk Notifications
- Send the same notification to multiple users simultaneously
- Target all users, regular users only, or specific user groups
- Include book recommendations that are automatically saved to all targeted users' reading lists
- Add custom email content for bulk communications

#### Notification Features
- **Book Integration**: Books sent in notifications are automatically saved to user reading lists
- **Email Enhancement**: Include book details and additional content in email notifications
- **Read Tracking**: Monitor which notifications have been read by users
- **Type Classification**: Categorize notifications as recommendations, general messages, or system updates
- **User Targeting**: Send to specific users or user groups based on criteria

#### Email Notifications
- Include book details (title, author, description) in email headers
- Add custom content to email body for personalized messages
- Automatic book saving to user reading lists when enabled
- Professional email formatting with book information

---

## 📋 Notification System Features

### Core Functionality
- **User Registration & Authentication**: Secure user accounts with password hashing
- **Book Catalog Management**: Add, edit, delete, and track reading progress
- **Admin Dashboard**: Comprehensive admin interface with system statistics
- **Open Library Integration**: Search and import books from Open Library API
- **Profile Management**: Edit profiles, change passwords, and account deletion
- **Notification System**: Admin-to-user communication with book recommendations

### User Features
- **Personal Book Catalog**: Each user has their own book collection
- **Reading Progress Tracking**: Mark books as read/unread with progress indicators
- **Book Filtering**: View read, unread, or all books separately
- **Profile Management**: Edit personal information and change passwords
- **Notification Center**: View and manage notifications from admins
- **Book Recommendations**: Receive personalized book suggestions

### Admin Features
- **System Dashboard**: Overview of users, books, and system health
- **User Management**: View all users, delete accounts, and manage permissions
- **Notification System**: Send individual or bulk notifications to users
- **Book Recommendations**: Recommend specific books to users
- **Email Notifications**: Send notifications via email (framework ready)
- **Statistics & Analytics**: Monitor user activity and reading patterns

### Advanced Features
- **Book View Tracking**: Automatically track how many times books are viewed
- **Book Attribution**: Track which user added each book to the catalog
- **Enhanced Notifications**: Include book details and additional content in email notifications
- **Automatic Book Saving**: Books sent in notifications can be automatically saved to user reading lists
- **Email Content Enhancement**: Admins can add custom content to email notifications
- **Reading List Integration**: Seamless integration between notifications and user reading lists

### Security Features
- **Password Hashing**: All passwords are securely hashed using Django's built-in algorithms
- **Session Management**: Secure session handling for user authentication
- **Admin Protection**: Admin users cannot be deleted and have special privileges
- **Email Validation**: Comprehensive email validation and uniqueness checking

---

## 📋 Notification System Installation & Setup

### Prerequisites
- Python 3.8 or higher
- SQLite database (default) or PostgreSQL
- Virtual environment (recommended)

### Quick Setup
1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd Devops
   ```

2. **Run the setup script** (recommended):
   ```bash
   chmod +x setup.sh
   ./setup.sh
   ```
   The setup script will:
   - Create a virtual environment
   - Install dependencies
   - Set up the Django project
   - Run database migrations
   - Create the admin user
   - Start the development server

### Manual Setup
1. **Create virtual environment**:
   ```bash
   python3 -m venv devops
   source devops/bin/activate  # On Windows: devops\Scripts\activate
   ```

2. **Install dependencies**:
   ```bash
   pip install django
   # or if requirements.txt exists:
   pip install -r requirements.txt
   ```

3. **Set up the database**:
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

4. **Create admin user**:
   ```bash
   python admin_manager.py
   ```

5. **Start the server**:
   ```bash
   python manage.py runserver
   ```

## 📋 Notification System Usage

### Admin Access
- **URL**: http://127.0.0.1:8000/login/
- **Username**: admin
- **Password**: admin

### Admin Dashboard Features
- **System Statistics**: View user counts, book statistics, and system health
- **User Management**: Manage user accounts and permissions
- **Notification Management**: Send notifications and book recommendations
- **Book Management**: Add, edit, and manage the book catalog

### Sending Notifications
1. **Individual Notifications**:
   - Go to Admin Dashboard → Notification Management
   - Click "Send Individual" or use "Notify" button on user list
   - Fill in title, message, and optional book recommendation
   - Choose to send email notification

2. **Bulk Notifications**:
   - Go to Admin Dashboard → Notification Management
   - Click "Send Bulk"
   - Select target users (all, regular, or specific)
   - Fill in notification details
   - Send to multiple users at once

### User Features
- **Registration**: Create new account at /register/
- **Book Management**: Add, edit, and track reading progress
- **Notifications**: View notifications at /notifications/
- **Profile Management**: Edit profile and change password

## 📋 Notification System URL Structure

### Authentication & User Management
- `/` - Login page (default landing)
- `/register/` - User registration
- `/login/` - User login
- `/logout/` - User logout
- `/profile/edit/` - Edit user profile
- `/profile/change-password/` - Change password
- `/profile/delete/` - Delete user profile

### Admin Functions
- `/admin-dashboard/` - Admin dashboard
- `/admin-dashboard/delete-user/<id>/` - Delete user (admin only)
- `/send-notification/` - Send individual notification
- `/send-notification/<user_id>/` - Send notification to specific user
- `/send-bulk-notification/` - Send bulk notification

### Book Management
- `/home/` - Home page with book catalog (requires login)
- `/add/` - Add new book
- `/edit/<id>/` - Edit book
- `/delete/<isbn>/` - Delete book
- `/toggle/<id>/` - Toggle read status
- `/read/` - View read books
- `/unread/` - View unread books
- `/open-library/` - Search Open Library
- `/open-library/save/` - Save book from Open Library

### Notification System
- `/notifications/` - View user notifications
- `/notifications/mark-read/<id>/` - Mark notification as read
- `/notifications/mark-all-read/` - Mark all notifications as read

## 📋 Notification System Database Models

### User Model
- `username`: Unique username for login
- `email`: Unique email address
- `password`: Hashed password
- `created_at`: Account creation timestamp

### Book Model
- `title`: Book title
- `author`: Book author
- `description`: Optional book description
- `published_date`: Publication date
- `isbn`: International Standard Book Number (unique, optional)
- `is_read`: Reading status boolean
- `view_count`: Number of times book has been viewed
- `added_by`: User who added the book

### Notification Model
- `user`: Foreign key to User (recipient)
- `title`: Notification title/headline
- `message`: Detailed notification message
- `book_recommendation`: Optional book recommendation
- `is_read`: Read status boolean
- `created_at`: Creation timestamp
- `notification_type`: Type (recommendation, general, system)

## 📋 Notification System Admin Management Script

The `admin_manager.py` script provides comprehensive admin user management:

```bash
python admin_manager.py
```

**Features**:
- Create admin user with secure password
- Verify admin user authentication
- Test password hashing and verification
- Display user statistics
- Reset admin password
- Comprehensive error handling

## 📋 Notification System Configuration

### Database Settings
The application is configured for SQLite by default. Update `settings.py` for PostgreSQL:

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'your_database_name',
        'USER': 'your_username',
        'PASSWORD': 'your_password',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

### Email Configuration (Future Enhancement)
Email notifications are framework-ready. Add email settings to `settings.py`:

```python
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'your_smtp_server'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'your_email@example.com'
EMAIL_HOST_PASSWORD = 'your_email_password'
```

## 📋 Notification System Security Features

- **Password Hashing**: All passwords are securely hashed using Django's built-in hashing
- **CSRF Protection**: All forms include CSRF protection
- **Session Management**: Secure session handling for user authentication
- **Admin Access Control**: Admin functions restricted to admin users only
- **Input Validation**: Comprehensive form validation and sanitization

## 📋 Notification System Development

### Project Structure
```
Devops/
├── books/                    # Main Django app
│   ├── models.py            # Database models
│   ├── views.py             # View functions
│   ├── forms.py             # Django forms
│   ├── urls.py              # URL routing
│   
│   └── templates/books/     # HTML templates
├── sba24070_book_catalogue/ # Django project settings
├── static/                  # Static files (CSS, JS)
├── admin_manager.py     # Admin management script
├── setup.sh                 # Setup script
└── manage.py               # Django management script
```

### Adding New Features
1. **Models**: Add to `books/models.py`
2. **Views**: Add to `books/views.py`
3. **URLs**: Add to `books/urls.py`
4. **Templates**: Add to `books/templates/books/`
5. **Forms**: Add to `books/forms.py`

## 📋 Notification System Troubleshooting

### Common Issues
1. **Database Connection**: Ensure SQLite file exists and is writable
2. **Migration Errors**: Run `python manage.py makemigrations` and `python manage.py migrate`
3. **Admin Access**: Use `python admin_manager.py` to create/reset admin user
4. **Static Files**: Ensure `STATICFILES_DIRS` is configured in settings

### Debug Mode
For development, ensure `DEBUG = True` in `settings.py` for detailed error messages.

## 📋 Notification System Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📋 Notification System License

This project is part of the SBA24070 coursework and is for educational purposes.

## 📋 Notification System Support

For issues and questions:
1. Check the troubleshooting section
2. Review the admin management script documentation
3. Check Django documentation for framework-specific issues

---

## 🏁 Quick Start Options

'''
- For local Django: use ./run_django.sh (HOST will be set to 'localhost')
- For Docker: use ./run_docker.sh (HOST will be set to 'db')
- You can also use ./setup.sh for a guided setup.
'''
