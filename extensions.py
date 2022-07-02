from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect
from flask_cors import CORS
from flask_httpauth import HTTPTokenAuth
from flask_apscheduler import APScheduler
from apscheduler.schedulers.background import BackgroundScheduler


scheduler = APScheduler(scheduler=BackgroundScheduler(timezone='Asia/Shanghai'))
auth = HTTPTokenAuth(scheme='JWT')
db = SQLAlchemy()
# csrf = CSRFProtect()
cors = CORS()