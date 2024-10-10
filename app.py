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



# Sign-up route
@app.route("/signup", methods=["GET", "POST"])
def signup():
    return render_template("signup.html")



@app.route("/one_one", methods=["GET", "POST"])
def one_one():
    return render_template("one_one.html")



@app.route("/one_two", methods=["GET", "POST"])
def one_two():
    return render_template("one_two.html")



@app.route("/two_one", methods=["GET", "POST"])
def two_one():
    return render_template("two_one.html")



@app.route("/two_two", methods=["GET", "POST"])
def two_two():
    return render_template("two_two.html")



@app.route("/three_one", methods=["GET", "POST"])
def three_one():
    return render_template("three_one.html")



@app.route("/three_two", methods=["GET", "POST"])
def three_two():
    return render_template("three_two.html")



if __name__ == "__main__":
    app.run(debug=True)
