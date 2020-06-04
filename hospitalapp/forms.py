from flask_wtf import FlaskForm, Form
from wtforms import StringField, FileField, SubmitField, PasswordField, BooleanField, IntegerField, RadioField, \
    DateField, TextField, SelectField,TextAreaField,DateTimeField
from wtforms.validators import DataRequired, Length, Regexp, EqualTo
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from flask_wtf.file import FileField, FileAllowed, FileRequired
from hospitalapp import photos, db
from hospitalapp.models import Pet, Doctor


class LoginFormEmployee(FlaskForm):
    Eusername = StringField('Username', validators=[DataRequired()])
    Epassword = PasswordField('Password', validators=[DataRequired()])
    Eremember_me = BooleanField('Remember Me')
    Esubmit = SubmitField('Sign In')


class LoginFormEmployee_chinese(FlaskForm):
    Eusername = StringField('用户名', validators=[DataRequired()])
    Epassword = PasswordField('密码', validators=[DataRequired()])
    Eremember_me = BooleanField('记住密码')
    Esubmit = SubmitField('登录')


class SignupFormEmployee(FlaskForm):
    Eusername = StringField('Username', validators=[DataRequired(),Regexp('^[a-zA-Z0-9]*$',
message='The username should contain only a-z, A-Z and 0-9.')])
    Eidcard = StringField('ID Card Number', validators=[DataRequired()])
    Ephone = StringField('phone', validators=[DataRequired()])
    Egender = RadioField('Gender', choices=[('0', 'Male'), ('1', 'Female')], validators=[DataRequired()])
    Eemail = StringField('Email', validators=[DataRequired()])
    Ehiredate = DateField('Date of employment ', format='%Y/%m/%d', validators=[DataRequired()])
    Epassword = PasswordField('Password', validators=[DataRequired(),Length(8, 25), EqualTo('Epassword2')])
    Epassword2 = PasswordField('Repeat Password', validators=[DataRequired(),Length(8, 25)])
    Esubmit = SubmitField('Register')



class ArrangeAppointmentFormEmployee(FlaskForm):
    Epet = IntegerField('Pet id', validators=[DataRequired()])
    Etype = RadioField('Type', choices=[('0', 'Emergency'), ('1', 'Standard')], validators=[DataRequired()])
    Edoc = StringField('Doctor', validators=[DataRequired()])
    Ecomplete = RadioField('Complete', choices=[('0', 'Complete'), ('1', 'Not Complete')], validators=[DataRequired()])
    Einf = StringField('Information', validators=[DataRequired()])
    Edate = DateField('Date of appointment ', format='%Y/%m/%d', validators=[DataRequired()])
    Ecost = StringField('Cost', validators=[DataRequired()])
    Esubmit = SubmitField('Submit')


class ModyAppointmentFormEmployee(FlaskForm):
    Epet = IntegerField(label='Pet id', render_kw={
        'class': "form-control",
        # 'placeholder': 'Please enter pet number'
    }, validators=[DataRequired()])
    Etype = RadioField(label='Type', choices=[('0', 'Emergency'), ('1', 'Standard')], render_kw={
        'class': "form-control",
        # 'placeholder': 'Please choose the type'
    }, validators=[DataRequired()])
    Edoc = StringField(label='Doctor', render_kw={
        'class': "form-control",
        'placeholder': 'Please enter doctor number'
    }, validators=[DataRequired()])
    Ecomplete = RadioField(label='Complete', choices=[('0', 'Complete'), ('1', 'Not Complete')], render_kw={
        'class': "form-control",
        'placeholder': 'Please choose complete status'
    }, validators=[DataRequired()])
    Einf = StringField(label='Information', render_kw={
        'class': "form-control",
        'placeholder': 'Please enter the information'
    }, validators=[DataRequired()])
    Edate = DateField(label='Date of appointment', format='%Y/%m/%d', render_kw={
        'class': "form-control",
        'placeholder': 'Please enter date'
    }, validators=[DataRequired()])
    Ecost = StringField(label='Cost', render_kw={
        'class': "form-control",
        'placeholder': 'Please enter the cost'
    }, validators=[DataRequired()])
    Esubmit = SubmitField('Submit')


class AddOperationForm(FlaskForm):
    Odate = DateField(label='Date of appointment ', format='%Y/%m/%d', render_kw={
        'class': "form-control",
        # 'placeholder': 'Please enter date'
    }, validators=[DataRequired()])
    Oinf = StringField(label='Information', render_kw={
        'class': "form-control",
        # 'placeholder': 'Please enter the information'
    }, validators=[DataRequired()])
    Ocost = StringField(label='Cost(Please enter number)', render_kw={
        'class': "form-control",
        # 'placeholder': 'Please enter the Cost'
    }, validators=[DataRequired()])
    Osubmit = SubmitField('Inform Customer of Operation')


class AddHospitalizationForm(FlaskForm):
    room = StringField(label='Room', render_kw={
        'class': "form-control",
        # 'placeholder': 'Please enter the Room'
    }, validators=[DataRequired()])
    startdate = DateField(label='Start date ', format='%Y-%m-%d', render_kw={
        'class': "form-control",
        # 'placeholder': 'Please enter start date'
    }, validators=[DataRequired()])
    enddate = DateField(label='End date ', format='%Y-%m-%d', render_kw={
        'class': "form-control",
        # 'placeholder': 'Please enter end date'
    }, validators=[DataRequired()])
    cost = StringField(label='Cost (Please enter number)', render_kw={
        'class': "form-control",
        # 'placeholder': 'Please enter the Cost'
    }, validators=[DataRequired()])
    submit = SubmitField('Inform customer of inpatient')


class AddPrescriptionForm(FlaskForm):
    medicine = StringField(label='Medicine', render_kw={
        'class': "form-control",
        # 'placeholder': 'Please enter the Medicine'
    }, validators=[DataRequired()])
    number = StringField(label='Number', render_kw={
        'class': "form-control",
        # 'placeholder': 'Please enter the Number'
    }, validators=[DataRequired()])
    submit = SubmitField('Confirm')


class CompleteOperationConfirmForm(FlaskForm):
    complete = RadioField(label='Complete', choices=[('0', 'Complete'), ('1', 'Not Complete')], render_kw={
        'class': "form-control",
        # 'placeholder': 'Please choose complete status'
    }, validators=[DataRequired()])
    submit = SubmitField('Confirm')


class AddProductForm(FlaskForm):
    Gid = IntegerField(label='Good id',
                       render_kw={'class': "form-control",
                                  'placeholder': "Please enter id in integers"},
                       validators=[DataRequired("This part is required")])
    Gname = StringField(label='Good name',
                        render_kw={'class': "form-control",
                                   'placeholder': "Please enter name"},
                        validators=[DataRequired("This part is required")])
    Ginfo = StringField(label='Information',
                        render_kw={'class': "form-control",
                                   'placeholder': "Please enter information"},
                        validators=[DataRequired("This part is required")])
    photo = FileField('File', validators=[FileRequired("This part is required"),
                                          FileAllowed(photos, "images only")])
    Gprice = IntegerField(label='Good price',
                          render_kw={'class': "form-control",
                                     'placeholder': "Please enter price in numbers"},
                          validators=[DataRequired("This part is required")])
    Gadddate = DateField(label='AddDate',
                         render_kw={'class': "form-control",
                                    'placeholder': "Please enter date in the form of YYYY-MM-DD"},
                         validators=[DataRequired("This part is required")])
    submit = SubmitField('submit')


class AddProductForm_chinese(FlaskForm):
    Gid = IntegerField('货物编号', validators=[DataRequired()])
    Gname = StringField('货物名称', validators=[DataRequired()])
    Ginfo = StringField('信息', validators=[DataRequired()])
    photo = FileField('上传图片', validators=[FileRequired(),
                                          FileAllowed(photos, "images only")])
    Gprice = IntegerField('货物价格', validators=[DataRequired()])
    Gadddate = DateField('添加日期', validators=[DataRequired()])
    submit = SubmitField('提交')

class ProductNumberForm(FlaskForm):
    number = IntegerField('number', validators=[DataRequired()])
    submit = SubmitField('Buy')


class PrescriptionForm(FlaskForm):
    Pmed = StringField('Medicine', validators=[DataRequired()])
    Pnumber = StringField('Number', validators=[DataRequired()])
    Pappointment = StringField('Appointment', validators=[DataRequired()])
    submit = SubmitField('Make prescription')


class HospitalizationForm(FlaskForm):
    appointment = StringField('Appointment', validators=[DataRequired()])
    doc = StringField('Doctor', validators=[DataRequired()])
    room = StringField('Room', validators=[DataRequired()])
    startdate = DateField('Start Date (', format='%Y/%m/%d', validators=[DataRequired()])
    enddate = DateField('End Date ', format='%Y/%m/%d', validators=[DataRequired()])
    cost = StringField('Cost', validators=[DataRequired()])
    submit = SubmitField('Manage Hospitalization')

class OrderForm(FlaskForm):
    Oname = StringField('Name', validators=[DataRequired()])
    Oaddress = StringField('Address', validators=[DataRequired()])
    Ophonenumber = IntegerField('phonenumber', validators=[DataRequired()])
    submit = SubmitField('Pay')

class PayForm(FlaskForm):
    cardnumber = IntegerField('creditcard', validators=[DataRequired()])
    password = IntegerField('password', validators=[DataRequired()])
    submit = SubmitField('Pay')

class LoginFormCustomer(FlaskForm):
    Cusername = StringField('Username', validators=[DataRequired()])
    Cpassword = PasswordField('Password', validators=[DataRequired(), Length(8, 128)])
    Cremember_me = BooleanField('Remember me')
    Csubmit = SubmitField('Log in')


class LoginFormCustomer_chinese(FlaskForm):
    Cusername = StringField('用户名', validators=[DataRequired()])
    Cpassword = PasswordField('密码', validators=[DataRequired(), Length(8, 128)])
    Cremember_me = BooleanField('记住密码')
    Csubmit = SubmitField('登录')


class SignupCustomer(FlaskForm):
    Cusername = StringField('Username', validators=[DataRequired(),Length(8, 30), Regexp('^[a-zA-Z0-9]*$',
message='The username should contain only a-z, A-Z and 0-9.')])
    Cpassword = PasswordField('Password', validators=[DataRequired(), Length(8, 25), EqualTo('Cpassword2')])
    Cpassword2 = PasswordField('Repeat Your Password', validators=[DataRequired(), Length(8, 25)])
    Cgender = RadioField('Gender', choices=[('1', 'Male'), ('2', 'Female')], default=1, validators=[DataRequired()])
    Cphone = StringField('Phone', validators=[DataRequired()])
    Cemail = StringField('Email', validators=[DataRequired()])
    Caccept_rules = BooleanField('I accept the site rules', validators=[DataRequired()])
    Csubmit = SubmitField('Sign up')


class SignupCustomer_chinese(FlaskForm):
    Cusername = StringField('用户名', validators=[DataRequired()])
    Cpassword = PasswordField('密码', validators=[DataRequired(), Length(8, 128)])
    Cpassword2 = PasswordField('请再次输入你的密码', validators=[DataRequired(), Length(8, 128)])
    Cgender = RadioField('性别', choices=[('1', '男'), ('2', '女')], default=1, validators=[DataRequired()])
    Cphone = StringField('电话', validators=[DataRequired()])
    Cemail = StringField('邮件', validators=[DataRequired()])
    Caccept_rules = BooleanField('我接受这个请求', validators=[DataRequired()])
    Csubmit = SubmitField('注册')


class PostForm(FlaskForm):
    topic = StringField(label='Topic', render_kw={
        'class': "form-control",
        'placeholder': 'Please enter your post'
    }, validators=[DataRequired()])
    content = TextAreaField(label='Content', render_kw={
        'class': "form-control",
        'placeholder': 'Please enter the content'
    }, validators=[DataRequired()])
    submit = SubmitField('Submit')


class AnswerForm(FlaskForm):
    content = TextAreaField(label='Content', render_kw={
        'class': "form-control",
        'placeholder': 'Please enter the answer'
    }, validators=[DataRequired()])
    submit = SubmitField('Confirm')

class PostForm(FlaskForm):
    topic = StringField(label='Topic', render_kw={
        'class': "form-control",
        'placeholder': 'Please enter your post'
    }, validators=[DataRequired()])
    content = TextAreaField(label='Content', render_kw={
        'class': "form-control",
        'placeholder': 'Please enter the content'
    }, validators=[DataRequired()])
    submit = SubmitField('Submit')

class PetForm(FlaskForm):
    name = StringField(label='Pet Name', render_kw={
        'class': "form-control",
        'placeholder': 'Please enter your pet name'
    }, validators=[DataRequired()])
    type = RadioField('Species',coerce=int, choices=[("cat", 'Cat'), ("dog", 'Dog')], render_kw={
        'class': "form-control",
        'placeholder': 'Please choose your pet species'
    }, validators=[DataRequired()])
    age = RadioField(label='Pet Age', render_kw={
        'class': "form-control",
        'placeholder': 'Please enter your pet age'
    }, validators=[DataRequired()])
    gender = RadioField(label='Pet Gender', choices=[('1', 'Male'), ('2', 'Female')], render_kw={
        'class': "form-control",
        'placeholder': 'Please choose your pet gendeer'
    }, validators=[DataRequired()])
    info = TextAreaField(label='Other information', render_kw={
        'class': "form-control",
        'placeholder': 'Please enter other information'
    }, validators=[DataRequired()])
    submit = SubmitField('Register')

class MakeAppointment(FlaskForm):
    pets = [('%d'% r.id, r.Pname) for r in Pet.query.all()]
    pet = SelectField(label='Select Pet', choices= pets,validators=[DataRequired()])
    ownerphone = StringField('OwnerPhone', validators=[DataRequired()])
    type = RadioField('Type', choices=[('0', 'Emergency'), ('1', 'Standard')], validators=[DataRequired()])
    otherdescription = StringField('OtherDescription', validators=[DataRequired()])
    chooseposition = SelectField('Choose Position',choices=[('Beijing', 'Beijing'), ('Shanghai', 'Shanghai'),('Chengdu', 'Chengdu')], default=0, validators=[DataRequired()])
    doctors = [('%d' % r.id, r.Dname) for r in Doctor.query.all()]
    doctor = SelectField(label='Choose doctor you want', choices=doctors, validators=[DataRequired()])
    datetime = DateTimeField('Choose a date', format='%Y/%m/%d',validators=[DataRequired()])
    submit = SubmitField('Submit')



class Addpetinformation(FlaskForm):
    Pname = StringField('Pet Name', validators=[DataRequired()])
    Page = IntegerField('Pet age',validators=[DataRequired(),Regexp('^[0-9]*$',
message='The pet age should contain be a number.')])
    Psex = RadioField('Gender', choices=[('1', 'Male'), ('2', 'Female')], default=1, validators=[DataRequired()])
    Pspecies = RadioField('Pet Type', choices=[('cat', 'Cat'), ('dog', 'Dog')], default=1, validators=[DataRequired()])
    Pinfo = TextAreaField('Pet Information', validators=[DataRequired()])
    submit = SubmitField('Save')




