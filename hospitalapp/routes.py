from flask import render_template, flash, redirect, url_for, session
from werkzeug.security import check_password_hash, generate_password_hash

from hospitalapp import app
from hospitalapp.forms import LoginForm, SignupForm,ArrangeAppointmentForm
from hospitalapp.models import *


@app.route('/')
@app.route('/index')
def index():
    user = {'username': 'Viola'}
    return render_template('index.html', title='Home', user=user)


@app.route('/loggedin_home')
def loggedin_home():
    if not session.get("USERNAME") is None:
        user_in_db = Employee.query.filter(Employee.Eusername == session.get("USERNAME")).first()
        return render_template('loggedin_home.html', Eusername=user_in_db.username)
    else:
        flash("Employee needs to either login or signup first")
        return redirect(url_for('login'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user_in_db = Employee.query.filter(Employee.Ename == form.Eusername.data).first()
        if not user_in_db:
            flash('No user found with username: {}'.format(form.Eusername.data))
            return redirect(url_for('login'))
        if check_password_hash(user_in_db.password_hash, form.Epassword.data):
            flash('Login success!')
            session["USERNAME"] = user_in_db.username
            return redirect(url_for('loggedin_home'))
        flash('Incorrect Password')
        return redirect(url_for('login'))
    return render_template('login.html', title='Sign In', form=form)


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = SignupForm()
    if form.validate_on_submit():
        if form.password.data != form.password2.data:
            flash('Passwords do not match!')
            return redirect(url_for('signup'))

        passw_hash = generate_password_hash(form.Epassword.data)
        employee = Employee(Ename=form.Eusername.data, Eemail=form.Eemail.data, password_hash=passw_hash)
        db.session.add(employee)
        db.session.commit()
        session["USERNAME"] = employee.Ename
        return redirect(url_for("loggedin_home"))
    return render_template('signup.html', title='Register a new user', form=form)

@app.route('/arrangeappointment', methods=['GET', 'POST'])
def post():
    form = ArrangeAppointmentForm()
    if not session.get("USERNAME") is None:
        if form.validate_on_submit():
            pet = form.Epet.data
            type = form.Etype.data
            doctor = form.Edoc.data
            complete = form.Ecomplete.data
            infomation = form.Einf.data
            date = form.Edate.data
            cost = form.Ecost.data
            appointment = Appointment(Apet=pet,Atype=type,Adoctor=doctor,Acomplete=complete,Ainf=infomation,Adate=date,Acost=cost)
            db.session.add(appointment)
            db.session.commit()
            return redirect(url_for('displayappointment'))
        render_template('arrangeappointment.html',title='arrangeappointment',form=form)
    else:
        flash("User needs to either login or signup first")
        return redirect(url_for('login'))
