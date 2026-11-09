from flask import Flask, render_template, session, redirect, url_for
from flask_session import Session
from forms import loginForm, signupForm
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config["SECRET_KEY"] = "your_secret_key"
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///users.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

Session(app)

db = SQLAlchemy(app)

class profile(db.Model):
    """
    A SQLAlchemy model representing a user profile.
    This model includes fields for the user's ID, username, and password.
    """
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)

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
        print(form.username.data)
        print(form.password.data)
        pass
    return render_template("login.html", form = form)

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)