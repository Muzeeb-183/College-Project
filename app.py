# Import essential modules from Flask and related libraries
from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_session import Session  # Handles user sessions
from flask_sqlalchemy import SQLAlchemy  # Manages SQLite database interactions
from werkzeug.security import generate_password_hash, check_password_hash  # For password hashing

# Set up the Flask application
app = Flask(__name__)

# Set up session configuration to store data in the filesystem (for server-side session management)
app.config["SESSION_PERMANENT"] = False  # Sessions are temporary (reset when the browser closes)
app.config["SESSION_TYPE"] = "filesystem"  # Session data will be saved in the filesystem

# Configure the database connection (SQLite in this case) and disable unnecessary tracking of changes
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'  # Set up SQLite to store user data
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Disable modification tracking to save resources

# Initialize session and database components
Session(app)  # Initialize session management
db = SQLAlchemy(app)  # Initialize database connection

# Define a User model (represents the structure of the "users" table in the database)
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)  # The unique user ID (primary key)
    email = db.Column(db.String(120), unique=True, nullable=False)  # User's email address (must be unique)
    password_hash = db.Column(db.String(200), nullable=False)  # Hashed password

    # Representation of a User instance, useful for debugging or logging
    def __repr__(self):
        return f'<User {self.email}>'

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
    return render_template("ar20_one_one.html")  # Render AR20 first-year first-semester page

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
