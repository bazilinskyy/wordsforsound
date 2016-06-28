# By Pavlo Bazilinskyy <pavlo.bazilinskyy@gmail.com>
import os
basedir = os.path.abspath(os.path.dirname(__file__))

CSRF_ENABLED = True
SECRET_KEY = 'you-will-never-guess'

OPENID_PROVIDERS = [
    {'name': 'Google', 'url': 'https://www.google.com/accounts/o8/id'},
    {'name': 'Yahoo', 'url': 'https://me.yahoo.com'},
    {'name': 'AOL', 'url': 'http://openid.aol.com/<username>'},
    {'name': 'Flickr', 'url': 'http://www.flickr.com/<username>'},
    {'name': 'MyOpenID', 'url': 'https://www.myopenid.com'}]

SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db')
SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')
SQLALCHEMY_TRACK_MODIFICATIONS = True
WHOOSH_BASE = os.path.join(basedir, 'search.db')

# email server
MAIL_SERVER = 'your.mailserver.com'
MAIL_PORT = 25
MAIL_USE_TLS = False
MAIL_USE_SSL = False
MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')

# administrator list
ADMINS = ['you@example.com']

# pagination
POSTS_PER_PAGE = 3
MAX_SEARCH_RESULTS = 50

# horizontal menu
ONGOING_PROJECTS_MENU = 5
FINISHED_PROJECTS_MENU= 5
ONGOING_ASSETS_MENU = 5
FINISHED_ASSETS_MENU= 5

# uploading sounds
SOUND_UPLOAD_FOLDER = 'static/sound_uploads/'
SOUND_ALLOWED_EXTENSIONS = ['wav', 'mp3', 'aac', 'ogg', 'oga', 'flac', 'm4a']

# uploading attachments
ATACHMENT_UPLOAD_FOLDER = 'static/attachment_uploads/'

# json files for tags
TAGS_FILE = '/static/tags.json'