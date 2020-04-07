import os

from datetime import date

from flask import render_template, flash, redirect, url_for, session, request, abort
from werkzeug.security import check_password_hash, generate_password_hash

from hospitalapp import app, db
from hospitalapp.forms import *
from hospitalapp.models import Customer,Employee,Pet,Medicine,Hospitalization,Hospital,Good,Operation,Order,Doctor,Prescription,Appointment
from hospitalapp import photos
from flask_uploads import UploadSet, IMAGES, configure_uploads

photos = UploadSet('products', IMAGES)
configure_uploads(app, photos)



@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html', title='Home')

@app.route('/about')
def about():
    return render_template('about_us.html', title='about')

@app.route('/customer_mainpage')
def customer_mainpage():
    return render_template('customer_mainpage.html', title='Home')

@app.route('/employee_mainpage')
def employee_mainpage():
    return render_template('employee_mainpage.html', title='Home')

@app.route('/loggedin_home_customer',methods=['GET', 'POST'])
def loggedin_home_customer():
    if not session.get("USERNAME") is None:
        user_in_db = Customer.query.filter(Customer.Cname == session.get("USERNAME")).first()
        return render_template('loggedin_home_customer.html', Cusername=user_in_db.Cname)
    else:
        flash("Customer needs to either login or signup first")
        return redirect(url_for('customer_mainpage'))


@app.route('/loggedin_home_employee')
def loggedin_home_employee():
    if not session.get("USERNAME") is None:
        user_in_db = Employee.query.filter(Employee.Ename == session.get("USERNAME")).first()
        return render_template('loggedin_home_employee.html', Eusername=user_in_db.Ename)
    else:
        flash("Employee needs to either login or signup first")
        return redirect(url_for('loginEmployee'))


@app.route('/loginEmployee', methods=['GET', 'POST'])
def loginEmployee():
    form = LoginFormEmployee()
    if form.validate_on_submit():
        user_in_db = Employee.query.filter(Employee.Ename == form.Eusername.data).first()
        if not user_in_db:
            flash('No user found with username: {}'.format(form.Eusername.data))
            return redirect(url_for('loginEmployee'))
        if check_password_hash(user_in_db.Epassword, form.Epassword.data):
            flash('Login success!')
            session["USERNAME"] = user_in_db.Ename
            return redirect(url_for('loggedin_home_employee'))
        flash('Incorrect Password')
        return redirect(url_for('login'))
    return render_template('login_employee.html', title='Sign In', form=form)


@app.route('/signupEmployee', methods=['GET', 'POST'])
def signupEmployee():
    form = SignupFormEmployee()
    if form.validate_on_submit():
        if form.Epassword.data != form.Epassword2.data:
            flash('Passwords do not match!')
            return redirect(url_for('signupEmployee'))

        passw_hash = generate_password_hash(form.Epassword.data)
        employee = Employee(Ename=form.Eusername.data, EIDcard=form.Eidcard.data, Ephone=form.Ephone.data,Egender=form.Egender.data, Eemail=form.Eemail.data, Ehiredate=form.Ehiredate.data, Epassword=passw_hash)
        db.session.add(employee)
        db.session.commit()
        session["USERNAME"] = employee.Ename
        return redirect(url_for("loginEmployee"))
    return render_template('signup_employee.html', title='Register a new user', form=form)


@app.route('/arrangeappointmentEmployee', methods=['GET', 'POST'])
def arrangeappointmentemployee():
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
            appointment = Appointment(Apet=pet,Atype=type,Adoc=doctor,Acomplete=complete,Ainfo=infomation,Adate=date,Acost=cost)
            db.session.add(appointment)
            db.session.commit()
            return redirect(url_for('loggedin_home_employee'))
        return render_template('arr_appointment_emp.html',title='arrangeappointment',form=form)
    else:
        flash("User needs to either login or signup first")
        return redirect(url_for('employee_mainpage'))

@app.route('/Prescription', methods=['GET', 'POST'])
def Prescription():
    form = PrescriptionForm()
    if not session.get("USERNAME") is None:
        if form.validate_on_submit():
            medicine = form.Pmed.data
            number = form.Pnumber.data
            appointment = form.Pappointment.data
            prescription = Prescription(Pmedicine=medicine,Pnumber=number,Pappointment=appointment)
            db.session.add(prescription)
            db.session.commit()
            return redirect(url_for('loggedin_home_employee'))
        return render_template('Prescription.html',title='Prescription',form=form)
    else:
        flash("User needs to either login or signup first")
        return redirect(url_for('employee_mainpage'))

@app.route('/Hospitalization', methods=['GET', 'POST'])
def Hospitalization():
    form = HospitalizationForm()
    if not session.get("USERNAME") is None:
        if form.validate_on_submit():
            appointment = form.appointment.data
            doc = form.doc.data
            room = form.room.data
            startdate = form.startdate.data
            enddate = form.enddate.data
            cost = form.cost.data
            hospitalization = Hospitalization(Sappointment=appointment,Sdoc=doc,Sroom=room,Sstartdate=startdate,Senddate=enddate,Scost=cost)
            db.session.add(hospitalization)
            db.session.commit()
            return redirect(url_for('loggedin_home_employee'))
        return render_template('Hospitalization.html',title='Hospitalization',form=form)
    else:
        flash("User needs to either login or signup first")
        return redirect(url_for('employee_mainpage'))

@app.route('/DisplayAppointmentEmployee', methods=['GET', 'POST'])
def DisplayAppointmentEmployee():
    form = ArrangeAppointmentFormEmployee
    if not session.get("USERNAME") is None:
        standard_appointments = Appointment.query.filter(Appointment.Atype=='1').all()
        emergency_appointments = Appointment.query.filter(Appointment.Atype=='0').all()
        return render_template('DisplayAppointmentEmployee.html', title='Display Appointment Employee', standard_appointments=standard_appointments,emergency_appointments=emergency_appointments,form=form)
    else:
        flash("User needs to either login or signup first")
        return redirect(url_for('employee_mainpage'))


@app.route('/ModifyAppointmentEmployee/<id>', methods=['GET', 'POST'])
def ModifyAppointmentEmployee(id):
    if not session.get("USERNAME") is None:
        appo_obj = Appointment.query.filter_by(id=id).first()
        if not appo_obj:
            abort(404)
        form = ModyAppointmentFormEmployee(obj=appo_obj)
        if form.validate_on_submit():
            appo_obj.Apet = form.data['Epet']
            appo_obj.Atype = form.data['Etype']
            appo_obj.Adoc = form.data['Edoc']
            appo_obj.Acomplete = form.data['Ecomplete']
            appo_obj.Ainfo = form.data['Einf']
            appo_obj.Adate = form.data['Edate']
            appo_obj.Acost = form.data['Ecost']
            db.session.add(appo_obj)
            db.session.commit()
            flash('Modify successfully', 'success')
            return redirect(url_for('loggedin_home_employee'))
        else:
            print(form.errors)
        return render_template('AppointmentDetail.html', title='Modify Appointment', form=form, id = id)

    else:
        flash("User needs to either login or signup first")
        return redirect(url_for('employee_mainpage'))

@app.route('/listproduct', methods=['GET', 'POST'])
def listproduct():
    goods = Good.query.all()
    return render_template('adminproduct.html',title='Shop', goods = goods)
    

@app.route('/addproduct', methods=['GET', 'POST'])
def addproduct():
    form = AddProductForm()
    if not session.get("USERNAME") is None:
        if form.validate_on_submit():
            if request.method == 'POST' and 'photo' in request.files:
                filename = photos.save(request.files['photo'])
                file_url = photos.get_basename(filename)
                id = form.Gid.data
                name = form.Gname.data
                info = form.Ginfo.data
                price = form.Gprice.data
                adddate = form.Gadddate.data
                good = Good(id=id, Gname=name, Ginfo=info, Gimage=file_url, Gprice=price, Gadddate=adddate)
                db.session.add(good)
                db.session.commit()
                flash("Add product successfully")
            return redirect(url_for('listproduct'))
        return render_template('addproduct.html', title='addproduct', form=form)
    else:
        flash("User needs to either login or signup first")
        return redirect(url_for('employee_mainpage'))

@app.route('/deleteproduct',methods=['GET', 'POST'])
def deleteproduct(id):
    good = Good.query.get_or_404(id)
    db.session.delete(good)
    db.session.commit()
    flash("Delete Product")
    return redirect(url_for('adminproduct'), id=id)

@app.route('/editproduct',methods=['GET', 'POST'])
def editproduct():
    form = AddProductForm()
    return render_template('addproduct.html', form=form)

    
            
@app.route('/order',methods=['GET', 'POST'])
def order():
    form = OrderForm()
    if form.validate_on_submit():
        return redirect(url_for('paypage'))
    render_template('order.html', title='order', form=form)


@app.route('/signupCustomer',methods=['GET', 'POST'])
def signupCustomer():
    form = SignupCustomer()
    if form.validate_on_submit():
        print("888888")
        if form.Cpassword.data != form.Cpassword2.data:
            flash('Passwords do not match!')
            print("99999")
            return redirect(url_for('signupCustomer'))
        passw_hash = generate_password_hash(form.Cpassword.data)
        #customer = Customer(Cname=form.Cusername.data, Cphone=form.Cphone.data, Cemail=form.Cemail.data, password_hash=passw_hash)
        customer = Customer(Cname=form.Cusername.data, Cphone=form.Cphone.data, Cemail=form.Cemail.data, Cgender=form.Cgender.data, Cpassword=passw_hash)
        db.session.add(customer)
        db.session.commit()
        session["USERNAME"] = customer.Cname
        flash('Welcome home, %s ! , you need sign in again' % customer.Cname)
        print("666666")
        return redirect(url_for('loginCustomer'))
    return render_template('signup_customer.html', title='Register a new user', form=form)


@app.route('/loginCustomer', methods=['GET', 'POST'])
def loginCustomer():
    form = LoginFormCustomer()
    if form.validate_on_submit():
        user_in_db = Customer.query.filter(Customer.Cname == form.Cusername.data).first()
        if not user_in_db:
            flash('No user found with username: {}'.format(form.Cusername.data))
            return redirect(url_for('loginCustomer'))
        if check_password_hash(user_in_db.Cpassword, form.Cpassword.data):
            flash('Login success!')
            session["USERNAME"] = user_in_db.Cname
            return redirect(url_for('loggedin_home_customer'))
        flash('Incorrect Password')
        return redirect(url_for('loginCustomer'))
    return render_template('login_customer.html', title='Login In', form=form)


@app.route('/logoutEmployee')
def logoutEmployee():
    session.pop("USERNAME", None)
    return redirect(url_for('employee_mainpage'))


@app.route('/Make Appointment', methods=['GET', 'POST'])
def make_appointment():
    form = MakeAppointment()
    return render_template('make_appointment_customer.html', title='Make Appointment', form=form)


@app.route('/Track State')
def track_state():

    return '<h1>Track State</h1>'
