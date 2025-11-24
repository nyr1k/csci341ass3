# Render.com Deployment Guide

## Quick Setup

1. Push your code to GitHub
2. Go to https://render.com and sign up/login
3. Click "New +" → "Web Service"
4. Connect your GitHub repository

## Configuration

**Build Command:**
```
./build.sh
```

**Start Command:**
```
gunicorn app:app
```

**Environment Variables:**
Add these in Render dashboard:
```
DB_NAME=your_database_name
DB_USER=your_database_user
DB_PASSWORD=your_database_password
DB_HOST=your_postgres_host
DB_PORT=5432
```

## Python Version

The `runtime.txt` file specifies Python 3.11.9 for compatibility with psycopg2-binary.

If Render defaults to Python 3.13, you may need to:
1. Use the `runtime.txt` file (some platforms)
2. Or update app.py to use environment variables for database config
