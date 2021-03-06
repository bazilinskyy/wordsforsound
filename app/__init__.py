# By Pavlo Bazilinskyy <pavlo.bazilinskyy@gmail.com>
import os
from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.login import LoginManager
from flask.ext.mail import Mail
from config import basedir, EMAIL_SYSTEM
if not os.environ.get('HEROKU'):
	from config_secret import ADMINS, MAIL_SERVER, MAIL_PORT, MAIL_USERNAME, \
    MAIL_PASSWORD

app = Flask(__name__)
app.config.from_object('config')
app.config['MAX_CONTENT_LENGTH'] = 512 * 1024 * 1024 # Max file upload size
db = SQLAlchemy(app)
lm = LoginManager()
lm.init_app(app)
lm.login_view = 'login'
mail = Mail(app)

if not app.debug and os.environ.get('HEROKU') is None:
    import logging
    from logging.handlers import RotatingFileHandler
    file_handler = RotatingFileHandler('tmp/wordsforsound.log', 'a',
                                       1 * 10024 * 1024, 10)
    file_handler.setLevel(logging.INFO)
    file_handler.setFormatter(logging.Formatter(
        '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'))
    app.logger.addHandler(file_handler)
    app.logger.setLevel(logging.INFO)
    app.logger.info('wordsforsound')

    # Configuaration for SMTP server, if used
    if EMAIL_SYSTEM == 'SMTP':
        from logging.handlers import SMTPHandler
        credentials = None
        if MAIL_USERNAME or MAIL_PASSWORD:
            credentials = (MAIL_USERNAME, MAIL_PASSWORD)
        mail_handler = SMTPHandler((MAIL_SERVER, MAIL_PORT),
                                   'wordsforsound@' + MAIL_SERVER, ADMINS,
                                   'wordsforsound', credentials)
        mail_handler.setLevel(logging.ERROR)

if os.environ.get('HEROKU') is not None:
    import logging
    stream_handler = logging.StreamHandler()
    app.logger.addHandler(stream_handler)
    app.logger.setLevel(logging.INFO)
    app.logger.info('wordsforsound')

from app import views, models