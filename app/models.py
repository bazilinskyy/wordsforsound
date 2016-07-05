# By Pavlo Bazilinskyy <pavlo.bazilinskyy@gmail.com>
from hashlib import md5
from app import db
from app import app
from enum import Enum
import logging
import re
import sys
from config import WHOOSH_ENABLED

# import flask_whooshalchemyplus as whooshalchemy

if sys.version_info >= (3, 0):
    enable_search = False
else:
    enable_search = WHOOSH_ENABLED
    if enable_search:
        import flask.ext.whooshalchemy as whooshalchemy

tags_sounds_table = db.Table(
    'tags_for_sound',
    db.Column('sound_id', db.Integer, db.ForeignKey('sound.id')),
    db.Column('tag_id', db.Integer, db.ForeignKey('tag.id'))
)

suppliers_projects_table = db.Table(
    'suppliers_projects',
    db.Column('supplier_id', db.Integer, db.ForeignKey('supplier_user.id')),
    db.Column('project_id', db.Integer, db.ForeignKey('project.id'))
)

clients_projects_table = db.Table(
    'clients_projects',
    db.Column('client_id', db.Integer, db.ForeignKey('client_user.id')),
    db.Column('project_id', db.Integer, db.ForeignKey('project.id'))
)

suppliers_assets_table = db.Table(
    'suppliers_assets',
    db.Column('supplier_id', db.Integer, db.ForeignKey('supplier_user.id')),
    db.Column('asset_id', db.Integer, db.ForeignKey('asset.id'))
)

clients_assets_table = db.Table(
    'clients_assets',
    db.Column('client_id', db.Integer, db.ForeignKey('client_user.id')),
    db.Column('asset_id', db.Integer, db.ForeignKey('asset.id'))
)

followers = db.Table(
    'followers',
    db.Column('follower_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('followed_id', db.Integer, db.ForeignKey('user.id'))
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
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String(50)) #used for sqlalchemy inheritance
    nickname = db.Column(db.String(64), index=True, unique=True)
    first_name = db.Column(db.String(64))
    last_name = db.Column(db.String(64))
    email = db.Column(db.String(120), index=True, unique=True)
    password = db.Column(db.String)
    about_me = db.Column(db.String(140))
    last_seen = db.Column(db.DateTime)
    assets_in_hands = db.relationship('Asset', backref='user_in_hands', lazy='dynamic')

    followed = db.relationship('User',
                           secondary=followers,
                           primaryjoin=(followers.c.follower_id == id),
                           secondaryjoin=(followers.c.followed_id == id),
                           backref=db.backref('followers', lazy='dynamic'),
                           lazy='dynamic')

    def follow(self, user):
        if not self.is_following(user):
            self.followed.append(user)
            return self

    def unfollow(self, user):
        if self.is_following(user):
            self.followed.remove(user)
            return self

    def is_following(self, user):
        return self.followed.filter(
            followers.c.followed_id == user.id).count() > 0

    @property
    def full_name(self):
        return "%s %s"%(self.first_name, self.last_name)

    @staticmethod
    def make_valid_nickname(nickname):
        return re.sub('[^a-zA-Z0-9_\.]', '', nickname)

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

    def __repr__(self):  # pragma: no cover
        return '<User %r>' % (self.nickname)

    __mapper_args__ = {
        'polymorphic_identity':'user',
        'polymorphic_on':type
    }

class ClientUser(User):
    """A user that can submit requests to create assets"""
    __tablename__ = 'client_user'

    id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)

    __mapper_args__ = {
        'polymorphic_identity':'client_user',
    }

class SupplierUser(User):
    """A user that can submit requests to create assets"""
    __tablename__ = 'supplier_user'

    id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)

    __mapper_args__ = {
        'polymorphic_identity':'supplier_user',
    }  
        
class Tag(db.Model):
    __tablename__ = 'tag'
    __searchable__ = ['name']
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200))
    timestamp = db.Column(db.DateTime)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id')) # last edit by
    description_id = db.Column(db.Integer, db.ForeignKey('description.id'))

    def __repr__(self):
        return '<Tag %r>' % (self.name)

class Sound(db.Model):
    __tablename__ = 'sound'
    __searchable__ = ['name', 'filename', 'description']
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200))
    url = db.Column(db.String(400)) #location
    filename = db.Column(db.String(200))
    description = db.Column(db.String(1000))
    tags = db.relationship('Tag',
                           secondary=tags_sounds_table,
                           backref=db.backref('sounds', lazy='dynamic'),
                           lazy='dynamic')
    timestamp = db.Column(db.DateTime)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id')) # last edit by
    asset_id = db.Column(db.Integer, db.ForeignKey('asset.id'))
    sound_type = db.Column(db.String(20))
    sound_family = db.Column(db.String(20))
    rights = db.Column(db.String(200)) # To use enum instead

    def __repr__(self):
        return '<Sound %r>' % (self.name)

class Asset(db.Model):
    __tablename__ = 'asset'
    __searchable__ = ['name', 'description']
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200))
    finished  = db.Column(db.Boolean)
    status = db.Column(db.Integer)
    in_hands_id = db.Column(db.Integer, db.ForeignKey('user.id')) # User that needs to take action with the asset
    iteration_number = db.Column(db.Integer)
    description = db.Column(db.String(1000))
    sounds = db.relationship('Sound', backref='asset',
                                lazy='dynamic')
    filename = db.Column(db.String(200))
    timestamp = db.Column(db.DateTime)
    project_id = db.Column(db.Integer, db.ForeignKey('project.id'))
    descriptions = db.relationship('Description', backref='asset',
                                lazy='dynamic')
    verifications = db.relationship('Verification', backref='asset',
                                lazy='dynamic')
    iterations = db.relationship('Iteration', backref='asset',
                                lazy='dynamic')
    suppliers = db.relationship('SupplierUser',
                           secondary=suppliers_assets_table,
                           backref=db.backref('assets_for_supplier', lazy='dynamic'),
                           lazy='dynamic')
    clients = db.relationship('ClientUser',
                           secondary=clients_assets_table,
                           backref=db.backref('assets_for_client', lazy='dynamic'),
                           lazy='dynamic')

    def supplier_add(self, supplier):
        if supplier not in self.suppliers.all():
            self.suppliers.append(supplier)
            logging.debug("Project %s added supplier %s" % (str(self), str(supplier)))
            return self
        else:
            logging.debug("Project %s already has supplier %s: " % (str(self), str(supplier)))

    def supplier_remove(self, supplier):
        if supplier in self.suppliers.all():
            self.suppliers.remove(supplier)
            logging.debug("Project %s removed supplier %s" % (str(self), str(supplier)))
        else:
            logging.debug("Project %s does not haee supplier %s: " % (str(self), str(supplier)))

    def client_add(self, client):
        if client not in self.clients.all():
            self.clients.append(client)
            logging.debug("Project %s added client %s" % (str(self), str(client)))
            return self
        else:
            logging.debug("Project %s already has client %s: " % (str(self), str(client)))

    def client_remove(self, client):
        if client in self.clients.all():
            self.clients.remove(client)
            logging.debug("Project %s removed client %s" % (str(self), str(client)))
        else:
            logging.debug("Project %s does not haee client %s: " % (str(self), str(client)))

    @property
    def unique_name(self):
        return name + '-' + timestamp


class Description(db.Model):
    __tablename__ = 'description'
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
    __tablename__ = 'verification'
    __searchable__ = ['description']
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(1000))
    asset_id = db.Column(db.Integer, db.ForeignKey('asset.id'))
    timestamp = db.Column(db.DateTime)
    filename = db.Column(db.String(200))

class Iteration(db.Model):
    __tablename__ = 'iteration'
    __searchable__ = ['description']
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(1000))
    filename = db.Column(db.String(200))
    asset_id = db.Column(db.Integer, db.ForeignKey('asset.id'))
    timestamp = db.Column(db.DateTime)

class Project(db.Model):
    __tablename__ = 'project'
    __searchable__ = ['name', 'description']
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200))
    finished  = db.Column(db.Boolean)
    description = db.Column(db.String(1000))
    filename = db.Column(db.String(200))
    timestamp = db.Column(db.DateTime)
    assets = db.relationship('Asset', backref='project',
                                lazy='dynamic')
    suppliers = db.relationship('SupplierUser',
                           secondary=suppliers_projects_table,
                           backref=db.backref('projects_for_supplier', lazy='dynamic'),
                           lazy='dynamic')
    clients = db.relationship('ClientUser',
                           secondary=clients_projects_table,
                           backref=db.backref('projects_for_client', lazy='dynamic'),
                           lazy='dynamic')

    def supplier_add(self, supplier):
        if supplier not in self.suppliers.all():
            self.suppliers.append(supplier)
            logging.debug("Project %s added supplier %s" % (str(self), str(supplier)))
            return self
        else:
            logging.debug("Project %s already has supplier %s: " % (str(self), str(supplier)))

    def supplier_remove(self, supplier):
        if supplier in self.suppliers.all():
            self.suppliers.remove(supplier)
            logging.debug("Project %s removed supplier %s" % (str(self), str(supplier)))
        else:
            logging.debug("Project %s does not haee supplier %s: " % (str(self), str(supplier)))

    def client_add(self, client):
        if client not in self.clients.all():
            self.clients.append(client)
            logging.debug("Project %s added client %s" % (str(self), str(client)))
            return self
        else:
            logging.debug("Project %s already has client %s: " % (str(self), str(client)))

    def client_remove(self, client):
        if client in self.clients.all():
            self.clients.remove(client)
            logging.debug("Project %s removed client %s" % (str(self), str(client)))
        else:
            logging.debug("Project %s does not haee client %s: " % (str(self), str(client)))

    @property
    def unique_name(self):
        return name + '-' + timestamp

if enable_search:
    whooshalchemy.whoosh_index(app, Project)
    whooshalchemy.whoosh_index(app, Asset)
    whooshalchemy.whoosh_index(app, Tag)
    whooshalchemy.whoosh_index(app, Sound)
    # whooshalchemy.whoosh_index(app, User)