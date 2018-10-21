from flask_login import UserMixin
from project import db, lm

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, index=True, primary_key=True)
    email = db.Column(db.String(64), index=True, unique=True)
    name = db.Column(db.String(64), index=True, unique=False)
    description = db.Column(db.String(1000), index=True, unique=False)
    current_dog_id = db.Column(db.Integer, index=True, nullable=True)
    profile_pic = db.Column(db.String(1000), index=True, unique=False) # as filepath
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
    # availability is a formatted string like the following
    # R~MT~4:30 pm
    # O~2018~10~20~4:30 pm
    # R or O - Recurring or One Time
    # if Recurring
    #    list days of week
    #    time as 24hr military time (1630)
    # if One Time
    #    datetime as string
    availability = db.Column(db.String(100), index=True, unique=False)
    # pickup_mode is either "pickup" or "delivery"
    pickup_mode = db.Column(db.String(100), index=True, unique=False)
    # address of dog
    address = db.Column(db.String(400), index=True, unique=False)
    pic = db.Column(db.String(1000), index=True, unique=False) # as filepath
    owner_id = db.Column(db.Integer, db.ForeignKey("user.id"))

    def __repr__(self):
        return "<Dog {}>".format(self.name)

class Reservation(db.Model):
    id = db.Column(db.Integer, index=True, primary_key=True)
    user_id = db.Column(db.Integer, index=True, unique=False)
    dog_id = db.Column(db.Integer, index=True, unique=False)
    time = db.Column(db.DateTime, index=True, unique=False)

    def __repr__(self):
        return "<Reservation - user: {} dog: {} time: {}>".format(self.user_id, self.dog_id, self.time)

