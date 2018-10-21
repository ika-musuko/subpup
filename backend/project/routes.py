from project import app

@app.route("/list_dog")
def list_dog():
    return "list a new dog"

@app.route("/about")
def about():
    return "about page"

@app.route("/insert_name")
def insert_name():
    return "insert name for new users"

@app.route("/log_in")
def log_in():
    return "login route, google login"

@app.route("/")
@app.route("/index")
def index():
    return "dog app"

