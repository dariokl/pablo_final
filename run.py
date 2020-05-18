import os
from dotenv import load_dotenv
load_dotenv()

from app import create_app, db

#Use to handle the command  flask db init / flask db migrate / flask db upgrade etc...
from flask_migrate import Migrate


app = create_app(os.environ.get('FLASK_CONFIG'))
migrate = Migrate(app, db)



