# By Pavlo Bazilinskyy <pavlo.bazilinskyy@gmail.com>
from hashlib import md5
from app import db
from app import app
from enum import Enum

import sys
# if sys.version_info >= (3, 0):
#     enable_search = False
# else:
#     enable_search = True
#     import flask.ext.whooshalchemy as whooshalchemy

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

class AssetStatus(Enum):
    description = 1
    iteration = 2
    verification = 3
    finished = 4

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nickname = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    about_me = db.Column(db.String(140))
    last_seen = db.Column(db.DateTime)
    # role
    # password

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
    description_id = db.Column(db.Integer, db.ForeignKey('description.id'))

    def __repr__(self):
        return '<Tag %r>' % (self.name)

class Sound(db.Model):
    __searchable__ = ['name']
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200))
    url = db.Column(db.String(400)) #location
    filename = db.Column(db.String(200))
    description = db.Column(db.String(1000))
    tags = db.relationship('Tag',
                               secondary=tags_sounds_table,
                               backref=db.backref('tags_for_sound', lazy='dynamic'),
                               lazy='dynamic')
    timestamp = db.Column(db.DateTime)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id')) # last edit by
    asset_id = db.Column(db.Integer, db.ForeignKey('asset.id'))
    sound_type = db.Column(db.String(20))
    sound_family = db.Column(db.String(20))

    def __repr__(self):
        return '<Sound %r>' % (self.name)

class Asset(db.Model):
    __searchable__ = ['name']
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200))
    finished  = db.Column(db.Boolean)
    status = db.Column(db.Integer)
    iteration_number = db.Column(db.Integer)
    description = db.Column(db.String(1000))
    sounds = db.relationship('Sound', backref='asset',
                                lazy='dynamic')
    filename = db.Column(db.String(200))
    project_id = db.Column(db.Integer, db.ForeignKey('project.id'))
    descriptions = db.relationship('Description', backref='asset',
                                lazy='dynamic')
    verifications = db.relationship('Verification', backref='asset',
                                lazy='dynamic')
    iterations = db.relationship('Iteration', backref='asset',
                                lazy='dynamic')
    timestamp = db.Column(db.DateTime)

    @property
    def unique_name(self):
        return name + '-' + timestamp


class Description(db.Model):
    __searchable__ = ['description']
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(1000))
    attachement = db.Column(db.String(1000))
    duration = db.Column(db.String(20))
    timestamp = db.Column(db.DateTime)
    # pitch = db.Column(db.Enum(Pitch))
    pitch = db.Column(db.String(20))
    # sound_type = db.Column(db.Enum(SoundType))
    sound_type = db.Column(db.String(20))
    # sound_family = db.Column(db.Enum(SoundFamily))
    sound_family = db.Column(db.String(20))
    asset_id = db.Column(db.Integer, db.ForeignKey('asset.id'))
    filename = db.Column(db.String(200))
    tags = db.relationship('Tag', backref='asset',
                            lazy='dynamic')

    def __repr__(self):
        return '<Description %r>' % (self.description[0:50])

class Verification(db.Model):
    __searchable__ = ['description']
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(1000))
    asset_id = db.Column(db.Integer, db.ForeignKey('asset.id'))
    timestamp = db.Column(db.DateTime)
    filename = db.Column(db.String(200))

class Iteration(db.Model):
    __searchable__ = ['description']
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(1000))
    filename = db.Column(db.String(200))
    asset_id = db.Column(db.Integer, db.ForeignKey('asset.id'))
    timestamp = db.Column(db.DateTime)

class Project(db.Model):
    __searchable__ = ['name']
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200))
    finished  = db.Column(db.Boolean)
    description = db.Column(db.String(1000))
    filename = db.Column(db.String(200))
    assets = db.relationship('Asset', backref='project',
                                lazy='dynamic')
    timestamp = db.Column(db.DateTime)

    @property
    def unique_name(self):
        return name + '-' + timestamp

# if enable_search:
#     whooshalchemy.whoosh_index(app, Sound)