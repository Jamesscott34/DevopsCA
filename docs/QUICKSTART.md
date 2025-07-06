# SBA24070 Book Catalogue App – Quickstart

**Database Flexibility Note:**
- You do **not** have to use the database provided by default.
- By default, the app uses SQLite, which requires no setup—just clone and run.
- You can switch to PostgreSQL (or another supported DB) by updating `settings.py` (or your `.env` for Docker) and running migrations.
- See below for setup instructions for both local and Docker environments.

## Setup (Recommended)

1. Clone the repository and enter the project directory.
2. Run the setup script:
   ```sh
   ./setup.sh
   ```
3. The script will:
   - Install dependencies
   - Run migrations
   - Collect static files
   - Create the admin user
   - Start the server
4. Open your browser and go to: [http://127.0.0.1:8000](http://127.0.0.1:8000)
5. Log in as admin:
   - Username: `admin`
   - Password: `admin`

## Manual Setup

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

## Docker Setup

1. Build and start the containers:
   ```sh
   docker compose up --build
   ```
2. Run migrations and collect static files:
   ```sh
   docker compose exec web python manage.py migrate
   docker compose exec web python manage.py collectstatic --noinput
   docker compose exec web python manage.py create_admin
   ```
3. Visit: [http://localhost:8000](http://localhost:8000)
   - Log in as admin: `admin` / `admin`

## Admin Login

- The admin user (`admin`/`admin`) can log in via the main login page at `/login/`.
- The admin dashboard is accessible after login. 