from project import db

class User(db.Model):
    email = db.Column(db.String(64), index=True, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)

    def __repr__(self):
        return "<User {}>".format(self.username)
    
