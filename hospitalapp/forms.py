from flask_wtf import FlaskForm, Form
from wtforms import StringField, FileField, SubmitField, PasswordField, BooleanField, IntegerField, RadioField, \
    DateField, TextField, SelectField
from wtforms.validators import DataRequired, Length
from wtforms.ext.sqlalchemy.fields import QuerySelectField 
from flask_wtf.file import FileField, FileAllowed, FileRequired
from hospitalapp import photos


class LoginFormEmployee(FlaskForm):
    Eusername = StringField('Username', validators=[DataRequired()])
    Epassword = PasswordField('Password', validators=[DataRequired()])
    Eremember_me = BooleanField('Remember Me')
    Esubmit = SubmitField('Sign In')


class SignupFormEmployee(FlaskForm):
    Eusername = StringField('Username', validators=[DataRequired()])
    Eidcard = StringField('id', validators=[DataRequired()])
    Ephone = StringField('phone', validators=[DataRequired()])
    Egender = RadioField('Gender', choices=[('0', 'Male'), ('1', 'Female')], validators=[DataRequired()])
    Eemail = StringField('Email', validators=[DataRequired()])
    Ehiredate = DateField('Date of employment (format: YYYY-MM-DD)', format='%Y-%m-%d', validators=[DataRequired()])
    Epassword = PasswordField('Password', validators=[DataRequired()])
    Epassword2 = PasswordField('Repeat Password', validators=[DataRequired()])
    Esubmit = SubmitField('Register')


class ArrangeAppointmentFormEmployee(FlaskForm):
    Epet = IntegerField('Pet id', validators=[DataRequired()])
    Etype = RadioField('Type', choices=[('0', 'Emergency'), ('1', 'Standard')], validators=[DataRequired()])
    Edoc = StringField('Doctor', validators=[DataRequired()])
    Ecomplete = RadioField('Complete', choices=[('0', 'Complete'), ('1', 'Not Complete')], validators=[DataRequired()])
    Einf = StringField('Information', validators=[DataRequired()])
    Edate = DateField('Date of appointment (format: YYYY-MM-DD)', format='%Y-%m-%d', validators=[DataRequired()])
    Ecost = StringField('Cost', validators=[DataRequired()])
    Esubmit = SubmitField('Submit')

class ModyAppointmentFormEmployee(FlaskForm):
    Epet = IntegerField(label='Pet id',render_kw={
        'class':"form-control",
        'placeholder':'Please enter pet number'
    }, validators=[DataRequired()])
    Etype = RadioField(label='Type', choices=[('0', 'Emergency'), ('1', 'Standard')], render_kw={
        'class':"form-control",
        'placeholder':'Please choose the type'
    },validators=[DataRequired()])
    Edoc = StringField(label='Doctor', render_kw={
        'class':"form-control",
        'placeholder':'Please enter doctor number'
    },validators=[DataRequired()])
    Ecomplete = RadioField(label='Complete', choices=[('0', 'Complete'), ('1', 'Not Complete')], render_kw={
        'class':"form-control",
        'placeholder':'Please choose complete status'
    },validators=[DataRequired()])
    Einf = StringField(label='Information',render_kw={
        'class':"form-control",
        'placeholder':'Please enter the information'
    }, validators=[DataRequired()])
    Edate = DateField(label='Date of appointment (format: YYYY-MM-DD)', format='%Y-%m-%d',render_kw={
        'class':"form-control",
        'placeholder':'Please enter date'
    }, validators=[DataRequired()])
    Ecost = StringField(label='Cost', render_kw={
        'class':"form-control",
        'placeholder':'Please enter the cost'
    },validators=[DataRequired()])
    Esubmit = SubmitField('Submit')

class AddProductForm(FlaskForm):
    Gid = IntegerField('Good id', validators=[DataRequired()])
    Gname = StringField('Good name', validators=[DataRequired()])
    Ginfo = StringField('Information', validators=[DataRequired()])
    photo = FileField('File', validators=[FileRequired(),
    FileAllowed(photos, "images only")])
    Gprice = IntegerField('Good price', validators=[DataRequired()])
    Gadddate = DateField('AddDate',validators=[DataRequired()])
    submit = SubmitField('AddProduct')

class PrescriptionForm(FlaskForm):
    Pmed = StringField('Medicine', validators=[DataRequired()])
    Pnumber = StringField('Number', validators=[DataRequired()])
    Pappointment = StringField('Appointment', validators=[DataRequired()])
    submit = SubmitField('Make prescription')

class HospitalizationForm(FlaskForm):
    appointment = StringField('Appointment', validators=[DataRequired()])
    doc = StringField('Doctor', validators=[DataRequired()])
    room = StringField('Room', validators=[DataRequired()])
    startdate = DateField('Start Date (format: YYYY-MM-DD)', format='%Y-%m-%d', validators=[DataRequired()])
    enddate = DateField('End Date (format: YYYY-MM-DD)', format='%Y-%m-%d', validators=[DataRequired()])
    cost = StringField('Cost', validators=[DataRequired()])
    submit = SubmitField('Manage Hospitalization')

class OrderForm(FlaskForm):
        Ordersubmit = SubmitField('Buy')


class LoginFormCustomer(FlaskForm):
    Cusername = StringField('Username', validators=[DataRequired()])
    Cpassword = PasswordField('Password', validators=[DataRequired(), Length(8, 128)])
    Cremember_me = BooleanField('Remember me')
    Csubmit = SubmitField('Log in')


class SignupCustomer(FlaskForm):
    Cusername = StringField('Username', validators=[DataRequired()])
    Cpassword = PasswordField('Password', validators=[DataRequired(), Length(8, 128)])
    Cpassword2 = PasswordField('Repeat Your Password', validators=[DataRequired(), Length(8, 128)])
    Cgender = RadioField('Gender', choices=[('1', 'Male'), ('2', 'Female')], default=1, validators=[DataRequired()])
    Cphone = StringField('Phone', validators=[DataRequired()])
    Cemail = StringField('Email', validators=[DataRequired()])
    Caccept_rules = BooleanField('I accept the site rules', validators=[DataRequired()])
    Csubmit = SubmitField('Sign up')


class MakeAppointment(FlaskForm):
    ownername = StringField('OwnerName', validators=[DataRequired()])
    ownerphone = StringField('OwnerPhone', validators=[DataRequired()])
    pettype = StringField('PetType', validators=[DataRequired()])
    otherdescription = StringField('OtherDescription', validators=[DataRequired()])
    submit = SubmitField('Submit')



