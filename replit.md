# Codexx Wallets

## Overview
Codexx Wallets is a Flask-based portfolio ecosystem application where verified builders, service providers, and project owners present real portfolios backed by actual work.

## Project Structure
- `app_new.py` - Main Flask application entry point using Application Factory Pattern
- `config.py` - Configuration classes for different environments
- `extensions.py` - Flask extensions initialization
- `models.py` - SQLAlchemy database models
- `blueprints/` - Modular route handlers (auth, dashboard, pages, portfolio, services)
- `utils/` - Utility functions (data, decorators, helpers, notifications, security)
- `templates/` - Jinja2 HTML templates
- `static/` - Static assets (CSS, JS, images)
- `migrations/` - Database migrations with Alembic

## Tech Stack
- Python 3.11
- Flask 3.1.1 with Blueprints
- SQLAlchemy with Flask-SQLAlchemy (supports PostgreSQL and SQLite)
- Flask-Login for authentication
- Flask-Dance for OAuth
- Gunicorn for production WSGI server
- WeasyPrint/PDFKit for PDF generation

## Running the Application
The application runs on port 5000 using the Flask development server:
```
python app_new.py
```

For production:
```
gunicorn app_new:app
```

## Database
- Development: SQLite (codexx.db)
- Production: PostgreSQL (via DATABASE_URL environment variable)

## Environment Variables
- `SECRET_KEY` / `SESSION_SECRET` - Flask session secret
- `DATABASE_URL` - PostgreSQL connection string
- `ADMIN_USERNAME` / `ADMIN_PASSWORD` - Admin credentials
- `ADMIN_TELEGRAM_BOT_TOKEN` / `ADMIN_TELEGRAM_CHAT_ID` - Telegram notifications
- `ADMIN_SMTP_*` - Email configuration
