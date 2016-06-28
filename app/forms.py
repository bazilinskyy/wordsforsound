# By Pavlo Bazilinskyy <pavlo.bazilinskyy@gmail.com>
from flask.ext.wtf import Form
from flask_wtf.file import FileField, FileAllowed, FileRequired
from wtforms import StringField, BooleanField, TextAreaField, RadioField, SelectMultipleField, SelectField
from wtforms.validators import DataRequired, Length, Optional, Email, EqualTo
from wtforms.widgets import TextArea
from config import SOUND_ALLOWED_EXTENSIONS
from models import Project
# from flask.ext.uploads import UploadSet, SOUNDS
# sounds = UploadSet('audio', AUDIO)

# class LoginForm(Form):
#     openid = StringField('openid', validators=[DataRequired()])
#     remember_me = BooleanField('remember_me', default=False)

# class SearchForm(Form):
#     search = StringField('search', validators=[DataRequired()])

def get_projects():
	projects = Project.query.all()
	choices = []
	for project in projects:
		choices.append((str(project.id), project.name))
	return choices

class DescriptionForm(Form):
	description = StringField('description', validators=[Optional(), Length(min=0, max=1000)], widget=TextArea())
	duration = StringField('duration', validators=[Optional()])
	pitch = StringField('pitch', validators=[Optional()])
	# form.area.choices = [(a.id, a.name) for a in Area.objects.all()]
	sound_type = RadioField('sound_type', choices=[('1', 'Earcon'),('2', 'Dynamic earcon'),('3', 'Spearcon')], default='1', validators=[DataRequired()])
	sound_family = SelectField('sound_family', choices=[('1','Warning'),('2','Notification'),('3','Confirmation'),('4','Status alert')])
	upload_file = FileField('upload_file')

class VerificationForm(Form):
	description = StringField('description', validators=[Optional(), Length(min=0, max=1000)], widget=TextArea())
	upload_file = FileField('upload_file')

class IterationForm(Form):
	description = StringField('description', validators=[Optional(), Length(min=0, max=1000)], widget=TextArea())
	upload_file = FileField('upload_file')

class NewAssetForm(Form):
	name = StringField('name', validators=[DataRequired()])
	# project = StringField('project', validators=[DataRequired()])
	project = SelectField('project', choices=get_projects())
	description = StringField('description', validators=[Optional(), Length(min=0, max=1000)], widget=TextArea())
	duration = StringField('duration', validators=[Optional()])
	pitch = StringField('pitch', validators=[Optional()])
	# form.area.choices = [(a.id, a.name) for a in Area.objects.all()]
	sound_type = RadioField('sound_type', choices=[('1', 'Earcon'),('2', 'Dynamic earcon'),('3', 'Spearcon')], default='1')
	sound_family = SelectField('sound_family', choices=[('1','Warning'),('2','Notification'),('3','Confirmation'),('4','Status alert')])
	upload_file = FileField('upload_file')
	tags = StringField('tags')

class NewProjectForm(Form):
	name = StringField('name', validators=[DataRequired()])
	description = StringField('description', validators=[Optional(), Length(min=0, max=1000)], widget=TextArea())
	upload_file = FileField('upload_file')

class AddTagForm(Form):
	name = StringField('name', validators=[DataRequired()])

class DeleteTagForm(Form):
	name = StringField('name', validators=[DataRequired()])

class DeleteSoundForm(Form):
	name = StringField('name', validators=[DataRequired()])

class AddSoundForm(Form):
	name = StringField('name', validators=[DataRequired()])
	description = StringField('description', validators=[Optional(), Length(min=0, max=1000)], widget=TextArea())
	sound_type = RadioField('sound_type', choices=[('1', 'Earcon'),('2', 'Dynamic earcon'),('3', 'Spearcon')], default='1', validators=[DataRequired()])
	sound_family = SelectField('sound_family', choices=[('1','Warning'),('2','Notification'),('3','Confirmation'),('4','Status alert')])
	upload_file = FileField('upload_file', validators=[FileRequired(), FileAllowed(SOUND_ALLOWED_EXTENSIONS, 'Sounds only!')])
	tags = StringField('tags')
	rights = StringField('rights', validators=[DataRequired()])
	# upload_file = FileField('upload_file', validators=[FileRequired(), FileAllowed(audio, 'Sounds only!')])

class EditSoundForm(Form):
	name = StringField('name', validators=[DataRequired()])
	description = StringField('description', validators=[Optional(), Length(min=0, max=1000)], widget=TextArea())
	sound_type = RadioField('sound_type', choices=[('1', 'Earcon'),('2', 'Dynamic earcon'),('3', 'Spearcon')], default='1', validators=[DataRequired()])
	sound_family = SelectField('sound_family', choices=[('1','Warning'),('2','Notification'),('3','Confirmation'),('4','Status alert')])
	upload_file = FileField('upload_file', validators=[FileRequired(), FileAllowed(SOUND_ALLOWED_EXTENSIONS, 'Sounds only!')])
	tags = StringField('tags')