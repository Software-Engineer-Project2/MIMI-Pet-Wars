import os

from datetime import datetime

from flask import render_template, flash, redirect, url_for, session, request, abort
from werkzeug.security import check_password_hash, generate_password_hash
from werkzeug.utils import secure_filename

from hospitalapp import app, db
from hospitalapp.forms import *
from hospitalapp.models import *
from hospitalapp import photos
from flask_uploads import UploadSet, IMAGES, configure_uploads

photos = UploadSet('photos', IMAGES)
configure_uploads(app, photos)


@app.route('/')
def choose_language():
    return render_template('choose_language.html', title='Home')


@app.route('/index')
def index():
    return render_template('index.html', title='Home')


@app.route('/index_chinese')
def index_chinese():
    return render_template('index_chinese.html', title='Home')


@app.route('/about')
def about():
    return render_template('about_us.html', title='about')


@app.route('/customer_mainpage')
def customer_mainpage():
    return render_template('customer_mainpage.html', title='Home')


@app.route('/customer_mainpage_chinese')
def customer_mainpage_chinese():
    return render_template('customer_mainpage_chinese.html', title='Home')


@app.route('/employee_mainpage')
def employee_mainpage():
    return render_template('employee_mainpage.html', title='Home')


@app.route('/employee_mainpage_chinese')
def employee_mainpage_chinese():
    return render_template('employee_mainpage_chinese.html', title='Home')


@app.route('/loggedin_home_customer', methods=['GET', 'POST'])
def loggedin_home_customer():
    if not session.get("USERNAME") is None:
        user_in_db = Customer.query.filter(Customer.Cname == session.get("USERNAME")).first()
        return render_template('loggedin_home_customer.html', Cusername=user_in_db.Cname)
    else:
        flash("Customer needs to either login or signup first")
        return redirect(url_for('customer_mainpage'))


@app.route('/loggedin_home_customer_chinese', methods=['GET', 'POST'])
def loggedin_home_customer_chinese():
    if not session.get("USERNAME") is None:
        user_in_db = Customer.query.filter(Customer.Cname == session.get("USERNAME")).first()
        return render_template('loggedin_home_customer_chinese.html', Cusername=user_in_db.Cname)
    else:
        flash("Customer needs to either login or signup first")
        return redirect(url_for('customer_mainpage_chinese'))


@app.route('/loggedin_home_employee')
def loggedin_home_employee():
    if not session.get("USERNAME") is None:
        user_in_db = Employee.query.filter(Employee.Ename == session.get("USERNAME")).first()
        return render_template('loggedin_home_employee.html', Eusername=user_in_db.Ename)
    else:
        flash("Employee needs to either login or signup first")
        return redirect(url_for('loginEmployee'))


@app.route('/loggedin_home_employee_chinese')
def loggedin_home_employee_chinese():
    if not session.get("USERNAME") is None:
        user_in_db = Employee.query.filter(Employee.Ename == session.get("USERNAME")).first()
        return render_template('loggedin_home_employee_chinese.html', Eusername=user_in_db.Ename)
    else:
        flash("雇员需要登录或者注册首先")
        return redirect(url_for('loginEmployee_chinese'))



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
        return redirect(url_for('loginEmployee'))
    return render_template('login_employee.html', title='Sign In', form=form)


@app.route('/loginEmployee_chinese', methods=['GET', 'POST'])
def loginEmployee_chinese():
    form = LoginFormEmployee_chinese()
    if form.validate_on_submit():
        user_in_db = Employee.query.filter(Employee.Ename == form.Eusername.data).first()
        if not user_in_db:
            flash('没有发现用户: {}'.format(form.Eusername.data))
            return redirect(url_for('loginEmployee'))
        if check_password_hash(user_in_db.Epassword, form.Epassword.data):
            flash('登录成功!')
            session["USERNAME"] = user_in_db.Ename
            return redirect(url_for('loggedin_home_employee_chinese'))
        flash('密码不正确')
        return redirect(url_for('loginEmployee'))
    return render_template('login_employee_chinese.html', title='Sign In', form=form)


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


@app.route('/employee_appointment')
def employee_appointment():
    if not session.get("USERNAME") is None:
        return render_template('employee_appointment.html', title='Home')
    else:
        flash("User needs to either login or signup first")
        return redirect(url_for('employee_mainpage'))


@app.route('/employee_appo_checkin', methods=['GET', 'POST'])
def employee_appo_checkin():
    if not session.get("USERNAME") is None:

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
        return redirect(url_for('employee_mainpage'))


@app.route('/employee_appo_checkin/view_appo/<id>', methods=['GET', 'POST'])
def employee_checkin_view():
    if not session.get("USERNAME") is None:
        appoint = Appointment.query.filter(Appointment.id == id).first()
        return render_template('employee_checkin_view.html', appoint=appoint)
    else:
        flash("User needs to either login or signup first")
        return redirect(url_for('employee_mainpage'))


@app.route('/employee_appo_checkin/checkin_appo/<id>', methods=['GET', 'POST'])
def employee_checkin(id):
    if not session.get("USERNAME") is None:
        appoint = Appointment.query.filter(Appointment.id == id).first()
        if request.method == 'GET':
            return render_template('employee_checkin.html', appoint=appoint)
        else:
            appoint.Astart = '1'
            db.session.commit()
            return redirect(url_for('employee_appo_checkin'))
    else:
        flash("User needs to either login or signup first")
        return redirect(url_for('employee_mainpage'))


@app.route('/employee_appo_outpatient', methods=['GET', 'POST'])
def employee_appo_outpatient():
    if not session.get("USERNAME") is None:
        pets = Pet.query.filter().all()
        customers = Customer.query.filter().all()
        appointments = Appointment.query.filter(Appointment.Astart == '1',
                                                Appointment.Acomplete == '0').all()  # type-1 complete-0 - Standard Appointments not checkin
        appointments2 = Appointment.query.filter(Appointment.Astart == '1',
                                                Appointment.Ostatus == '3').all()
        appointments3 = Appointment.query.filter(Appointment.Astart == '1',
                                                 Appointment.Hstatus == '5').all()
        appointments.append(appointments2)
        appointments.append(appointments2)
        print(appointments)
        # type-1 complete-0 - Standard Appointments not checkin
        return render_template('employee_appo_outpatient.html', title='Display appointment not checkin yet',
                               appointments=appointments, pets=pets, customers=customers)
    else:
        flash("User needs to either login or signup first")
        return redirect(url_for('employee_mainpage'))


@app.route('/employee_appo_outpatient/complete/<id>', methods=['GET', 'POST'])
def employee_outpatient_finish(id):
    if not session.get("USERNAME") is None:
        appoint = Appointment.query.filter(Appointment.id == id).first()
        if request.method == 'GET':
            return render_template('employee_outpatient_complete.html', appoint=appoint)
        else:
            appoint.Acomplete = '1'
            db.session.commit()
            return redirect(url_for('employee_appo_outpatient'))
    else:
        flash("User needs to either login or signup first")
        return redirect(url_for('employee_mainpage'))


@app.route('/employee_appo_outpatient/operation/<id>', methods=['GET', 'POST'])
def employee_outpatient_operation(id):
    if not session.get("USERNAME") is None:
        form = AddOperationForm()
        appoint = Appointment.query.filter(Appointment.id == id).first()
        doctor = Doctor.query.filter(Doctor.id == appoint.Adoc).first()
        if form.validate_on_submit():
            operation = Operation(oappointment=appoint, odoctor=doctor, Odate=form.Odate.data, Oinf=form.Oinf.data,
                                  Ocost=form.Ocost.data)
            appoint.OperationStatus = "Inform customer operation"
            appoint.Ostatus = '1'
            db.session.add(operation)
            db.session.commit()
            return redirect(url_for('employee_appo_outpatient'))
        return render_template('employee_outpatient_operation.html',
                               title='Enter operation information and inform customer', form=form, appoint=appoint)
    else:
        flash("User needs to either login or signup first")
        return redirect(url_for('employee_mainpage'))


@app.route('/employee_appo_outpatient/inpatient/<id>', methods=['GET', 'POST'])
def employee_outpatient_inpatient(id):
    if not session.get("USERNAME") is None:
        form = AddHospitalizationForm()
        appoint = Appointment.query.filter(Appointment.id == id).first()
        doctor = Doctor.query.filter(Doctor.id == appoint.Adoc).first()
        if form.validate_on_submit():
            inpatient = Hospitalization(happointment=appoint, sdoctor=doctor, Sroom=form.room.data,
                                        Sstartdate=form.startdate.data, Senddate=form.enddate.data,
                                        Scost=form.cost.data)
            appoint.HospitalizationStatus = "Inform customer inpatient"
            appoint.Hstatus = '1'
            db.session.add(inpatient)
            db.session.commit()
            return redirect(url_for('employee_appo_outpatient'))
        return render_template('employee_outpatient_inpatient.html',
                               title='Enter operation information and inform customer', form=form, appoint=appoint)
    else:
        flash("User needs to either login or signup first")
        return redirect(url_for('employee_mainpage'))


@app.route('/employee_appo_inpatient', methods=['GET', 'POST'])
def employee_appo_inpatient():
    if not session.get("USERNAME") is None:
        pets = Pet.query.filter().all()
        customers = Customer.query.filter().all()
        Iappointments = Appointment.query.filter(Appointment.Astart == '1', Appointment.Acomplete == '0',
                                                 Appointment.Hstatus == '2').all()  # type-1 complete-0 - Standard Appointments not checkin
        Rappointments = Appointment.query.filter(Appointment.Astart == '1', Appointment.Acomplete == '0',
                                                 Appointment.Hstatus == '4').all()  # type-1 complete-0 - Standard Appointments not checkin
        # type-1 complete-0 - Standard Appointments not checkin
        return render_template('employee_appo_inpatient.html', title='Display In-patient appointments',
                               Iappointments=Iappointments, Rappointments=Rappointments, pets=pets, customers=customers)
    else:
        flash("User needs to either login or signup first")
        return redirect(url_for('employee_mainpage'))


@app.route('/employee_appo_inpatient/release/<id>', methods=['GET', 'POST'])
def employee_inpatient_release(id):
    if not session.get("USERNAME") is None:
        if request.method == 'GET':
            appoint = Appointment.query.filter(Appointment.id == id).first()
            return render_template('employee_inpatient_release.html', title="Inform customer to Rlease",
                                   appoint=appoint)
        else:
            appoint = Appointment.query.filter(Appointment.id == id).first()
            appoint.Hstatus = '3'
            appoint.HospitalizationStatus = "Inform customer of release"
            db.session.commit()
            return redirect(url_for('employee_appo_inpatient'))
    else:
        flash("User needs to either login or signup first")
        return redirect(url_for('employee_mainpage'))


@app.route('/employee_appo_inpatient/release_complete/<id>', methods=['GET', 'POST'])
def employee_inpatient_releasecomplete(id):
    if not session.get("USERNAME") is None:
        if request.method == 'GET':
            appoint = Appointment.query.filter(Appointment.id == id).first()
            return render_template('employee_inpatient_releasecomplete.html', title="Complete inpatient",
                                   appoint=appoint)
        else:
            appoint = Appointment.query.filter(Appointment.id == id).first()
            appoint.Hstatus = '5'
            appoint.HospitalizationStatus = "Released"
            db.session.commit()
            return redirect(url_for('employee_appo_inpatient'))
    else:
        flash("User needs to either login or signup first")
        return redirect(url_for('employee_mainpage'))


@app.route('/employee_appo_operation', methods=['GET', 'POST'])
def employee_appo_operation():
    if not session.get("USERNAME") is None:
        pets = Pet.query.filter().all()
        customers = Customer.query.filter().all()
        appoints = Appointment.query.filter(Appointment.Astart == '1', Appointment.Acomplete == '0',
                                                Appointment.Ostatus == '2').all()  # type-1 complete-0 - Standard Appointments not checkin
        operations = Operation.query.filter().all()
        print(operations)
        print(appoints)
        print(pets)
        return render_template('employee_appo_operation.html', title='Display In-patient appointments',
                               appoints=appoints,pets=pets, customers=customers,operations=operations)
    else:
        flash("User needs to either login or signup first")
        return redirect(url_for('employee_mainpage'))

@app.route('/employee_appo_operation/complete operation/<id>', methods=['GET', 'POST'])
def employee_operation_complete(id):
    if not session.get("USERNAME") is None:
        if request.method == 'GET':
            appoint = Appointment.query.filter(Appointment.id == id).first()
            return render_template('employee_operation_complete.html', title="Complete operation",
                                   appoint=appoint)
        else:
            appoint = Appointment.query.filter(Appointment.id == id).first()
            appoint.Ostatus = '3'
            appoint.OperationStatus = "Operation Completed"
            db.session.commit()
            return redirect(url_for('employee_appo_operation'))
    else:
        flash("User needs to either login or signup first")
        return redirect(url_for('employee_mainpage'))


@app.route('/employee_appo_completed', methods=['GET', 'POST'])
def employee_appo_completed():
    if not session.get("USERNAME") is None:
        pets = Pet.query.filter().all()
        customers = Customer.query.filter().all()
        appointments = Appointment.query.filter(
            Appointment.Acomplete == '1').all()  # type-1 complete-0 - Standard Appointments not checkin
        return render_template('employee_appo_completed.html', title='Display appointment completed',
                               appointments=appointments, pets=pets, customers=customers)
    else:
        flash("User needs to either login or signup first")
        return redirect(url_for('employee_mainpage'))

@app.route('/employee_pets', methods=['GET', 'POST'])
def employee_pets():
    if not session.get("USERNAME") is None:
        pets = Pet.query.filter().all()
        customers = Customer.query.filter().all()
        return render_template('employee_pets.html', title='Display In-patient appointments',pets=pets, customers=customers)
    else:
        flash("User needs to either login or signup first")
        return redirect(url_for('employee_mainpage'))

@app.route('/employee_customers', methods=['GET', 'POST'])
def employee_customers():
    if not session.get("USERNAME") is None:
        customers = Customer.query.filter().all()
        return render_template('employee_customers.html', title='Display In-patient appointments', customers=customers)
    else:
        flash("User needs to either login or signup first")
        return redirect(url_for('employee_mainpage'))

@app.route('/employee_doctors', methods=['GET', 'POST'])
def employee_doctors():
    if not session.get("USERNAME") is None:
        doctors = Doctor.query.filter().all()
        return render_template('employee_doctors.html', title='Display In-patient appointments',doctors=doctors)
    else:
        flash("User needs to either login or signup first")
        return redirect(url_for('employee_mainpage'))

@app.route('/listproduct', methods=['GET', 'POST'])
def listproduct():
    goods = Good.query.all()
    return render_template('adminproduct.html', title='Shop', goods=goods)


@app.route('/employee_posts')
def employee_posts():
    if not session.get("USERNAME") is None:
        posts = Post.query.all()
        read_posts = set()
        for post in posts:
            if post.Panswer.all():
                read_posts.add(post)

        unread_posts = Post.query.filter(Post.Panswer == None).all()

        print('unread posts', unread_posts)
        return render_template('employee_posts.html', unread_posts=unread_posts, read_posts=read_posts)
    else:
        return redirect(url_for('employee_mainpage'))


@app.route('/employee_posts/<id>', methods=['GET', 'POST'])
def employee_post_detail(id):
    if not session.get("USERNAME") is None:
        post = Post.query.filter_by(id=id).first()
        answer = post.Panswer.all()
        return render_template('employee_post_detail.html', post=post, answer=answer)
    else:
        return redirect(url_for('employee_mainpage'))


@app.route('/employee_posts/employee_answer_post/<id>', methods=['GET', 'POST'])
def employee_answer_post(id):
    form = AnswerForm()
    if not session.get("USERNAME") is None:
        post = Post.query.filter_by(id=id).first()
        if form.validate_on_submit():
            answer = Answer(Acontent=form.content.data, Apost=post.id)
            db.session.add(answer)
            db.session.commit()
            return redirect(url_for('employee_posts'))
        return render_template('employee_answer_post.html', post=post, form=form, id=id)
    else:
        return redirect(url_for('employee_mainpage'))


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
                # flash("Add product successfully")
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
    # flash("Delete Product")
    return redirect(url_for('listproduct'))


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


@app.route('/shoppage_chinese', methods=['GET', 'POST'])
def shoppage_chinese():
    goods = Good.query.all()
    return render_template('shoppage_chinese.html', goods=goods)


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


@app.route('/signupCustomer_chinese', methods=['GET', 'POST'])
def signupCustomer_chinese():
    form = SignupCustomer_chinese()
    if form.validate_on_submit():
        print("888888")
        if form.Cpassword.data != form.Cpassword2.data:
            flash('密码不匹配!')
            return redirect(url_for('signupCustomer_chinese'))
        passw_hash = generate_password_hash(form.Cpassword.data)
        # customer = Customer(Cname=form.Cusername.data, Cphone=form.Cphone.data, Cemail=form.Cemail.data, password_hash=passw_hash)
        customer = Customer(Cname=form.Cusername.data, Cphone=form.Cphone.data, Cemail=form.Cemail.data,
                            Cgender=form.Cgender.data, Cpassword=passw_hash)
        db.session.add(customer)
        db.session.commit()
        session["USERNAME"] = customer.Cname
        flash('欢迎你, %s ! , 你已经注册成功' % customer.Cname)
        return redirect(url_for('loginCustomer_chinese'))
    return render_template('signup_customer_chinese.html', title='Register a new user', form=form)


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


@app.route('/loginCustomer_chinese', methods=['GET', 'POST'])
def loginCustomer_chinese():
    form = LoginFormCustomer_chinese()
    if form.validate_on_submit():
        user_in_db = Customer.query.filter(Customer.Cname == form.Cusername.data).first()
        if not user_in_db:
            flash('没有发现用户名 {}'.format(form.Cusername.data))
            return redirect(url_for('loginCustomer_chinese'))
        if check_password_hash(user_in_db.Cpassword, form.Cpassword.data):
            flash('登录成功!')
            session["USERNAME"] = user_in_db.Cname
            return redirect(url_for('loggedin_home_customer_chinese'))
        flash('密码不正确')
        return redirect(url_for('loginCustomer_chinese'))
    return render_template('login_customer_chinese.html', title='Login In', form=form)


@app.route('/customer_add_post', methods=['GET', 'POST'])
def customer_add_post():
    form = PostForm()
    if not session.get("USERNAME") is None:
        customer_in_db = Customer.query.filter(Customer.Cname == session.get("USERNAME")).first()
        if form.validate_on_submit():
            post = Post(Ptopic=form.topic.data, Pcontent=form.content.data, poster=customer_in_db)
            db.session.add(post)
            db.session.commit()
            return redirect(url_for('customer_posts'))
        return render_template('customer_add_post.html', user=customer_in_db, form=form)
    else:
        return redirect(url_for('loginCustomer'))


@app.route('/customer_posts_chinese')
def customer_posts_chinese():
    if not session.get("USERNAME") is None:
        customer_in_db = Customer.query.filter(Customer.Cname == session.get("USERNAME")).first()
        posts = customer_in_db.Cpost.all()
        read_posts = set()
        for p in posts:
            if p.Panswer.all():
                read_posts.add(p)
        unread_posts = customer_in_db.Cpost.filter(Post.Panswer == None).all()
        return render_template('customer_posts_chinese.html', user=customer_in_db, unread_posts=unread_posts,
                               read_posts=read_posts)
    else:
        return redirect(url_for('loginCustomer_chinese'))

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


@app.route('/customer_posts/<id>', methods=['GET', 'POST'])
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
    return redirect(url_for('employee_mainpage'))


@app.route('/Make Appointment', methods=['GET', 'POST'])
def make_appointment():
    form = MakeAppointment()
    if form.validate_on_submit():
        pet = Pet.query.filter(Pet.id == int(form.pet.data)).first()
        appointment = Appointment(apppetter=pet, Atype=form.type.data,
                                  Adoc=form.doctor.data, Alocation=form.chooseposition.data, Adate=form.datetime.data,
                                  Ainfo=form.otherdescription.data,
                                  Acomplete='0', Astart='0')
        db.session.add(appointment)
        db.session.commit()
        return redirect(url_for('loggedin_home_customer'))

    return render_template('make_appointment_customer.html', title='Make Appointment', form=form)


@app.route('/Make Appointment_chinese', methods=['GET', 'POST'])
def make_appointment_chinese():
    form = MakeAppointment_chinese()
    if form.validate_on_submit():
        pet = Pet.query.filter(Pet.id == int(form.pet.data)).first()
        appointment = Appointment(apppetter=pet, Atype=form.type.data,
                                  Adoc=form.doctor.data, Alocation=form.chooseposition.data, Adate=form.datetime.data,
                                  Ainfo=form.otherdescription.data,
                                  Acomplete='0', Astart='0')
        db.session.add(appointment)
        db.session.commit()
        return redirect(url_for('loggedin_home_customer_chinese'))

    return render_template('make_appointment_customer_chinese.html', title='Make Appointment', form=form)


@app.route('/Add Pet information', methods=['GET', 'POST'])
def add_pet_information():
    form = Addpetinformation()
    if not session.get("USERNAME") is None:
        user = session.get("USERNAME")
        user_in_db = Customer.query.filter(Customer.Cname == session.get("USERNAME")).first()
        mes = 'Hello, %s ! , you can add your pet information here' % user
        if form.validate_on_submit():
            pet = Pet(Pname=form.Pname.data, Page=form.Page.data, Psex=form.Psex.data, Pspecies=form.Pspecies.data,
                      Pinfo=form.Pinfo.data, owner=user_in_db)
            db.session.add(pet)
            db.session.commit()
            flash('Save Pet Information Successfully !!!')
            return redirect(url_for('customer_my_pets'))
        return render_template('add_pet_information.html', title='Add Pet Information', warn='New pet', form=form,
                               mes=mes)
    else:
        return redirect(url_for('loginCustomer'))


@app.route('/Add Pet information_chinese', methods=['GET', 'POST'])
def add_pet_information_chinese():
    form = Addpetinformation_chinese()
    if not session.get("USERNAME") is None:
        user = session.get("USERNAME")
        user_in_db = Customer.query.filter(Customer.Cname == session.get("USERNAME")).first()
        mes = '您好, %s ! , 您能在此添加您的宠物信息' % user
        if form.validate_on_submit():
            pet = Pet(Pname=form.Pname.data, Page=form.Page.data, Psex=form.Psex.data, Pspecies=form.Pspecies.data,
                      Pinfo=form.Pinfo.data, owner=user_in_db)
            db.session.add(pet)
            db.session.commit()
            flash('保存宠物信息成功 !!!')
            return redirect(url_for('customer_my_pets'))
        return render_template('add_pet_information_chinese.html', title='Add Pet Information', warn='New pet', form=form,
                               mes=mes)
    else:
        return redirect(url_for('loginCustomer_chinese'))


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


@app.route('/My Pets_chinese', methods=['GET', 'POST'])
def customer_my_pets_chinese():
    if not session.get("USERNAME") is None:
        user_in_db = Customer.query.filter(Customer.Cname == session.get("USERNAME")).first()
        pets = user_in_db.Cpet.all()
        user = session["USERNAME"]
        mes = '你好, %s ! , 这是你的宠物信息' % user
        return render_template('customer_my_pets_chinese.html', pets=pets, mes=mes)
    else:
        return redirect(url_for('loginCustomer_chinese'))


@app.route('/My Pets/edit_pet/<id>', methods=['GET', 'POST'])
def customer_edit_pet(id):
    if not session.get("USERNAME") is None:
        if request.method == 'GET':
            user_in_db = Customer.query.filter(Customer.Cname == session.get("USERNAME")).first()
            pet = Pet.query.filter(Pet.Powner == user_in_db.id).first()
            return render_template('customer_edit_pet.html', pet=pet)
        else:
            user_in_db = Customer.query.filter(Customer.Cname == session.get("USERNAME")).first()
            pet = Pet.query.filter(Pet.Powner == user_in_db.id).first()
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
        if request.method == 'GET':
            pet = Pet.query.filter(Pet.id == id).first()
            return render_template('customer_delete_pet.html', pet=pet)
        else:
            pet = Pet.query.filter(Pet.id == id).first()
            db.session.delete(pet)
            db.session.commit()
            return redirect(url_for('customer_my_pets'))
    else:
        return redirect(url_for('loginCustomer'))


@app.route('/customer_my_appointments', methods=['GET', 'POST'])
def customer_my_appointments():
    user_in_db = Customer.query.filter(Customer.Cname == session.get("USERNAME")).first()
    pets = Pet.query.filter(Pet.Powner == user_in_db.id).all()
    if not session.get("USERNAME") is None:
        if request.method == 'GET':
            appoints = []
            for pet in pets:
                a = Appointment.query.filter(Appointment.Apet == pet.id).all()
                appoints.extend(a)
    return render_template('customer_my_appointments.html', pets=pets, appoints=appoints)


@app.route('/customer_my_appointments_chinese', methods=['GET', 'POST'])
def customer_my_appointments_chinese():
    user_in_db = Customer.query.filter(Customer.Cname == session.get("USERNAME")).first()
    pets = Pet.query.filter(Pet.Powner == user_in_db.id).all()
    if not session.get("USERNAME") is None:
        if request.method == 'GET':
            appoints = []
            for pet in pets:
                a = Appointment.query.filter(Appointment.Apet == pet.id).all()
                appoints.extend(a)
    return render_template('customer_my_appointments_chinese.html', pets=pets, appoints=appoints)


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
            appoint.Adate = datetime.now()
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
            return render_template('customer_appo_operation.html', appoint=appoint)
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
            return render_template('customer_appo_inpatient.html', title="Allows operation", appoint=appoint)
        else:
            appoint = Appointment.query.filter(Appointment.id == id).first()
            if appoint.Hstatus == '1':
                appoint.Hstatus = '2'
                appoint.HospitalizationStatus = "Ready to inpatient"
                db.session.commit()
                flash("Ready to sugery")
            else:
                flash("No surgical approval is required")
            return redirect(url_for('customer_my_appointments'))
    else:
        return redirect(url_for('loginCustomer'))


@app.route('/customer_my_appointments/release/<id>', methods=['GET', 'POST'])
def customer_appo_release(id):
    if not session.get("USERNAME") is None:
        if request.method == 'GET':
            appoint = Appointment.query.filter(Appointment.id == id).first()
            return render_template('customer_appo_release.html', title="Allows release", appoint=appoint)
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
