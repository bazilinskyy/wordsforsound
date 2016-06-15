# By Pavlo Bazilinskyy <pavlo.bazilinskyy@gmail.com>
from flask.ext.wtf import Form
from wtforms import StringField, BooleanField, TextAreaField, RadioField, SelectMultipleField, SelectField
from wtforms.validators import DataRequired, Length, Optional, Email, EqualTo
from wtforms.widgets import TextArea

# class LoginForm(Form):
#     openid = StringField('openid', validators=[DataRequired()])
#     remember_me = BooleanField('remember_me', default=False)

# class SearchForm(Form):
#     search = StringField('search', validators=[DataRequired()])

class DescriptionForm(Form):
	description = StringField('description', validators=[Optional(), Length(min=0, max=1000)], widget=TextArea())
	duration = StringField('duration', validators=[Optional()])
	pitch = StringField('pitch', validators=[Optional()])
	# form.area.choices = [(a.id, a.name) for a in Area.objects.all()]
	sound_type = RadioField('sound_type', choices=[('1', 'Earcon'),('2', 'Dynamic earcon'),('3', 'Spearcon')], validators=[DataRequired()])
	sound_family = SelectField('sound_family', choices=[('1','Warning'),('2','Notification'),('3','Confirmation'),('4','Status alert'),('5','Spatial')])

class NewAssetForm(Form):
	name = StringField('name', validators=[DataRequired()])
	description = StringField('description', validators=[Optional(), Length(min=0, max=1000)], widget=TextArea())
	duration = StringField('duration', validators=[Optional()])
	pitch = StringField('pitch', validators=[Optional()])
	# form.area.choices = [(a.id, a.name) for a in Area.objects.all()]
	sound_type = RadioField('sound_type', choices=[('1', 'Earcon'),('2', 'Dynamic earcon'),('3', 'Spearcon')], validators=[DataRequired()])
	sound_family = SelectField('sound_family', choices=[('1','Warning'),('2','Notification'),('3','Confirmation'),('4','Status alert'),('5','Spatial')])

class AddTagForm(Form):
	name = StringField('name', validators=[DataRequired()])

class AddSoundForm(Form):
	name = StringField('name', validators=[DataRequired()])
	description = StringField('description', validators=[Optional(), Length(min=0, max=1000)], widget=TextArea())
	# form.area.choices = [(a.id, a.name) for a in Area.objects.all()]
	sound_type = RadioField('sound_type', choices=[('1', 'Earcon'),('2', 'Dynamic earcon'),('3', 'Spearcon')], validators=[DataRequired()])
	sound_family = SelectField('sound_family', choices=[('1','Warning'),('2','Notification'),('3','Confirmation'),('4','Status alert'),('5','Spatial')])