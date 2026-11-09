from flask import Flask, render_template, session, redirect, url_for
from flask_session import Session
from forms import loginForm, signupForm
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config["SECRET_KEY"] = "your_secret_key"
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"

Session(app)

@app.route("/")
@app.route("/home")
def home():
    """
    A simple Flask route that returns a greeting message."""
    if "user_id" not in session:
        return redirect(url_for("login"))
    return "Hello, world!"

@app.route("/login", methods = ["GET", "POST"])
def login():
    """
    A Flask route that handles user login.
    If the user is already logged in (i.e., "user_id" is in the session), they are redirected to the home page.
    Otherwise, a login form is displayed, and upon submission, the login logic is processed.
    """
    if "user_id" in session:
        return redirect(url_for("home"))
    
    form = loginForm()
    if form.validate_on_submit():
        # Process login logic here
        pass
    return render_template("login.html", form = form)

if __name__ == "__main__":
    app.run(debug=True)