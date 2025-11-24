# Online Caregivers Platform - Web Application
## CSCI 341 - Database Management Systems - Assignment 3, Part 3

A Flask-based web application with full CRUD functionality for managing an online caregivers platform database.

## Features

✅ **Complete CRUD Operations** for all tables:
- Users (base user accounts)
- Caregivers (caregiver profiles)
- Members (family members seeking care)
- Addresses (member addresses)
- Jobs (job postings by members)
- Job Applications (caregiver applications to jobs)
- Appointments (scheduled caregiving appointments)

✅ **User-Friendly Interface**:
- Clean, modern design with color-coded cards
- Responsive navigation
- Flash messages for user feedback
- Form validation
- Confirmation dialogs for deletions

✅ **Database Integration**:
- PostgreSQL database connection
- Proper foreign key relationships
- Transaction handling with rollback on errors

## Project Structure

```
assign3/
├── app.py                          # Main Flask application
├── config.py                       # Database configuration
├── requirements.txt                # Python dependencies
├── schema.sql                      # Database schema
├── data.sql                        # Sample data
├── templates/
│   ├── base.html                   # Base template with navigation
│   ├── index.html                  # Home page
│   ├── users/
│   │   ├── list.html              # List all users
│   │   ├── create.html            # Create new user
│   │   └── edit.html              # Edit user
│   ├── caregivers/
│   │   ├── list.html
│   │   ├── create.html
│   │   └── edit.html
│   ├── members/
│   │   ├── list.html
│   │   ├── create.html
│   │   └── edit.html
│   ├── addresses/
│   │   ├── list.html
│   │   ├── create.html
│   │   └── edit.html
│   ├── jobs/
│   │   ├── list.html
│   │   ├── create.html
│   │   └── edit.html
│   ├── job_applications/
│   │   ├── list.html
│   │   └── create.html
│   └── appointments/
│       ├── list.html
│       ├── create.html
│       └── edit.html
└── README.md                       # This file
```

## Installation & Local Setup

### Prerequisites
- Python 3.8 or higher
- PostgreSQL 12 or higher
- pip (Python package manager)

### Step 1: Database Setup

1. Create the database:
```bash
createdb assign3_db
```

2. Import the schema and data:
```bash
psql assign3_db < schema.sql
psql assign3_db < data.sql
```

### Step 2: Install Python Dependencies

```bash
pip install -r requirements.txt
```

### Step 3: Configure Database Connection

Edit `config.py` and update the database credentials:
```python
DB_CONFIG = {
    'dbname': 'assign3_db',
    'user': 'your_username',
    'password': 'your_password',
    'host': 'localhost',
    'port': '5432'
}
```

Or update the credentials directly in `app.py` (lines 11-17).

### Step 4: Run the Application

```bash
python app.py
```

The application will be available at: **http://localhost:5000**

## Deployment to PythonAnywhere

### Step 1: Create a PythonAnywhere Account
1. Go to https://www.pythonanywhere.com
2. Sign up for a free account

### Step 2: Upload Your Files
1. Go to the "Files" tab
2. Create a new directory: `assign3`
3. Upload all project files (app.py, config.py, requirements.txt, and templates folder)

### Step 3: Set Up PostgreSQL Database
1. Go to the "Databases" tab
2. Create a new PostgreSQL database
3. Note the database name, username, password, and host
4. Use the PostgreSQL console to import your schema and data:
   ```sql
   \i /path/to/schema.sql
   \i /path/to/data.sql
   ```

### Step 4: Install Dependencies
1. Go to the "Consoles" tab
2. Start a Bash console
3. Navigate to your project directory:
   ```bash
   cd assign3
   ```
4. Create a virtual environment:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```
5. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

### Step 5: Configure the Web App
1. Go to the "Web" tab
2. Click "Add a new web app"
3. Choose "Manual configuration" and select Python 3.10
4. Set the source code directory to: `/home/yourusername/assign3`
5. Set the working directory to: `/home/yourusername/assign3`
6. Edit the WSGI configuration file:
   ```python
   import sys
   path = '/home/yourusername/assign3'
   if path not in sys.path:
       sys.path.append(path)
   
   from app import app as application
   ```

### Step 6: Update Database Configuration
Edit `app.py` or `config.py` with your PythonAnywhere database credentials:
```python
DB_CONFIG = {
    'dbname': 'yourusername$assign3_db',
    'user': 'yourusername',
    'password': 'your_database_password',
    'host': 'yourusername.postgres.pythonanywhere-services.com',
    'port': '10000'  # Check your actual port
}
```

### Step 7: Reload and Access
1. Click "Reload" on the Web tab
2. Your app will be live at: `http://yourusername.pythonanywhere.com`

## Alternative Free Hosting Options

### Heroku (Paid - Free tier discontinued)
- Follow Heroku's deployment guide for Flask apps
- Use Heroku Postgres add-on

### Railway.app (Free tier available)
1. Connect your GitHub repository
2. Add PostgreSQL database
3. Set environment variables
4. Deploy automatically

### Render.com (Free tier available)
1. Create a new Web Service from Git
2. Add PostgreSQL database
3. Set environment variables
4. Deploy

### AWS Lightsail (Educational credits available with @nu.edu.kz email)
1. Create a Lightsail instance
2. Install Python and PostgreSQL
3. Configure security groups
4. Deploy your application

## Usage Guide

### Creating Data Flow
1. **First**: Create Users (base accounts)
2. **Then**: Create Caregivers or Members (linked to users)
3. **For Members**: Add Addresses
4. **Next**: Members can post Jobs
5. **Then**: Caregivers can submit Job Applications
6. **Finally**: Create Appointments between caregivers and members

### Navigation
- Use the top navigation bar to access different sections
- Each section has:
  - **List view**: Shows all records with Edit and Delete buttons
  - **Create view**: Form to add new records
  - **Edit view**: Form to modify existing records

### Features Demonstrated

**Create (C)**:
- Add new users, caregivers, members, addresses, jobs, applications, and appointments
- Form validation ensures data integrity
- Foreign key constraints prevent orphaned records

**Read (R)**:
- View all records in organized tables
- Join queries show related information (e.g., caregiver names with jobs)
- Truncated display for long text fields

**Update (U)**:
- Edit any record through intuitive forms
- Existing values pre-populated
- Changes committed with transaction safety

**Delete (D)**:
- Remove records with confirmation dialogs
- CASCADE delete ensures referential integrity
- Error handling for constraint violations

## Database Schema

The application manages 7 tables:
- **users**: Base user information
- **caregivers**: Caregiver-specific data (inherits from users)
- **members**: Member-specific data (inherits from users)
- **addresses**: Member addresses
- **jobs**: Job postings by members
- **job_applications**: Applications from caregivers to jobs
- **appointments**: Scheduled appointments

## Security Notes

⚠️ **Important for Production**:
1. Change the `SECRET_KEY` in app.py to a random secure value
2. Set `DEBUG = False` in production
3. Use environment variables for sensitive data
4. Implement user authentication and authorization
5. Add input sanitization to prevent SQL injection
6. Use HTTPS for secure connections

## Troubleshooting

### Database Connection Error
- Check that PostgreSQL is running
- Verify database credentials in config.py
- Ensure the database exists and schema is loaded

### Module Import Errors
- Activate your virtual environment
- Run `pip install -r requirements.txt`
- Check Python version compatibility

### Port Already in Use
- Change the port in app.py: `app.run(port=8000)`
- Or kill the process using port 5000

### Template Not Found
- Ensure templates folder structure is correct
- Check file names match exactly (case-sensitive)

## Video Demonstration Requirements

When recording your video demonstration:
1. Show the application running (home page)
2. Demonstrate CRUD operations for at least 2-3 tables
3. Show the relationships between tables (e.g., creating a caregiver requires a user)
4. Display the deployed application URL
5. Briefly explain the technology stack

## Executive Summary Template

Include in your submission:
- ✅ Part 1: Database created with schema and data
- ✅ Part 2: Python queries completed
- ✅ Part 3: Web application with full CRUD operations
- Framework used: Flask
- Database: PostgreSQL
- Deployment platform: PythonAnywhere (or other)
- Challenges faced and solutions
- What works and what doesn't (be honest!)

## Contact & Support

For issues with this application, refer to:
- Flask Documentation: https://flask.palletsprojects.com/
- PostgreSQL Documentation: https://www.postgresql.org/docs/
- PythonAnywhere Help: https://help.pythonanywhere.com/

---

**Good luck with your assignment! 🎓**
