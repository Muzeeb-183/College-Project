from flask import Flask, render_template, request, redirect, url_for, flash, session

from flask_session import Session
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'  # Database URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Disable track modifications
Session(app)

# Initialize database
db = SQLAlchemy(app)

# User model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)

    def __repr__(self):
        return f'<User {self.email}>'

# Create database tables
with app.app_context():
    db.create_all()

@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

# Home route
@app.route("/")
def index():
    return render_template("index.html")

# Sign-in route
# Sign-in route
@app.route("/signin", methods=["GET", "POST"])
def signin():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")
        user = User.query.filter_by(email=email, password=password).first()
        if user:
            flash("Login successful!", "success")
            session['user_id'] = user.id  # Store user id in session
            session['user_email'] = user.email  # Optionally store user email
            return redirect(url_for("index"))
        else:
            flash("Invalid credentials. Please try again.", "danger")
    return render_template("signin.html")


# Sign-up route
@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")
        if User.query.filter_by(email=email).first():
            flash("Email already registered. Please use a different email.", "danger")
        else:
            new_user = User(email=email, password=password)
            db.session.add(new_user)
            db.session.commit()
            flash("Sign up successful! You can now log in.", "success")
            return redirect(url_for("signin"))
    return render_template("signup.html")
# Sign-out route
@app.route("/signout")
def signout():
    session.clear()  # Clear all session data
    flash("You have been logged out.", "success")
    return redirect(url_for("signin"))

@app.route("/about", methods=["GET", "POST"])
def about():
    return render_template("about.html")

@app.route("/regulations", methods=["GET", "POST"])
def regulations():
    return render_template("regulations.html")

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

#------------------------------------------------------#

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

if __name__ == "__main__":
    app.run(debug=True)
