# Flask Portfolio Web App

A fullstack portfolio web application built with Flask — designed to showcase projects, skills, and background, with a fully database-driven admin dashboard for managing all content.

Live: [benno-klan.com](https://benno-klan.com)

---

## Features

**Public-facing**
- Hero section with background image and transparent navbar
- Typing animation and GitHub / LinkedIn social links
- Project showcase with detail pages and Markdown-rendered descriptions
- Clickable tech badges that filter projects by technology
- About page with dynamic timeline, current status, and certificates
- Contact form with database storage

**Admin dashboard**
- Full CRUD for projects (with image upload and Markdown editor)
- Timeline, current status, and certificate management
- User management with role system (admin / user)
- Contact message inbox
- Dashboard with live stats

---

## Tech Stack

| Layer | Tech |
|---|---|
| Backend | Flask, Flask-Login, SQLAlchemy, Flask-Migrate |
| Database | MySQL (Docker) |
| Frontend | Jinja2, Bootstrap 5, HTML, CSS, JavaScript |
| Editor | EasyMDE (Markdown editor for admin) |
| Deployment | Docker, Docker Compose, Gunicorn |
| Version Control | Git & GitHub |

---

## Local Setup

```bash
git clone https://github.com/tfForster/flask-webapp.git
cd flask-webapp
pip install -r requirements.txt
python webapp.py
```

Open at `http://localhost:5000`

---

## Docker (Production-like)

```bash
docker compose up -d --build
docker compose exec web flask db upgrade
```

---

## Deployment (VPS)

```bash
git pull
docker compose up -d --build
```

GitHub is the source of truth. All content (projects, timeline, status, certificates) is managed via the admin dashboard at `/admin` — no redeploy needed for content changes.

---

## Project Structure

```
app/
├── models/         # SQLAlchemy models (User, Project, ContactMessage, TimelineEvent, CurrentStatus, Certificate)
├── routes/         # Flask Blueprints (auth, main, projects, contact, about, admin)
├── templates/      # Jinja2 templates
│   ├── admin/
│   ├── auth/
│   ├── widgets/    # navbar, footer
│   └── components/ # tech_badges macro
└── static/         # CSS, JS, images, uploads
```

---

## Notes

- Project descriptions support Markdown — write bullet points and headings directly in the admin form
- This project is part of my ongoing learning in backend / fullstack development and grows with every new thing I pick up
