from flask_wtf import FlaskForm, Form
from wtforms import StringField, FileField, SubmitField, PasswordField, BooleanField, IntegerField, RadioField, \
    DateField
from wtforms.validators import DataRequired, Length


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
    Etype = RadioField('type',validators=[DataRequired()])
    Edoc = IntegerField('Doctor id',validators=[DataRequired()])
    Ecomplete = BooleanField('If complete', validators=[DataRequired()])
    Einf = StringField('Information', validators=[DataRequired()])
    Edate = DateField('Date',validators=[DataRequired()])
    Ecost = IntegerField('Cost',validators=[DataRequired()])
    Esubmit = SubmitField('Register')


class AddProductForm(FlaskForm):
    Gid = IntegerField('Good id', validators=[DataRequired()])
    Gname = StringField('Good name', validators=[DataRequired()])
    Ginfo = StringField('Information', validators=[DataRequired()])
    Gimage = FileField('File', validators=[DataRequired()])
    Gprice = IntegerField('Good id', validators=[DataRequired()])
    Gadddate = DateField('AddDate',validators=[DataRequired()])
    Gsubmit = SubmitField('AddProduct')


class OrderForm(FlaskForm):
        Ordersubmit = SubmitField('Buy')


class LoginFormCustomer(Form):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired(), Length(8,128)])
    remember = BooleanField('Remember me')
    submit = SubmitField('Log in')


class SignupCustomer(Form):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired(), Length(8, 128)])
    phone = StringField('Phone', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired()])
    submit = SubmitField('Sign up')


class AddAppointment(Form):
    ownername = StringField('OwnerName', validators=[DataRequired()])
    ownerphone = StringField('OwnerPhone', validators=[DataRequired()])
    pettype = StringField('PetType', validators=[DataRequired()])
    otherdescription = StringField('OtherDescription', validators=[DataRequired()])
    submit = SubmitField('Submit')



