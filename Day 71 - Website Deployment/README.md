# Day 71 - Website Deployment

A small Flask blog used to practise deployment.

## Run locally

1. Install dependencies:
   python -m pip install -r requirements.txt

2. Set a local secret key in PowerShell:
   $env:FLASK_SECRET_KEY = "local-development-secret-change-this"

3. Run:
   python main.py

4. Open http://127.0.0.1:5000/

## Production

- Set FLASK_SECRET_KEY to a long, random secret in the hosting dashboard.
- Set DATABASE_URL to the PostgreSQL connection URL supplied by the hosting provider.
- Start the service with: gunicorn main:app
- Never commit .env files, passwords, or database credentials.

This is a learning project. For a production blog, use managed database migrations
when the database schema changes, and add appropriate security protections.
