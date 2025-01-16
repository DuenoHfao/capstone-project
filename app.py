from flask import Flask, render_template, request, redirect, url_for, session, flash
import os
import logging
import secrets
from dotenv import load_dotenv
from datetime import datetime
from static.dynamo_requests import *

load_dotenv()

app = Flask(__name__)
logger = logging.getLogger(__name__)
app.secret_key = secrets.token_hex(16)


if not UserModel.exists():
    UserModel.create_table(read_capacity_units=1, write_capacity_units=1, wait=True)
    logger.info('Created new table')

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
            return redirect(url_for('templates',filename="login"))

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
                return 'credential success'
                return redirect(url_for("home"))
            
            else:
                flash("Invalid credentials. Please try again.", "error")
        except DoesNotExist:
            flash("Invarequest.form.getlid credentials. Please try again.", "error")

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

@app.route("/terms")
def terms():
    return render_template("terms.html", logged_in=is_logged_in())

if __name__ == "__main__":
    logging.basicConfig(filename='myapp.log', level=logging.INFO)
    logger.info(f'Started at {datetime.now()}')

    app.run(host='0.0.0.0', port=5500)