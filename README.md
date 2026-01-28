# Codexx Wallets - Elite Proof-of-Work Ecosystem

Codexx Wallets is a premium professional portfolio platform designed for high-caliber professionals. It centers on verified execution history, closed filtering, and unmediated transparency.

## ðŸš€ Vision & Methodology
*   **Proof over Promise**: Verified execution history over self-proclaimed skills.
*   **Closed Filtering**: Access controlled through direct internal vetting.
*   **Unmediated Transparency**: Peer-to-peer and client-to-professional connectivity.
*   **Build in Silence, Show in Public**: Private cultivation and public showcase with absolute proof.

## ðŸ›  Technical Architecture
*   **Backend**: Python 3.11 with Flask 3.x
*   **Database**: PostgreSQL
*   **Frontend**: Jinja2 with Bootstrap 5
*   **Authentication**: Custom session-based auth with Admin/Demo/User roles.
*   **Notifications**: Dual-channel (Telegram Bot API & SMTP Email).
*   **Security**: Rate-limiting, IP-based activity monitoring, and separate notification channels.

## ðŸ“ Project Structure
*   `app.py`: Main Flask application logic and routing.
*   `models.py`: SQLAlchemy database models (PostgreSQL).
*   `config.py`: Environment-based configuration management.
*   `data.json`: Core application data (Legacy support).
*   `templates/`: Jinja2 HTML templates.
*   `static/`: CSS, JS, and professional assets.
*   `backups/`: Automated data backup system.

## ðŸ“¦ Deployment
The project is configured for deployment on:
*   **Replit**: Primary development and production environment.
*   **Render**: Production deployment using the included `render.yaml` and `Procfile`.

## ðŸ›¡ Security & Privacy
Codexx Wallets implements a strict separation between Administrative and User data. Notification channels (Telegram/SMTP) are isolated to ensure privacy and professional integrity.

---
Â© 2026 Codexx Wallets. All rights reserved.
