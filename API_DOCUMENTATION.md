# 📚 Book Catalog REST API Documentation

This document provides comprehensive documentation for the Book Catalog REST API, including all endpoints, authentication, and usage examples.

## 🚀 Base URL

```
http://127.0.0.1:8000/api/
```

## 🔐 Authentication

The API uses session-based authentication. Users must first authenticate through the login endpoint to receive a session cookie.

### Authentication Flow

1. **Register** (optional): Create a new user account
2. **Login**: Authenticate and receive session cookie
3. **Use API**: Include session cookie in subsequent requests
4. **Logout**: Clear session when done

## 📋 API Endpoints

### 🔑 Authentication Endpoints

#### Register User
```http
POST /api/auth/register/
```

**Request Body:**
```json
{
    "username": "newuser",
    "email": "user@example.com",
    "password": "securepassword",
    "confirm_password": "securepassword"
}
```

**Response:**
```json
{
    "message": "User registered successfully.",
    "user": {
        "id": 2,
        "username": "newuser",
        "email": "user@example.com",
        "created_at": "2024-01-15T10:30:00Z"
    }
}
```

#### Login
```http
POST /api/auth/login/
```

**Request Body:**
```json
{
    "username": "admin",
    "password": "admin"
}
```

**Response:**
```json
{
    "message": "Login successful.",
    "user": {
        "id": 1,
        "username": "admin",
        "email": "admin@example.com",
        "created_at": "2024-01-01T00:00:00Z"
    },
    "is_admin": true
}
```

#### Logout
```http
POST /api/auth/logout/
```

**Response:**
```json
{
    "message": "Logout successful."
}
```

#### Change Password
```http
POST /api/auth/change_password/
```

**Request Body:**
```json
{
    "current_password": "oldpassword",
    "new_password": "newpassword",
    "confirm_new_password": "newpassword"
}
```

**Response:**
```json
{
    "message": "Password changed successfully."
}
```

### 📚 Book Endpoints

#### Get All Books
```http
GET /api/books/
```

**Query Parameters:**
- `is_read`: Filter by read status (`true`/`false`)
- `search`: Search in title, author, or description
- `page`: Page number for pagination

**Response:**
```json
{
    "count": 10,
    "next": "http://127.0.0.1:8000/api/books/?page=2",
    "previous": null,
    "results": [
        {
            "id": 1,
            "title": "The Great Gatsby",
            "author": "F. Scott Fitzgerald",
            "description": "A story of the Jazz Age...",
            "published_date": "1925-04-10",
            "isbn": "978-0743273565",
            "is_read": false,
            "view_count": 5,
            "added_by": 1,
            "added_by_username": "admin",
            "is_read_display": "Unread",
            "created_at": "2024-01-15T10:30:00Z"
        }
    ]
}
```

#### Get Single Book
```http
GET /api/books/{id}/
```

#### Create Book
```http
POST /api/books/
```

**Request Body:**
```json
{
    "title": "New Book Title",
    "author": "Author Name",
    "description": "Book description",
    "published_date": "2024-01-15",
    "isbn": "978-1234567890",
    "is_read": false
}
```

#### Update Book
```http
PUT /api/books/{id}/
PATCH /api/books/{id}/
```

#### Delete Book
```http
DELETE /api/books/{id}/
```

#### Toggle Read Status
```http
POST /api/books/{id}/toggle_read/
```

#### Get Read Books
```http
GET /api/books/read_books/
```

#### Get Unread Books
```http
GET /api/books/unread_books/
```

#### Get Book Statistics
```http
GET /api/books/statistics/
```

**Response:**
```json
{
    "total_books": 10,
    "read_books": 3,
    "unread_books": 7,
    "read_percentage": 30.0,
    "unread_percentage": 70.0,
    "most_read_books": [...],
    "most_viewed_books": [...]
}
```

### 👥 User Endpoints (Admin Only)

#### Get All Users
```http
GET /api/users/
```

**Note:** Only accessible by admin users.

#### Get Single User
```http
GET /api/users/{id}/
```

#### Create User
```http
POST /api/users/
```

#### Update User
```http
PUT /api/users/{id}/
PATCH /api/users/{id}/
```

#### Delete User
```http
DELETE /api/users/{id}/
```

#### Get User Statistics
```http
GET /api/users/statistics/
```

**Response:**
```json
{
    "total_users": 5,
    "admin_users": 1,
    "regular_users": 4,
    "users": [...]
}
```

### 🔔 Notification Endpoints

#### Get All Notifications
```http
GET /api/notifications/
```

**Note:** Users see only their own notifications. Admins see all notifications.

#### Get Single Notification
```http
GET /api/notifications/{id}/
```

#### Create Notification
```http
POST /api/notifications/
```

**Request Body:**
```json
{
    "title": "New Book Recommendation",
    "message": "Check out this great book!",
    "notification_type": "recommendation",
    "book_recommendation": 1
}
```

#### Update Notification
```http
PUT /api/notifications/{id}/
PATCH /api/notifications/{id}/
```

#### Delete Notification
```http
DELETE /api/notifications/{id}/
```

#### Mark Notification as Read
```http
POST /api/notifications/{id}/mark_read/
```

#### Mark All Notifications as Read
```http
POST /api/notifications/mark_all_read/
```

#### Get Unread Count
```http
GET /api/notifications/unread_count/
```

**Response:**
```json
{
    "unread_count": 3
}
```

### 📊 System Statistics (Admin Only)

#### Get System Statistics
```http
GET /api/statistics/
```

**Response:**
```json
{
    "book_stats": {
        "total_books": 25,
        "read_books": 8,
        "unread_books": 17,
        "read_percentage": 32.0,
        "unread_percentage": 68.0,
        "most_read_books": [...],
        "most_viewed_books": [...]
    },
    "user_stats": {
        "total_users": 5,
        "admin_users": 1,
        "regular_users": 4,
        "users": [...]
    },
    "total_notifications": 15,
    "read_notifications": 12,
    "unread_notifications": 3
}
```

## 🔧 Usage Examples

### JavaScript/Fetch API

#### Login and Get Books
```javascript
// Login
const loginResponse = await fetch('http://127.0.0.1:8000/api/auth/login/', {
    method: 'POST',
    headers: {
        'Content-Type': 'application/json',
    },
    body: JSON.stringify({
        username: 'admin',
        password: 'admin'
    }),
    credentials: 'include' // Important for session cookies
});

const loginData = await loginResponse.json();
console.log('Login successful:', loginData);

// Get books (session cookie will be automatically included)
const booksResponse = await fetch('http://127.0.0.1:8000/api/books/', {
    credentials: 'include'
});

const booksData = await booksResponse.json();
console.log('Books:', booksData);
```

#### Create a New Book
```javascript
const newBook = await fetch('http://127.0.0.1:8000/api/books/', {
    method: 'POST',
    headers: {
        'Content-Type': 'application/json',
    },
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

const bookData = await newBook.json();
console.log('Book created:', bookData);
```

#### Toggle Book Read Status
```javascript
const toggleResponse = await fetch('http://127.0.0.1:8000/api/books/1/toggle_read/', {
    method: 'POST',
    credentials: 'include'
});

const toggleData = await toggleResponse.json();
console.log('Book updated:', toggleData);
```

### Python/Requests

#### Login and Get Books
```python
import requests

# Login
login_data = {
    'username': 'admin',
    'password': 'admin'
}

session = requests.Session()
login_response = session.post('http://127.0.0.1:8000/api/auth/login/', json=login_data)
print('Login response:', login_response.json())

# Get books
books_response = session.get('http://127.0.0.1:8000/api/books/')
books_data = books_response.json()
print('Books:', books_data)
```

#### Create a New Book
```python
new_book_data = {
    'title': '1984',
    'author': 'George Orwell',
    'description': 'A dystopian novel about totalitarianism.',
    'published_date': '1949-06-08',
    'isbn': '978-0451524935',
    'is_read': False
}

book_response = session.post('http://127.0.0.1:8000/api/books/', json=new_book_data)
print('Book created:', book_response.json())
```

## 🛡️ Security Features

### Authentication & Authorization
- **Session-based authentication** for secure user sessions
- **Role-based access control** (admin vs regular users)
- **Password hashing** for secure password storage
- **CSRF protection** for form submissions

### Data Validation
- **Input validation** on all endpoints
- **Password confirmation** for user registration
- **Email uniqueness** validation
- **Book attribution** to prevent unauthorized access

### API Security
- **Rate limiting** (configurable)
- **Request size limits** to prevent abuse
- **JSON parsing** with error handling
- **Secure headers** and CORS configuration

## 📝 Error Handling

### Common Error Responses

#### 400 Bad Request
```json
{
    "error": "Invalid data provided",
    "details": {
        "field_name": ["Error message"]
    }
}
```

#### 401 Unauthorized
```json
{
    "error": "Authentication required"
}
```

#### 403 Forbidden
```json
{
    "error": "Admin access required"
}
```

#### 404 Not Found
```json
{
    "error": "Resource not found"
}
```

#### 500 Internal Server Error
```json
{
    "error": "Internal server error"
}
```

## 🔄 Pagination

All list endpoints support pagination with the following response format:

```json
{
    "count": 100,
    "next": "http://127.0.0.1:8000/api/books/?page=2",
    "previous": null,
    "results": [...]
}
```

**Query Parameters:**
- `page`: Page number (default: 1)
- `page_size`: Items per page (default: 20, max: 100)

## 🔍 Filtering & Searching

### Book Filtering
- `is_read=true/false`: Filter by read status
- `search=keyword`: Search in title, author, or description

### Example
```http
GET /api/books/?is_read=false&search=fantasy
```

## 📊 Response Format

All API responses follow a consistent JSON format:

### Success Response
```json
{
    "data": {...},
    "message": "Operation successful"
}
```

### Error Response
```json
{
    "error": "Error message",
    "details": {...}
}
```

## 🚀 Getting Started

1. **Start the Django server:**
   ```bash
   python manage.py runserver
   ```

2. **Access the API root:**
   ```
   http://127.0.0.1:8000/api/
   ```

3. **Use the browsable API:**
   - Visit any endpoint in your browser
   - Interactive documentation and testing interface
   - Form-based data entry for testing

4. **Test with curl:**
   ```bash
   # Login
   curl -X POST http://127.0.0.1:8000/api/auth/login/ \
        -H "Content-Type: application/json" \
        -d '{"username":"admin","password":"admin"}' \
        -c cookies.txt

   # Get books
   curl http://127.0.0.1:8000/api/books/ -b cookies.txt
   ```

## 📚 Additional Resources

- **Django REST Framework Documentation**: https://www.django-rest-framework.org/
- **API Testing Tools**: Postman, Insomnia, or curl
- **JavaScript Fetch API**: https://developer.mozilla.org/en-US/docs/Web/API/Fetch_API
- **Python Requests Library**: https://requests.readthedocs.io/

---

This API provides a complete REST interface for the Book Catalog application, enabling integration with any frontend framework or mobile application. 