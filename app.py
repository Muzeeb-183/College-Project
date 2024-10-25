from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify
from flask_session import Session  # Handles user sessions
from flask_sqlalchemy import SQLAlchemy  # Manages SQLite database interactions
from werkzeug.security import generate_password_hash, check_password_hash  # For password hashing
import os  # For file path manipulation
from werkzeug.utils import secure_filename
import sqlite3
from datetime import datetime

# Set up the Flask application
app = Flask(__name__)

# Set up session configuration to store data in the filesystem (for server-side session management)
app.config["SESSION_PERMANENT"] = False  # Sessions are temporary (reset when the browser closes)
app.config["SESSION_TYPE"] = "filesystem"  # Session data will be saved in the filesystem

# Configure the database connection (SQLite in this case) and disable unnecessary tracking of changes
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'  # Set up SQLite to store user data
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Disable modification tracking to save resources

# Define the upload folder and add it to app.config
app.config['UPLOAD_FOLDER'] = os.path.join('instance')  # Directory where uploaded files will be saved
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)  # Create the upload folder if it doesn't exist

UPLOAD_FOLDER = 'uploads/'
ALLOWED_EXTENSIONS = {'pdf', 'png', 'jpg', 'jpeg', 'gif'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# Check for allowed file types
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
# Initialize session and database components
Session(app)  # Initialize session management
db = SQLAlchemy(app)  # Initialize database connection

# Continue with the rest of your application code...


# Define a User model (represents the structure of the "users" table in the database)
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)  # The unique user ID (primary key)
    email = db.Column(db.String(120), unique=True, nullable=False)  # User's email address (must be unique)
    password_hash = db.Column(db.String(200), nullable=False)  # Hashed password

    def __repr__(self):
        return f'<User {self.email}>'

class Upload(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    regulation = db.Column(db.String, nullable=False)
    semester = db.Column(db.String, nullable=False)
    subject = db.Column(db.String, nullable=False)
    filename = db.Column(db.String, nullable=False)
    file = db.Column(db.LargeBinary, nullable=False)  # Store file as BLOB
    uploaded_at = db.Column(db.DateTime, default=db.func.current_timestamp())

    def __repr__(self):
        return f'<Upload {self.filename}>'

# Create the database tables if they don't already exist
with app.app_context():
    db.create_all()  # Create all tables based on the defined models

# Function to prevent browser caching (useful for security reasons)
@app.after_request
def after_request(response):
    """Ensure that browser doesn't cache responses"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"  # Instruct browser not to cache
    response.headers["Expires"] = 0  # Immediately expire the response
    response.headers["Pragma"] = "no-cache"  # Disable caching
    return response

# Home route that renders the homepage (index.html)

# File upload route for handling chapter-wise PDFs and images
# Route to handle file uploads and save data to the database
@app.route('/upload', methods=['POST'])
def upload_file():
    # Retrieve regulation, semester, and subject from the session
    regulation = session.get('regulation')
    semester = session.get('semester')
    subject = session.get('subject')

    # Validate required values are not None
    if not (regulation and semester and subject):
        flash("Missing session data for regulation, semester, or subject.")
        return '', 400  # Return a 400 status if there's an issue

    # Retrieve the uploaded file
    file = request.files.get('fileInput')
    if not file:
        flash("No file uploaded.")
        return '', 400  # Return a 400 status if no file is uploaded

    # Save file and other details in the database
    file_content = file.read()
    uploaded_at = datetime.now()

    conn = sqlite3.connect('instance/users.db')
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO upload (regulation, semester, subject, filename, uploaded_at, file) VALUES (?, ?, ?, ?, ?, ?) ",
        (regulation, semester, subject, file.filename, uploaded_at, file_content)
    )
    conn.commit()
    conn.close()

    return '', 200  # Return a 200 status for successful uploads



@app.route("/subjectsInside/<regulation>/<semester>/<subject>", methods=['GET'])
def subjectsInside(regulation, semester, subject):
    # Store the values in session for later use in upload
    session['regulation'] = regulation
    session['semester'] = semester
    session['subject'] = subject
    return render_template('subjectsInsideContent.html', regulation=regulation, semester=semester, subject=subject)


@app.route('/chapter_wise', methods=['GET', 'POST'])
def chapter_wise():
    if request.method == 'POST':
        # Handle the file upload
        regulation = request.form['regulation']
        semester = request.form['semester']
        subject = request.form['subject']

        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        
        file = request.files['file']
        
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)

        if allowed_file(file.filename):
            filename = secure_filename(file.filename)

            # Save the file data to the database
            file_data = file.read()
            with sqlite3.connect('instance/users.db') as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    INSERT INTO upload (regulation, semester, subject, filename, file_data, upload_date)
                    VALUES (?, ?, ?, ?, ?, ?)
                """, (regulation, semester, subject, filename, file_data, datetime.now()))
                conn.commit()

            flash('File successfully uploaded')
            return redirect(url_for('chapter_wise'))

        flash('File type not allowed')
        return redirect(request.url)

    return render_template('chapterss.html')


@app.route('/success')
def success_page():
    return "File uploaded successfully!"


@app.route("/notes", methods=["GET", "POST"])
def notes():
    return render_template("notes.html")

@app.route('/question_banks')
def question_banks():
    # Your code here
    return render_template('questionBank.html')
                           
@app.route("/semester_papers", methods=["GET", "POST"])
def semester_papers():
    return render_template("semPapers.html")


@app.route("/mid_papers", methods=["GET", "POST"])
def mid_papers():
    return render_template("midPapers.html")

@app.route("/supply_papers", methods=["GET", "POST"])
def supply_papers():
    return render_template("supplyPapers.html")


@app.route("/")
def index():
    return render_template("index.html")  # Render the home page template

# Sign-in route that handles login functionality using hashed password verification
@app.route("/signin", methods=["GET", "POST"])
def signin():
    if request.method == "POST":  # If the form is submitted (POST request)
        email = request.form.get("email")  # Get the user's email from the form
        password = request.form.get("password")  # Get the user's password from the form
        user = User.query.filter_by(email=email).first()  # Find the user by email
        if user and check_password_hash(user.password_hash, password):  # Validate the password against the hash
            flash("Login successful!", "success")  # Display a success message
            session['user_id'] = user.id  # Store the user's ID in the session for authentication
            session['user_email'] = user.email  # Optionally store the email in the session
            return redirect(url_for("index"))  # Redirect the user to the homepage after successful login
        else:
            flash("Invalid credentials. Please try again.", "danger")  # Display an error message for invalid login
    return render_template("signin.html")  # Render the login page for GET requests or failed login attempts

# Sign-up route that handles user registration with hashed passwords
@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":  # If the form is submitted (POST request)
        email = request.form.get("email")  # Get the email from the form
        password = request.form.get("password")  # Get the password from the form
        if User.query.filter_by(email=email).first():  # Check if the email is already registered
            flash("Email already registered. Please use a different email.", "danger")  # Show an error if the email exists
        else:
            password_hash = generate_password_hash(password)  # Hash the password before storing
            new_user = User(email=email, password_hash=password_hash)  # Create a new user with the hashed password
            db.session.add(new_user)  # Add the new user to the database
            db.session.commit()  # Commit the changes to save the new user
            flash("Sign up successful! You can now log in.", "success")  # Display a success message
            return redirect(url_for("signin"))  # Redirect to the login page after a successful sign-up
    return render_template("signup.html")  # Render the sign-up page

# Sign-out route that logs the user out
@app.route("/signout")
def signout():
    session.clear()  # Clear the session data (log the user out)
    flash("You have been logged out.", "success")  # Display a logout confirmation message
    return redirect(url_for("signin"))  # Redirect the user to the login page

# About page route that renders the about.html template
@app.route("/about", methods=["GET", "POST"])
def about():
    return render_template("about.html")  # Render the about page template

# Regulations page route that renders regulations.html template
@app.route("/regulations", methods=["GET", "POST"])
def regulations():
    return render_template("regulations.html")  # Render the regulations page template

# Routes for AR20 semester-specific pages
@app.route("/AR_20_semesters", methods=["GET", "POST"])
def AR_20_semesters():
    return render_template("ar20_semesters.html")  # Render AR20 semester overview page

@app.route("/one_one", methods=["GET", "POST"])
def one_one():
    session['regulation'] = 'AR20'  # Set appropriate regulation
    session['semester'] = '1-1'     # Set appropriate semester
    return render_template('ar20_one_one.html')

@app.route("/one_two", methods=["GET", "POST"])
def one_two():
    return render_template("ar20_one_two.html")  # Render AR20 first-year second-semester page

@app.route("/two_one", methods=["GET", "POST"])
def two_one():
    return render_template("ar20_two_one.html")  # Render AR20 second-year first-semester page

@app.route("/two_two", methods=["GET", "POST"])
def two_two():
    return render_template("ar20_two_two.html")  # Render AR20 second-year second-semester page

@app.route("/three_one", methods=["GET", "POST"])
def three_one():
    return render_template("ar20_three_one.html")  # Render AR20 third-year first-semester page

@app.route("/three_two", methods=["GET", "POST"])
def three_two():
    return render_template("ar20_three_two.html")  # Render AR20 third-year second-semester page

# Routes for AR23 semester-specific pages
@app.route("/AR_23_semesters", methods=["GET", "POST"])
def AR_23_semesters():
    return render_template("ar23_semesters.html")  # Render AR23 semester overview page

@app.route("/ar_23_one_one", methods=["GET", "POST"])
def ar_23_one_one():
    return render_template("ar23_one_one.html")  # Render AR23 first-year first-semester page

@app.route("/ar_23_one_two", methods=["GET", "POST"])
def ar_23_one_two():
    return render_template("ar23_one_two.html")  # Render AR23 first-year second-semester page

@app.route("/ar_23_two_one", methods=["GET", "POST"])
def ar_23_two_one():
    return render_template("ar23_two_one.html")  # Render AR23 second-year first-semester page

@app.route("/ar_23_two_two", methods=["GET", "POST"])
def ar_23_two_two():
    return render_template("ar23_two_two.html")  # Render AR23 second-year second-semester page

@app.route("/ar_23_three_one", methods=["GET", "POST"])
def ar_23_three_one():
    return render_template("ar23_three_one.html")  # Render AR23 third-year first-semester page

@app.route("/ar_23_three_two", methods=["GET", "POST"])
def ar_23_three_two():
    return render_template("ar23_three_two.html")  # Render AR23 third-year second-semester page


# Main entry point to start the Flask app
if __name__ == "__main__":
    app.run(debug=True)  # Run the Flask app in debug mode
