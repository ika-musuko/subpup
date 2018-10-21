from flask import url_for, redirect, render_template
from flask_dance.consumer import oauth_authorized
from flask_login import current_user, login_user, login_required, logout_user
from flask_dance.contrib.google import google
from project import app, google_blueprint
from project.models import *

@app.route("/")
@app.route("/index")
def index():
    # return "dog app %s" % (current_user.email if current_user else  "...no one logged in")
    return render_template("index.html")

@login_required
@app.route("/manage_listings")
def manage_listings():
    return render_template("manage_listings.html")

@app.route("/about")
def about():
    return "about page"

@app.route("/register")
def insert_name():
    return render_template("register.html")

@app.route("/go_to_login")
def go_to_login():
    return redirect(url_for('index'))

# !!! USE log_in/google !!!
@oauth_authorized.connect_via(google_blueprint)
@app.route("/log_in", methods=["GET", "POST"])
def log_in(blueprint, token):
    # get oauth response
    resp = google.get("/oauth2/v2/userinfo")
    email = resp.json()['email']

    if resp.ok:
        # see if the user already exists
        user = User.query.filter_by(email=email).first()

        # if they don't have an account yet, make a new one
        if not user:
            user = User(email=email)
            db.session.add(user)
            db.session.commit()

        login_user(user)
        return redirect(url_for("index"))

@app.route("/log_out", methods=["GET", "POST"])
def log_out():
   logout_user()
   return redirect(url_for("index"))
