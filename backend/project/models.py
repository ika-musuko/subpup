from project import db

class User(db.Model):
    id = db.Column(db.Integer, index=True, primary_key=True)
    email = db.Column(db.String(64), index=True, unique=True)
    name = db.Column(db.String(64), index=True, unique=False)
    description = db.Column(db.String(1000), index=True, unique=False)
    current_dog_id = db.Column(db.Integer, index=True, nullable=True)
    profile_pic = db.Column(db.String(1000), index=True, unique=False) # as filepath
    dogs = db.relationship("Dog", backref="owner", lazy="dynamic")

    def __repr__(self):
        return "<User {}>".format(self.name)

class Dog(db.Model):
    id = db.Column(db.Integer, index=True, primary_key=True)
    name = db.Column(db.String(64), index=True, unique=False)
    breed = db.Column(db.String(100), index=True, unique=False)
    # availability is a formatted string like the following
    # R or O - Recurring or One Time
    # if Recurring
    #    day of week as MTWRFSU (U = sunday)
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
    user_id = db.Column(db.Integer, index=True, unique=False)
    dog_id = db.Column(db.Integer, index=True, unique=False)
    time = db.Column(db.DateTime, index=True, unique=False)

    def __repr__(self):
        return "<Reservation - user: {} dog: {} time: {}>".format(self.user_id, self.dog_id, self.time)

