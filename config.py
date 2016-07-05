# By Pavlo Bazilinskyy <pavlo.bazilinskyy@gmail.com>
import os
basedir = os.path.abspath(os.path.dirname(__file__))

CSRF_ENABLED = True
SECRET_KEY = 'you-will-never-guess'

SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db')
SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')
SQLALCHEMY_TRACK_MODIFICATIONS = True
WHOOSH_BASE = os.path.join(basedir, 'search.db')

# slow database query threshold (in seconds)
DATABASE_QUERY_TIMEOUT = 0.5

# Whoosh does not work on Heroku
WHOOSH_ENABLED = True#os.environ.get('HEROKU') is None

# pagination
TAGS_PER_PAGE = 10
SOUNDS_PER_PAGE = 10
ASSETS_PER_PAGE = 5
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