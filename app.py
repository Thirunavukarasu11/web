from flask import Flask, abort, render_template, request, redirect, url_for, session, flash, jsonify
from flask_cors import CORS
import os
import sqlite3
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from datetime import datetime
from dotenv import load_dotenv

app = Flask(__name__)
CORS(app)

# Set up your Flask-Mail configuration
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'thirunavukarasu110902@gmail.com'
app.config['MAIL_PASSWORD'] = 'Arasu@1109'
app.config['MAIL_DEFAULT_SENDER'] = 'dilthiru0311@gmail.com'

# Load environment variables from .env file
load_dotenv()

# Use a fixed secret key from the environment file
app.secret_key = os.getenv("SECRET_KEY", "fallback_secret_key")

# Email credentials from .env file
SMTP_USER = os.getenv("SMTP_USER")
SMTP_PASSWORD = os.getenv("SMTP_PASSWORD")
SMTP_SERVER = os.getenv("SMTP_SERVER", 'smtp.gmail.com')
SMTP_PORT = int(os.getenv("SMTP_PORT", 587))

# Dummy login details for one user (use a database for production)
USERNAME = "user@necurity.com"
PASSWORD = "password123"

# Initialize database on app start
# Connect to the database
conn = sqlite3.connect('my_database.db')

# Create a table
cursor = conn.cursor()
cursor.execute('''
    CREATE TABLE IF NOT EXISTS emails (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        email_address TEXT NOT NULL,
        rejected_flag BOOLEAN DEFAULT FALSE
    )
''')

print("Table created successfully.")

conn.close()

# Function to get a database connection
def get_db_connection():
    conn = sqlite3.connect('your_database.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def login():
    return render_template('login.html')

@app.route('/')
def index():
    # Render the template with both lists
    return render_template('template1.html', cve_list=cve_list, rejected_list=rejected_list)

@app.route('/login', methods=['POST'])
def login_post():
    username = request.form.get('email')
    password = request.form.get('password')

    if username == USERNAME and password == PASSWORD:
        session['user'] = username
        flash('Logged in successfully!', 'success')
        return redirect(url_for('dashboard'))
    else:
        flash('Invalid credentials, please try again!', 'danger')
        return redirect(url_for('login'))

@app.route('/dashboard')
def dashboard():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM emails WHERE status = 'sent'")
    sent_count = cursor.fetchone()[0]
    cursor.execute("SELECT COUNT(*) FROM emails WHERE status = 'pending'")
    pending_count = cursor.fetchone()[0]
    cursor.execute("SELECT COUNT(*) FROM emails WHERE status = 'rejected'")
    rejected_count = cursor.fetchone()[0]
    conn.close()
    
    return render_template('dashboard.html', sent_count=sent_count, pending_count=pending_count, rejected_count=rejected_count)

@app.route('/user_profile')
def user_profile():
    if 'user' not in session:
        flash('You need to log in first!', 'danger')
        return redirect(url_for('login'))
    return render_template('user_profile.html')

def send_email(recipient_email, cve_number, email_content):
    msg = MIMEMultipart()
    msg['From'] = SMTP_USER
    msg['To'] = recipient_email
    msg['Subject'] = f'Important Notification: {cve_number}'

    msg.attach(MIMEText(email_content, 'html'))

    try:
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            print("start head")
            server.login(SMTP_USER, SMTP_PASSWORD)
            print("Login successful")
            server.send_message(msg)
        print("Email sent successfully!")
    except Exception as e:
        print(f"Failed to send email: {e}")

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO sent_emails (email, date_sent) VALUES (?, ?)", 
                   (recipient_email, datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
    conn.commit()
    conn.close()

def verify_db():
    # Connect to the database
    conn = sqlite3.connect('your_database.db')
    cursor = conn.cursor()

    # Check the table structure (columns)
    cursor.execute('PRAGMA table_info(emails);')  # List the columns in the 'emails' table
    table_info = cursor.fetchall()

    print("Table Structure for 'emails' Table:")
    for column in table_info:
        print(column)

    # Check some sample data in the 'emails' table
    cursor.execute('SELECT * FROM emails LIMIT 5;')  # Fetch first 5 rows from the 'emails' table
    data = cursor.fetchall()

    print("\nSample Data from 'emails' Table:")
    for row in data:
        print(row)

    conn.close()

# Call the function to verify the database
verify_db()

@app.route('/send_email', methods=['POST'])
def send_email_api():
    try:
        # Debugging: Log the incoming request
        print("Received request to send email")
        data = request.json
        print("Request Data:", data)

        recipient_email = data['email']
        cve_number = data['cve_number']
        email_content = data['content']

        print("Preparing to send email to:", recipient_email)

        # SMTP configuration
        msg = MIMEMultipart('alternative')
        msg['From'] = SMTP_USER
        msg['To'] = recipient_email
        msg['Subject'] = f"New CVE Update: {cve_number}"
        msg.attach(MIMEText(email_content, 'html'))

        # Sending the email
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(SMTP_USER, SMTP_PASSWORD)
            server.send_message(msg)

        # Logging to the database
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO sent_emails (email, date_sent) VALUES (?, ?)",
            (recipient_email, datetime.now().strftime('%Y-%m-%d %H:%M:%S')),
        )
        conn.commit()
        conn.close()

        print("Email sent successfully!")
        return jsonify({"message": f"Email sent successfully to {recipient_email}!"}), 200

    except Exception as e:
        print("Error:", str(e))
        return jsonify({"error": str(e)}), 500

def verify_db():
    # Connect to the database
    conn = sqlite3.connect('your_database.db')  # Ensure the database file is correct
    cursor = conn.cursor()
    # Optionally, you can check if the tables exist, or create them if they do not
    cursor.execute('SELECT name FROM sqlite_master WHERE type="table" AND name="emails";')
    table_exists = cursor.fetchone()
    if table_exists:
        print("Table 'emails' exists")
    else:
        print("Table 'emails' does not exist")
    conn.close()

def insert_sent_email(recipient_email):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO sent_emails (email, date_sent) VALUES (?, ?)", 
                   (recipient_email, datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
    conn.commit()
    conn.close()

def add_rejected_flag_column():
    conn = sqlite3.connect('your_database.db')
    cursor = conn.cursor()
    cursor.execute("ALTER TABLE emails ADD COLUMN rejected_flag INTEGER DEFAULT 0")  # 0 means FALSE
    conn.commit()
    conn.close()
    # This function sends the actual email (use your SMTP logic here)
    

@app.route('/templates')
def templates():
    return render_template('templates.html')

@app.route('/logout')
def logout():
    session.pop('user', None)
    flash('You have been logged out successfully.', 'success')
    return redirect(url_for('login'))

@app.route('/send_approval_email', methods=['POST'])
def send_approval_email():
    try:
        data = request.get_json()
        
        recipient_email = data.get('recipient_email')
        cve_number = data.get('cve_number')
        email_content = data.get('email_content')

        if not recipient_email or not email_content:
            raise ValueError("Recipient email or email content is missing")
        
        # Call function to send email
        send_email(recipient_email, cve_number, email_content)
        
        return jsonify({"success": True})
    
    except ValueError as ve:
        return jsonify({"success": False, "error": str(ve)}), 400
    except Exception as e:
        return jsonify({"success": False, "error": f"An error occurred: {str(e)}"}), 500
    
# Function to reject CVE (with update to rejected_flag in the database)
@app.route('/reject_cve', methods=['POST'])
def reject_cve():
    cve_to_reject = request.form.get('cve')  # Get the CVE from the form data
    print(f"CVE to reject: {cve_to_reject}")  # Debugging output

    if cve_to_reject:
        try:
            # Connect to the database
            conn = sqlite3.connect('my_database.db')
            cursor = conn.cursor()

            # Update the rejected_flag for the given CVE
            cursor.execute("UPDATE emails SET rejected_flag = 1 WHERE email_address = ?", (cve_to_reject,))
            conn.commit()
            conn.close()

            flash('CVE rejected successfully!', 'success')
        except Exception as e:
            flash(f"Error rejecting CVE: {e}", 'danger')

    return redirect(url_for('index'))  # Redirect to the main page after rejection

# Function to render the rejected CVEs in the rejected list
@app.route('/rejected')
def rejected_list():
    conn = sqlite3.connect('my_database.db')
    cursor = conn.cursor()

    # Query for rejected emails (rejected_flag = 1)
    cursor.execute("SELECT * FROM emails WHERE rejected_flag = 1")
    rows = cursor.fetchall()

    conn.close()

    # If no rejected entries found, show a message
    if not rows:
        flash('No rejected entries found.', 'info')
    
    return render_template('rejected_list.html', rows=rows)

@app.route('/choose_template', methods=['POST'])
def choose_template():
    selected_template = request.form.get('template')
    if selected_template:
        flash(f"You have selected {selected_template}!", 'success')
        return redirect(url_for('dashboard'))
    else:
        flash('Please select a template!', 'danger')
        return redirect(url_for('templates'))

@app.route('/email_template', methods=['POST'])
def email_template():
    subject = request.form['subject']
    cve_number = request.form['cve_number']
    severity = request.form['severity']
    description = request.form['description']
    
    return render_template('template1.html', subject=subject, cve_number=cve_number, severity=severity, description=description)

@app.route('/email_sent')
def email_sent():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM sent_emails")
    sent_emails = cursor.fetchall()
    conn.close()

    return render_template('email_sent.html', sent_emails=sent_emails)

@app.route('/approval_list')
def approval_list():
    # Your logic to fetch and display the approval list
    return render_template('approval_list.html')


@app.route('/template1')
def template1():
    return render_template('template1.html')

@app.route('/template2')
def template2():
    return render_template('template2.html')

@app.route('/template3')
def template3():
    return render_template('template3.html')

@app.route('/user-management')
def user_management():
    return render_template('user_management.html')  # Replace with your actual template

if __name__ == "__main__":
    app.run(debug=True)