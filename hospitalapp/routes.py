import os

from datetime import date

from flask import render_template, flash, redirect, url_for, session, request, abort
from werkzeug.security import check_password_hash, generate_password_hash

from hospitalapp import app, db
from hospitalapp.forms import *
from hospitalapp.models import *
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


@app.route('/loggedin_home_customer', methods=['GET', 'POST'])
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
        employee = Employee(Ename=form.Eusername.data, EIDcard=form.Eidcard.data, Ephone=form.Ephone.data,
                            Egender=form.Egender.data, Eemail=form.Eemail.data, Ehiredate=form.Ehiredate.data,
                            Epassword=passw_hash)
        db.session.add(employee)
        db.session.commit()
        session["USERNAME"] = employee.Ename
        return redirect(url_for("loginEmployee"))
    return render_template('signup_employee.html', title='Register a new user', form=form)


@app.route('/ArrMainEmp')
def ArrMainEmp():
    if not session.get("USERNAME") is None:
        user_in_db = Employee.query.filter(Employee.Ename == session.get("USERNAME")).first()
        return render_template('Arr_Main_Emp.html', Eusername=user_in_db.Ename)
    else:
        flash("Employee needs to either login or signup first")
        return redirect(url_for('loginEmployee'))


@app.route('/arraarrangeappointmentEmployee', methods=['GET', 'POST'])
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
            appointment = Appointment(Apet=pet, Atype=type, Adoc=doctor, Acomplete=complete, Ainfo=infomation,
                                      Adate=date, Acost=cost, AneedHospitalization='1', AneedOperation='1',
                                      AneedPrescription='1')
            db.session.add(appointment)
            db.session.commit()
            return redirect(url_for('loggedin_home_employee'))
        return render_template('arr_appointment_emp.html', title='arrangeappointment', form=form)
    else:
        flash("User needs to either login or signup first")
        return redirect(url_for('employee_mainpage'))


# @app.route('/Prescription', methods=['GET', 'POST'])
# def Prescription():
#     form = PrescriptionForm()
#     if not session.get("USERNAME") is None:
#         if form.validate_on_submit():
#             medicine = form.Pmed.data
#             number = form.Pnumber.data
#             appointment = form.Pappointment.data
#             prescription = Prescription(Pmedicine=medicine,Pnumber=number,Pappointment=appointment)
#             db.session.add(prescription)
#             db.session.commit()
#             return redirect(url_for('loggedin_home_employee'))
#         return render_template('Prescription.html',title='Prescription',form=form)
#     else:
#         flash("User needs to either login or signup first")
#         return redirect(url_for('employee_mainpage'))




@app.route('/AddHospitalization/<id>', methods=['GET', 'POST'])
def AddHospitalization(id):
    form = AddHospitalizationForm()
    if not session.get("USERNAME") is None:
        appo_obj = Appointment.query.filter_by(id=id).first()
        if not appo_obj:
            abort(404)
        if form.validate_on_submit():
            appo_obj.AneedHospitalization = '0'  # this appointment need an hospitalization
            appo_obj.HospitalizationPer = '1'  # customer not permit the hospitalization
            hospitalization = Hospitalization(Sdoc=appo_obj.Adoc, Sappointment=id, Sroom=form.room.data,
                                              Sstartdate=form.startdate.data, Senddate=form.enddate.data,
                                              Scost=form.cost.data)
            db.session.add(hospitalization)
            db.session.commit()
            flash('Add hospitalization successfully', 'success')
            return redirect(url_for('ArrAppEmployeeYD'))
        else:
            print(form.errors)
        return render_template('AddHospitalization.html', title='Add Hospitalization', form=form, id=id)
    else:
        flash("User needs to either login or signup first")
        return redirect(url_for('employee_mainpage'))

@app.route('/AddPrescription/<id>', methods=['GET', 'POST'])
def AddPrescription(id):
    form1 = AddPrescriptionForm()
    form2 = AddPrescriptionForm()
    form3 = AddPrescriptionForm()
    if not session.get("USERNAME") is None:
        appo_obj = Appointment.query.filter_by(id=id).first()
        if not appo_obj:
            abort(404)
        if form1.submit.data and form1.validate():
            appo_obj.AneedPrescription = '0'  # this appointment need an prescription
            prescription1 = Prescription(Pmedicine=form1.medicine.data, Pnumber=form1.number.data, Pappointment=id)
            db.session.add(prescription1)
            db.session.commit()
            flash('Add hospitalization successfully', 'success')
            return redirect(url_for('AddPrescription', id=id))
        else:
            print(form1.errors)
        if form2.submit.data and form2.validate():
            appo_obj.AneedPrescription = '0'  # this appointment need an prescription
            prescription2 = Prescription(Pmedicine=form2.medicine.data, Pnumber=form2.number.data, Pappointment=id)
            db.session.add(prescription2)
            db.session.commit()
            flash('Add hospitalization successfully', 'success')
            return redirect(url_for('AddPrescription', id=id))
        else:
            print(form2.errors)
        if form3.submit.data and form3.validate():
            appo_obj.AneedPrescription = '0'  # this appointment need an prescription
            prescription3 = Prescription(Pmedicine=form3.medicine.data, Pnumber=form3.number.data, Pappointment=id)
            db.session.add(prescription3)
            db.session.commit()
            flash('Add hospitalization successfully', 'success')
            return redirect(url_for('AddPrescription', id=id))
        else:
            print(form3.errors)
        return render_template('AddPrescription.html', title='Add Prescription', form1=form1, form2=form2, form3=form3,
                               id=id)
    else:
        flash("User needs to either login or signup first")
        return redirect(url_for('employee_mainpage'))

@app.route('/OperationMain', methods=['GET', 'POST'])
def OperationMain():
    if not session.get("USERNAME") is None:
        user_in_db = Employee.query.filter(Employee.Ename == session.get("USERNAME")).first()
        return render_template('OperationMain.html', Eusername=user_in_db.Ename)
    else:
        flash("Employee needs to either login or signup first")
        return redirect(url_for('loginEmployee'))

@app.route('/HospitalizationMain', methods=['GET', 'POST'])
def HospitalizationMain():
    if not session.get("USERNAME") is None:
        user_in_db = Employee.query.filter(Employee.Ename == session.get("USERNAME")).first()
        return render_template('HospitalizationMain.html', Eusername=user_in_db.Ename)
    else:
        flash("Employee needs to either login or signup first")
        return redirect(url_for('loginEmployee'))

@app.route('/ApplyingOperationPermission', methods=['GET', 'POST'])
# Arrange confirmed appointments
def ApplyingOperationPermission():
    if not session.get("USERNAME") is None:
        standard_appointments = Appointment.query.filter(Appointment.Atype == '1',
                                                         Appointment.Acomplete == '1',Appointment.AneedOperation=='0',Appointment.OperationPer=='1').all()
        emergency_appointments = Appointment.query.filter(Appointment.Atype == '0',
                                                          Appointment.Acomplete == '1',Appointment.AneedOperation=='0',Appointment.OperationPer=='1').all()
        return render_template('ApplyingOperationPermission.html', title='Displays procedures for which customer approval is being sought',
                               standard_appointments=standard_appointments,
                               emergency_appointments=emergency_appointments)
    else:
        flash("User needs to either login or signup first")
        return redirect(url_for('employee_mainpage'))

@app.route('/UnderOperation', methods=['GET', 'POST'])
# Arrange confirmed appointments
def UnderOperation():
    if not session.get("USERNAME") is None:
        standard_appointments = Appointment.query.filter(Appointment.Atype == '1',
                                                         Appointment.Acomplete == '1',Appointment.AneedOperation=='0',Appointment.OperationPer=='0',Appointment.OperationEnd=='1').all()
        emergency_appointments = Appointment.query.filter(Appointment.Atype == '0',
                                                          Appointment.Acomplete == '1',Appointment.AneedOperation=='0',Appointment.OperationPer=='0',Appointment.OperationEnd=='1').all()
        return render_template('UnderOperation.html', title='Preparing for operation',
                               standard_appointments=standard_appointments,
                               emergency_appointments=emergency_appointments)
    else:
        flash("User needs to either login or signup first")
        return redirect(url_for('employee_mainpage'))

@app.route('/AddOperation/<id>', methods=['GET', 'POST'])
def AddOperation(id):
    form = AddOperationForm()
    if not session.get("USERNAME") is None:
        appo_obj = Appointment.query.filter_by(id=id).first()
        if not appo_obj:
            abort(404)
        if form.validate_on_submit():
            appo_obj.AneedOperation = '0'  # this appointment need an operation
            appo_obj.OperationPer = '1'  # customer not permit the operation
            operation = Operation(Oappiiontment=id, Odoc=appo_obj.Adoc, Odate=form.Odate.data, Oinf=form.Oinf.data,
                                  Ocost=form.Ocost.data)
            db.session.add(operation)
            db.session.commit()
            flash('Add operation successfully', 'success')
            return redirect(url_for('ArrAppEmployeeYD'))
        else:
            print(form.errors)
        return render_template('AddOperation.html', title='Add Operation', form=form, id=id)
    else:
        flash("User needs to either login or signup first")
        return redirect(url_for('employee_mainpage'))


@app.route('/CompleteOpeConfirm/<id>', methods=['GET', 'POST'])
# Arrange confirmed appointments
def CompleteOpeConfirm(id):
    form = CompleteOperationConfirmForm()
    if not session.get("USERNAME") is None:
        appointment = Appointment.query.filter(id == id).first()
        if form.validate_on_submit():
            appointment.OperationEnd=form.complete.data
            db.session.commit()
            flash('Confirm successfully', 'success')
            return redirect(url_for('UnderOperation'))
        return render_template('CompleteOperationConfirm.html', title='Preparing for operation',form=form,id=id)
    else:
        flash("User needs to either login or signup first")
        return redirect(url_for('employee_mainpage'))

@app.route('/CompletedOperation', methods=['GET', 'POST'])
# Arrange confirmed appointments
def CompletedOperation():
    if not session.get("USERNAME") is None:
        standard_appointments = Appointment.query.filter(Appointment.Atype == '1',
                                                         Appointment.Acomplete == '1',Appointment.AneedOperation=='0',Appointment.OperationPer=='0',Appointment.OperationEnd=='0').all()
        emergency_appointments = Appointment.query.filter(Appointment.Atype == '0',
                                                          Appointment.Acomplete == '1',Appointment.AneedOperation=='0',Appointment.OperationPer=='0',Appointment.OperationEnd=='0').all()
        return render_template('CompletedOperation.html', title='Completed Operation',
                               standard_appointments=standard_appointments,
                               emergency_appointments=emergency_appointments)
    else:
        flash("User needs to either login or signup first")
        return redirect(url_for('employee_mainpage'))

@app.route('/ApplyingHospitalizationPermission', methods=['GET', 'POST'])
# 9. The customer's permission for hospitalization is being sought
def ApplyingHospitalizationPermission():
    if not session.get("USERNAME") is None:
        standard_appointments = Appointment.query.filter(Appointment.Atype == '1',
                                                         Appointment.Acomplete == '1',Appointment.AneedHospitalization=='0',Appointment.HospitalizationPer=='1').all()
        emergency_appointments = Appointment.query.filter(Appointment.Atype == '0',
                                                          Appointment.Acomplete == '1',Appointment.AneedHospitalization=='0',Appointment.HospitalizationPer=='1').all()
        return render_template('ApplyingHospitalizationPermission.html', title='Displays procedures for which customer approval is being sought',
                               standard_appointments=standard_appointments,
                               emergency_appointments=emergency_appointments)
    else:
        flash("User needs to either login or signup first")
        return redirect(url_for('employee_mainpage'))

@app.route('/InHospitalization', methods=['GET', 'POST'])
# 10. The pet is in hospital
def InHospitalization():
    if not session.get("USERNAME") is None:
        standard_appointments = Appointment.query.filter(Appointment.Atype == '1',
                                                         Appointment.Acomplete == '1',Appointment.AneedHospitalization=='0',Appointment.HospitalizationPer=='0',Appointment.HospitalizationEnd=='1').all()
        emergency_appointments = Appointment.query.filter(Appointment.Atype == '0',
                                                          Appointment.Acomplete == '1',Appointment.AneedHospitalization=='0',Appointment.HospitalizationPer=='0',Appointment.HospitalizationEnd=='1').all()
        return render_template('InHospitalization.html', title='Displays procedures for which customer approval is being sought',
                               standard_appointments=standard_appointments,
                               emergency_appointments=emergency_appointments)
    else:
        flash("User needs to either login or signup first")
        return redirect(url_for('employee_mainpage'))

@app.route('/ReleaseHos', methods=['GET', 'POST'])
# 7. Have been discharged from hospital
def ReleaseHos():
    if not session.get("USERNAME") is None:
        standard_appointments = Appointment.query.filter(Appointment.Atype == '1',
                                                         Appointment.Acomplete == '1',Appointment.AneedHospitalization=='0',Appointment.HospitalizationPer=='0',Appointment.HospitalizationEnd=='0').all()
        emergency_appointments = Appointment.query.filter(Appointment.Atype == '0',
                                                          Appointment.Acomplete == '1',Appointment.AneedHospitalization=='0',Appointment.HospitalizationPer=='0',Appointment.HospitalizationEnd=='0').all()
        return render_template('ReleaseHos.html', title='Displays procedures for which customer approval is being sought',
                               standard_appointments=standard_appointments,
                               emergency_appointments=emergency_appointments)
    else:
        flash("User needs to either login or signup first")
        return redirect(url_for('employee_mainpage'))

@app.route('/ArrAppEmployeeYD', methods=['GET', 'POST'])
# Arrange confirmed appointments
def ArrAppEmployeeYD():
    if not session.get("USERNAME") is None:
        standard_appointments = Appointment.query.filter(Appointment.Atype == '1',
                                                         Appointment.Acomplete == '0').all()  # 0 : has been diagnosed
        emergency_appointments = Appointment.query.filter(Appointment.Atype == '0', Appointment.Acomplete == '0').all()
        return render_template('ArrAppEmployeeYD.html', title='Display appointment has completed diagnosis',
                               standard_appointments=standard_appointments,
                               emergency_appointments=emergency_appointments)
    else:
        flash("User needs to either login or signup first")
        return redirect(url_for('employee_mainpage'))


@app.route('/ArrAppEmployeeND', methods=['GET', 'POST'])
def ArrAppEmployeeND():
    if not session.get("USERNAME") is None:
        standard_appointments = Appointment.query.filter(Appointment.Atype == '1',
                                                         Appointment.Acomplete == '1').all()  # 1 : not diagnosis yet
        emergency_appointments = Appointment.query.filter(Appointment.Atype == '0', Appointment.Acomplete == '1').all()
        return render_template('ArrAppEmployeeND.html', title='Display Appointment Employee',
                               standard_appointments=standard_appointments,
                               emergency_appointments=emergency_appointments)
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
        return render_template('AppointmentDetail.html', title='Modify Appointment', form=form, id=id)

    else:
        flash("User needs to either login or signup first")
        return redirect(url_for('employee_mainpage'))


@app.route('/listproduct', methods=['GET', 'POST'])
def listproduct():
    goods = Good.query.all()
    return render_template('adminproduct.html', title='Shop', goods=goods)


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
                #flash("Add product successfully")
            return redirect(url_for('listproduct'))
        return render_template('addproduct.html', title='addproduct', form=form)
    else:
        flash("User needs to either login or signup first")
        return redirect(url_for('employee_mainpage'))


@app.route('/deleteproduct/<id>', methods=['GET', 'POST'])
def deleteproduct(id):
    good = Good.query.get_or_404(id)
    db.session.delete(good)
    db.session.commit()
    #flash("Delete Product")
    return redirect(url_for('listproduct'))


@app.route('/editproduct/<id>', methods=['GET', 'POST'])
def editproduct(id):
    form = AddProductForm()
    good = Good.query.get_or_404(id)
    form.Gid.data=good.id
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
            #flash("Add product successfully")
        return redirect(url_for('listproduct'))
    return render_template('editproduct.html', form=form)


@app.route('/order', methods=['GET', 'POST'])
def order():
    form = OrderForm()
    if form.validate_on_submit():
        return redirect(url_for('paypage'))
    render_template('order.html', title='order', form=form)


@app.route('/signupCustomer', methods=['GET', 'POST'])
def signupCustomer():
    form = SignupCustomer()
    if form.validate_on_submit():
        print("888888")
        if form.Cpassword.data != form.Cpassword2.data:
            flash('Passwords do not match!')
            print("99999")
            return redirect(url_for('signupCustomer'))
        passw_hash = generate_password_hash(form.Cpassword.data)
        # customer = Customer(Cname=form.Cusername.data, Cphone=form.Cphone.data, Cemail=form.Cemail.data, password_hash=passw_hash)
        customer = Customer(Cname=form.Cusername.data, Cphone=form.Cphone.data, Cemail=form.Cemail.data,
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
