# By Pavlo Bazilinskyy <pavlo.bazilinskyy@gmail.com>
from flask.ext.wtf import Form
from flask_wtf.file import FileField, FileAllowed, FileRequired
from wtforms import StringField, BooleanField, TextAreaField, RadioField, SelectMultipleField, \
	SelectField, PasswordField
from wtforms.validators import DataRequired, Length, Optional, Email, EqualTo
from wtforms.widgets import TextArea
from config import SOUND_ALLOWED_EXTENSIONS
from models import Project, User, ClientUser, SupplierUser
from sound_types import sound_types
from sound_families import sound_families

class LoginForm(Form):
    remember_me = BooleanField('remember_me', default=False)
    username = StringField('Username')
    password = StringField('Password')

class EditUserForm(Form):
    nickname = StringField('nickname', validators=[DataRequired()])
    first_name = StringField('first_name', validators=[DataRequired()])
    last_name = StringField('last_name', validators=[DataRequired()])
    about_me = TextAreaField('about_me', validators=[Length(min=0, max=140)])
    receive_emails = BooleanField('receive_emails', default=True)
    upload_file = FileField('upload_file')
    email = StringField('email', validators=[DataRequired(), Email(message=None)])

    def __init__(self, original_nickname, *args, **kwargs):
        Form.__init__(self, *args, **kwargs)
        self.original_nickname = original_nickname

    def validate(self):
        if not Form.validate(self):
            return False
        if self.nickname.data == self.original_nickname:
            return True
        if self.nickname.data != User.make_valid_nickname(self.nickname.data):
            self.nickname.errors.append(
                'This nickname has invalid characters. '
                'Please use letters, numbers, dots and underscores only.')
            return False
        user = User.query.filter_by(nickname=self.nickname.data).first()
        if user is not None:
            self.nickname.errors.append(
                'This nickname is already in use. '
                'Please choose another one.')
            return False
        return True

class RegisterForm(Form):
    nickname = StringField(
        'nickname',
        validators=[DataRequired(), Length(min=3, max=25)]
    )
    email = StringField(
        'email',
        validators=[DataRequired(), Email(message=None)]
    )
    password = PasswordField(
        'password',
        validators=[DataRequired(), Length(min=8, max=15)]
    )
    confirm_pass = PasswordField(
        'Re-enter password',
        validators=[
            DataRequired(), EqualTo('password', message='Passwords should be the same.')
        ]
    )

    user_type = SelectField('user_type', choices=[('1','I need sounds'),('2','I make sounds')])

    def validate(self):
        if not Form.validate(self):
            return False
        if User.query.filter(User.email == self.email.data).all():
            self.email.errors.append("User with this email already exists!")
        if User.query.filter(User.nickname == self.nickname.data).all():
            self.nickname.errors.append("User with this nickname already exists!")
        return True

class EmailForm(Form):
    email = StringField('Email', validators=[DataRequired(), Email()])

class PasswordForm(Form):
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField('Password', validators=[DataRequired(), EqualTo(password)])

class SearchForm(Form):
    search = StringField('search', validators=[DataRequired()])

class DescriptionForm(Form):
    description = StringField('description', validators=[Optional(), Length(min=0, max=1000)], widget=TextArea())
    duration = StringField('duration', validators=[Optional()])
    pitch = StringField('pitch', validators=[Optional()])
    sound_type = RadioField('sound_type', choices=sound_types, default='1', validators=[DataRequired()])
    sound_family = SelectField('sound_family', choices=sound_families)
    upload_file = FileField('upload_file')
    notify_by_email = BooleanField('remember_me', default=False)
    tags = StringField('tags')
    sounds = StringField('sounds')

class VerificationForm(Form):
    description = StringField('description', validators=[Optional(), Length(min=0, max=1000)], widget=TextArea())
    upload_file = FileField('upload_file')
    notify_by_email = BooleanField('remember_me', default=False)

class IterationForm(Form):
    description = StringField('description', validators=[Optional(), Length(min=0, max=1000)], widget=TextArea())
    upload_file = FileField('upload_file')
    notify_by_email = BooleanField('remember_me', default=False)

class NewAssetForm(Form):
    name = StringField('name', validators=[DataRequired()])
    project = SelectField('project', validators=[DataRequired()])
    description = StringField('description', validators=[Optional(), Length(min=0, max=1000)], widget=TextArea())
    duration = StringField('duration', validators=[Optional()])
    pitch = StringField('pitch', validators=[Optional()])
    sound_type = RadioField('sound_type', choices=sound_types, default='1')
    sound_family = SelectField('sound_family', choices=sound_families)
    upload_file = FileField('upload_file')
    tags = StringField('tags')
    sounds = StringField('sounds')
    clients = SelectMultipleField('clients', validators=[DataRequired()])
    suppliers = SelectMultipleField('suppliers', validators=[DataRequired()])
    notify_by_email = BooleanField('remember_me', default=True)

class EditAssetForm(Form):
    name = StringField('name', validators=[DataRequired()])
    description = StringField('description', validators=[Optional(), Length(min=0, max=1000)], widget=TextArea())
    upload_file = FileField('upload_file')
    notify_by_email = BooleanField('remember_me', default=True)

class NewProjectForm(Form):
	name = StringField('name', validators=[DataRequired()])
	description = StringField('description', validators=[Optional(), Length(min=0, max=1000)], widget=TextArea())
	upload_file = FileField('upload_file')

class AddTagForm(Form):
	name = StringField('name', validators=[DataRequired()])

class EditTagForm(Form):
    name = StringField('name', validators=[DataRequired()])

class DeleteTagForm(Form):
	name = StringField('name', validators=[DataRequired()])

class DeleteSoundForm(Form):
	name = StringField('name', validators=[DataRequired()])

class AddSoundForm(Form):
	name = StringField('name', validators=[DataRequired()])
	description = StringField('description', validators=[Optional(), Length(min=0, max=1000)], widget=TextArea())
	sound_type = RadioField('sound_type', choices=sound_types, default='1', validators=[DataRequired()])
	sound_family = SelectField('sound_family', choices=sound_families)
	upload_file = FileField('upload_file', validators=[FileRequired(), FileAllowed(SOUND_ALLOWED_EXTENSIONS, 'Sounds only!')])
	tags = StringField('tags')
	rights = StringField('rights')

class EditSoundForm(Form):
    name = StringField('name', validators=[DataRequired()])
    description = StringField('description', validators=[Optional(), Length(min=0, max=1000)], widget=TextArea())
    sound_type = RadioField('sound_type', choices=sound_types, default='1', validators=[DataRequired()])
    sound_family = SelectField('sound_family', choices=sound_families)
    upload_file = FileField('upload_file', validators=[FileAllowed(SOUND_ALLOWED_EXTENSIONS, 'Sounds only!')])
    tags = StringField('tags')
    rights = StringField('rights')