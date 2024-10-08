# app.py
from flask import Flask, render_template
from flask_session import Session

app = Flask(__name__)

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

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
@app.route("/signin", methods=["GET", "POST"])
def signin():
    return render_template("signin.html")

if __name__ == "__main__":
    app.run(debug=True)
