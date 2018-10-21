from project import app, db
from project.models import *

@app.shell_context_processor
def make_shell_context():
    return {'db' : db, 'User' : User, 'Dog' : Dog, 'Reservation' : Reservation}
