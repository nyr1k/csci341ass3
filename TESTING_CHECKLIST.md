# Testing Checklist - Online Caregivers Platform

Use this checklist to verify all CRUD operations work correctly before recording your video.

## Pre-Testing Setup

- [ ] Database is running (PostgreSQL)
- [ ] Schema loaded successfully (`psql assign3_db < schema.sql`)
- [ ] Sample data inserted (`psql assign3_db < data.sql`)
- [ ] Dependencies installed (`pip install -r requirements.txt`)
- [ ] config.py updated with correct credentials
- [ ] Application starts without errors (`python app.py`)
- [ ] Can access http://localhost:5000 in browser

---

## Users Table Testing

### CREATE
- [ ] Navigate to Users → Add New User
- [ ] Fill in all fields (try user_id: 5)
- [ ] Click "Create User"
- [ ] Verify success message appears
- [ ] Verify user appears in Users list

### READ
- [ ] Navigate to Users
- [ ] Verify all existing users are displayed
- [ ] Check that name, email, city, phone are visible

### UPDATE
- [ ] Click "Edit" on a user
- [ ] Change phone number
- [ ] Click "Update User"
- [ ] Verify success message
- [ ] Verify changes are visible in list

### DELETE
- [ ] Click "Delete" on the newly created user
- [ ] Confirm deletion in dialog
- [ ] Verify success message
- [ ] Verify user is removed from list

---

## Caregivers Table Testing

### CREATE
- [ ] Navigate to Caregivers → Add New Caregiver
- [ ] Select a user from dropdown (must exist first!)
- [ ] Fill in photo URL, gender, care type, hourly rate
- [ ] Click "Create Caregiver"
- [ ] Verify success message
- [ ] Verify caregiver appears in list with user details

### READ
- [ ] Navigate to Caregivers
- [ ] Verify JOIN query shows user name and email
- [ ] Check hourly rate is displayed correctly

### UPDATE
- [ ] Click "Edit" on a caregiver
- [ ] Change hourly rate
- [ ] Click "Update Caregiver"
- [ ] Verify changes saved

### DELETE
- [ ] Try deleting a caregiver
- [ ] Verify cascade behavior (if they have appointments/applications)

**Note:** You cannot create a caregiver without first creating a user!

---

## Members Table Testing

### CREATE
- [ ] Navigate to Members → Add New Member
- [ ] Select a user from dropdown
- [ ] Fill in house rules and dependent description
- [ ] Click "Create Member"
- [ ] Verify success message

### READ
- [ ] Navigate to Members
- [ ] Verify user details are shown via JOIN

### UPDATE
- [ ] Edit member's house rules
- [ ] Save changes
- [ ] Verify updated

### DELETE
- [ ] Try deleting a member
- [ ] Note cascade effects on addresses, jobs, appointments

---

## Addresses Table Testing

### CREATE
- [ ] Navigate to Addresses → Add New Address
- [ ] Select a member from dropdown
- [ ] Fill in house number, street, town
- [ ] Create address
- [ ] Verify success

### READ
- [ ] View all addresses
- [ ] Verify member name is shown

### UPDATE
- [ ] Edit an address
- [ ] Change street name
- [ ] Save and verify

### DELETE
- [ ] Delete an address
- [ ] Verify removed from list

**Note:** Addresses require members to exist first!

---

## Jobs Table Testing

### CREATE
- [ ] Navigate to Jobs → Post New Job
- [ ] Select a member
- [ ] Choose care type
- [ ] Enter requirements (e.g., "soft-spoken, 09:00-12:00")
- [ ] Set date posted
- [ ] Create job
- [ ] Verify success

### READ
- [ ] View all jobs
- [ ] Check requirements are displayed

### UPDATE
- [ ] Edit a job
- [ ] Change requirements
- [ ] Save changes

### DELETE
- [ ] Delete a job
- [ ] Note cascade deletion of job applications

---

## Job Applications Table Testing

### CREATE
- [ ] Navigate to Applications → Add New Application
- [ ] Select a caregiver
- [ ] Select a job
- [ ] Set date applied
- [ ] Submit application
- [ ] Verify shows in list with proper JOINs

### READ
- [ ] View all applications
- [ ] Verify shows: caregiver name, job details, member name
- [ ] Check complex JOIN query works

### DELETE
- [ ] Delete an application
- [ ] Verify composite primary key deletion works

**Note:** Cannot create application without existing caregiver and job!

---

## Appointments Table Testing

### CREATE
- [ ] Navigate to Appointments → Create New Appointment
- [ ] Select a caregiver
- [ ] Select a member
- [ ] Set date (e.g., tomorrow)
- [ ] Set time (e.g., 09:00)
- [ ] Set work hours (e.g., 3.0)
- [ ] Choose status (pending/accepted/declined)
- [ ] Create appointment
- [ ] Verify success

### READ
- [ ] View all appointments
- [ ] Check date/time formatting
- [ ] Verify status color coding works
- [ ] Confirm caregiver and member names display

### UPDATE
- [ ] Edit an appointment
- [ ] Change status from pending to accepted
- [ ] Change work hours
- [ ] Save changes
- [ ] Verify updates visible

### DELETE
- [ ] Delete an appointment
- [ ] Verify removed

---

## Relationship Testing

### Foreign Key Constraints
- [ ] Try deleting a user who is a caregiver
  - Expected: CASCADE delete (caregiver record also deleted)
- [ ] Try deleting a user who is a member with appointments
  - Expected: CASCADE delete (member, appointments deleted)
- [ ] Try creating caregiver with non-existent user_id
  - Expected: Error message

### Data Integrity
- [ ] Try creating appointment with invalid caregiver_id
  - Expected: Error or dropdown prevents it
- [ ] Try creating job application with invalid job_id
  - Expected: Error or dropdown prevents it

---

## UI/UX Testing

- [ ] Navigation bar works from all pages
- [ ] Home page displays all 7 cards
- [ ] Success messages appear in green
- [ ] Error messages appear in red
- [ ] Confirmation dialogs show for deletions
- [ ] Forms have proper labels
- [ ] Required fields are marked
- [ ] Truncated text in tables doesn't overflow
- [ ] Tables are readable and organized

---

## Error Handling Testing

- [ ] Try submitting empty form
  - Expected: HTML5 validation prevents submission
- [ ] Try creating duplicate primary key
  - Expected: Error message shown
- [ ] Try invalid email format
  - Expected: HTML5 validation error
- [ ] Try negative hourly rate
  - Expected: Database constraint violation error
- [ ] Disconnect database and try operation
  - Expected: Connection error shown, no crash

---

## Cross-Browser Testing (Optional)

- [ ] Chrome/Chromium
- [ ] Firefox
- [ ] Safari
- [ ] Edge

---

## Performance Testing

- [ ] List pages load within 2 seconds
- [ ] Forms submit without significant delay
- [ ] No console errors in browser developer tools
- [ ] Database queries complete quickly

---

## Deployment Testing (If Deployed)

- [ ] Application accessible via public URL
- [ ] All CRUD operations work on deployed version
- [ ] Database connection stable
- [ ] No CORS or security issues
- [ ] Mobile responsive design works

---

## Video Recording Checklist

Before recording:
- [ ] Clear any test data that looks messy
- [ ] Insert clean, realistic sample data
- [ ] Close unnecessary browser tabs
- [ ] Prepare what to say for each section
- [ ] Test screen recording software
- [ ] Check audio levels

During recording:
- [ ] Show home page first
- [ ] Demonstrate at least 3 CRUD operations
- [ ] Show relationships between tables
- [ ] Mention technology stack (Flask, PostgreSQL)
- [ ] Show deployed URL (if applicable)
- [ ] Keep under 10 minutes

After recording:
- [ ] Watch the video to check quality
- [ ] Verify audio is clear
- [ ] Upload to Google Drive
- [ ] Set sharing to "Anyone with link can view"
- [ ] Copy link for submission

---

## Pre-Submission Checklist

Files to include in ZIP:
- [ ] schema.sql
- [ ] data.sql (with actual data, not empty)
- [ ] app.py
- [ ] config.py
- [ ] requirements.txt
- [ ] README.md
- [ ] templates/ folder (with all subfolders and HTML files)
- [ ] Executive summary (PDF or Word)
- [ ] Text file with video link

Double-check:
- [ ] All files are latest versions
- [ ] No sensitive passwords in submitted files
- [ ] ZIP file is under Moodle size limit
- [ ] Video link is accessible (test in incognito mode)
- [ ] Executive summary has names and IDs

---

## Common Issues & Quick Fixes

**Issue:** "Template not found"  
**Fix:** Check templates folder structure, ensure correct paths

**Issue:** "User already exists as caregiver/member"  
**Fix:** Dropdown only shows available users - refresh if needed

**Issue:** "Foreign key violation"  
**Fix:** Create parent records first (user before caregiver, member before job)

**Issue:** "Port 5000 in use"  
**Fix:** Change port in app.py or kill process: `lsof -ti:5000 | xargs kill -9`

**Issue:** Forms not submitting  
**Fix:** Check browser console for errors; verify required fields filled

---

## Testing Complete! ✅

If all items are checked, you're ready to:
1. Record your video demonstration
2. Write your executive summary
3. Submit your assignment

**Good luck! 🎓**
