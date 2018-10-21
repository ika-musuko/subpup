from flask import url_for, redirect, render_template, request
from flask_dance.consumer import oauth_authorized
from flask_login import current_user, login_user, login_required, logout_user
from flask_dance.contrib.google import google
from project import app, google_blueprint
from project.forms import DogForm
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

@app.route("/user/<user_id>")
def user(user_id: int):
    the_user = User.query.filter_by(user_id=user_id).first()
    return render_template("user.html", user=the_user)

@login_required
@app.route("/dog/<dog_id>")
def dog(dog_id: int):
    the_dog = Dog.query.filter_by(dog_id=dog_id).first()
    the_owner = User.query.filter_by(user_id=the_dog.owner_id).first()
    return render_template("dog.html", dog=the_dog, owner=the_owner)

@login_required
@app.route("/add_dog")
def add_dog():
    dogform = DogForm()
    return render_template("add_dog.html", dogform=dogform)

@app.route("/about")
def about():
    return "about page"

@app.route("/register")
def register():
    return render_template("register.html")

@app.route("/register", methods=["POST"])
def register_post():
    name = request.form["name-input"]
    current_user.name = name
    db.session.commit()
    return redirect(url_for("index"))

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
            return redirect(url_for("register"))

        login_user(user)
        return redirect(url_for("index"))

@app.route("/log_out", methods=["GET", "POST"])
def log_out():
   logout_user()
   return redirect(url_for("index"))
