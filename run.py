from app import app
from app.models import db, Units, User

@app.shell_context_processor
def shell_context():
    return {'db':db,'Units':Units,'User':User}