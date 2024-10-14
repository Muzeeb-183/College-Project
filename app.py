# Import necessary modules and packages from Flask and related libraries
from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_session import Session  # For handling user sessions
from flask_sqlalchemy import SQLAlchemy  # For handling the SQLite database

# Initialize the Flask app
app = Flask(__name__)

# Configure session to use filesystem (for storing user session data on the server)
app.config["SESSION_PERMANENT"] = False  # Sessions are not permanent (reset after browser is closed)
app.config["SESSION_TYPE"] = "filesystem"  # Store session data in the filesystem

# Configure the database URI (SQLite in this case) and disable track modifications
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'  # SQLite database for user data
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Disable modification tracking to save resources

# Initialize Flask-Session and Flask-SQLAlchemy
Session(app)  # Initialize session management
db = SQLAlchemy(app)  # Initialize the database connection

# Define a User model (database table schema)
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)  # Unique user ID (primary key)
    email = db.Column(db.String(120), unique=True, nullable=False)  # User's email (must be unique)
    password = db.Column(db.String(200), nullable=False)  # User's password

    # Representation of a User instance, useful for debugging
    def __repr__(self):
        return f'<User {self.email}>'

# Create the database tables based on the User model (if they don't exist)
with app.app_context():
    db.create_all()  # Create all tables

# Function to ensure no browser caching for security purposes
@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"  # Don't cache the response
    response.headers["Expires"] = 0  # Expire immediately
    response.headers["Pragma"] = "no-cache"  # Prevent caching
    return response

# Home route: Render the homepage
@app.route("/")
def index():
    return render_template("index.html")

# Sign-in route: Handle login logic
@app.route("/signin", methods=["GET", "POST"])
def signin():
    if request.method == "POST":  # If form is submitted
        email = request.form.get("email")  # Get the email from the form
        password = request.form.get("password")  # Get the password from the form
        user = User.query.filter_by(email=email, password=password).first()  # Check if the user exists
        if user:  # If user is found, log them in
            flash("Login successful!", "success")  # Display success message
            session['user_id'] = user.id  # Store user ID in session for identification
            session['user_email'] = user.email  # Optionally store email in session
            return redirect(url_for("index"))  # Redirect to home page after login
        else:
            flash("Invalid credentials. Please try again.", "danger")  # If credentials are wrong, display error
    return render_template("signin.html")  # Render sign-in page for GET requests or failed login

# Sign-up route: Handle user registration
@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":  # If form is submitted
        email = request.form.get("email")  # Get email from the form
        password = request.form.get("password")  # Get password from the form
        if User.query.filter_by(email=email).first():  # Check if the email is already registered
            flash("Email already registered. Please use a different email.", "danger")  # Show error if email exists
        else:
            new_user = User(email=email, password=password)  # Create a new user
            db.session.add(new_user)  # Add the user to the database
            db.session.commit()  # Commit the changes (save the new user)
            flash("Sign up successful! You can now log in.", "success")  # Show success message
            return redirect(url_for("signin"))  # Redirect to sign-in page after successful sign-up
    return render_template("signup.html")  # Render the sign-up page

# Sign-out route: Handle user logout
@app.route("/signout")
def signout():
    session.clear()  # Clear the session data (log the user out)
    flash("You have been logged out.", "success")  # Display a logout message
    return redirect(url_for("signin"))  # Redirect to sign-in page

# About page route: Render about.html
@app.route("/about", methods=["GET", "POST"])
def about():
    return render_template("about.html")

# Regulations page route: Render regulations.html
@app.route("/regulations", methods=["GET", "POST"])
def regulations():
    return render_template("regulations.html")

# Routes for AR20 semester-specific pages
@app.route("/AR_20_semesters", methods=["GET", "POST"])
def AR_20_semesters():
    return render_template("ar20_semesters.html")

@app.route("/one_one", methods=["GET", "POST"])
def one_one():
    return render_template("ar20_one_one.html")

@app.route("/one_two", methods=["GET", "POST"])
def one_two():
    return render_template("ar20_one_two.html")

@app.route("/two_one", methods=["GET", "POST"])
def two_one():
    return render_template("ar20_two_one.html")

@app.route("/two_two", methods=["GET", "POST"])
def two_two():
    return render_template("ar20_two_two.html")

@app.route("/three_one", methods=["GET", "POST"])
def three_one():
    return render_template("ar20_three_one.html")

@app.route("/three_two", methods=["GET", "POST"])
def three_two():
    return render_template("ar20_three_two.html")

# Routes for AR23 semester-specific pages
@app.route("/AR_23_semesters", methods=["GET", "POST"])
def AR_23_semesters():
    return render_template("ar23_semesters.html")

@app.route("/ar_23_one_one", methods=["GET", "POST"])
def ar_23_one_one():
    return render_template("ar23_one_one.html")

@app.route("/ar_23_one_two", methods=["GET", "POST"])
def ar_23_one_two():
    return render_template("ar23_one_two.html")

@app.route("/ar_23_two_one", methods=["GET", "POST"])
def ar_23_two_one():
    return render_template("ar23_two_one.html")

@app.route("/ar_23_two_two", methods=["GET", "POST"])
def ar_23_two_two():
    return render_template("ar23_two_two.html")

@app.route("/ar_23_three_one", methods=["GET", "POST"])
def ar_23_three_one():
    return render_template("ar23_three_one.html")

@app.route("/ar_23_three_two", methods=["GET", "POST"])
def ar_23_three_two():
    return render_template("ar23_three_two.html")

# Main entry point to start the app when the script is run
if __name__ == "__main__":
    app.run(debug=True)  # Start the app in debug mode
