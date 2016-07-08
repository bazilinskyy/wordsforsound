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
    # __searchable__ = ['nickname', 'first_name', 'last_name']
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
    descriptions = db.relationship('Description', backref='user', lazy='dynamic')
    iterations = db.relationship('Iteration', backref='user', lazy='dynamic')
    verifications = db.relationship('Verification', backref='user', lazy='dynamic')
    projects = db.relationship('Project', backref='user', lazy='dynamic')

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
    description_id = db.Column(db.Integer, db.ForeignKey('description.id'))
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
            logging.debug("Project %s does not have supplier %s: " % (str(self), str(supplier)))

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
            logging.debug("Project %s does not have client %s: " % (str(self), str(client)))

    def description_add(self, description):
        if description not in self.descriptions.all():
            self.descriptions.append(description)
            logging.debug("Project %s added description %s" % (str(self), str(description)))
            return self
        else:
            logging.debug("Project %s already has description %s: " % (str(self), str(description)))

    def description_remove(self, description):
        if description in self.descriptions.all():
            self.descriptions.remove(description)
            logging.debug("Project %s removed description %s" % (str(self), str(description)))
        else:
            logging.debug("Project %s does not have description %s: " % (str(self), str(description)))

    def iteration_add(self, iteration):
        if iteration not in self.iterations.all():
            self.iterations.append(iteration)
            logging.debug("Project %s added iteration %s" % (str(self), str(iteration)))
            return self
        else:
            logging.debug("Project %s already has iteration %s: " % (str(self), str(iteration)))

    def iteration_remove(self, iteration):
        if iteration in self.iterations.all():
            self.iterations.remove(iteration)
            logging.debug("Project %s removed iteration %s" % (str(self), str(iteration)))
        else:
            logging.debug("Project %s does not have iteration %s: " % (str(self), str(iteration)))

    def verification_add(self, verification):
        if verification not in self.verifications.all():
            self.verifications.append(verification)
            logging.debug("Project %s added verification %s" % (str(self), str(verification)))
            return self
        else:
            logging.debug("Project %s already has verification %s: " % (str(self), str(verification)))

    def verification_remove(self, verification):
        if verification in self.verifications.all():
            self.verifications.remove(verification)
            logging.debug("Project %s removed verification %s" % (str(self), str(verification)))
        else:
            logging.debug("Project %s does not have verification %s: " % (str(self), str(verification)))

    def get_last_description(self):
        if self.descriptions.count() != 0:
            description = self.descriptions[-1]
            logging.debug("Project %s\'s last description is %s" % (str(self), str(description)))
            return description
        else:
            logging.debug("Project %s does not have any descriptions to get the last description." % (str(self)))
            return None

    def get_last_iteration(self):
        if self.iterations.count() != 0:
            iteration = self.iterations[-1]
            logging.debug("Project %s\'s last iteration is %s" % (str(self), str(iteration)))
            return iteration
        else:
            logging.debug("Project %s does not have any iterations to get the last iteration." % (str(self)))
            return None

    def get_last_verification(self):
        if self.verifications.count() != 0:
            verification = self.verifications[-1]
            logging.debug("Project %s\'s last verification is %s" % (str(self), str(verification)))
            return verification
        else:
            logging.debug("Project %s does not have any verifications to get the last verification." % (str(self)))
            return None

    def init_in_hands(self):
        self.in_hands_id = self.suppliers[0].id  # After creating the request for the asset the \
                                                 # first user to work on it is the first supplier  

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
    user_id = db.Column(db.Integer, db.ForeignKey('user.id')) # last edit by
    tags = db.relationship('Tag', backref='asset',
                            lazy='dynamic')
    sounds = db.relationship('Sound', backref='description_entity',
                            lazy='dynamic')

    def get_sound_type(self):
        if self.sound_type == '1':
            return 'Earcon'
        elif self.sound_type == '2':
            return 'Dynamic earcon'
        elif self.sound_type == '3':
            return 'Spearcon'
        else:
             return 'Unkonwn type'

    def get_sound_family(self):
        if self.sound_family == '1':
            return 'Warning'
        elif self.sound_family == '2':
            return 'Notification'
        elif self.sound_family == '3':
            return 'Confirmation'
        elif self.sound_family == '4':
            return 'Status alert'
        else:
             return 'Unkonwn family'

    def get_pitch(self):
        if len(self.pitch) != 0:
            return self.pitch
        else:
            return 'N/A'

    def get_duration(self):
        if len(self.duration) != 0:
            return self.duration
        else:
            return 'N/A'

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
    user_id = db.Column(db.Integer, db.ForeignKey('user.id')) # last edit by

class Iteration(db.Model):
    __tablename__ = 'iteration'
    __searchable__ = ['description']
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(1000))
    filename = db.Column(db.String(200))
    asset_id = db.Column(db.Integer, db.ForeignKey('asset.id'))
    timestamp = db.Column(db.DateTime)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id')) # last edit by

class Project(db.Model):
    __tablename__ = 'project'
    __searchable__ = ['name', 'description']
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200))
    finished  = db.Column(db.Boolean)
    description = db.Column(db.String(1000))
    filename = db.Column(db.String(200))
    timestamp = db.Column(db.DateTime)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id')) # last edit by
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

    def asset_add(self, asset):
        if asset not in self.assets.all():
            self.assets.append(asset)
            logging.debug("Project %s added asset %s" % (str(self), str(asset)))
        else:
            logging.debug("Project %s already has asset %s: " % (str(self), str(asset)))

    def asset_remove(self, asset):
        if asset in self.assets.all():
            self.assets.remove(asset)
            logging.debug("Project %s removed asset %s" % (str(self), str(asset)))
        else:
            logging.debug("Project %s does not haee asset %s: " % (str(self), str(asset)))

    @property
    def unique_name(self):
        return name + '-' + timestamp

if enable_search:
    whooshalchemy.whoosh_index(app, Project)
    whooshalchemy.whoosh_index(app, Asset)
    whooshalchemy.whoosh_index(app, Tag)
    whooshalchemy.whoosh_index(app, Sound)
    # whooshalchemy.whoosh_index(app, User)