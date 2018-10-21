from project import app
from datetime import datetime

@app.context_processor
def inject_app_context():
    return {
        "debug": app.debug,
    }

