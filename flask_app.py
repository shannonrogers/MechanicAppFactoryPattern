from app import create_app
from app.models import db
import os

app = create_app('ProductionConfig')

with app.app_context(): 
    # db.drop_all()
    db.create_all()

