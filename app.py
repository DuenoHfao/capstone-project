from flask import Flask, render_template, request, redirect, url_for, session, flash
import os
import logging
import secrets
from datetime import datetime   
from dotenv import load_dotenv
from pynamodb.models import Model
from pynamodb.attributes import UnicodeAttribute
from pynamodb.exceptions import DoesNotExist

load_dotenv()

app = Flask(__name__)
logger = logging.getLogger(__name__)

app.secret_key = secrets.token_hex(16)

# DynamoDB table schema (js googled a basic ass one bruh)
class UserModel(Model):
    class Meta:
        table_name = "users"
        region = "ap-southeast-1"
        aws_access_key_id = os.getenv('AWS_ACCESS_KEY')
        aws_secret_access_key = os.getenv('AWS_SECRET_ACCESS_KEY')

    email = UnicodeAttribute(hash_key=True, null=False)
    password = UnicodeAttribute()


# Create the table if it doesn't exist
if not UserModel.exists():
    UserModel.create_table(read_capacity_units=1, write_capacity_units=1, wait=True)

# Check if user is logged in
def is_logged_in():
    return "user" in session


@app.route("/")
def home():
    return render_template("home.html", logged_in=is_logged_in())

@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")

        try:
            # Check if the user already exists
            UserModel.get(email)
            flash("Email already registered. Please log in.", "error")
            return redirect(url_for("login"))
        except DoesNotExist:
            # Else c    reate a new user
            user = UserModel(email=email, password=password)
            user.save()
            flash("Account created successfully! Please log in.", "success")
            return redirect(url_for("login"))

    return render_template("signup.html", logged_in=is_logged_in())

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")

        try:
            user = UserModel.get(email)
            if user.password == password:
                session["user"] = email
                flash("Logged in successfully!", "success")
                return redirect(url_for("dashboard"))
            else:
                flash("Invalid credentials. Please try again.", "error")
        except DoesNotExist:
            flash("Invalid credentials. Please try again.", "error")

    return render_template("login.html", logged_in=is_logged_in())

@app.route("/logout")
def logout():
    session.pop("user", None)
    flash("Logged out successfully.", "success")
    return redirect(url_for("home"))

@app.route("/dashboard")
def dashboard():
    if not is_logged_in():
        flash("You need to log in to access this page.", "error")
        return redirect(url_for("login"))

    return render_template("dashboard.html", logged_in=is_logged_in())

@app.route("/reset-password", methods=["GET", "POST"])
def reset_password():
    if request.method == "POST":
        email = request.form.get("email")

        try:
            UserModel.get(email)
            flash("Password reset instructions sent to your email.", "success")
        except DoesNotExist:
            flash("Email not found.", "error")

        return redirect(url_for("login"))

    return render_template("reset_password.html", logged_in=is_logged_in())

if __name__ == "__main__":
    logging.basicConfig(filename='myapp.log', level=logging.INFO)
    logger.info(f'Started at {datetime.now()}')

    app.run(host='0.0.0.0', port=5500, debug=True)