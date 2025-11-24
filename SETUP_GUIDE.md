# Quick Setup Guide - Online Caregivers Platform

## For Local Testing (5 Minutes)

### 1. Update Database Configuration

Open `config.py` and update your PostgreSQL credentials:
```python
DB_CONFIG = {
    'dbname': 'assign3_db',
    'user': 'your_username',      # Change this
    'password': 'your_password',   # Change this
    'host': 'localhost',
    'port': '5432'
}
```

### 2. Make sure your database is set up

If you haven't already imported your schema and data:
```bash
psql assign3_db < schema.sql
psql assign3_db < data.sql
```

### 3. Install Dependencies & Run

**Option A - Using the run script (Linux/Mac):**
```bash
chmod +x run.sh
./run.sh
```

**Option B - Manual setup:**
```bash
pip install -r requirements.txt
python app.py
```

### 4. Access the Application

Open your browser and go to: **http://localhost:5000**

---

## For PythonAnywhere Deployment (15 Minutes)

### 1. Sign up at PythonAnywhere
- Go to https://www.pythonanywhere.com
- Create a free account

### 2. Create PostgreSQL Database
- Go to **Databases** tab
- Initialize a PostgreSQL server (may take a few minutes)
- Create a database named `assign3_db`
- Note your connection details

### 3. Upload Files
- Go to **Files** tab
- Upload: `app.py`, `config.py`, `requirements.txt`, `schema.sql`, `data.sql`
- Upload the entire `templates` folder (with all subfolders)

### 4. Import Database Schema
- Go to **Databases** tab
- Click on "Postgres console" for your database
- Run:
  ```
  \i /home/yourusername/schema.sql
  \i /home/yourusername/data.sql
  ```

### 5. Update Configuration
Edit `config.py` with your PythonAnywhere details:
```python
DB_CONFIG = {
    'dbname': 'yourusername$assign3_db',
    'user': 'yourusername',
    'password': 'your_postgres_password',
    'host': 'yourusername.postgres.pythonanywhere-services.com',
    'port': '10000'  # Check your actual port in Databases tab
}
```

### 6. Set Up Web App
- Go to **Web** tab
- Click "Add a new web app"
- Choose "Manual configuration"
- Select Python 3.10
- In the "Code" section:
  - Source code: `/home/yourusername`
  - Working directory: `/home/yourusername`
- Edit WSGI configuration file:
  ```python
  import sys
  path = '/home/yourusername'
  if path not in sys.path:
      sys.path.append(path)
  
  from app import app as application
  ```

### 7. Install Dependencies
- Go to **Consoles** tab
- Start a Bash console
- Run:
  ```bash
  pip3 install --user -r requirements.txt
  ```

### 8. Reload and Test
- Go back to **Web** tab
- Click **Reload** button
- Visit: `http://yourusername.pythonanywhere.com`

---

## Testing CRUD Operations

### Test Flow:

1. **Create a User**
   - Go to Users → Add New User
   - Fill in all fields (user_id: 5, email, name, etc.)

2. **Create a Caregiver**
   - Go to Caregivers → Add New Caregiver
   - Select the user you just created
   - Fill in caregiver details

3. **Create a Member**
   - Go to Members → Add New Member
   - Create or select another user
   - Fill in member details

4. **Add Address**
   - Go to Addresses → Add New Address
   - Select the member
   - Enter address details

5. **Post a Job**
   - Go to Jobs → Post New Job
   - Select a member
   - Fill in job requirements

6. **Apply to Job**
   - Go to Applications → Add New Application
   - Select caregiver and job
   - Submit application

7. **Create Appointment**
   - Go to Appointments → Create New Appointment
   - Select caregiver and member
   - Set date, time, and hours

8. **Update Records**
   - Click Edit on any record
   - Modify fields
   - Save changes

9. **Delete Records**
   - Click Delete on any record
   - Confirm deletion
   - Note: Some deletions may fail due to foreign key constraints

---

## Common Issues & Solutions

### "Database connection failed"
- Check PostgreSQL is running: `sudo systemctl status postgresql`
- Verify credentials in config.py
- Test connection: `psql -U username -d assign3_db`

### "Module not found"
- Install requirements: `pip install -r requirements.txt`
- Activate virtual environment if using one

### "Template not found"
- Ensure templates folder is in the same directory as app.py
- Check folder structure matches README

### "Port 5000 already in use"
- Change port in app.py to 8000 or 8080
- Or kill process: `lsof -ti:5000 | xargs kill -9`

### PythonAnywhere: "502 Bad Gateway"
- Check error log in Web tab
- Verify WSGI configuration
- Ensure all dependencies are installed
- Reload the app

---

## Video Recording Tips

For your assignment video:

1. **Introduction (30 seconds)**
   - Show the home page
   - Mention it's Part 3 of Assignment 3

2. **CRUD Demonstration (5-7 minutes)**
   - Create: Add a new user, caregiver, job
   - Read: Show list views
   - Update: Edit an existing record
   - Delete: Delete a record

3. **Show Relationships (2 minutes)**
   - Demonstrate foreign key constraints
   - Show how caregivers link to users
   - Show job applications linking caregivers and jobs

4. **Deployed Application (1 minute)**
   - Show the PythonAnywhere URL
   - Access it from browser

5. **Conclusion (30 seconds)**
   - Mention technologies used
   - Any challenges faced

**Recording Tools:**
- OBS Studio (free)
- Zoom (record meeting)
- Screen recording on Mac/Windows

---

## Submission Checklist

Before submitting:

- [ ] schema.sql (your database schema)
- [ ] data.sql (with actual inserted data, not empty)
- [ ] app.py (Flask application)
- [ ] config.py (configuration file)
- [ ] requirements.txt
- [ ] templates folder (with all HTML files)
- [ ] README.md (this documentation)
- [ ] Executive summary (1 page PDF/Word)
- [ ] Video link (Google Drive, unlisted YouTube, etc.)
- [ ] All files in a ZIP archive

---

**You're all set! Good luck with your demonstration! 🚀**
