import os
from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_dance.contrib.google import make_google_blueprint

app = Flask(__name__)
app.config.from_object(Config)
app.secret_key = "ssss"

db = SQLAlchemy(app)
migrate = Migrate(app, db)

lm = LoginManager()
lm.init_app(app)
lm.login_view = "go_to_login"

# google login
offline_state = not os.getenv("IS_ONLINE")
google_blueprint = make_google_blueprint(
    client_id=os.getenv("GOOGLE_CLIENT_ID") or "",  # Your client_id here
    client_secret=os.getenv("GOOGLE_CLIENT_SECRET") or "",  # Your client secret here
    scope=[
        "https://www.googleapis.com/auth/plus.me",
        "https://www.googleapis.com/auth/userinfo.email",
    ]
)

app.register_blueprint(google_blueprint, url_prefix='/log_in')

from project import routes, models
