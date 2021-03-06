import os
import time
import re
from datetime import datetime

from flask import render_template, flash, redirect, url_for, session, request, abort #, jsonify
#from sqlalchemy.testing.pickleable import User
from werkzeug.security import check_password_hash, generate_password_hash
from werkzeug.utils import secure_filename

from hospitalapp import app, db
from hospitalapp.forms import *
from hospitalapp.models import *
from hospitalapp import photos
from flask_uploads import UploadSet, IMAGES, configure_uploads

photos = UploadSet('photos', IMAGES)
configure_uploads(app, photos)
@app.route('/test')
def plz():
    return render_template('base.html')

@app.route('/')
def start():
    return render_template('start.html')    

@app.route('/lang')
def choose_language():
    return render_template('choose_language.html', title='Home')

@app.route('/procedure')
def procedure():
    return render_template('portfolio_details.html') 

@app.route('/index')
def index():
    return render_template('index.html')




@app.route('/senior_login', methods=['GET', 'POST'])
def senior_login():
    form = LoginFormCustomer()
    if request.method == "POST":
        user_in_db = Customer.query.filter(Customer.Cname == form.Cusername.data).first()
        if not user_in_db:
            flash('No user found with username: {}'.format(form.Cusername.data))
            return redirect(url_for('senior_login'))
        if check_password_hash(user_in_db.Cpassword, form.Cpassword.data):
            flash('login success !')
            session["USERNAME"] = user_in_db.Cname
            return redirect(url_for('loggedin_home_senior'))
        flash('Incorrect Password')
        return redirect(url_for('senior_login'))
    return render_template('senior_login.html', title='Login In', form=form)


@app.route('/signupSenior', methods=['GET', 'POST'])
def signupSenior():
    form = SignupCustomer()
    if form.validate_on_submit():
        if form.Cpassword.data != form.Cpassword2.data:
            flash('Passwords do not match!')
            return redirect(url_for('signupSenior'))
        passw_hash = generate_password_hash(form.Cpassword.data)
        customer = Customer(Cname=form.Cusername.data, Cphone=form.Cphone.data, Cemail=form.Cemail.data,
                            Cgender=form.Cgender.data, Cpassword=passw_hash)
        db.session.add(customer)
        db.session.commit()
        session["USERNAME"] = customer.Cname
        flash('Welcome home, %s ! , you need sign in again' % customer.Cname)
        return redirect(url_for('senior_login'))
    return render_template('signup_customer.html', title='Register a new user', form=form)


@app.route('/loggedin_home_senior', methods=['GET', 'POST'])
def loggedin_home_senior():
    if not session.get("USERNAME") is None:
        user_in_db = Customer.query.filter(Customer.Cname == session.get("USERNAME")).first()
        print(user_in_db.Cname)
        pets = user_in_db.Cpet.all()
        doctors = Doctor.query.filter().all()
        if not session.get("USERNAME") is None:
            if request.method == 'GET':
                posts = user_in_db.Cpost.all()
                read_posts = set()
                for p in posts:
                    if p.Panswer.all():
                        read_posts.add(p)
                unread_posts = user_in_db.Cpost.filter(Post.Panswer == None).all()
                appoints = []
                for pet in pets:
                    a = Appointment.query.filter(Appointment.Apet == pet.id).all()
                    print(a)
                    appoints.extend(a)
        return render_template('loggedin_home_senior.html', Cusername=user_in_db.Cname, pets=pets, appoints=appoints,
                               read_posts=read_posts, unread_posts=unread_posts, doctors=doctors)
    else:
        flash("Customer needs to either login or signup first")
        return redirect(url_for('senior_login'))


@app.route('/loggedin_home_senior/write_post', methods=['GET', 'POST'])
def senior_write_post():
    user_in_db = Customer.query.filter(Customer.Cname == session.get("USERNAME")).first()
    if request.method == "POST":
        post = Post(Ptopic=request.form['topic'], Pcontent=request.form['content'], poster=user_in_db)
        db.session.add(post)
        db.session.commit()
    return redirect(url_for('loggedin_home_senior'))


@app.route('/loggedin_home_senior/add_pet', methods=['GET', 'POST'])
def senior_add_pet():
    user_in_db = Customer.query.filter(Customer.Cname == session.get("USERNAME")).first()
    if request.method == "POST":
        pet = Pet(Pname=request.form['pet_name'], Page=request.form['pet_age'], Psex=request.form['pet_gender'],
                  Pspecies=request.form['pet_species'],
                  Pinfo=request.form['pet_info'], owner=user_in_db)
        db.session.add(pet)
        db.session.commit()
    return redirect(url_for('loggedin_home_senior'))


@app.route('/loggedin_home_senior/edit_pet/<id>', methods=['GET', 'POST'])
def senior_edit_pet(id):
    if not session.get("USERNAME") is None:
        if request.method == 'GET':
            user_in_db = Customer.query.filter(Customer.Cname == session.get("USERNAME")).first()
            pet = Pet.query.filter(Pet.Powner == user_in_db.id).first()
            return render_template('senior_edit_pet.html', pet=pet)
        else:
            user_in_db = Customer.query.filter(Customer.Cname == session.get("USERNAME")).first()
            pet = Pet.query.filter(Pet.Powner == user_in_db.id).first()
            if not request.form['name'] :
                flash("Please enter petname")
                return redirect(url_for("loggedin_home_senior"))
            if not request.form['age'] :
                flash("Please enter pet age")
                return redirect(url_for("loggedin_home_senior"))
            if is_number(request.form['age'])==False:
                flash("Please fill in the Numbers in the age")
                return redirect(url_for("loggedin_home_senior"))
            pet.Pname = request.form['name']
            pet.Page = request.form['age']
            pet.Psex = request.form['gender']
            pet.Pspecies = request.form['species']
            pet.Pinfo = request.form['information']
            db.session.commit()
            print("edit successfully")
            return redirect(url_for('loggedin_home_senior'))
    else:
        return redirect(url_for('senior_login'))


@app.route('/loggedin_home_senior/delete_pet/<id>', methods=['GET', 'POST'])
def senior_delete_pet(id):
    if not session.get("USERNAME") is None:
        pet = Pet.query.get_or_404(id)
        db.session.delete(pet)
        db.session.commit()
        return redirect(url_for('loggedin_home_senior'))
    else:
        return redirect(url_for('senior_login'))


@app.route('/loggedin_home_senior/operation/<id>', methods=['GET', 'POST'])
def senior_appo_operation(id):
    if not session.get("USERNAME") is None:
        if request.method == 'GET':
            appoint = Appointment.query.filter(Appointment.id == id).first()
            operation = Operation.query.filter(Operation.Oappiiontment == id).first()
            if operation and appoint.Ostatus == '1':
                print(operation)
                doc = Doctor.query.filter(Doctor.id == operation.Odoc).first()
                return render_template('senior_appo_operation.html', appoint=appoint, operation=operation, doc=doc)
            else:
                flash("No surgical approval is required for this appointment")
                return redirect(url_for('loggedin_home_senior'))
        else:
            appoint = Appointment.query.filter(Appointment.id == id).first()
            if appoint.Ostatus == '1':
                appoint.Ostatus = '2'
                appoint.OperationStatus = "Ready to surgery"
                db.session.commit()
                flash("Ready to sugery")
            else:
                flash("No surgical approval is required")
            return redirect(url_for('loggedin_home_senior'))
    else:
        return redirect(url_for('senior_login'))


@app.route('/loggedin_home_senior/inpatient/<id>', methods=['GET', 'POST'])
def senior_appo_inpatient(id):
    if not session.get("USERNAME") is None:
        if request.method == 'GET':
            appoint = Appointment.query.filter(Appointment.id == id).first()
            inpatient = Hospitalization.query.filter(Hospitalization.Sappointment == id).first()
            if inpatient and appoint.Hstatus == '1':
                doc = Doctor.query.filter(Doctor.id == inpatient.Sdoc).first()
                return render_template('senior_appo_inpatient.html', title="Allows operation", appoint=appoint,
                                       inpatient=inpatient, doc=doc)
            else:
                flash("No in-patient approval is required for this appointment")
                return redirect(url_for('loggedin_home_senior'))

        else:
            appoint = Appointment.query.filter(Appointment.id == id).first()
            if appoint.Hstatus == '1':
                appoint.Hstatus = '2'
                appoint.HospitalizationStatus = "Ready to inpatient"
                db.session.commit()
                flash("Ready to inpatient")
            else:
                flash("No inpatient approval is required")
            return redirect(url_for('loggedin_home_senior'))
    else:
        return redirect(url_for('senior_login'))


@app.route('/loggedin_home_senior/emergency_appointment', methods=['GET', 'POST'])
def senior_emergency_appoint():
    if request.method == "POST":
        
        try:
            pet_name = request.form["appoint_name"]
        except:
            flash("Please select petname")
            return redirect(url_for("senior_emergency_appoint"))
            raise exceptions.BadRequestKeyError(str(e))
        try:
            print('date--------',request.form["date"])
            date_str = request.form["date"]
            date_str = date_str+" 00:00:00"
            date = datetime.strptime(date_str, '%Y-%m-%d %H:%M:%S')
        except:
            flash("Please enter date")
            return redirect(url_for("senior_emergency_appoint"))
            raise exceptions.BadRequestKeyError(str(e))
        try:
            docname = request.form['doctor']
        except KeyError as e:
            flash("Please select correct doctor")
            return redirect(url_for("senior_emergency_appoint"))
            raise exceptions.BadRequestKeyError(str(e))
        pet = Pet.query.filter(Pet.Pname == pet_name).first()
        flash("Make an appointment successfully")
        appointment = Appointment(apppetter=pet, Atype='0',
                                  Adoc=docname, Alocation=request.form["location"], Adate=date,
                                  Ainfo='senior emergency appointment', Acomplete='0',Astart='0', Ostatus="0", Hstatus='0')
        db.session.add(appointment)
        db.session.commit()
    return redirect(url_for('loggedin_home_senior'))


@app.route('/loggedin_home_senior/standard_appointment', methods=['GET', 'POST'])
def senior_standard_appoint():
    if request.method == "POST":
        try:
            pet_name = request.form["appoint_name"]
        except:
            flash("Please select petname")
            return redirect(url_for("senior_standard_appoint"))
            raise exceptions.BadRequestKeyError(str(e))
        try:
            print('date--------',request.form["date"])
            date_str = request.form["date"]
            date_str = date_str+" 00:00:00"
            date = datetime.strptime(date_str, '%Y-%m-%d %H:%M:%S')
        except:
            flash("Please enter date")
            return redirect(url_for("senior_standard_appoint"))
            raise exceptions.BadRequestKeyError(str(e))
        try:
            docname = request.form['doctor']
        except KeyError as e:
            flash("Please select correct doctor")
            return redirect(url_for("senior_standard_appoint"))
            raise exceptions.BadRequestKeyError(str(e))
        pet = Pet.query.filter(Pet.Pname == pet_name).first()
        flash("Make an appointment successfully")
        appointment = Appointment(apppetter=pet, Atype='1',
                                  Adoc=docname, Alocation=request.form["location"], Adate=date,
                                  Ainfo=request.form["info"], Acomplete='0',Astart='0', Ostatus="0", Hstatus='0')
        db.session.add(appointment)
        db.session.commit()
    return redirect(url_for('loggedin_home_senior'))


@app.route('/loggedin_home_senior/delete_appoint/<id>', methods=['GET', 'POST'])
def senior_delete_appoint(id):
    if not session.get("USERNAME") is None:
        appoint = Appointment.query.get_or_404(id)
        db.session.delete(appoint)
        db.session.commit()
        return redirect(url_for('loggedin_home_senior'))
    else:
        return redirect(url_for('senior_login'))


@app.route('/loggedin_home_senior/edit_appoint/<id>', methods=['GET', 'POST'])
def senior_edit_appoint(id):
    if not session.get("USERNAME") is None:
        if request.method == 'GET':
            appoint = Appointment.query.filter(Appointment.id == id).first()
            docID = appoint.Adoc
            doc = Doctor.query.filter(Doctor.id == docID).first()
            doctors = Doctor.query.all()
            return render_template('senior_edit_appo.html', doctors=doctors, doc=doc, appoint=appoint)
        else:
            appoint = Appointment.query.filter(Appointment.id == id).first()
            appoint.Atype = request.form['type']
            appoint.Adate = datetime.now()
            appoint.Alocation = request.form['location']
            docname = request.form['doctor']
            doctor = Doctor.query.filter(Doctor.Dname == docname).first()
            appoint.Adoc = doctor.id
            appoint.Ainfo = request.form['information']
            db.session.commit()
            return redirect(url_for('loggedin_home_senior'))
    else:
        return redirect(url_for('senior_login'))


@app.route('/loggedin_home_senior/release/<id>', methods=['GET', 'POST'])
def senior_appo_release(id):
    if not session.get("USERNAME") is None:
        if request.method == 'GET':
            appoint = Appointment.query.filter(Appointment.id == id).first()
            inpatient = Hospitalization.query.filter(Hospitalization.Sappointment == id).first()
            if inpatient and appoint.Hstatus == '3':
                doc = Doctor.query.filter(Doctor.id == inpatient.Sdoc).first()
                return render_template('senior_appo_release.html', title="Allows release", appoint=appoint,
                                       inpatient=inpatient, doc=doc)
            else:
                flash("No in-patient release approval is required for this appointment")
                return redirect(url_for('loggedin_home_senior'))
        else:
            appoint = Appointment.query.filter(Appointment.id == id).first()
            if appoint.Hstatus == '3':
                appoint.Hstatus = '4'
                appoint.HospitalizationStatus = "Ready to release"
                db.session.commit()
                flash("Ready to release")
            else:
                flash("No release approval is required")
            return redirect(url_for('loggedin_home_senior'))
    else:
        return redirect(url_for('senior_login'))


@app.route('/loggedin_home_customer', methods=['GET', 'POST'])
def loggedin_home_customer():
    if not session.get("USERNAME") is None:
        user_in_db = Customer.query.filter(Customer.Cname == session.get("USERNAME")).first()
        return render_template('loggedin_home_customer.html', Cusername=user_in_db.Cname)
    else:
        flash("Customer needs to either login or signup first")
        return redirect(url_for('loginCustomer'))



@app.route('/loggedin_home_employee')
def loggedin_home_employee():
    if not session.get("EMPLOYEE") is None:
        user_in_db = Employee.query.filter(Employee.Ename == session.get("EMPLOYEE")).first()
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
            session["EMPLOYEE"] = user_in_db.Ename
            return redirect(url_for('loggedin_home_employee'))
        flash('Incorrect Password')
        return redirect(url_for('loginEmployee'))
    return render_template('login_employee.html', title='Sign In', form=form)

@app.route('/employee_profile', methods=['GET', 'POST'])
def employee_profile():
    if not session.get("EMPLOYEE") is None:
        emp = Employee.query.filter(Employee.Ename == session.get("USERNAME")).first()
        if request.method == 'GET':
            return render_template('employee_profile.html', emp=emp)
        else:
            if validatePhone(request.form['phone'])==1:
                emp.Ephone = request.form['phone']
            else:
                flash("Please enter an 11-digit mobile phone number starting with 1")
                return redirect(url_for("employee_profile"))
            if validateEmail(request.form['email'])==1:
                emp.Eemail = request.form['email']
            else:
                flash("Please enter the correct email")
                return redirect(url_for("employee_profile"))
            emp.Egender = request.form['gender']
            db.session.commit()
            return redirect(url_for('loggedin_home_employee'))
    else:
        return redirect(url_for('loginEmployee'))
@app.route('/customer_profile', methods=['GET', 'POST'])
def customer_profile():
    if not session.get("USERNAME") is None:
        customer = Customer.query.filter(Customer.Cname == session.get("USERNAME")).first()
        if request.method == 'GET':
            return render_template('customer_profile.html', customer=customer)
        else:
            if validatePhone(request.form['phone'])==1:
                customer.Cphone = request.form['phone']
            else:
                flash("Please enter an 11-digit mobile phone number starting with 1")
                return redirect(url_for("customer_profile"))
            if validateEmail(request.form['email'])==1:
                customer.Cemail = request.form['email']
            else:
                flash("Please enter the correct email")
                return redirect(url_for("customer_profile"))
            customer.Cgender = request.form['gender']
            db.session.commit()
            return redirect(url_for('loggedin_home_customer'))
    else:
        return redirect(url_for('loginCustomer'))

@app.route('/senior_profile', methods=['GET', 'POST'])
def senior_profile():
    if not session.get("USERNAME") is None:
        customer = Customer.query.filter(Customer.Cname == session.get("USERNAME")).first()
        if request.method == 'GET':
            return render_template('senior_profile.html', customer=customer)
        else:
            if validatePhone(request.form['phone'])==1:
                customer.Cphone = request.form['phone']
            else:
                flash("Please enter an 11-digit mobile phone number starting with 1")
                return redirect(url_for("senior_profile"))
            if validateEmail(request.form['email'])==1:
                customer.Cemail = request.form['email']
            else:
                flash("Please enter the correct email")
                return redirect(url_for("senior_profile"))
            customer.Cgender = request.form['gender']
            db.session.commit()
            return redirect(url_for('loggedin_home_senior'))
    else:
        return redirect(url_for('senior_login'))
        

@app.route('/signupEmployee', methods=['GET', 'POST'])
def signupEmployee():
    form = SignupFormEmployee()
    if form.validate_on_submit():
        if form.Epassword.data != form.Epassword2.data:
            flash('Passwords do not match!')
            return redirect(url_for('signupEmployee'))

        passw_hash = generate_password_hash(form.Epassword.data)
        if validatePhone(form.Ephone.data) == 1:
            phone = form.Ephone.data
        else:
            flash("Please enter an 11-digit mobile phone number starting with 1")
            return redirect(url_for("signupEmployee"))

        if validateEmail(form.Eemail.data) == 1:
            email = form.Eemail.data
        else:
            flash("Please enter the correct email")
            return redirect(url_for("signupEmployee"))
        employee = Employee(Ename=form.Eusername.data, EIDcard=form.Eidcard.data, Ephone=phone,
                            Egender=form.Egender.data, Eemail=email, Ehiredate=datetime.now(),
                            Epassword=passw_hash)
        db.session.add(employee)
        db.session.commit()
        session["EMPLOYEE"] = employee.Ename
        return redirect(url_for("loginEmployee"))
    return render_template('signup_employee.html', title='Register a new user', form=form)


@app.route('/employee_appointment')
def employee_appointment():
    if not session.get("EMPLOYEE") is None:
        return render_template('employee_appointment.html', title='Home')
    else:
        flash("User needs to either login or signup first")
        return redirect(url_for('loginEmployee'))


@app.route('/employee_appo_checkin', methods=['GET', 'POST'])
def employee_appo_checkin():
    if not session.get("EMPLOYEE") is None:

        pets = Pet.query.filter().all()
        customers = Customer.query.filter().all()
        s_appointments = Appointment.query.filter(Appointment.Atype == '1',
                                                  Appointment.Astart == '0',
                                                  Appointment.Acomplete == '0').all()  # type-1 complete-0 - Standard Appointments not checkin
        print(s_appointments)
        e_appointments = Appointment.query.filter(Appointment.Atype == '0',
                                                  Appointment.Astart == '0', Appointment.Acomplete == '0').all()
        # type-1 complete-0 - Standard Appointments not checkin
        print(e_appointments)
        return render_template('employee_appo_checkin.html', title='Display appointment not checkin yet',
                               s_appointments=s_appointments,
                               e_appointments=e_appointments, pets=pets, customers=customers)
    else:
        flash("User needs to either login or signup first")
        return redirect(url_for('loginEmployee'))

@app.route('/employee_appo_checkin/view_appo/<id>', methods=['GET', 'POST'])
def employee_checkin_view(id):
    if not session.get("EMPLOYEE") is None:
        customer = Customer.query.filter(Customer.Cname == session.get("USERNAME")).first()
        appoint = Appointment.query.filter(Appointment.id == id).first()
        pet = Pet.query.filter(Pet.id == appoint.Apet).first()
        doctors = Doctor.query.filter().all()
        return render_template('employee_checkin_view.html', appoint=appoint, customer=customer, pet=pet, doctors=doctors)
    else:
        flash("User needs to either login or signup first")
        return redirect(url_for('loginEmployee'))


@app.route('/employee_appo_checkin/checkin_appo/<id>', methods=['GET', 'POST'])
def employee_checkin(id):
    appoint = Appointment.query.get_or_404(id)
    appoint.Astart = '1'
    db.session.commit()
    return redirect(url_for('employee_appo_checkin'))


@app.route('/employee_appo_outpatient', methods=['GET', 'POST'])
def employee_appo_outpatient():
    if not session.get("EMPLOYEE") is None:
        pets = Pet.query.filter().all()
        customers = Customer.query.filter().all()
        appointments = Appointment.query.filter(Appointment.Astart == '1',
                                                Appointment.Acomplete == '0').all()  # type-1 complete-0 - Standard Appointments not checkin
        appointments2 = Appointment.query.filter(Appointment.Astart == '1',Appointment.Ostatus == '3').all()
        appointments3 = Appointment.query.filter(Appointment.Astart == '1',Appointment.Hstatus == '5').all()
        appointments.append(appointments2)
        appointments.append(appointments3)
        print(appointments)
        # type-1 complete-0 - Standard Appointments not checkin
        return render_template('employee_appo_outpatient.html', title='Display appointment not checkin yet',
                               appointments=appointments, pets=pets, customers=customers)
    else:
        flash("User needs to either login or signup first")
        return redirect(url_for('loginEmployee'))


@app.route('/employee_appo_outpatient/complete/<id>', methods=['GET', 'POST'])
def employee_outpatient_finish(id):
    appoint = Appointment.query.get_or_404(id)
    appoint.Acomplete = '1'
    db.session.commit()
    return redirect(url_for('employee_appo_outpatient'))

@app.route('/employee_appo_outpatient/operation/<id>', methods=['GET', 'POST'])
def employee_outpatient_operation(id):
    if not session.get("EMPLOYEE") is None:
        form = AddOperationForm()
        appoint = Appointment.query.filter(Appointment.id == id).first()
        doctor = Doctor.query.filter(Doctor.id == appoint.Adoc).first()
        if appoint.Ostatus == '0':
            if request.method == 'POST':
                if is_number(form.Ocost.data):
                    try:
                        print('date--------',request.form["date"])
                        date_str = request.form["date"]
                        date_str = date_str+" 00:00:00"
                        date = datetime.strptime(date_str, '%Y-%m-%d %H:%M:%S')
                    except:
                        flash("Please enter date")
                        return redirect(url_for("employee_outpatient_operation",id=id))
                        raise exceptions.BadRequestKeyError(str(e))
                    operation = Operation(oappointment=appoint, odoctor=doctor, Odate=date, Oinf=form.Oinf.data,
                                        Ocost=form.Ocost.data)
                    appoint.OperationStatus = "Inform customer operation"
                    appoint.Ostatus = '1'
                    db.session.add(operation)
                    db.session.commit()
                    return redirect(url_for('employee_appo_outpatient'))
                    
                else:
                    flash("Please enter the cost with number")
                    redirect(url_for("employee_outpatient_operation", id=id))
            return render_template('employee_outpatient_operation.html', title='Display appointment not checkin yet',
                               appoint=appoint,doctor=doctor,form=form)
        else:
            flash("The appointment already has surgery")
            return redirect(url_for('employee_appo_outpatient'))
    else:
        flash("User needs to either login or signup first")
        return redirect(url_for('loginEmployee'))

@app.route('/employee_appo_outpatient/inpatient/<id>', methods=['GET', 'POST'])
def employee_outpatient_inpatient(id):
    if not session.get("EMPLOYEE") is None:
        form = AddHospitalizationForm()
        appoint = Appointment.query.filter(Appointment.id == id).first()
        doctor = Doctor.query.filter(Doctor.id == appoint.Adoc).first()
        if appoint.Hstatus == '0':
            if request.method == 'POST':
                if is_number(form.cost.data):
                    startdate_str = request.form["startdate"]
                    enddate_str = request.form["enddate"]
                    startdate_str = startdate_str+" 00:00:00"
                    enddate_str = enddate_str+" 00:00:00"
                    if startdate_str==" 00:00:00":
                        flash("Please enter start date ")
                        redirect(url_for("employee_outpatient_inpatient", id=id))
                    elif enddate_str==" 00:00:00":
                        flash("Please enter end date ")
                        redirect(url_for("employee_outpatient_inpatient", id=id))
                    else:
                        startdate = datetime.strptime(startdate_str, '%Y-%m-%d %H:%M:%S')
                        enddate = datetime.strptime(enddate_str, '%Y-%m-%d %H:%M:%S')
                        if startdate >= enddate:
                            flash("Please enter an end date later than the start date ")
                            redirect(url_for("employee_outpatient_inpatient", id=id))
                        else:
                            inpatient = Hospitalization(happointment=appoint, sdoctor=doctor, Sroom=request.form["room"],
                                                        Sstartdate=startdate, Senddate=enddate,
                                                        Scost=form.cost.data)
                            appoint.HospitalizationStatus = "Inform customer inpatient"
                            appoint.Hstatus = '1'
                            db.session.add(inpatient)
                            db.session.commit()
                            return redirect(url_for('employee_appo_outpatient'))
                else:
                    flash("Please enter correct cost ")
                    redirect(url_for("employee_outpatient_inpatient", id=id))
            return render_template('employee_outpatient_inpatient.html',
                                   title='Enter operation information and inform customer', form=form, appoint=appoint)
        else:
            flash("The appointment already has in-patient")
            return redirect(url_for('employee_appo_outpatient'))
    else:
        flash("User needs to either login or signup first")
        return redirect(url_for('loginEmployee'))


@app.route('/employee_appo_inpatient', methods=['GET', 'POST'])
def employee_appo_inpatient():
    if not session.get("EMPLOYEE") is None:
        pets = Pet.query.filter().all()
        customers = Customer.query.filter().all()
        Iappointments = Appointment.query.filter(Appointment.Astart == '1', Appointment.Acomplete == '0',
                                                 Appointment.Hstatus == '2').all()  # type-1 complete-0 - Standard Appointments not checkin
        Rappointments = Appointment.query.filter(Appointment.Astart == '1', Appointment.Acomplete == '0',
                                                 Appointment.Hstatus == '4').all()  # type-1 complete-0 - Standard Appointments not checkin
        # type-1 complete-0 - Standard Appointments not checkin
        Wappointments = Appointment.query.filter(Appointment.Astart == '1', Appointment.Acomplete == '0',
                                                 Appointment.Hstatus == '3').all()
        return render_template('employee_appo_inpatient.html', title='Display In-patient appointments',
                               Iappointments=Iappointments, Rappointments=Rappointments, Wappointments=Wappointments,
                               pets=pets, customers=customers)
    else:
        flash("User needs to either login or signup first")
        return redirect(url_for('loginEmployee'))

@app.route('/employee_appo_inpatient/release/<id>', methods=['GET', 'POST'])
def employee_inpatient_release(id):
    if not session.get("EMPLOYEE") is None:
        appoint = Appointment.query.get_or_404(id)
        appoint.Hstatus = '3'
        appoint.HospitalizationStatus = "Inform customer of release"
        db.session.commit()
        return redirect(url_for('employee_appo_inpatient'))
    else:
        flash("User needs to either login or signup first")
        return redirect(url_for('loginEmployee'))


@app.route('/employee_appo_inpatient/release_complete/<id>', methods=['GET', 'POST'])
def employee_inpatient_releasecomplete(id):
    if not session.get("EMPLOYEE") is None:
        appoint = Appointment.query.get_or_404(id)
        appoint.Hstatus = '5'
        appoint.HospitalizationStatus = "Released"
        db.session.commit()
        return redirect(url_for('employee_appo_inpatient'))
    else:
        flash("User needs to either login or signup first")
        return redirect(url_for('loginEmployee'))


@app.route('/employee_appo_operation', methods=['GET', 'POST'])
def employee_appo_operation():
    if not session.get("EMPLOYEE") is None:
        pets = Pet.query.filter().all()
        customers = Customer.query.filter().all()
        appoints = Appointment.query.filter(Appointment.Astart == '1', Appointment.Acomplete == '0',
                                            Appointment.Ostatus == '2').all()  # type-1 complete-0 - Standard Appointments not checkin
        operations = Operation.query.filter().all()
        print(operations)
        print(appoints)
        print(pets)
        return render_template('employee_appo_operation.html', title='Display In-patient appointments',
                               appoints=appoints, pets=pets, customers=customers, operations=operations)
    else:
        flash("User needs to either login or signup first")
        return redirect(url_for('loginEmployee'))


@app.route('/employee_appo_operation/complete operation/<id>', methods=['GET', 'POST'])
def employee_operation_complete(id):
    if not session.get("EMPLOYEE") is None:
        appoint = Appointment.query.get_or_404(id)
        appoint.Ostatus = '3'
        appoint.OperationStatus = "Operation Completed"
        db.session.commit()
        return redirect(url_for('employee_appo_operation'))
    else:
        flash("User needs to either login or signup first")
        return redirect(url_for('loginEmployee'))


@app.route('/employee_appo_completed', methods=['GET', 'POST'])
def employee_appo_completed():
    if not session.get("EMPLOYEE") is None:
        pets = Pet.query.filter().all()
        customers = Customer.query.filter().all()
        appointments = Appointment.query.filter(
            Appointment.Acomplete == '1').all()  # type-1 complete-0 - Standard Appointments not checkin
        return render_template('employee_appo_completed.html', title='Display appointment completed',
                               appointments=appointments, pets=pets, customers=customers)
    else:
        flash("User needs to either login or signup first")
        return redirect(url_for('loginEmployee'))


@app.route('/employee_pets', methods=['GET', 'POST'])
def employee_pets():
    if not session.get("EMPLOYEE") is None:
        pets = Pet.query.filter().all()
        customers = Customer.query.filter().all()
        return render_template('employee_pets.html', title='Display In-patient appointments', pets=pets,
                               customers=customers)
    else:
        flash("User needs to either login or signup first")
        return redirect(url_for('loginEmployee'))


@app.route('/employee_pets/delete_pet/<id>', methods=['GET', 'POST'])
def employee_pets_delete(id):
    pet = Pet.query.get_or_404(id)
    db.session.delete(pet)
    appoints = Appointment.query.filter(Appointment.Apet == id).all()
    operations = Operation.query.filter().all()
    inpatients = Hospitalization.query.filter().all()
    for appoint in appoints:
        for operation in operations:
            if operation.Oappiiontment == appoint.id:
                db.session.delete(operation)
        for inpatient in inpatients:
            if inpatient.Sappointment == appoint.id:
                db.session.delete(inpatient)
        db.session.delete(appoint)
    db.session.commit()
    return redirect(url_for('employee_pets'))


@app.route('/employee_customers', methods=['GET', 'POST'])
def employee_customers():
    if not session.get("EMPLOYEE") is None:
        customers = Customer.query.filter().all()
        return render_template('employee_customers.html', title='Display In-patient appointments', customers=customers)
    else:
        flash("User needs to either login or signup first")
        return redirect(url_for('loginEmployee'))

@app.route('/employee_doctors', methods=['GET', 'POST'])
def employee_doctors():
    if not session.get("EMPLOYEE") is None:
        doctors = Doctor.query.filter().all()
        hospital = Hospital.query.filter().all()
        return render_template('employee_doctors.html', title='Display In-patient appointments', doctors=doctors,hospital=hospital)
    else:
        flash("User needs to either login or signup first")
        return redirect(url_for('employee_mainpage'))

@app.route('/employee_doctors/delete_doctor/<id>', methods=['GET', 'POST'])
def employee_doctorss_delete(id):
    doctor = Doctor.query.get_or_404(id)
    appoints = Appointment.query.filter(Appointment.Adoc == id).all()
    operations = Operation.query.filter(Operation.Odoc == id).all()
    inpatients = Hospitalization.query.filter(Hospitalization.Sdoc==id).all()
    if operations:
        for operation in operations:
            db.session.delete(operation)
    if inpatients:
        for inpatient in inpatients:
            db.session.delete(inpatient)
    if appoints:
        for appoint in appoints:
            db.session.delete(appoint)
    db.session.delete(doctor)
    db.session.commit()
    return redirect(url_for('employee_doctors'))

@app.route('/employee_doctorss/edit_doctor/<id>', methods=['GET', 'POST'])
def employee_doctor_edit(id):
    if not session.get("EMPLOYEE") is None:
        doc = Doctor.query.filter(Doctor.id == id).first()
        if request.method == 'GET':
            hospitals = Hospital.query.all()
            return render_template('employee_doctor_edit.html',doc = doc, hospitals=hospitals)
        else:
            if validatePhone(request.form['phone'])==0:
                flash("Please enter correct phone")
                return redirect(url_for('employee_doctor_edit',id=id))
            if is_number(request.form['level'])is False:
                flash("Please enter correct level")
                return redirect(url_for('employee_doctor_edit',id=id))
            else:
                doc.department = request.form['department']
                doc.Dphone= request.form['phone']
                doc.Dlevel= request.form['level']
                doc.Dinf= request.form['info']
                doc.Dhospital= request.form['hospital']
                db.session.commit()
                return redirect(url_for('employee_doctors'))
    else:
        return redirect(url_for('loginEmployee'))

@app.route('/employee_doctorss/add_doctor', methods=['GET', 'POST'])
def employee_add_doctor():
    if not session.get("EMPLOYEE") is None:
        if request.method == 'GET':
            hospitals = Hospital.query.all()
            return render_template('employee_add_doctor.html', hospitals=hospitals)
        else:
            if validatePhone(request.form['phone'])==0:
                flash("Please enter correct phone")
                return redirect(url_for('employee_add_doctor'))
            if is_number(request.form['level'])is False:
                flash("Please enter correct level")
                return redirect(url_for('employee_add_doctor'))
            else:
                doc = Doctor(Dname = request.form['name'],department = request.form['department'],
                            Dphone= request.form['phone'],Dlevel= request.form['level'],Dinf= request.form['info'],Dhospital= request.form['hospital'])
                db.session.add(doc)
                db.session.commit()
                return redirect(url_for('employee_doctors'))
    else:
        return redirect(url_for('loginEmployee'))


@app.route('/listproduct', methods=['GET', 'POST'])
def listproduct():
    goods = Good.query.all()
    return render_template('adminproduct.html', title='Shop', goods=goods)


@app.route('/employee_posts')
def employee_posts():
    if not session.get("EMPLOYEE") is None:
        posts = Post.query.all()
        read_posts = set()
        for post in posts:
            if post.Panswer.all():
                read_posts.add(post)

        unread_posts = Post.query.filter(Post.Panswer == None).all()

        print('unread posts', unread_posts)
        return render_template('employee_posts.html', unread_posts=unread_posts, read_posts=read_posts)
    else:
        return redirect(url_for('loginEmployee'))

@app.route('/employee_post_detail/<id>', methods=['GET', 'POST'])
def employee_post_detail(id):
    if not session.get("EMPLOYEE") is None:
        post = Post.query.filter_by(id=id).first()
        answer = post.Panswer.all()

        return render_template('employee_post_detail.html', post=post, answer=answer)
    else:
        return redirect(url_for('loginEmployee'))

@app.route('/customer_posts/delete_post/<id>', methods=['GET', 'POST'])
def customer_delete_post(id):
    if not session.get('USERNAME') is None:
        post = Post.query.get_or_404(id)
        answer = Answer.query.filter(Answer.Apost==post.id).first()
        if answer:
            db.session.delete(answer)
        db.session.delete(post)
        db.session.commit()
        return redirect(url_for('customer_posts'))
    else:
        return redirect(url_for('loginCustomer'))

@app.route('/senior_posts/delete_post/<id>', methods=['GET', 'POST'])
def senior_delete_post(id):
    if not session.get('USERNAME') is None:
        post = Post.query.get_or_404(id)
        answer = Answer.query.filter(Answer.Apost==post.id).first()
        if answer:
            db.session.delete(answer)
        db.session.delete(post)
        db.session.commit()
        return redirect(url_for('loggedin_home_senior'))
    else:
        return redirect(url_for('loggedin_home_senior'))

@app.route('/employee_posts/employee_answer_post/<id>', methods=['GET', 'POST'])
def employee_answer_post(id):
    form = AnswerForm()
    if not session.get("EMPLOYEE") is None:
        post = Post.query.filter_by(id=id).first()
        if form.validate_on_submit():
            answer = Answer(Acontent=form.content.data, Apost=post.id)
            db.session.add(answer)
            db.session.commit()
            return redirect(url_for('employee_posts'))
        return render_template('employee_answer_post.html', post=post, form=form, id=id)
    else:
        return redirect(url_for('loginEmployee'))


@app.route('/shoppage/detail/<id>', methods=['GET', 'POST'])
def detail(id):
    good = Good.query.get_or_404(id)
    form = ProductNumberForm()
    if form.validate_on_submit():
        if request.method == 'POST':
            good.ifincart = 1
            good.Gnumber = form.number.data
            db.session.commit()
        return redirect(url_for('shopcart'))
    return render_template('detail.html', good=good, form=form)


@app.route('/shopcart', methods=['Get', 'Post'])
def shopcart():
    total = 0
    goods = Good.query.filter_by(ifincart=1)
    for good in goods:
        total = total + good.Gprice * good.Gnumber
    return render_template('shopcart.html', goods=goods, total=total)


@app.route('/deletecart/<Gid>', methods=['Get', 'Post'])
def deletecart(Gid):
    good = Good.query.get_or_404(Gid)
    good.ifincart = 0
    good.Gnumber = 0
    db.session.commit()
    goods = Good.query.filter_by(ifincart=1)
    return render_template('shopcart.html', goods=goods)


@app.route('/buy', methods=['Get', 'Post'])
def buy():
    total = 0
    goods = Good.query.filter_by(ifincart=1)
    Oid = str(time.strftime('%Y%m%d%H%M%S', time.localtime(time.time()))) + str(time.time()).replace('.', '')
    id = str(time.strftime('%Y%m%d%H%M%S', time.localtime(time.time()))) + str(time.time()).replace('.', '')
    form = OrderForm()
    if form.validate_on_submit():
        if request.method == 'POST':
            for good in goods:
                total = total + good.Gprice * good.Gnumber
                relation = GORelation(id=id, Goodid=good.id, Orderid=Oid, number=good.Gnumber)
                id = id + str(1)
                db.session.add(relation)
            name = form.Oname.data
            address = form.Oaddress.data
            phonenumber = form.Ophonenumber.data
            order = Order(id=Oid, Oname=name, Ostate='not pay', Oprice=total, Oaddress=address,
                          Ophonenumber=phonenumber)
            db.session.add(order)
            db.session.commit()
        return redirect(url_for('notpayorders'))
    return render_template('buy.html', goods=goods, form=form)


@app.route('/pay/<id>', methods=['GET', 'POST'])
def pay(id):
    form = PayForm()
    order = Order.query.get_or_404(id)
    if form.validate_on_submit():
        if request.method == 'POST':
            order.Ostate = 'paid'
            db.session.commit()
            return redirect(url_for('paidorders'))
    return render_template('pay.html', form=form, order=order)


@app.route('/orders', methods=['GET', 'POST'])
def orders():
    return render_template('orders.html')


@app.route('/notpayorders', methods=['GET', 'POST'])
def notpayorders():
    orders = Order.query.filter_by(Ostate='not pay')
    return render_template('order.html', orders=orders)


@app.route('/paidorders', methods=['GET', 'POST'])
def paidorders():
    orders = Order.query.filter_by(Ostate='paid')
    return render_template('paidorders.html', orders=orders)


@app.route('/addproduct', methods=['GET', 'POST'])
def addproduct():
    form = AddProductForm()
    if not session.get("EMPLOYEE") is None:
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
                # flash("Add product successfully")
            return redirect(url_for('listproduct'))
        return render_template('addproduct.html', title='addproduct', form=form)
    else:
        flash("User needs to either login or signup first")
        return redirect(url_for('loginEmployee'))



@app.route('/deleteproduct/<id>', methods=['GET', 'POST'])
def deleteproduct(id):
    good = Good.query.get_or_404(id)
    db.session.delete(good)
    db.session.commit()
    # flash("Delete Product")
    return redirect(url_for('listproduct'))

@app.route('/deleteproduct/<id>', methods=['GET', 'POST'])
def deleteproduct_chinese(id):
    good = Good.query.get_or_404(id)
    db.session.delete(good)
    db.session.commit()
    # flash("Delete Product")
    return redirect(url_for('listproduct_chinese'))


@app.route('/editproduct/<id>', methods=['GET', 'POST'])
def editproduct(id):
    form = AddProductForm()
    good = Good.query.get_or_404(id)
    form.Gid.data = good.id
    if form.validate_on_submit():
        if request.method == 'POST' and 'photo' in request.files:
            filename = photos.save(request.files['photo'])
            file_url = photos.get_basename(filename)
            good.Gname = form.Gname.data
            good.Ginfo = form.Ginfo.data
            good.Gprice = form.Gprice.data
            good.Gadddate = form.Gadddate.data
            good.Gimage = file_url
            db.session.commit()
            # flash("Add product successfully")
        return redirect(url_for('listproduct'))
    return render_template('editproduct.html', form=form)



@app.route('/shoppage', methods=['GET', 'POST'])
def shoppage():
    goods = Good.query.all()
    return render_template('shoppage.html', goods=goods)


@app.route('/order', methods=['GET', 'POST'])
def order():
    form = OrderForm()
    if form.validate_on_submit():
        return redirect(url_for('paypage'))
    render_template('order.html', title='order', form=form)

@app.route('/orderdetail/<id>', methods=['GET', 'POST'])
def orderdetail(id):
    order = Order.query.get_or_404(id)
    relationships = GORelation.query.filter_by(Orderid = id)
    return render_template('orderdetail.html', order=order, relationships=relationships)


@app.route('/signupCustomer', methods=['GET', 'POST'])
def signupCustomer():
    form = SignupCustomer()
    if form.validate_on_submit():
        if form.Cpassword.data != form.Cpassword2.data:
            flash('Passwords do not match!')
            return redirect(url_for('signupCustomer'))
        passw_hash = generate_password_hash(form.Cpassword.data)
        if validatePhone(form.Cphone.data) == 1:
            phone = form.Cphone.data
        else:
            flash("Please enter an 11-digit mobile phone number starting with 1")
            return redirect(url_for("signupCustomer"))

        if validateEmail(form.Cemail.data) == 1:
            email = form.Cemail.data
        else:
            flash("Please enter the correct email")
            return redirect(url_for("signupCustomer"))
        userEmail_in_db = Customer.query.filter(Customer.Cemail == form.Cemail.data).first()
        userPhone_in_db = Customer.query.filter(Customer.Cphone == form.Cphone.data).first()
        if userEmail_in_db is not None:
            flash('Email has been registered!')
            return redirect(url_for('signupCustomer'))
        if userPhone_in_db is not None:
            flash('Phone has been registered!')
            return redirect(url_for('signupCustomer'))
        passw_hash = generate_password_hash(form.Cpassword.data)
        # customer = Customer(Cname=form.Cusername.data, Cphone=form.Cphone.data, Cemail=form.Cemail.data, password_hash=passw_hash)
        customer = Customer(Cname=form.Cusername.data, Cphone=phone, Cemail=email,
                            Cgender=form.Cgender.data, Cpassword=passw_hash)
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


@app.route('/customer_add_post', methods=['GET', 'POST'])
def customer_add_post():
    form = PostForm()
    if not session.get("USERNAME") is None:
        customer_in_db = Customer.query.filter(Customer.Cname == session.get("USERNAME")).first()
        if request.method == "POST":
            post = Post(Ptopic=request.form['topic'], Pcontent=request.form['content'], poster=customer_in_db)
            db.session.add(post)
            db.session.commit()
            return redirect(url_for('customer_posts'))
        return render_template('customer_add_post.html', user=customer_in_db, form=form)
    else:
        return redirect(url_for('loginCustomer'))

@app.route('/customer_posts')
def customer_posts():
    if not session.get("USERNAME") is None:
        customer_in_db = Customer.query.filter(Customer.Cname == session.get("USERNAME")).first()
        posts = customer_in_db.Cpost.all()
        read_posts = set()
        for p in posts:
            if p.Panswer.all():
                read_posts.add(p)
        unread_posts = customer_in_db.Cpost.filter(Post.Panswer == None).all()
        return render_template('customer_posts.html', user=customer_in_db, unread_posts=unread_posts,
                               read_posts=read_posts)
    else:
        return redirect(url_for('loginCustomer'))


@app.route('/customer_posts_detail/<id>', methods=['GET', 'POST'])
def customer_post_detail(id):
    if not session.get("USERNAME") is None:
        customer = Customer.query.filter(Customer.Cname == session.get("USERNAME")).first()
        post = Post.query.filter_by(id=id).first()
        answer = post.Panswer.all()
        return render_template('customer_post_detail.html', post=post, answer=answer, customer=customer)
    else:
        return redirect(url_for('loginCustomer'))


@app.route('/logoutEmployee', methods=['GET', 'POST'])
def logoutEmployee():
    session.pop("USERNAME", None)
    return redirect(url_for('loginEmployee'))

@app.route('/logoutCustomer', methods=['GET', 'POST'])
def logoutCustomer():
    session.pop("USERNAME", None)
    return redirect(url_for('loginCustomer'))

@app.route('/Make Appointment', methods=['GET', 'POST'])
def make_appointment():
    user = session.get("USERNAME")
    user_in_db = Customer.query.filter(Customer.Cname == session.get("USERNAME")).first()
    pets = Pet.query.filter(Pet.Powner==user_in_db.id).all()
    doctors = Doctor.query.all()
    petnames=[]
    docnames=[]
    for p in pets:
        petnames.append(p.Pname)
    for d in doctors:
        docnames.append(d.Dname)
    if request.method == "GET":
        return render_template('make_appointment_customer.html', title='Make Appointment', pets=pets, doctors=doctors)
    else:
        
        
        try:
            pet_name = request.form["pet name"]
        except:
            flash("Please select petname")
            return redirect(url_for("make_appointment"))
            raise exceptions.BadRequestKeyError(str(e))
        if pet_name not in petnames:
            flash("Please select correct pet name")
            return redirect(url_for("make_appointment"))
        else:
            pet = Pet.query.filter(Pet.Pname == pet_name).first()
        try:
            print('date--------',request.form["date"])
            date_str = request.form["date"]
            date_str = date_str+" 00:00:00"
            date = datetime.strptime(date_str, '%Y-%m-%d %H:%M:%S')
            type = request.form['type']
        except:
            flash("Please enter date")
            return redirect(url_for("make_appointment"))
            raise exceptions.BadRequestKeyError(str(e))
        try:
            docname = request.form['doctor']
        except KeyError as e:
            flash("Please select correct doctor")
            return redirect(url_for("make_appointment"))
            raise exceptions.BadRequestKeyError(str(e))
        if docname not in docnames:
            flash("Please select correct doctor name")
            return redirect(url_for("make_appointment"))
        else:
            doctor = Doctor.query.filter(Doctor.Dname == docname).first()
        appointment = Appointment(apppetter=pet, Atype=type,
                                  adoctor=doctor, Alocation=request.form["location"], Adate=date,
                                  Ainfo=request.form["information"], Acomplete='0', Astart='0', Ostatus="0", Hstatus='0')
        db.session.add(appointment)
        db.session.commit()
        return redirect(url_for('customer_my_appointments'))




@app.route('/Add Pet information', methods=['GET', 'POST'])
def add_pet_information():
    form = Addpetinformation()
    if not session.get("USERNAME") is None:
        user = session.get("USERNAME")
        user_in_db = Customer.query.filter(Customer.Cname == session.get("USERNAME")).first()
        mes = 'Hello, %s ! , you can add your pet information here' % user
        if request.method=="POST":
            if is_number(request.form["age"]):
                pet = Pet(Pname=form.Pname.data, Page=request.form["age"], Psex=request.form["sex"], Pspecies=request.form["species"],
                        Pinfo=form.Pinfo.data, owner=user_in_db)
                db.session.add(pet)
                db.session.commit()
                flash('Save Pet Information Successfully !!!')
                return redirect(url_for('customer_my_pets'))
            else:
                flash("Please enter number in age ")
        return render_template('add_pet_information.html', title='Add Pet Information', warn='New pet', form=form,
                               mes=mes)
    else:
        return redirect(url_for('loginCustomer'))



@app.route('/My Pets', methods=['GET', 'POST'])
def customer_my_pets():
    if not session.get("USERNAME") is None:
        user_in_db = Customer.query.filter(Customer.Cname == session.get("USERNAME")).first()
        pets = user_in_db.Cpet.all()
        user = session["USERNAME"]
        mes = 'Hello, %s ! , Here are your pets information' % user
        return render_template('customer_my_pets.html', pets=pets, mes=mes)
    else:
        return redirect(url_for('loginCustomer'))


@app.route('/My Pets/edit_pet/<id>', methods=['GET', 'POST'])
def customer_edit_pet(id):
    if not session.get("USERNAME") is None:
        if request.method == 'GET':
            user_in_db = Customer.query.filter(Customer.Cname == session.get("USERNAME")).first()
            pet = Pet.query.filter(Pet.id==id).first()
            return render_template('customer_edit_pet.html', pet=pet)
        else:
            user_in_db = Customer.query.filter(Customer.Cname == session.get("USERNAME")).first()
            pet = Pet.query.filter(Pet.Powner == user_in_db.id).first()
            if not request.form['name'] :
                flash("Please enter petname")
                return redirect(url_for("customer_edit_pet", id = id))
            if not request.form['age'] :
                flash("Please enter age")
                return redirect(url_for("customer_edit_pet", id = id))
            if is_number(request.form['age'])==False:
                flash("Please fill in the Numbers in the age")
                return redirect(url_for("customer_edit_pet", id=id))
            pet.Pname = request.form['name']
            pet.Page = request.form['age']
            pet.Psex = request.form['gender']
            pet.Pspecies = request.form['species']
            pet.Pinfo = request.form['information']
            db.session.commit()
            return redirect(url_for('customer_my_pets'))
    else:
        return redirect(url_for('loginCustomer'))



@app.route('/My Pets/delete_pet/<id>', methods=['GET', 'POST'])
def customer_delete_pet(id):
    if not session.get("USERNAME") is None:
        pet = Pet.query.get_or_404(id)
        db.session.delete(pet)
        db.session.commit()
        return redirect(url_for('customer_my_pets'))
    else:
        return redirect(url_for('loginCustomer'))



@app.route('/customer_my_appointments', methods=['GET', 'POST'])
def customer_my_appointments():
    user_in_db = Customer.query.filter(Customer.Cname == session.get("USERNAME")).first()
    pets = Pet.query.filter(Pet.Powner == user_in_db.id).all()
    doctors =Doctor.query.filter().all()
    if not session.get("USERNAME") is None:
        if request.method == 'GET':
            appoints = []
            for pet in pets:
                a = Appointment.query.filter(Appointment.Apet == pet.id).all()
                print(a)
                appoints.extend(a)
    return render_template('customer_my_appointments.html', pets=pets, appoints=appoints,doctors=doctors)
    


@app.route('/customer_my_appointments/edit_appo/<id>', methods=['GET', 'POST'])
def customer_edit_appointments(id):
    if not session.get("USERNAME") is None:
        if request.method == 'GET':
            appoint = Appointment.query.filter(Appointment.id == id).first()
            docID = appoint.Adoc
            doc = Doctor.query.filter(Doctor.id == docID).first()
            doctors = Doctor.query.all()
            return render_template('customer_edit_appo.html', doctors=doctors, doc=doc, appoint=appoint)
        else:
            appoint = Appointment.query.filter(Appointment.id == id).first()
            appoint.Atype = request.form['type']
            try:
                print('date--------',request.form["date"])
                date_str = request.form["date"]
                date_str = date_str+" 00:00:00"
                date = datetime.strptime(date_str, '%Y-%m-%d %H:%M:%S')
            except:
                flash("Please enter date")
                return redirect(url_for("customer_edit_appointments",id=id))
                raise exceptions.BadRequestKeyError(str(e))
            appoint.Adate = date
            appoint.Alocation = request.form['location']
            docname = request.form['doctor']
            doctor = Doctor.query.filter(Doctor.Dname == docname).first()
            appoint.Adoc = doctor.id
            appoint.Ainfo = request.form['information']
            db.session.commit()
            return redirect(url_for('customer_my_appointments'))
    else:
        return redirect(url_for('loginCustomer'))


@app.route('/customer_my_appointments/delete_appo/<id>', methods=['GET', 'POST'])
def customer_delete_appointments(id):
    if not session.get("USERNAME") is None:
        if request.method == 'GET':
            appoint = Appointment.query.filter(Appointment.id == id).first()
            return render_template('customer_delete_appo.html', appoint=appoint)
        else:
            appoint = Appointment.query.filter(Appointment.id == id).first()
            db.session.delete(appoint)
            db.session.commit()
            return redirect(url_for('customer_my_appointments'))
    else:
        return redirect(url_for('loginCustomer'))

@app.route('/customer_my_appointments/operation/<id>', methods=['GET', 'POST'])
def customer_appo_operation(id):
    if not session.get("USERNAME") is None:
        if request.method == 'GET':
            appoint = Appointment.query.filter(Appointment.id == id).first()
            operation = Operation.query.filter(Operation.Oappiiontment == id).first()
            if operation and appoint.Ostatus == '1':
                print(operation)
                doc = Doctor.query.filter(Doctor.id == operation.Odoc).first()
                return render_template('customer_appo_operation.html', appoint=appoint, operation=operation, doc=doc)
            else:
                flash("No surgical approval is required for this appointment")
                return redirect(url_for('customer_my_appointments'))
        else:
            appoint = Appointment.query.filter(Appointment.id == id).first()
            if appoint.Ostatus == '1':
                appoint.Ostatus = '2'
                appoint.OperationStatus = "Ready to surgery"
                db.session.commit()
                flash("Ready to sugery")
            else:
                flash("No surgical approval is required")
            return redirect(url_for('customer_my_appointments'))
    else:
        return redirect(url_for('loginCustomer'))


@app.route('/customer_my_appointments/inpatient/<id>', methods=['GET', 'POST'])
def customer_appo_inpatient(id):
    if not session.get("USERNAME") is None:
        if request.method == 'GET':
            appoint = Appointment.query.filter(Appointment.id == id).first()
            inpatient = Hospitalization.query.filter(Hospitalization.Sappointment == id).first()
            if inpatient and appoint.Hstatus == '1':
                doc = Doctor.query.filter(Doctor.id == inpatient.Sdoc).first()
                return render_template('customer_appo_inpatient.html', title="Allows operation", appoint=appoint,
                                       inpatient=inpatient, doc=doc)
            else:
                flash("No in-patient approval is required for this appointment")
                return redirect(url_for('customer_my_appointments'))

        else:
            appoint = Appointment.query.filter(Appointment.id == id).first()
            if appoint.Hstatus == '1':
                appoint.Hstatus = '2'
                appoint.HospitalizationStatus = "Ready to inpatient"
                db.session.commit()
                flash("Ready to sugery")
            else:
                flash("No inpatient approval is required")
            return redirect(url_for('customer_my_appointments'))
    else:
        return redirect(url_for('loginCustomer'))


@app.route('/customer_my_appointments/release/<id>', methods=['GET', 'POST'])
def customer_appo_release(id):
    if not session.get("USERNAME") is None:
        if request.method == 'GET':
            appoint = Appointment.query.filter(Appointment.id == id).first()
            inpatient = Hospitalization.query.filter(Hospitalization.Sappointment == id).first()
            if inpatient and appoint.Hstatus == '3':
                doc = Doctor.query.filter(Doctor.id == inpatient.Sdoc).first()
                return render_template('customer_appo_release.html', title="Allows release", appoint=appoint,
                                       inpatient=inpatient, doc=doc)
            else:
                flash("No in-patient release approval is required for this appointment")
                return redirect(url_for('customer_my_appointments'))
        else:
            appoint = Appointment.query.filter(Appointment.id == id).first()
            if appoint.Hstatus == '3':
                appoint.Hstatus = '4'
                appoint.HospitalizationStatus = "Ready to release"
                db.session.commit()
                flash("Ready to release")
            else:
                flash("No release approval is required")
            return redirect(url_for('customer_my_appointments'))
    else:
        return redirect(url_for('loginCustomer'))


    
@app.route('/checkuser', methods=['POST'])
def check_username():
	chosen_name = request.form['username']
	user_in_db = User.query.filter(User.username == chosen_name).first()
	if not user_in_db:
		return jsonify({'text': 'Username is available',
						'returnvalue': 0})
	else:
		return jsonify({'text': 'Sorry! Username is already taken',
						'returvalue': 1})    

    
    


def validatePhone(str):
    if len(str) != 11:
        return False
    elif str[0] != "1":
        return False
        # elif str
    for i in str:
        if i >= "0" or i <= "9":
            return 1

    return 0

def validateEmail(email):
    if len(email) > 7:
        if re.match("^.+\\@(\\[?)[a-zA-Z0-9\\-\\.]+\\.([a-zA-Z]{2,3}|[0-9]{1,3})(\\]?)$", email) != None:
            return 1
    return 0

def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        pass

    try:
        import unicodedata
        unicodedata.numeric(s)
        return True
    except (TypeError, ValueError):
        pass

    return False


@app.errorhandler(404)
def page_not_found(e):
    return render_template('page-error-404.html'), 404

@app.errorhandler(500)
def page_not_found(e):
    return render_template('page-error-500.html'), 500