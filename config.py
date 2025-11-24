"""
Configuration file for the Online Caregivers Platform
Update these settings according to your database setup
"""

# Database Configuration
DB_CONFIG = {
    'dbname': 'assign3_db',      # Your database name
    'user': 'nyrik',              # Your PostgreSQL username
    # For local development with peer authentication, don't specify host/port
    # This uses Unix socket connection instead of TCP
}

# Flask Configuration
SECRET_KEY = 'your-secret-key-change-this-in-production'
DEBUG = True

# For PythonAnywhere deployment, update the configuration as follows:
# DB_CONFIG = {
#     'dbname': 'your_pythonanywhere_db_name',
#     'user': 'your_pythonanywhere_username',
#     'password': 'your_pythonanywhere_db_password',
#     'host': 'your-username.postgres.pythonanywhere-services.com',
#     'port': '10000'  # or the port provided by PythonAnywhere
# }
