from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect
from flask_cors import CORS

db = SQLAlchemy()
csrf = CSRFProtect()
cors = CORS()