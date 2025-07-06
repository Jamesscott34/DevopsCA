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
=======
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
