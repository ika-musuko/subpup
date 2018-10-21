from flask_login import UserMixin
from project import db, lm
import datetime


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, index=True, primary_key=True)
    email = db.Column(db.String(64), index=True, unique=True)
    name = db.Column(db.String(64), index=True, unique=False)
    description = db.Column(db.String(1000), index=True, unique=False)
    current_dog_id = db.Column(db.Integer, index=True, nullable=True)
    profile_pic = db.Column(db.String(1000), index=True, unique=False)  # as filepath
    user_rating = db.Column(db.Float, index=True, unique=False)
    owner_rating = db.Column(db.Float, index=True, unique=False)
    dogs = db.relationship("Dog", backref="owner", lazy="dynamic")

    def __repr__(self):
        return "<User {}>".format(self.name)


@lm.user_loader
def load_user(id: str):
    return User.query.get(int(id))


class Dog(db.Model):
    id = db.Column(db.Integer, index=True, primary_key=True)
    name = db.Column(db.String(64), index=True, unique=False)
    breed = db.Column(db.String(100), index=True, unique=False)
    description = db.Column(db.String(1000), index=True, unique=False)
    start_time = db.Column(db.Time, index=True, unique=False)
    end_time = db.Column(db.Time, index=True, unique=False)
    available_date = db.Column(db.Date, index=True, unique=False)
    # pickup_mode is either "pickup" or "delivery"
    pickup_mode = db.Column(db.String(100), index=True, unique=False)
    # address of dog
    address = db.Column(db.String(400), index=True, unique=False)
    pic = db.Column(db.String(1000), index=True, unique=False, default="imgs/subpup.png")  # as filepath
    owner_id = db.Column(db.Integer, db.ForeignKey("user.id"))

    def __repr__(self):
        return "<Dog {}>".format(self.name)

    @property
    def availability(self) -> str:
        return "{} {}-{}".format(date_fmt(self.available_date), time_fmt(self.start_time), time_fmt(self.end_time))

def date_fmt(d) -> str:
    if d is None:
        return "Not Available"
    time_delta = d - datetime.datetime.now().date()
    if time_delta.days == 0:
        return "Today"
    elif time_delta.days == 1:
        return "Tomorrow"
    return d.__str__()

def time_fmt(t) -> str:
    if t is None:
        return ""
    return t.strftime("%I:%M %p")

class Reservation(db.Model):
    id = db.Column(db.Integer, index=True, primary_key=True)
    user_id = db.Column(db.Integer, index=True, unique=False)
    dog_id = db.Column(db.Integer, index=True, unique=False)

    def __repr__(self):
        return "<Reservation - user: {} dog: {}>".format(self.user_id, self.dog_id)
