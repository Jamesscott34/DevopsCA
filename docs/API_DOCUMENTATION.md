# 📚 Book Catalog REST API Documentation

This document provides comprehensive documentation for the Book Catalog REST API, including all endpoints, authentication, and usage examples.

---

## 📖 Overview & Quickstart
- **Base URL:**
  ```
  http://127.0.0.1:8000/api/
  ```
- **Authentication:** Session-based (login to get a session cookie)
- **Admin endpoints:** Only accessible by admin users
- **See also:**
  - [README.md](README.md) (setup, environment, admin management)
  - [docs/QUICKSTART.md](docs/QUICKSTART.md) (onboarding)
  - [KUBERNETES.md](KUBERNETES.md) (Kubernetes deployment)
  - [HELM_DEPLOYMENT.md](HELM_DEPLOYMENT.md) (Helm deployment)

---

## 🚦 API Quickstart
1. Register or login via `/api/auth/register/` or `/api/auth/login/`
2. Use the session cookie for all further requests
3. Access book/user endpoints as needed
4. For admin actions, login as `admin` (see setup scripts)

---

## 🔐 Authentication

The API uses session-based authentication. Users must first authenticate through the login endpoint to receive a session cookie.

### Authentication Flow
1. **Register** (optional): Create a new user account
2. **Login**: Authenticate and receive session cookie
3. **Use API**: Include session cookie in subsequent requests
4. **Logout**: Clear session when done

---

## 📋 API Endpoints

### 🔑 Authentication Endpoints

#### Register User
```http
POST /api/auth/register/
```

**cURL Example:**
```sh
curl -X POST http://127.0.0.1:8000/api/auth/register/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "newuser",
    "email": "user@example.com",
    "password": "securepassword",
    "confirm_password": "securepassword"
  }'
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

**cURL Example:**
```sh
curl -X POST http://127.0.0.1:8000/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "admin",
    "password": "admin"
  }'
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

**cURL Example:**
```sh
curl -X POST http://127.0.0.1:8000/api/auth/logout/ \
  -b cookies.txt
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

**cURL Example:**
```sh
curl -X POST http://127.0.0.1:8000/api/auth/change_password/ \
  -H "Content-Type: application/json" \
  -b cookies.txt \
  -d '{
    "current_password": "oldpassword",
    "new_password": "newpassword",
    "confirm_new_password": "newpassword"
  }'
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

**cURL Example:**
```sh
curl http://127.0.0.1:8000/api/books/ -b cookies.txt
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

**cURL Example:**
```sh
curl http://127.0.0.1:8000/api/books/1/ -b cookies.txt
```

#### Create Book
```http
POST /api/books/
```

**cURL Example:**
```sh
curl -X POST http://127.0.0.1:8000/api/books/ \
  -H "Content-Type: application/json" \
  -b cookies.txt \
  -d '{
    "title": "New Book Title",
    "author": "Author Name",
    "description": "Book description",
    "published_date": "2024-01-15",
    "isbn": "978-1234567890",
    "is_read": false
  }'
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

**cURL Example (PUT):**
```sh
curl -X PUT http://127.0.0.1:8000/api/books/1/ \
  -H "Content-Type: application/json" \
  -b cookies.txt \
  -d '{
    "title": "Updated Title",
    "author": "Updated Author",
    "description": "Updated description",
    "published_date": "2024-01-15",
    "isbn": "978-1234567890",
    "is_read": true
  }'
```

**cURL Example (PATCH):**
```sh
curl -X PATCH http://127.0.0.1:8000/api/books/1/ \
  -H "Content-Type: application/json" \
  -b cookies.txt \
  -d '{
    "is_read": true
  }'
```

#### Delete Book
```http
DELETE /api/books/{id}/
```

**cURL Example:**
```sh
curl -X DELETE http://127.0.0.1:8000/api/books/1/ -b cookies.txt
```

#### Toggle Read Status
```http
POST /api/books/{id}/toggle_read/
```

**cURL Example:**
```sh
curl -X POST http://127.0.0.1:8000/api/books/1/toggle_read/ -b cookies.txt
```

#### Get Read Books
```http
GET /api/books/read_books/
```

**cURL Example:**
```sh
curl http://127.0.0.1:8000/api/books/read_books/ -b cookies.txt
```

#### Get Unread Books
```http
GET /api/books/unread_books/
```

**cURL Example:**
```sh
curl http://127.0.0.1:8000/api/books/unread_books/ -b cookies.txt
```

#### Get Book Statistics
```http
GET /api/books/statistics/
```

**cURL Example:**
```sh
curl http://127.0.0.1:8000/api/books/statistics/ -b cookies.txt
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

#### Get All Books (All Users)
```http
GET /api/books/all/
```
**Description:** Returns all books in the database, regardless of user. Any authenticated user can access this endpoint.

**cURL Example:**
```sh
curl http://127.0.0.1:8000/api/books/all/ -b cookies.txt
```

**Response:**
```json
[
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

#### Get/Update Own Profile (Authenticated User)
```http
GET /api/users/me/
PUT /api/users/me/
PATCH /api/users/me/
```
**Description:** Retrieve or update your own user profile. Any authenticated user can access this endpoint to view or update their own information.

**cURL Example (GET):**
```sh
curl http://127.0.0.1:8000/api/users/me/ -b cookies.txt
```

**GET Response:**
```json
{
  "id": 2,
  "username": "regularuser",
  "email": "user@example.com",
  "created_at": "2024-01-15T10:30:00Z"
}
```

**cURL Example (PATCH):**
```sh
curl -X PATCH http://127.0.0.1:8000/api/users/me/ \
  -H "Content-Type: application/json" \
  -b cookies.txt \
  -d '{
    "email": "newemail@example.com"
  }'
```

**PATCH Response:**
```json
{
  "id": 2,
  "username": "regularuser",
  "email": "newemail@example.com",
  "created_at": "2024-01-15T10:30:00Z"
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

---

## 🐞 Troubleshooting & FAQ
- **401 Unauthorized:**
  - Make sure you are logged in and sending the session cookie with requests
- **403 Forbidden:**
  - You are trying to access an admin-only endpoint as a regular user
- **500 Server Error:**
  - Check your environment variables and database connection
- **How do I get an admin user?**
  - Use the setup scripts (`run_django.sh`, `run_docker.sh`, `setup.sh`) or `admin_manager.py` to create/reset the admin user
- **How do I test the API?**
  - Use `curl`, Postman, or the provided JavaScript example ([static/js/api-example.js](static/js/api-example.js))
- **Where do I find my API base URL?**
  - Local: `http://127.0.0.1:8000/api/`
  - Docker: `http://localhost:8000/api/`
  - Kubernetes: Use the NodePort or Ingress URL

---

## 🔗 More Documentation
- [README.md](README.md)
- [docs/QUICKSTART.md](docs/QUICKSTART.md)
- [KUBERNETES.md](KUBERNETES.md)
- [HELM_DEPLOYMENT.md](HELM_DEPLOYMENT.md)

---

This API provides a complete REST interface for the Book Catalog application, enabling integration with any frontend framework or mobile application. 