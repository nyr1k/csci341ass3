# Fix for Render.com Python 3.13 Deployment Issue

## Problem
Render.com defaults to Python 3.13, but `psycopg2-binary==2.9.9` has compatibility issues with Python 3.13.

## Solutions

### Option 1: Force Python 3.11 (Recommended for Render)

1. **Create `render.yaml`** in your project root:

```yaml
services:
  - type: web
    name: caregivers-platform
    env: python
    buildCommand: "./build.sh"
    startCommand: "gunicorn app:app"
    envVars:
      - key: PYTHON_VERSION
        value: "3.11.9"
      - key: DATABASE_URL
        fromDatabase:
          name: your_database_name
          property: connectionString
```

2. **Push to GitHub and deploy via Render dashboard**

### Option 2: Use PostgreSQL from Render Dashboard

1. In Render dashboard, go to your Web Service
2. Click "Environment" tab
3. Add these variables:
   - `PYTHON_VERSION` = `3.11.9`
   - `DATABASE_URL` = (connect to your PostgreSQL database)

### Option 3: Upgrade to psycopg3 (Alternative)

If you want to use Python 3.13, update `requirements.txt`:

```
Flask==3.0.0
psycopg[binary]==3.1.13
Werkzeug==3.0.1
Jinja2==3.1.2
MarkupSafe==2.1.3
itsdangerous==2.1.2
click==8.1.7
gunicorn==21.2.0
```

Then update `app.py` imports:
```python
# Change from:
import psycopg2
from psycopg2.extras import RealDictCursor

# To:
import psycopg
from psycopg.rows import dict_row
```

And update connection code:
```python
def get_db_connection():
    """Create and return a database connection"""
    conn = psycopg.connect(**DB_CONFIG, row_factory=dict_row)
    return conn
```

## Current Configuration

The project now includes:
- ✅ `runtime.txt` - Specifies Python 3.11.9
- ✅ `.python-version` - For local development
- ✅ `build.sh` - Build script for Render
- ✅ `app.py` - Updated to use DATABASE_URL environment variable
- ✅ `gunicorn` added to requirements.txt

## Deploy to Render

1. **Push code to GitHub:**
   ```bash
   git add .
   git commit -m "Add Render deployment configuration"
   git push
   ```

2. **Create Web Service on Render:**
   - Go to https://render.com/dashboard
   - Click "New +" → "Web Service"
   - Connect your GitHub repo
   - Settings:
     - **Name:** caregivers-platform
     - **Environment:** Python 3
     - **Build Command:** `./build.sh`
     - **Start Command:** `gunicorn app:app`
     - **Python Version:** Will use runtime.txt (3.11.9)

3. **Add PostgreSQL Database:**
   - In Render dashboard, create a PostgreSQL database
   - Copy the "Internal Database URL"
   - Add as environment variable `DATABASE_URL` to your web service

4. **Deploy:**
   - Click "Create Web Service"
   - Wait for deployment to complete

## Testing Locally

Your app should still work locally with the Unix socket connection:
```bash
python3 app.py
```

The environment variable logic only activates when `DATABASE_URL` or `DB_HOST` is set.
