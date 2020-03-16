from flask_wtf import FlaskForm
from wtforms import *
from wtforms.validators import DataRequired

class LoginForm(FlaskForm):
	Eusername = StringField('Username', validators=[DataRequired()])
	Epassword = PasswordField('Password', validators=[DataRequired()])
	Eremember_me = BooleanField('Remember Me')
	Esubmit = SubmitField('Sign In')

class SignupForm(FlaskForm):
	Eusername = StringField('Username', validators=[DataRequired()])
	Eidcard = StringField('id',validators=[DataRequired()])
	Egender = RadioField('Gender',validators=[DataRequired()])
	Eemail = StringField('Email', validators=[DataRequired()])
	Ehiredate = DateField('Date of employment (format: YYYY-MM-DD)', format='%Y-%m-%d', validators=[DataRequired()])
	Epassword = PasswordField('Password', validators=[DataRequired()])
	Epassword2 = PasswordField('Repeat Password', validators=[DataRequired()])
	Eaccept_rules = BooleanField('I accept the site rules', validators=[DataRequired()])
	Esubmit = SubmitField('Register')

class ArrangeAppointmentForm(FlaskForm):
	Epet = IntegerField('Pet id', validators=[DataRequired()])
	Etype = RadioField('type',validators=[DataRequired()])
	Edoc = IntegerField('Doctor id',validators=[DataRequired()])
	Ecomplete = BooleanField('If complete', validators=[DataRequired()])
	Einf = StringField('Information', validators=[DataRequired()])
	Edate = DateField('Date',validators=[DataRequired()])
	Ecost = IntegerField('Cost',validators=[DataRequired()])
	Esubmit = SubmitField('Register')




