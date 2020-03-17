from datetime import date

from flask import render_template, flash, redirect, url_for, session, request
from werkzeug.security import check_password_hash, generate_password_hash

from hospitalapp import app
from hospitalapp.forms import LoginFormEmployee, LoginFormCustomer, SignupFormEmployee, SignupCustomer,\
    ArrangeAppointmentFormEmployee, AddProductForm, OrderForm
from hospitalapp.models import *


@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html', title='Home')


@app.route('/customer_mainpage')
def customer_mainpage():
    return render_template('customer_mainpage.html', title='Home')

@app.route('/employee_mainpage')
def employee_mainpage():
    return render_template('employee_mainpage.html', title='Home')

@app.route('/loggedin_home')
def loggedin_home():
    if not session.get("USERNAME") is None:
        user_in_db = Employee.query.filter(Employee.Eusername == session.get("USERNAME")).first()
        return render_template('loggedin_home.html', Eusername=user_in_db.username)
    else:
        flash("Employee needs to either login or signup first")
        return redirect(url_for('login'))


@app.route('/loginEmployee', methods=['GET', 'POST'])
def loginEmployee():
    form = LoginFormEmployee()
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


@app.route('/signupEmployee', methods=['GET', 'POST'])
def signupEmployee():
    form = SignupFormEmployee()
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


@app.route('/arrangeappointmentEmployee', methods=['GET', 'POST'])
def post():
    form = ArrangeAppointmentFormEmployee()
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


@app.route('/addproduct', methods=['GET', 'POST'])
def addproduct():
    form = AddProductForm()
    if not session.get("USERNAME") is None:#
        if form.validate_on_submit():
            id = form.Gid.data
            name = form.Gname.data
            information = form.Ginfo.data
            image = request.files['file'].read()
            price = form.Gprice.data
            adddate = form.Gadddate.data
            good = Good(Gid=id, Gname=name, Ginfo=information, Gimage=image, Gprice=price, Gadddate=date)
            db.session.add(good)
            db.session.commit()
            flash("Add product successfully")
            return redirect(url_for('shoppage'))
        render_template('addproduct.html', title='addproduct', form=form)
    else:
        flash("User needs to either login or signup first")#
        return redirect(url_for('login'))#
            
@app.route('/order')
def order():
    form = OrderForm()
    if form.validate_on_submit():
        return redirect(url_for('paypage'))
    render_template('order.html', title='order', form=form)


@app.route('/signupCustomer')
def signupCustomer():
    form = SignupCustomer()
    if request.method == 'POST' and form.validate():
        flash("Welcome come to Pet Wars")
    passw_hash = generate_password_hash(form.Cpassword.data)
    customer = Customer(Ename=form.Eusername.data, Eemail=form.Eemail.data, password_hash=passw_hash)
    db.session.add(customer)
    db.session.commit()
    session["USERNAME"] = customer.Cname
    # handle...
    return render_template('signup.html', form=form)


@app.route('/loginCustomer', methods=['GET', 'POST'])
def loginCustomer():
    form = LoginFormCustomer()
    user_in_db = Customer.query.filter(Customer.Cname == form.Cusername.data).first()
    if not user_in_db:
        flash('No user found with username: {}'.format(form.Cusername.data))
        return redirect(url_for('login'))
    if request.method == 'POST' and check_password_hash(user_in_db.password_hash, form.Cpassword.data): #handle yes
        flash('Login success!')
        session["USERNAME"] = user_in_db.username
        return redirect(url_for('loggedin_home'))
    flash('Incorrect Password')
    return render_template('login.html', form=form)



