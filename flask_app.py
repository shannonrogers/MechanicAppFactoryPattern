from app import create_app
from app.models import db
import os

app = create_app('ProductionConfig')

if __name__ == '__main__':
    with app.app_context(): 
        # db.drop_all()
        db.create_all()
    app.run()
