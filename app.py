"""
Online Caregivers Platform - Flask Web Application
CSCI 341 - Database Management Systems - Assignment 3, Part 3
"""

from flask import Flask, render_template, request, redirect, url_for, flash
import psycopg2
from psycopg2.extras import RealDictCursor
from datetime import datetime, date
import os

# Import configuration
try:
    from config import DB_CONFIG, SECRET_KEY, DEBUG
except ImportError:
    # Fallback configuration if config.py is not found
    DB_CONFIG = {
        'dbname': 'assign3_db',
        'user': 'nyrik',
        'password': 'your_password',
        'host': 'localhost',
        'port': '5432'
    }
    SECRET_KEY = 'your-secret-key-change-this-in-production'
    DEBUG = True

# Override with environment variables for deployment (Render, Heroku, etc.)
if os.environ.get('DATABASE_URL'):
    # DATABASE_URL is handled directly in get_db_connection
    pass
elif os.environ.get('DB_HOST'):
    # Use individual environment variables
    DB_CONFIG = {
        'dbname': os.environ.get('DB_NAME', DB_CONFIG.get('dbname')),
        'user': os.environ.get('DB_USER', DB_CONFIG.get('user')),
        'password': os.environ.get('DB_PASSWORD', DB_CONFIG.get('password')),
        'host': os.environ.get('DB_HOST', DB_CONFIG.get('host')),
        'port': os.environ.get('DB_PORT', DB_CONFIG.get('port', '5432'))
    }

if os.environ.get('SECRET_KEY'):
    SECRET_KEY = os.environ.get('SECRET_KEY')

app = Flask(__name__)
app.secret_key = SECRET_KEY

def get_db_connection():
    """Create and return a database connection"""
    if os.environ.get('DATABASE_URL'):
        url = os.environ.get('DATABASE_URL')
        if url.startswith('postgres://'):
            url = url.replace('postgres://', 'postgresql://', 1)
        return psycopg2.connect(url)
    conn = psycopg2.connect(**DB_CONFIG)
    return conn


# ============================================================================
# HOME PAGE
# ============================================================================

@app.route('/')
def index():
    """Home page with navigation to all tables"""
    return render_template('index.html')


# ============================================================================
# USERS CRUD OPERATIONS
# ============================================================================

@app.route('/users')
def users_list():
    """Display all users"""
    conn = get_db_connection()
    cur = conn.cursor(cursor_factory=RealDictCursor)
    cur.execute('SELECT * FROM users ORDER BY user_id')
    users = cur.fetchall()
    cur.close()
    conn.close()
    return render_template('users/list.html', users=users)


@app.route('/users/create', methods=['GET', 'POST'])
def users_create():
    """Create a new user"""
    if request.method == 'POST':
        conn = get_db_connection()
        cur = conn.cursor()
        try:
            cur.execute('''
                INSERT INTO users (user_id, u_email, u_name, u_surname, u_city, 
                                   u_phone_number, u_profile_descr, u_password)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            ''', (
                request.form['user_id'],
                request.form['email'],
                request.form['name'],
                request.form['surname'],
                request.form['city'],
                request.form['phone'],
                request.form['profile_descr'],
                request.form['password']
            ))
            conn.commit()
            flash('User created successfully!', 'success')
            return redirect(url_for('users_list'))
        except Exception as e:
            conn.rollback()
            flash(f'Error creating user: {str(e)}', 'error')
        finally:
            cur.close()
            conn.close()
    
    return render_template('users/create.html')


@app.route('/users/edit/<int:id>', methods=['GET', 'POST'])
def users_edit(id):
    """Edit an existing user"""
    conn = get_db_connection()
    cur = conn.cursor(cursor_factory=RealDictCursor)
    
    if request.method == 'POST':
        try:
            cur.execute('''
                UPDATE users 
                SET u_email = %s, u_name = %s, u_surname = %s, u_city = %s, 
                    u_phone_number = %s, u_profile_descr = %s, u_password = %s
                WHERE user_id = %s
            ''', (
                request.form['email'],
                request.form['name'],
                request.form['surname'],
                request.form['city'],
                request.form['phone'],
                request.form['profile_descr'],
                request.form['password'],
                id
            ))
            conn.commit()
            flash('User updated successfully!', 'success')
            return redirect(url_for('users_list'))
        except Exception as e:
            conn.rollback()
            flash(f'Error updating user: {str(e)}', 'error')
        finally:
            cur.close()
            conn.close()
    
    cur.execute('SELECT * FROM users WHERE user_id = %s', (id,))
    user = cur.fetchone()
    cur.close()
    conn.close()
    
    if user is None:
        flash('User not found!', 'error')
        return redirect(url_for('users_list'))
    
    return render_template('users/edit.html', user=user)


@app.route('/users/delete/<int:id>', methods=['POST'])
def users_delete(id):
    """Delete a user"""
    conn = get_db_connection()
    cur = conn.cursor()
    try:
        cur.execute('DELETE FROM users WHERE user_id = %s', (id,))
        conn.commit()
        flash('User deleted successfully!', 'success')
    except Exception as e:
        conn.rollback()
        flash(f'Error deleting user: {str(e)}', 'error')
    finally:
        cur.close()
        conn.close()
    
    return redirect(url_for('users_list'))


# ============================================================================
# CAREGIVERS CRUD OPERATIONS
# ============================================================================

@app.route('/caregivers')
def caregivers_list():
    """Display all caregivers with user info"""
    conn = get_db_connection()
    cur = conn.cursor(cursor_factory=RealDictCursor)
    cur.execute('''
        SELECT c.*, u.u_name, u.u_surname, u.u_email, u.u_city
        FROM caregivers c
        JOIN users u ON c.caregiver_id = u.user_id
        ORDER BY c.caregiver_id
    ''')
    caregivers = cur.fetchall()
    cur.close()
    conn.close()
    return render_template('caregivers/list.html', caregivers=caregivers)


@app.route('/caregivers/create', methods=['GET', 'POST'])
def caregivers_create():
    """Create a new caregiver"""
    conn = get_db_connection()
    cur = conn.cursor(cursor_factory=RealDictCursor)
    
    if request.method == 'POST':
        try:
            cur.execute('''
                INSERT INTO caregivers (caregiver_id, c_photo, c_gender, c_care_type, c_hourly_rate)
                VALUES (%s, %s, %s, %s, %s)
            ''', (
                request.form['caregiver_id'],
                request.form['photo'],
                request.form['gender'],
                request.form['care_type'],
                request.form['hourly_rate']
            ))
            conn.commit()
            flash('Caregiver created successfully!', 'success')
            return redirect(url_for('caregivers_list'))
        except Exception as e:
            conn.rollback()
            flash(f'Error creating caregiver: {str(e)}', 'error')
    
    # Get list of users who are not already caregivers
    cur.execute('''
        SELECT user_id, u_name, u_surname 
        FROM users 
        WHERE user_id NOT IN (SELECT caregiver_id FROM caregivers)
        ORDER BY user_id
    ''')
    available_users = cur.fetchall()
    cur.close()
    conn.close()
    
    return render_template('caregivers/create.html', users=available_users)


@app.route('/caregivers/edit/<int:id>', methods=['GET', 'POST'])
def caregivers_edit(id):
    """Edit an existing caregiver"""
    conn = get_db_connection()
    cur = conn.cursor(cursor_factory=RealDictCursor)
    
    if request.method == 'POST':
        try:
            cur.execute('''
                UPDATE caregivers 
                SET c_photo = %s, c_gender = %s, c_care_type = %s, c_hourly_rate = %s
                WHERE caregiver_id = %s
            ''', (
                request.form['photo'],
                request.form['gender'],
                request.form['care_type'],
                request.form['hourly_rate'],
                id
            ))
            conn.commit()
            flash('Caregiver updated successfully!', 'success')
            return redirect(url_for('caregivers_list'))
        except Exception as e:
            conn.rollback()
            flash(f'Error updating caregiver: {str(e)}', 'error')
    
    cur.execute('''
        SELECT c.*, u.u_name, u.u_surname
        FROM caregivers c
        JOIN users u ON c.caregiver_id = u.user_id
        WHERE c.caregiver_id = %s
    ''', (id,))
    caregiver = cur.fetchone()
    cur.close()
    conn.close()
    
    if caregiver is None:
        flash('Caregiver not found!', 'error')
        return redirect(url_for('caregivers_list'))
    
    return render_template('caregivers/edit.html', caregiver=caregiver)


@app.route('/caregivers/delete/<int:id>', methods=['POST'])
def caregivers_delete(id):
    """Delete a caregiver"""
    conn = get_db_connection()
    cur = conn.cursor()
    try:
        cur.execute('DELETE FROM caregivers WHERE caregiver_id = %s', (id,))
        conn.commit()
        flash('Caregiver deleted successfully!', 'success')
    except Exception as e:
        conn.rollback()
        flash(f'Error deleting caregiver: {str(e)}', 'error')
    finally:
        cur.close()
        conn.close()
    
    return redirect(url_for('caregivers_list'))


# ============================================================================
# MEMBERS CRUD OPERATIONS
# ============================================================================

@app.route('/members')
def members_list():
    """Display all members with user info"""
    conn = get_db_connection()
    cur = conn.cursor(cursor_factory=RealDictCursor)
    cur.execute('''
        SELECT m.*, u.u_name, u.u_surname, u.u_email, u.u_city
        FROM members m
        JOIN users u ON m.member_id = u.user_id
        ORDER BY m.member_id
    ''')
    members = cur.fetchall()
    cur.close()
    conn.close()
    return render_template('members/list.html', members=members)


@app.route('/members/create', methods=['GET', 'POST'])
def members_create():
    """Create a new member"""
    conn = get_db_connection()
    cur = conn.cursor(cursor_factory=RealDictCursor)
    
    if request.method == 'POST':
        try:
            cur.execute('''
                INSERT INTO members (member_id, m_house_rules, m_depend_descr)
                VALUES (%s, %s, %s)
            ''', (
                request.form['member_id'],
                request.form['house_rules'],
                request.form['depend_descr']
            ))
            conn.commit()
            flash('Member created successfully!', 'success')
            return redirect(url_for('members_list'))
        except Exception as e:
            conn.rollback()
            flash(f'Error creating member: {str(e)}', 'error')
    
    # Get list of users who are not already members
    cur.execute('''
        SELECT user_id, u_name, u_surname 
        FROM users 
        WHERE user_id NOT IN (SELECT member_id FROM members)
        ORDER BY user_id
    ''')
    available_users = cur.fetchall()
    cur.close()
    conn.close()
    
    return render_template('members/create.html', users=available_users)


@app.route('/members/edit/<int:id>', methods=['GET', 'POST'])
def members_edit(id):
    """Edit an existing member"""
    conn = get_db_connection()
    cur = conn.cursor(cursor_factory=RealDictCursor)
    
    if request.method == 'POST':
        try:
            cur.execute('''
                UPDATE members 
                SET m_house_rules = %s, m_depend_descr = %s
                WHERE member_id = %s
            ''', (
                request.form['house_rules'],
                request.form['depend_descr'],
                id
            ))
            conn.commit()
            flash('Member updated successfully!', 'success')
            return redirect(url_for('members_list'))
        except Exception as e:
            conn.rollback()
            flash(f'Error updating member: {str(e)}', 'error')
    
    cur.execute('''
        SELECT m.*, u.u_name, u.u_surname
        FROM members m
        JOIN users u ON m.member_id = u.user_id
        WHERE m.member_id = %s
    ''', (id,))
    member = cur.fetchone()
    cur.close()
    conn.close()
    
    if member is None:
        flash('Member not found!', 'error')
        return redirect(url_for('members_list'))
    
    return render_template('members/edit.html', member=member)


@app.route('/members/delete/<int:id>', methods=['POST'])
def members_delete(id):
    """Delete a member"""
    conn = get_db_connection()
    cur = conn.cursor()
    try:
        cur.execute('DELETE FROM members WHERE member_id = %s', (id,))
        conn.commit()
        flash('Member deleted successfully!', 'success')
    except Exception as e:
        conn.rollback()
        flash(f'Error deleting member: {str(e)}', 'error')
    finally:
        cur.close()
        conn.close()
    
    return redirect(url_for('members_list'))


# ============================================================================
# ADDRESSES CRUD OPERATIONS
# ============================================================================

@app.route('/addresses')
def addresses_list():
    """Display all addresses"""
    conn = get_db_connection()
    cur = conn.cursor(cursor_factory=RealDictCursor)
    cur.execute('''
        SELECT a.*, u.u_name, u.u_surname
        FROM addresses a
        JOIN users u ON a.a_member_id = u.user_id
        ORDER BY a.a_member_id
    ''')
    addresses = cur.fetchall()
    cur.close()
    conn.close()
    return render_template('addresses/list.html', addresses=addresses)


@app.route('/addresses/create', methods=['GET', 'POST'])
def addresses_create():
    """Create a new address"""
    conn = get_db_connection()
    cur = conn.cursor(cursor_factory=RealDictCursor)
    
    if request.method == 'POST':
        try:
            cur.execute('''
                INSERT INTO addresses (a_member_id, a_house_number, a_street, a_town)
                VALUES (%s, %s, %s, %s)
            ''', (
                request.form['member_id'],
                request.form['house_number'],
                request.form['street'],
                request.form['town']
            ))
            conn.commit()
            flash('Address created successfully!', 'success')
            return redirect(url_for('addresses_list'))
        except Exception as e:
            conn.rollback()
            flash(f'Error creating address: {str(e)}', 'error')
    
    # Get list of members
    cur.execute('''
        SELECT m.member_id, u.u_name, u.u_surname
        FROM members m
        JOIN users u ON m.member_id = u.user_id
        ORDER BY m.member_id
    ''')
    members = cur.fetchall()
    cur.close()
    conn.close()
    
    return render_template('addresses/create.html', members=members)


@app.route('/addresses/edit/<int:member_id>', methods=['GET', 'POST'])
def addresses_edit(member_id):
    """Edit an existing address"""
    conn = get_db_connection()
    cur = conn.cursor(cursor_factory=RealDictCursor)
    
    if request.method == 'POST':
        try:
            cur.execute('''
                UPDATE addresses 
                SET a_house_number = %s, a_street = %s, a_town = %s
                WHERE a_member_id = %s
            ''', (
                request.form['house_number'],
                request.form['street'],
                request.form['town'],
                member_id
            ))
            conn.commit()
            flash('Address updated successfully!', 'success')
            return redirect(url_for('addresses_list'))
        except Exception as e:
            conn.rollback()
            flash(f'Error updating address: {str(e)}', 'error')
    
    cur.execute('''
        SELECT a.*, u.u_name, u.u_surname
        FROM addresses a
        JOIN users u ON a.a_member_id = u.user_id
        WHERE a.a_member_id = %s
    ''', (member_id,))
    address = cur.fetchone()
    cur.close()
    conn.close()
    
    if address is None:
        flash('Address not found!', 'error')
        return redirect(url_for('addresses_list'))
    
    return render_template('addresses/edit.html', address=address)


@app.route('/addresses/delete/<int:member_id>', methods=['POST'])
def addresses_delete(member_id):
    """Delete an address"""
    conn = get_db_connection()
    cur = conn.cursor()
    try:
        cur.execute('DELETE FROM addresses WHERE a_member_id = %s', (member_id,))
        conn.commit()
        flash('Address deleted successfully!', 'success')
    except Exception as e:
        conn.rollback()
        flash(f'Error deleting address: {str(e)}', 'error')
    finally:
        cur.close()
        conn.close()
    
    return redirect(url_for('addresses_list'))


# ============================================================================
# JOBS CRUD OPERATIONS
# ============================================================================

@app.route('/jobs')
def jobs_list():
    """Display all jobs"""
    conn = get_db_connection()
    cur = conn.cursor(cursor_factory=RealDictCursor)
    cur.execute('''
        SELECT j.*, u.u_name, u.u_surname
        FROM jobs j
        JOIN users u ON j.j_member_id = u.user_id
        ORDER BY j.job_id DESC
    ''')
    jobs = cur.fetchall()
    cur.close()
    conn.close()
    return render_template('jobs/list.html', jobs=jobs)


@app.route('/jobs/create', methods=['GET', 'POST'])
def jobs_create():
    """Create a new job"""
    conn = get_db_connection()
    cur = conn.cursor(cursor_factory=RealDictCursor)
    
    if request.method == 'POST':
        try:
            cur.execute('''
                INSERT INTO jobs (job_id, j_member_id, j_care_type, j_reqs, j_date_post)
                VALUES (%s, %s, %s, %s, %s)
            ''', (
                request.form['job_id'],
                request.form['member_id'],
                request.form['care_type'],
                request.form['reqs'],
                request.form['date_post']
            ))
            conn.commit()
            flash('Job created successfully!', 'success')
            return redirect(url_for('jobs_list'))
        except Exception as e:
            conn.rollback()
            flash(f'Error creating job: {str(e)}', 'error')
    
    # Get list of members
    cur.execute('''
        SELECT m.member_id, u.u_name, u.u_surname
        FROM members m
        JOIN users u ON m.member_id = u.user_id
        ORDER BY m.member_id
    ''')
    members = cur.fetchall()
    cur.close()
    conn.close()
    
    return render_template('jobs/create.html', members=members)


@app.route('/jobs/edit/<int:id>', methods=['GET', 'POST'])
def jobs_edit(id):
    """Edit an existing job"""
    conn = get_db_connection()
    cur = conn.cursor(cursor_factory=RealDictCursor)
    
    if request.method == 'POST':
        try:
            cur.execute('''
                UPDATE jobs 
                SET j_member_id = %s, j_care_type = %s, j_reqs = %s, j_date_post = %s
                WHERE job_id = %s
            ''', (
                request.form['member_id'],
                request.form['care_type'],
                request.form['reqs'],
                request.form['date_post'],
                id
            ))
            conn.commit()
            flash('Job updated successfully!', 'success')
            return redirect(url_for('jobs_list'))
        except Exception as e:
            conn.rollback()
            flash(f'Error updating job: {str(e)}', 'error')
    
    cur.execute('SELECT * FROM jobs WHERE job_id = %s', (id,))
    job = cur.fetchone()
    
    cur.execute('''
        SELECT m.member_id, u.u_name, u.u_surname
        FROM members m
        JOIN users u ON m.member_id = u.user_id
        ORDER BY m.member_id
    ''')
    members = cur.fetchall()
    
    cur.close()
    conn.close()
    
    if job is None:
        flash('Job not found!', 'error')
        return redirect(url_for('jobs_list'))
    
    return render_template('jobs/edit.html', job=job, members=members)


@app.route('/jobs/delete/<int:id>', methods=['POST'])
def jobs_delete(id):
    """Delete a job"""
    conn = get_db_connection()
    cur = conn.cursor()
    try:
        cur.execute('DELETE FROM jobs WHERE job_id = %s', (id,))
        conn.commit()
        flash('Job deleted successfully!', 'success')
    except Exception as e:
        conn.rollback()
        flash(f'Error deleting job: {str(e)}', 'error')
    finally:
        cur.close()
        conn.close()
    
    return redirect(url_for('jobs_list'))


# ============================================================================
# JOB APPLICATIONS CRUD OPERATIONS
# ============================================================================

@app.route('/job_applications')
def job_applications_list():
    """Display all job applications"""
    conn = get_db_connection()
    cur = conn.cursor(cursor_factory=RealDictCursor)
    cur.execute('''
        SELECT ja.*, 
               uc.u_name as caregiver_name, uc.u_surname as caregiver_surname,
               j.j_care_type, j.j_reqs,
               um.u_name as member_name, um.u_surname as member_surname
        FROM job_applications ja
        JOIN caregivers c ON ja.ja_caregiver_id = c.caregiver_id
        JOIN users uc ON c.caregiver_id = uc.user_id
        JOIN jobs j ON ja.ja_job_id = j.job_id
        JOIN members m ON j.j_member_id = m.member_id
        JOIN users um ON m.member_id = um.user_id
        ORDER BY ja.ja_date_applied DESC
    ''')
    applications = cur.fetchall()
    cur.close()
    conn.close()
    return render_template('job_applications/list.html', applications=applications)


@app.route('/job_applications/create', methods=['GET', 'POST'])
def job_applications_create():
    """Create a new job application"""
    conn = get_db_connection()
    cur = conn.cursor(cursor_factory=RealDictCursor)
    
    if request.method == 'POST':
        try:
            cur.execute('''
                INSERT INTO job_applications (ja_caregiver_id, ja_job_id, ja_date_applied)
                VALUES (%s, %s, %s)
            ''', (
                request.form['caregiver_id'],
                request.form['job_id'],
                request.form['date_applied']
            ))
            conn.commit()
            flash('Job application created successfully!', 'success')
            return redirect(url_for('job_applications_list'))
        except Exception as e:
            conn.rollback()
            flash(f'Error creating job application: {str(e)}', 'error')
    
    # Get list of caregivers
    cur.execute('''
        SELECT c.caregiver_id, u.u_name, u.u_surname, c.c_care_type
        FROM caregivers c
        JOIN users u ON c.caregiver_id = u.user_id
        ORDER BY c.caregiver_id
    ''')
    caregivers = cur.fetchall()
    
    # Get list of jobs
    cur.execute('''
        SELECT j.job_id, j.j_care_type, j.j_reqs, u.u_name, u.u_surname
        FROM jobs j
        JOIN members m ON j.j_member_id = m.member_id
        JOIN users u ON m.member_id = u.user_id
        ORDER BY j.job_id DESC
    ''')
    jobs = cur.fetchall()
    
    cur.close()
    conn.close()
    
    return render_template('job_applications/create.html', caregivers=caregivers, jobs=jobs)


@app.route('/job_applications/delete/<int:caregiver_id>/<int:job_id>', methods=['POST'])
def job_applications_delete(caregiver_id, job_id):
    """Delete a job application"""
    conn = get_db_connection()
    cur = conn.cursor()
    try:
        cur.execute('''
            DELETE FROM job_applications 
            WHERE ja_caregiver_id = %s AND ja_job_id = %s
        ''', (caregiver_id, job_id))
        conn.commit()
        flash('Job application deleted successfully!', 'success')
    except Exception as e:
        conn.rollback()
        flash(f'Error deleting job application: {str(e)}', 'error')
    finally:
        cur.close()
        conn.close()
    
    return redirect(url_for('job_applications_list'))


# ============================================================================
# APPOINTMENTS CRUD OPERATIONS
# ============================================================================

@app.route('/appointments')
def appointments_list():
    """Display all appointments"""
    conn = get_db_connection()
    cur = conn.cursor(cursor_factory=RealDictCursor)
    cur.execute('''
        SELECT a.*, 
               uc.u_name as caregiver_name, uc.u_surname as caregiver_surname,
               um.u_name as member_name, um.u_surname as member_surname
        FROM appointments a
        JOIN caregivers c ON a.ap_caregiver_id = c.caregiver_id
        JOIN users uc ON c.caregiver_id = uc.user_id
        JOIN members m ON a.ap_member_id = m.member_id
        JOIN users um ON m.member_id = um.user_id
        ORDER BY a.ap_date DESC, a.ap_time DESC
    ''')
    appointments = cur.fetchall()
    cur.close()
    conn.close()
    return render_template('appointments/list.html', appointments=appointments)


@app.route('/appointments/create', methods=['GET', 'POST'])
def appointments_create():
    """Create a new appointment"""
    conn = get_db_connection()
    cur = conn.cursor(cursor_factory=RealDictCursor)
    
    if request.method == 'POST':
        try:
            cur.execute('''
                INSERT INTO appointments (appointment_id, ap_caregiver_id, ap_member_id, 
                                          ap_date, ap_time, ap_work_hours, ap_status)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            ''', (
                request.form['appointment_id'],
                request.form['caregiver_id'],
                request.form['member_id'],
                request.form['date'],
                request.form['time'],
                request.form['work_hours'],
                request.form['status']
            ))
            conn.commit()
            flash('Appointment created successfully!', 'success')
            return redirect(url_for('appointments_list'))
        except Exception as e:
            conn.rollback()
            flash(f'Error creating appointment: {str(e)}', 'error')
    
    # Get list of caregivers
    cur.execute('''
        SELECT c.caregiver_id, u.u_name, u.u_surname, c.c_care_type
        FROM caregivers c
        JOIN users u ON c.caregiver_id = u.user_id
        ORDER BY c.caregiver_id
    ''')
    caregivers = cur.fetchall()
    
    # Get list of members
    cur.execute('''
        SELECT m.member_id, u.u_name, u.u_surname
        FROM members m
        JOIN users u ON m.member_id = u.user_id
        ORDER BY m.member_id
    ''')
    members = cur.fetchall()
    
    cur.close()
    conn.close()
    
    return render_template('appointments/create.html', caregivers=caregivers, members=members)


@app.route('/appointments/edit/<int:id>', methods=['GET', 'POST'])
def appointments_edit(id):
    """Edit an existing appointment"""
    conn = get_db_connection()
    cur = conn.cursor(cursor_factory=RealDictCursor)
    
    if request.method == 'POST':
        try:
            cur.execute('''
                UPDATE appointments 
                SET ap_caregiver_id = %s, ap_member_id = %s, ap_date = %s, 
                    ap_time = %s, ap_work_hours = %s, ap_status = %s
                WHERE appointment_id = %s
            ''', (
                request.form['caregiver_id'],
                request.form['member_id'],
                request.form['date'],
                request.form['time'],
                request.form['work_hours'],
                request.form['status'],
                id
            ))
            conn.commit()
            flash('Appointment updated successfully!', 'success')
            return redirect(url_for('appointments_list'))
        except Exception as e:
            conn.rollback()
            flash(f'Error updating appointment: {str(e)}', 'error')
    
    cur.execute('SELECT * FROM appointments WHERE appointment_id = %s', (id,))
    appointment = cur.fetchone()
    
    # Get list of caregivers
    cur.execute('''
        SELECT c.caregiver_id, u.u_name, u.u_surname, c.c_care_type
        FROM caregivers c
        JOIN users u ON c.caregiver_id = u.user_id
        ORDER BY c.caregiver_id
    ''')
    caregivers = cur.fetchall()
    
    # Get list of members
    cur.execute('''
        SELECT m.member_id, u.u_name, u.u_surname
        FROM members m
        JOIN users u ON m.member_id = u.user_id
        ORDER BY m.member_id
    ''')
    members = cur.fetchall()
    
    cur.close()
    conn.close()
    
    if appointment is None:
        flash('Appointment not found!', 'error')
        return redirect(url_for('appointments_list'))
    
    return render_template('appointments/edit.html', appointment=appointment, 
                         caregivers=caregivers, members=members)


@app.route('/appointments/delete/<int:id>', methods=['POST'])
def appointments_delete(id):
    """Delete an appointment"""
    conn = get_db_connection()
    cur = conn.cursor()
    try:
        cur.execute('DELETE FROM appointments WHERE appointment_id = %s', (id,))
        conn.commit()
        flash('Appointment deleted successfully!', 'success')
    except Exception as e:
        conn.rollback()
        flash(f'Error deleting appointment: {str(e)}', 'error')
    finally:
        cur.close()
        conn.close()
    
    return redirect(url_for('appointments_list'))


# ============================================================================
# RUN APPLICATION
# ============================================================================

if __name__ == '__main__':
    app.run(debug=DEBUG, host='0.0.0.0', port=5000)
