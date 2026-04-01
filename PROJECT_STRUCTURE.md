# Flask Portfolio Webapp – Projektstruktur

## 1. Projektüberblick

Beschreibung:
Eine Fullstack Portfolio Webapp mit Admin-Bereich zur Verwaltung von Projekten, Nutzern und Kontaktanfragen.

Tech Stack:
- Flask
- SQLAlchemy
- MySQL (Docker)
- Flask-Migrate (Alembic)
- Docker Compose
- Gunicorn

Deployment:
- GitHub = Source of Truth
- VPS zieht per git pull
- Start über docker compose up -d --build


---

## 2. Ordnerstruktur

Root:
- webapp.py → Einstiegspunkt
- docker-compose.yml → Container Setup
- Dockerfile → Web-Container Definition
- requirements.txt → Python Dependencies

app/
- __init__.py → App Factory
- models/ → Datenbank-Modelle
- routes/ → Blueprints / Routen
- templates/ → Jinja2 Templates
- static/ → CSS, JS, Bilder, Uploads

instance/
- database.db (nur lokal relevant)

migrations/
- Alembic Migrationen

---

## 3. Models

### User
(Datei: app/models/user.py)

Beschreibung:
Repräsentiert einen registrierten Benutzer der Anwendung. 
Wird für Login und Rollenverwaltung (Admin/User) genutzt.

Wichtige Felder:
- id (Primary Key)
- username (unique)
- email (unique)
- password_hash
- role ("user" oder "admin")

Besondere Methoden:
- set_password(password) → speichert gehashtes Passwort
- check_password(password) → prüft Passwort
- is_admin() → prüft ob Benutzer Admin ist

Beziehungen:
- keine direkten Foreign Keys

### Project
(Datei: app/models/project.py)

Beschreibung:
Repräsentiert ein Projekt, das in der Webapp angezeigt wird. 
Enthält alle Infos für Projektübersicht, Detailseite und mögliche Links zu GitHub oder Live-Demo.

Wichtige Felder:
- id (Primary Key)
- title (Pflichtfeld, Name des Projekts)
- short_description (optional, kurze Vorschau)
- description (Pflichtfeld, ausführliche Beschreibung)
- tech_stack (Technologien als String)
- github_url (optional, Link zum Repo)
- live_url (optional, Link zur Live-Demo)
- image (optional, Name der hochgeladenen Bilddatei)
- created_at (automatisch, Zeit der Erstellung)
- order (Reihenfolge beim Anzeigen)

Beziehungen:
- keine direkten Foreign Keys (Projekt kann ggf. durch andere Modelle referenziert werden)

### ContactMessage
(Datei: app/models/contact_message.py)

Beschreibung:
Repräsentiert eine Kontaktanfrage, die über das Kontaktformular der Webapp verschickt wird.

Wichtige Felder:
- id (Primary Key)
- name (Pflichtfeld, Name der Person)
- email (Pflichtfeld, E-Mail-Adresse)
- message (Pflichtfeld, Nachrichtentext)
- created_at (automatisch, Zeitpunkt der Nachrichtenerstellung)

Beziehungen:
- keine direkten Foreign Keys

## 4. Routes

### Auth Blueprint
(Datei: app/routes/auth.py)

Beschreibung:
Handles Benutzerregistrierung, Login, Logout und Account-Seite.  

Endpoints:

- `GET/POST /register` → Benutzer registrieren  
  - POST verarbeitet Registrierung, prüft auf existierende E-Mail, speichert User, setzt Passwort, gibt Feedback via Flash.  
- `GET/POST /login` → Benutzer einloggen  
  - POST prüft Email + Passwort, loggt User ein, redirect zu Projekten, Feedback via Flash.  
- `GET /logout` → Benutzer ausloggen  
  - Nur für eingeloggte User, loggt aus, redirect zu Login, Flash-Info.  
- `GET /account` → Benutzerkonto anzeigen  
  - Nur für eingeloggte User, rendert Account-Seite mit `current_user`.

Besondere Logik:
- Prüft Benutzerrolle für Admin/User
- Nutzt Flask-Login für Session-Management
- Setzt Flash-Nachrichten bei Fehlern oder Erfolgen

Beziehungen zu Models:
- Verknüpft mit User-Model für Registrierung, Login und Rollenprüfung

### Main Blueprint
(Datei: app/routes/main.py)

Beschreibung:
Enthält die Startseite der Webapp.

Endpoints:

- `GET /` → Startseite  
  - Lädt die 3 neuesten Projekte (nach created_at sortiert)  
  - Rendert `index.html` mit Projekt-Vorschau

Beziehungen zu Models:
- Project (für Anzeige der neuesten Projekte)

### Projects Blueprint
(Datei: app/routes/projects.py)

Beschreibung:
Enthält die Projektübersicht und Detailseiten einzelner Projekte.

Endpoints:

- `GET /projects/` (bzw. `/` innerhalb des Blueprints) → Projektübersicht  
  - Sortiert Projekte nach Session-Wert (`newest` oder `oldest`)  
  - Standard: neueste zuerst  
  - Rendert `projects.html`

- `GET /projects/<project_id>` → Projekt-Detailseite  
  - Lädt ein einzelnes Projekt per ID  
  - 404 wenn nicht gefunden  
  - Rendert `project_detail.html`

Besondere Logik:
- Nutzt Session (`project_sort`) für Sortierreihenfolge

Beziehungen zu Models:
- Project (für Übersicht und Detailanzeige)

### Contact Blueprint
(Datei: app/routes/contact.py)

Beschreibung:
Enthält das Kontaktformular und speichert eingehende Nachrichten in der Datenbank.

Endpoints:

- `GET/POST /contact/` (bzw. `/` im Blueprint) → Kontaktseite  
  - GET: Rendert das Kontaktformular  
  - POST: Validiert Eingaben (name, email, message)  
  - Speichert Nachricht als ContactMessage in der Datenbank  
  - Zeigt Flash-Nachricht bei Erfolg oder Fehler  

Besondere Logik:
- Einfache Formular-Validierung
- Speichert Daten direkt via SQLAlchemy

Beziehungen zu Models:
- ContactMessage (Speicherung von Kontaktanfragen)

### About Blueprint
(Datei: app/routes/about.py)

Beschreibung:
Statische „Über mich“-Seite der Webapp.

Endpoints:

- `GET /about/` (bzw. `/` im Blueprint) → About-Seite  
  - Rendert `about.html`

Beziehungen zu Models:
- keine

## 8. Admin (Blueprint)
(Datei: app/routes/admin)

### Dateien
- `__init__.py` → initialisiert den Admin-Blueprint
- `bp.py` → zentrale Registrierung der Admin-Routes / Blueprint
- `dashboard.py` → Dashboard-Seiten (Übersicht, Statistiken, Startseite Admin)
- `projects.py` → Admin-Management für Projekte (CRUD)
- `contacts.py` → Admin-Management für Kontaktanfragen
- `users.py` → Admin-Management für Benutzer (CRUD, Rollen)
- `utils.py` → Hilfsfunktionen für Admin-Bereich (z. B. Berechtigungen, Filter)

### Admin Blueprint
(Datei: app/routes/admin/bp.py)

Beschreibung:
Definiert den zentralen Admin-Blueprint (`admin_bp`) mit URL-Prefix `/admin`.  
Alle Admin-Routen werden über diesen Blueprint registriert.

Besondere Logik:
- Setzt den URL-Prefix `/admin`
- Wird in der App Factory (`app/__init__.py`) registriert
- Dient als Sammelpunkt für alle Admin-Module (dashboard, users, projects, contacts)

### Dashboard
(Datei: app/routes/admin/dashboard.py)

Beschreibung:
Stellt die Admin-Übersicht bereit. Zeigt Kennzahlen über die Anwendung (Anzahl Nutzer, Nachrichten und Projekte).

Endpoints:
- `/admin/`  
  - Methode: GET  
  - Funktion: Rendert das Dashboard-Template `admin/dashboard.html` mit Zählerwerten für Users, Messages und Projects.

- `/admin/stats`  
  - Methode: GET  
  - Funktion: Gibt die gleichen Kennzahlen als JSON zurück (für API/Ajax-Zwecke).

Besondere Logik:
- Alle Routen sind `@login_required`.
- Zählt die Einträge aus den Models: User, ContactMessage, Project.
- Nutzt Flask-Login für Zugriffsschutz.

### Admin Contacts
(Datei: app/routes/admin/contacts.py)

Beschreibung:
Verwaltung der Kontaktanfragen im Admin-Bereich. Anzeigen, Detailansicht und Löschen von Nachrichten.

Endpoints:
- `/admin/contacts`  
  - Methode: GET  
  - Funktion: Listet alle Kontaktanfragen in absteigender Reihenfolge (`id desc`) und rendert `admin/contact_requests.html`.

- `/admin/contact/<int:message_id>`  
  - Methode: GET  
  - Funktion: Zeigt die Detailansicht einer einzelnen Kontaktanfrage (`admin/contact_detail.html`).  

- `/admin/contacts/delete/<int:message_id>`  
  - Methode: GET  
  - Funktion: Löscht eine bestimmte Kontaktanfrage aus der Datenbank und zeigt eine Flash-Nachricht.  

Besondere Logik:
- Alle Routen sind `@login_required`.
- Nutzt `ContactMessage` Model.
- Löschen erfolgt über SQLAlchemy Session Commit.
- Flash-Messages informieren über erfolgreiche Aktionen.

### Admin Users
(Datei: app/routes/admin/users.py)

Beschreibung:
Verwaltung der Benutzer im Admin-Bereich. Anzeigen, Bearbeiten, Löschen und Rollenänderung von Usern.

Endpoints:
- `/admin/users`  
  - Methode: GET  
  - Funktion: Listet alle Benutzer und rendert `admin/users.html`.

- `/admin/user/<int:user_id>`  
  - Methode: GET / POST  
  - Funktion:  
    - GET: Zeigt Detailseite eines Benutzers (`admin/user_detail.html`).  
    - POST: Aktualisiert Username und Email des Benutzers.

- `/admin/user/delete/<int:user_id>`  
  - Methode: GET  
  - Funktion: Löscht einen Benutzer aus der Datenbank.  
  - Besonderheit: Admin kann sich nicht selbst löschen.

- `/admin/user/toggle_role/<int:user_id>`  
  - Methode: GET  
  - Funktion: Wechselt Rolle zwischen `"user"` und `"admin"`.

Besondere Logik:
- Alle Routen sind `@login_required`.
- Schutz gegen Selbstlöschung über `current_user`.
- Rollenumschaltung erfolgt direkt per String-Toggle.
- Änderungen werden per SQLAlchemy `commit()` gespeichert.

Beziehungen zu Models:
- User

### Admin Projects
(Datei: app/routes/admin/projects.py)

Beschreibung:
Verwaltung von Projekten im Admin-Bereich. Anzeigen, Sortieren, Erstellen, Bearbeiten und Löschen von Projekten.

Endpoints:
- `/admin/projects`  
  - Methode: GET  
  - Funktion: Listet alle Projekte, sortiert nach `newest` (default) oder `oldest`. Rendert `admin/projects.html`.

- `/admin/project/new`  
  - Methode: GET / POST  
  - Funktion:  
    - GET: Zeigt Formular zum Erstellen eines neuen Projekts (`admin/project_form.html`).  
    - POST: Speichert neues Projekt mit Bildupload.

- `/admin/project/edit/<int:project_id>`  
  - Methode: GET / POST  
  - Funktion:  
    - GET: Zeigt Bearbeitungsformular für ein Projekt.  
    - POST: Aktualisiert Projektdaten und optional das Bild.

- `/admin/project/delete/<int:project_id>`  
  - Methode: POST  
  - Funktion: Löscht ein Projekt.

- `/admin/projects/sort`  
  - Methode: POST  
  - Funktion: Setzt Sortierreihenfolge (`newest` / `oldest`) in Session.

Besondere Logik:
- Alle Routen sind `@login_required`.
- Bild-Uploads werden über `handle_image_upload()` verarbeitet.
- Projektänderungen werden per SQLAlchemy `commit()` gespeichert.
- Session wird für Projektsortierung genutzt.

Beziehungen zu Models:
- Project

### Admin Utils
(Datei: app/routes/admin/utils.py)

Beschreibung:
Hilfsfunktionen für den Admin-Bereich, hauptsächlich für das sichere Hochladen von Projektbildern.

Funktionen:

- `allowed_file(filename)`  
  - Prüft, ob die Dateiendung erlaubt ist.  
  - Nutzt `ALLOWED_EXTENSIONS` aus der Flask-Konfiguration.

- `handle_image_upload()`  
  - Verarbeitet Bild-Uploads aus Formularen.  
  - Prüft:
    - ob eine Datei vorhanden ist
    - ob die Dateiendung erlaubt ist  
  - Erstellt einen eindeutigen Dateinamen mit `uuid`.  
  - Speichert das Bild im `UPLOAD_FOLDER`.  
  - Gibt den neuen Dateinamen zurück (oder `None` wenn kein Upload erfolgt).

Besondere Logik:
- Verhindert Dateikonflikte durch zufällige UUID-Dateinamen.
- Nutzt `secure_filename`-ähnliches Verhalten durch kontrollierte Speicherung.
- Konfigurationsabhängig (`UPLOAD_FOLDER`, `ALLOWED_EXTENSIONS`).

## Deployment Workflow

1. Entwicklung lokal (VS Code)
2. Änderungen committen und zu GitHub pushen
3. VPS aktualisieren:
   - git pull
   - docker compose up -d --build

GitHub dient als zentrale Source of Truth für den Code.

## Application Entry Point

- `webapp.py` → Startet die Flask-App
- Lädt die App Factory aus `app/__init__.py`
- Registriert Blueprints und Extensions

## Templates & Static

Templates:
- `templates/` enthält alle Jinja2 Templates
- Unterordner:
  - `admin/` → Admin-Seiten
  - `auth/` → Login / Register
  - `widgets/` → wiederverwendbare Template-Komponenten

Static:
- `static/css` → Stylesheets
- `static/js` → JavaScript
- `static/img` → Bilder
- `static/uploads` → hochgeladene Projektbilder