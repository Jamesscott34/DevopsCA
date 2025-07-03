# 📚 SBA24070 Book Catalogue App

This is a Django-based book catalogue system developed as part of a DevOps assignment. It allows users to manage personal book collections with the ability to:

- Add/edit/delete books manually
- Browse and import books from the Open Library API
- Toggle read/unread status
- Store descriptions and auto-generate ISBNs

---

## 🚀 How It Works

- **Home Page** shows all saved books in a table.
- **Manual Add** lets you enter title, author, published date, description, and an auto-generated ISBN (starting with `JS`).
- **Open Library Search** lets you search external books, view results, and import selected ones into your library with auto-generated ISBNs.
- **Books are saved in a PostgreSQL/SQLite DB** using Django’s ORM.
- **Books can be edited, deleted, and marked read/unread**.

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
- [x] Branching + Merging with Git (open-library-integration → master → api-js-bridge)

---

## 📦 Tech Stack

- **Backend**: Django (Python 3.13)  
- **Database**: SQLite (default), PostgreSQL ready  
- **Frontend**: HTML + Bootstrap  
- **External API**: [Open Library](https://openlibrary.org/developers/api)  
- **Version Control**: Git + GitHub  
- **Deployment**: Docker & Kubernetes (coming soon)

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
python manage.py migrate

# 5. Start the dev server
python manage.py runserver
