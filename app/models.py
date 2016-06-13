# By Pavlo Bazilinskyy <pavlo.bazilinskyy@gmail.com>
from hashlib import md5
from app import db
from app import app
from enum import Enum

import sys
if sys.version_info >= (3, 0):
    enable_search = False
else:
    enable_search = True
    import flask.ext.whooshalchemy as whooshalchemy

tags_sounds_table = db.Table(
    'tags_for_sound',
    db.Column('sound_id', db.Integer, db.ForeignKey('sound.id')),
    db.Column('tag_id', db.Integer, db.ForeignKey('tag.id'))
)

class Pitch(Enum):
    A = 1
    B = 2
    C = 3
    D = 4
    E = 5
    F = 6
    G = 7

class SoundType(Enum):
    earcon = 1
    dynamic_earcon = 2
    spearcon = 3

class SoundFamily(Enum):
    warning = 1
    notification = 2
    confirmation = 3
    status_alert = 4
    spatial = 5
    looming = 6

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nickname = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    about_me = db.Column(db.String(140))
    last_seen = db.Column(db.DateTime)

    @staticmethod
    def make_unique_nickname(nickname):
        if User.query.filter_by(nickname=nickname).first() is None:
            return nickname
        version = 2
        while True:
            new_nickname = nickname + str(version)
            if User.query.filter_by(nickname=new_nickname).first() is None:
                break
            version += 1
        return new_nickname

    @property
    def is_authenticated(self):
        return True

    @property
    def is_active(self):
        return True

    @property
    def is_anonymous(self):
        return False

    def get_id(self):
        try:
            return unicode(self.id)  # python 2
        except NameError:
            return str(self.id)  # python 3

    def avatar(self, size):
        return 'http://www.gravatar.com/avatar/%s?d=mm&s=%d' % \
            (md5(self.email.encode('utf-8')).hexdigest(), size)

    def __repr__(self):
        return '<User %r>' % (self.nickname)

# TODO Do we need to have categories as well?
class Tag(db.Model):
    __searchable__ = ['name']
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200))
    timestamp = db.Column(db.DateTime)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id')) # last edit by

    def __repr__(self):
        return '<Tag %r>' % (self.name)

class Sound(db.Model):
    __searchable__ = ['name']
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200))
    url = db.Column(db.String(400))
    tags = db.relationship('Tag',
                               secondary=tags_sounds_table,
                               backref=db.backref('tags_for_sound', lazy='dynamic'),
                               lazy='dynamic')
    timestamp = db.Column(db.DateTime)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id')) # last edit by

    def __repr__(self):
        return '<Tag %r>' % (self.name)

class Description(db.Model):
    __searchable__ = ['description']
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(1000))
    attachement = db.Column(db.String(1000))
    duration = db.Column(db.Float)
    pitch = db.Column(db.Enum(Pitch))
    sound_type = db.Column(db.Enum(SoundType))
    sound_family = db.Column(db.Enum(SoundFamily))

class Validation(db.Model):
    __searchable__ = ['comment']
    id = db.Column(db.Integer, primary_key=True)
    comment = db.Column(db.String(1000))

if enable_search:
    whooshalchemy.whoosh_index(app, Sound)