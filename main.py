from flask import Flask, render_template, session, redirect, url_for, flash
from flask_session import Session
from forms import loginForm, signupForm
from flask_sqlalchemy import SQLAlchemy
import hashlib

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

def validate_user():
    if "user_id" in session and profile.query.filter_by(id=session["user_id"]).first() is not None:
        return True
    return False

@app.route("/")
@app.route("/home")
def home():
    """
    A simple Flask route that returns a greeting message."""
    if not validate_user():
        return redirect(url_for("login"))
    user = profile.query.filter_by(id=session["user_id"]).first()
    return render_template("home.html", username=user.username)

@app.route("/login", methods = ["GET", "POST"])
def login():
    """
    A Flask route that handles user login.
    If the user is already logged in (i.e., "user_id" is in the session), they are redirected to the home page.
    Otherwise, a login form is displayed, and upon submission, the login logic is processed.
    """
    if validate_user():
        return redirect(url_for("home"))
    
    form = loginForm()
    if form.validate_on_submit():
        if profile.query.filter_by(username=form.username.data).first() is None:
            flash("User does not exist. Please sign up first.", "danger")
        else:
            # Authenticate the user
            user = profile.query.filter_by(username=form.username.data).first()
            if user.password == hashlib.sha256(form.password.data.encode()).hexdigest():
                session["user_id"] = user.id
                flash(f"Welcome back, {user.username}!", "success")
                return redirect(url_for("home"))
            else:
                flash("Invalid username or password.", "danger")
    return render_template("login.html", form = form)

@app.route("/signup", methods = ["GET", "POST"])
def signup():
    """
    A Flask route that handles user signup.
    If the user is already logged in (i.e., "user_id" is in the session), they are redirected to the home page.
    Otherwise, a signup form is displayed, and upon submission, the signup logic is processed.
    """
    if validate_user():
        return redirect(url_for("home"))

    form = signupForm()
    if form.validate_on_submit():
        if profile.query.filter_by(username=form.username.data).first() is not None:
            flash("Username already exists. Please choose a different one.", "danger")
        else:
            # Create a new user profile
            new_user = profile(username=form.username.data, password=hashlib.sha256(form.password.data.encode()).hexdigest())
            db.session.add(new_user)
            db.session.commit()
            flash("Account created successfully!", "success")
            return redirect(url_for("login"))
    return render_template("signup.html", form = form)

@app.route("/logout")
def logout():
    session.clear()
    flash("You have been logged out.", "info")
    return redirect(url_for("home"))

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)