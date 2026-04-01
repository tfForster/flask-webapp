# Flask Portfolio Web App

A fullstack portfolio web application built with Flask.
It allows visitors to view projects, send contact messages, and includes an admin dashboard for managing content.

---

## 🚀 Features

* 📂 Project showcase with detail pages
* 🔐 User authentication (login & registration)
* 🛠 Admin dashboard for managing:

  * Projects (create, edit, delete)
  * Users (manage & roles)
  * Contact messages
* 📬 Contact form with database storage
* 🖼 Image upload for projects
* 📊 Basic admin statistics (users, messages, projects)

---

## 🧱 Tech Stack

* **Backend:** Flask, Flask-Login, SQLAlchemy
* **Database:** MySQL (Docker)
* **Migrations:** Flask-Migrate (Alembic)
* **Frontend:** Jinja2, HTML, CSS
* **Deployment:** Docker, Docker Compose, Gunicorn
* **Version Control:** Git & GitHub

---

## ⚙️ Installation & Setup (Local Development)

### 1. Clone the repository

```bash
git clone https://github.com/tfForster/flask-webapp.git
cd flask-webapp
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Run the application

```bash
python webapp.py
```

### 4. Open in browser

```
http://localhost:5000
```

---

## 🐳 Optional: Run with Docker (Production-like)

If you want to run the app in a containerized environment:

```bash
docker compose up -d --build
```

Run migrations:

```bash
docker compose exec web flask db upgrade
```

---

## 🚀 Deployment (VPS)

The application is deployed using Docker on a VPS.

### Update application:

```bash
git pull
docker compose up -d --build
```

The app is accessible via the server's IP or domain.

---

## 🔁 Workflow

1. Develop locally
2. Push changes to GitHub
3. Pull changes on VPS
4. Restart containers

GitHub acts as the **Source of Truth**

---

## 🔑 Admin Access

* Admin dashboard:

```
/admin
```

* Features:

  * Manage projects
  * View contact messages
  * Manage users and roles

---

## 📦 Project Structure

The project follows a modular Flask architecture using Blueprints:

* `routes/` → Application routes (auth, projects, contact, admin, etc.)
* `models/` → Database models (User, Project, ContactMessage)
* `templates/` → Jinja2 templates
* `static/` → CSS, JS, images, uploads

---

## 📌 Notes

* This project is part of my learning journey in backend / fullstack development
* Focus: clean structure, real-world features, and practical deployment

---

## 📬 Contact

If you have feedback or questions, feel free to reach out.
