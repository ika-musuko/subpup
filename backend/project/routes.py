import os
from flask import url_for, redirect, render_template, request
from flask_dance.consumer import oauth_authorized
from flask_login import current_user, login_user, login_required, logout_user
from flask_dance.contrib.google import google
from project import app, google_blueprint, db
from project.forms import DogForm
from project.models import User, Dog, Reservation
from werkzeug.utils import secure_filename


@app.route("/")
@app.route("/index")
def index():
    if current_user.is_authenticated:
        dogs = Dog.query.all()
        return render_template("index.html", dogs=dogs)

    return render_template("index.html")


@login_required
@app.route("/manage_listings")
def manage_listings():
    my_dogs = Dog.query.filter_by(owner_id=current_user.id)
    return render_template("manage_listings.html", dogs=my_dogs)


@app.route("/user/<user_id>")
def user(user_id: int):
    the_user = User.query.filter_by(user_id=user_id).first()
    return render_template("user.html", user=the_user)


@login_required
@app.route("/my_reservations")
def my_reservations():
    # thanks database experience........
    reserved_dogs = Dog.query\
        .join(Reservation, Reservation.user_id == current_user.id)\
        .group_by(Reservation.dog_id)\
        .all()
    return render_template("my_reservations.html", dogs=reserved_dogs)


@login_required
@app.route("/make_reservation/<dog_id>")
def make_reservation(dog_id: int):
    dog = Dog.query.filter_by(id=dog_id).first()
    new_reservation = Reservation(
        user_id=current_user.id,
        dog_id=dog_id,
    )
    db.session.add(new_reservation)
    db.session.commit()
    return redirect(url_for("index"))


@login_required
@app.route("/dog/<dog_id>")
def dog(dog_id: int):
    the_dog = Dog.query.filter_by(id=dog_id).first()
    the_owner = User.query.filter_by(id=the_dog.owner_id).first()
    return render_template("dog.html", dog=the_dog, owner=the_owner)


@login_required
@app.route("/add_dog", methods=["GET", "POST"])
def add_dog():
    dogform = DogForm()
    if dogform.validate_on_submit():
        # get the uploaded pic and save it
        if dogform.pic.data:
            pic_filename = secure_filename(dogform.pic.data.filename)
            pic_filepath = os.path.join("imgs", "dogs", pic_filename)
            dogform.pic.data.save(os.path.join(app.root_path, "static", pic_filepath))
        else:
            pic_filepath = "imgs/subpup.png"

        # make a new dog to store to the database
        new_dog = Dog(
            name=dogform.name.data,
            description=dogform.description.data,
            breed=dogform.breed.data,
            pic=pic_filepath,
            owner_id=current_user.id,
            available_date=dogform.date.data,
            start_time=dogform.start_time.data,
            end_time=dogform.end_time.data,
        )
        db.session.add(new_dog)
        db.session.commit()
        return redirect(url_for("index"))
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
