# 📚 SBA24070 Book Catalogue App

[![CI/CD Pipeline](https://github.com/Jamesscott34/DevopsCA/actions/workflows/ci-cd.yml/badge.svg)](https://github.com/Jamesscott34/DevopsCA/actions/workflows/ci-cd.yml)
[![Docker Pulls](https://img.shields.io/docker/pulls/jamesdeanscott/devops-book-app.svg)](https://hub.docker.com/r/jamesdeanscott/devops-book-app)
[![Kubernetes](https://img.shields.io/badge/kubernetes-ready-blue?logo=kubernetes)](https://kubernetes.io/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

**Welcome!** This is a full-featured Django book catalogue with flexible deployment options: **Local Development**, **Docker Compose**, **Kubernetes (Minikube)**, and **Helm**. Choose your preferred environment and get started in minutes!

## 🚀 Quick Start

| Environment      | Command(s)                                 | Access URL                | Database | Setup Time |
|------------------|--------------------------------------------|---------------------------|----------|------------|
| **Local Dev**    | `./custom_scripts/run_django.sh`           | http://127.0.0.1:8000    | SQLite   | 2 min      |
| **Docker**       | `./custom_scripts/run_docker.sh`           | http://localhost:8000     | Postgres | 3 min      |
| **Kubernetes**   | `./custom_scripts/setup.sh`                | minikube IP + NodePort   | Postgres | 5 min      |
| **Helm**         | See [Helm Guide](docs/HELM_DEPLOYMENT.md) | minikube/cloud IP        | Postgres | 5 min      |

**Default Admin:** `admin` / `admin` (created automatically)

---

## ✨ Features

### 📚 Book Management
- **Complete CRUD Operations**: Create, read, update, and delete books with full validation
- **ISBN Auto-Population**: Automatically generates ISBNs if left blank during book creation
- **Smart Deletion**: Supports deletion by title and author when ISBN is missing or invalid
- **Cover Image Support**: Upload and display book cover images
- **Tag System**: Organize books with custom tags for better categorization
- **Reading Progress Tracking**: Track your reading progress for each book
- **View Count Analytics**: Monitor which books are most popular

### 🔍 Open Library Integration
- **Live Search**: Real-time search through Open Library's vast database
- **One-Click Import**: Import book details directly from Open Library API
- **Automatic Data Population**: Fills in title, author, description, and cover image
- **ISBN Validation**: Validates ISBNs against Open Library database
- **Book Recommendations**: Get personalized book recommendations based on your library

### 👥 User Management
- **Custom User Model**: Extended user model with additional fields
- **User Registration & Authentication**: Secure login/logout system
- **Profile Management**: Users can update their profiles and preferences
- **User Notes**: Personal notes system for each user
- **Admin Referral System**: Admins can assign referral books to users

### 🔔 Notification System
- **Real-time Notifications**: Instant notifications for book assignments
- **Read/Unread Status**: Track notification read status
- **Book Recommendations**: Receive notifications for new book suggestions
- **Admin Notifications**: Admins get notified of user activities

### 🛠️ Admin Dashboard
- **Comprehensive Analytics**: User statistics and book analytics
- **User Management**: View, edit, and delete user accounts
- **Book Management**: Manage all books across all users
- **Referral Assignment**: Assign books to users through admin interface
- **Notification Management**: Send and manage system notifications
- **User Notes Management**: View and manage user notes

### 🔌 REST API
- **Full CRUD Endpoints**: Complete API for all book operations
- **Session Authentication**: Secure API access with session-based auth
- **JSON Response Format**: Clean, consistent API responses
- **Error Handling**: Comprehensive error responses and validation
- **API Documentation**: Complete API reference and examples

### 🐳 Multi-Environment Deployment
- **Local Development**: SQLite database for quick development
- **Docker Compose**: Containerized deployment with PostgreSQL
- **Kubernetes**: Production-ready deployment with Minikube
- **Helm Charts**: Advanced Kubernetes deployment with Helm
- **Environment Configuration**: Automatic environment detection and setup

### 🔧 Developer Tools
- **Custom Scripts**: Automated setup and management scripts
- **Admin Management**: Automated admin user creation and management
- **Database Host Helper**: Automatic database host configuration
- **Test Suite**: Comprehensive test coverage for all features
- **Build Status Monitoring**: Real-time build status tracking

---

## 🚧 Upcoming Features

### 📱 Enhanced User Experience
- **Mobile-Responsive Design**: Improved mobile interface and PWA support
- **Dark/Light Theme**: User-selectable theme preferences
- **Advanced Search**: Full-text search with filters and sorting
- **Reading Lists**: Create and share custom reading lists
- **Book Reviews & Ratings**: User review and rating system

### 🔗 Social Features
- **User Profiles**: Public user profiles with reading history
- **Book Clubs**: Create and join book clubs
- **Social Sharing**: Share books and reading progress on social media
- **Friend System**: Add friends and see their reading activity
- **Book Recommendations**: AI-powered personalized recommendations

### 📊 Advanced Analytics
- **Reading Statistics**: Detailed reading progress and time tracking
- **Genre Analytics**: Analyze reading preferences by genre
- **Reading Goals**: Set and track reading goals
- **Export Features**: Export reading lists and statistics
- **Dashboard Widgets**: Customizable admin dashboard widgets

### 🔐 Enhanced Security
- **OAuth Integration**: Google, Facebook, and GitHub login
- **Two-Factor Authentication**: Enhanced account security
- **API Rate Limiting**: Protect API endpoints from abuse
- **Audit Logging**: Track all user actions for security
- **Data Encryption**: Encrypt sensitive user data
- **Email Verification**: Email-based account verification system
- **Password Reset**: Email-based password reset functionality

### 📧 Email System
- **Email Notifications**: Email alerts for book assignments and recommendations
- **Email Digest**: Weekly/monthly email summaries of reading activity
- **Email Preferences**: User-configurable email notification settings
- **Welcome Emails**: Automated welcome emails for new users
- **Book Recommendation Emails**: Personalized book suggestion emails
- **Reading Progress Emails**: Periodic updates on reading progress
- **Admin Email Alerts**: Email notifications for admin activities

### 🚀 Performance & Scalability
- **Caching System**: Redis-based caching for improved performance
- **CDN Integration**: Content delivery network for static files
- **Database Optimization**: Query optimization and indexing
- **Background Tasks**: Celery integration for async tasks
- **Microservices Architecture**: Break down into microservices

### 📚 Content Enhancement
- **Multiple Book Sources**: Integration with Amazon, Goodreads APIs
- **E-book Support**: Upload and read e-books (PDF, EPUB)
- **Audiobook Integration**: Support for audiobook tracking
- **Book Series Management**: Track book series and reading order
- **Library Import**: Import books from external library systems

### 🤖 AI & Machine Learning
- **Smart Recommendations**: ML-powered book recommendations
- **Reading Time Estimation**: Predict reading time based on book length
- **Genre Classification**: Automatic genre classification
- **Content Summarization**: AI-generated book summaries
- **Sentiment Analysis**: Analyze user reviews and feedback

---

## 🛠️ Environment-Specific Guides

### 🏠 Local Development (SQLite)
Perfect for quick development and testing:
```bash
# Clone and run
git clone https://github.com/Jamesscott34/DevopsCA.git
cd DevopsCA
./custom_scripts/run_django.sh
```
- ✅ No database setup required
- ✅ Automatic admin creation
- ✅ Hot reload for development
- 🌐 Visit: [http://127.0.0.1:8000](http://127.0.0.1:8000)

### 🐳 Docker Compose (Postgres)
For containerized development with persistent data:
```bash
# Start with Docker Compose
./custom_scripts/run_docker.sh
```
- ✅ Postgres database with persistent volumes
- ✅ Automatic migrations and static files
- ✅ Easy management commands
- 🌐 Visit: [http://localhost:8000](http://localhost:8000)

**Docker Management Commands:**
```bash
# Run Django commands
docker-compose exec web python manage.py migrate
docker-compose exec web python manage.py createsuperuser
docker-compose exec web python manage.py collectstatic --noinput

# View logs
docker-compose logs web
docker-compose logs db

# Stop services
docker-compose down
```

### ☸️ Kubernetes (Minikube)
For production-like deployment with full automation:
```bash
# Full automated setup
./custom_scripts/setup.sh
```
- ✅ Interactive secrets setup
- ✅ Automatic pod deployment
- ✅ Database initialization
- ✅ Browser auto-open
- 🌐 Access via minikube service URL

**Manual Kubernetes Commands:**
```bash
# Apply manifests
kubectl apply -f k8s/secret.yaml
kubectl apply -f k8s/configmap.yaml
kubectl apply -f k8s/postgres-deployment.yaml
kubectl apply -f k8s/deployment.yaml
kubectl apply -f k8s/service.yaml

# Run migrations
kubectl exec -it <django-pod> -- python manage.py migrate
kubectl exec -it <django-pod> -- python manage.py createsuperuser
```

### 🚢 Helm Deployment
For advanced Kubernetes deployments:
```bash
# Install with Helm
helm install my-book-app ./book-catalogue

# Upgrade
helm upgrade my-book-app ./book-catalogue

# Uninstall
helm uninstall my-book-app
```

---

## 🗄️ Database Configuration

The app supports multiple database configurations:

| Environment | Database | Host | Port | Notes |
|-------------|----------|------|------|-------|
| Local Dev   | SQLite   | -    | -    | No setup required |
| Docker      | Postgres | `db` | `5432` | Service name |
| Kubernetes  | Postgres | `postgres` | `5432` | Service name |
| Local Postgres | Postgres | `localhost` | `5432` | Manual setup |

**Environment Variables:**
```bash
POSTGRES_DB=your_db_name
POSTGRES_USER=your_db_user
POSTGRES_PASSWORD=your_password
POSTGRES_HOST=db  # or localhost for local Postgres
POSTGRES_PORT=5432
```

---

## 👨‍💻 Admin & User Management

### Default Admin User
- **Username:** `admin`
- **Password:** `admin`
- **Email:** `admin@example.com`

### Admin Management Script
```bash
# Full admin setup
python custom_scripts/admin_manager.py

# Specific actions
python custom_scripts/admin_manager.py create    # Create admin
python custom_scripts/admin_manager.py verify    # Check admin exists
python custom_scripts/admin_manager.py reset     # Reset password to 'admin'
python custom_scripts/admin_manager.py stats     # Show user statistics
```

### Admin Dashboard Features
- 📊 User statistics and book analytics
- 👥 User management (view, edit, delete)
- 📚 Book management for all users
- 🔗 Referral book assignment
- 📧 Notification system
- 📝 User notes management

---

## 🔧 Helper Scripts

| Script | Purpose | Usage |
|--------|---------|-------|
| `run_django.sh` | Local development setup | `./custom_scripts/run_django.sh` |
| `run_docker.sh` | Docker Compose setup | `./custom_scripts/run_docker.sh` |
| `setup.sh` | Kubernetes automation | `./custom_scripts/setup.sh` |
| `admin_manager.py` | Admin user management | `python custom_scripts/admin_manager.py` |
| `host_helper.py` | DB host configuration | `python custom_scripts/host_helper.py` |

---

## 🐞 Troubleshooting

### Common Issues

**Database Connection Errors:**
```bash
# Check your DB host configuration
python custom_scripts/host_helper.py

# For Docker/K8s, ensure Postgres is running
docker-compose ps
kubectl get pods
```

**Admin Login Issues:**
```bash
# Reset admin password
python custom_scripts/admin_manager.py reset
```

**Static Files Not Loading:**
```bash
# Collect static files
python manage.py collectstatic --noinput
docker-compose exec web python manage.py collectstatic --noinput
kubectl exec -it <django-pod> -- python manage.py collectstatic --noinput
```

**Port Conflicts:**
```bash
# Change Docker Compose ports
# Edit docker-compose.yml:
# ports:
#   - "8080:8000"  # Use different host port
```

### Environment Reset

| Environment | Reset Command |
|-------------|---------------|
| Local | `rm -rf devops/ db.sqlite3 && ./custom_scripts/run_django.sh` |
| Docker | `docker-compose down -v && ./custom_scripts/run_docker.sh` |
| Kubernetes | `kubectl delete -f k8s/ && ./custom_scripts/setup.sh` |

---

## 📚 API Documentation

- **Base URL:** `http://127.0.0.1:8000/api/`
- **Authentication:** Session-based (login required)
- **Documentation:** [API Guide](docs/API_DOCUMENTATION.md)
- **Examples:** [JavaScript API Example](static/js/api-example.js)

**Quick API Test:**
```bash
# Login and get session cookie
curl -X POST http://127.0.0.1:8000/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{"username": "admin", "password": "admin"}' \
  -c cookies.txt

# Get books
curl http://127.0.0.1:8000/api/books/ -b cookies.txt
  ```

---

## 🏗️ Architecture

### Tech Stack
- **Backend:** Django 4.2+ (Python 3.8+)
- **Database:** SQLite (default), PostgreSQL ready
- **Frontend:** HTML + Bootstrap + Custom CSS
- **External API:** [Open Library](https://openlibrary.org/developers/api)
- **Containerization:** Docker + Docker Compose
- **Orchestration:** Kubernetes + Helm
- **Authentication:** Custom user model with password hashing

### Key Features
- ✅ User registration and authentication
- ✅ Book CRUD operations with ISBN generation
- ✅ Open Library integration and search
- ✅ Admin dashboard with user management
- ✅ Notification system with book recommendations
- ✅ REST API with full CRUD operations
- ✅ Book statistics and reading progress
- ✅ User notes and referral system
- ✅ Multi-environment deployment support

---

## 📖 Documentation

- [Quickstart Guide](docs/QUICKSTART.md) - Get started in any environment
- [Kubernetes Deployment](docs/KUBERNETES.md) - Manual K8s setup
- [Helm Deployment](docs/HELM_DEPLOYMENT.md) - Advanced K8s with Helm
- [API Documentation](docs/API_DOCUMENTATION.md) - Complete API reference

---

## 👨‍💻 Author

**James Scott**  
- **Student ID:** SBA24070  
- **Email:** jamesdeanscott19@gmail.com  
- **GitHub:** [github.com/Jamesscott34](https://github.com/Jamesscott34)

---

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

---

**Ready to get started? Choose your environment above and follow the quick start guide!** 🚀
