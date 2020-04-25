from datetime import datetime
from hospitalapp import db



class Customer(db.Model):
    __tablename__ = 'pet_customer'
    id = db.Column(db.Integer, primary_key=True, unique=True)
    Cname = db.Column(db.String(70), index=True)
    Cpassword = db.Column(db.Integer)
    Cphone = db.Column(db.String(64))
    Cemail = db.Column(db.String(255))
    Cgender = db.Column(db.String(10), index=True)
    Corder = db.relationship('Order', backref='ocustomer', lazy='dynamic')#
    Cpet = db.relationship('Pet', backref='owner', lazy='dynamic')#
    Cpost = db.relationship('Post', backref='poster', lazy='dynamic')





class Pet(db.Model):
    __tablename__ = 'pet_pet'
    id = db.Column(db.Integer, primary_key=True)
    Pname = db.Column(db.String(70))
    Page = db.Column(db.Integer)
    Psex = db.Column(db.String(64))
    Pspecies = db.Column(db.String(64))
    Powner = db.Column(db.Integer, db.ForeignKey('pet_customer.id'))#G
    Pinfo = db.Column(db.String(1048))
    appointment = db.relationship('Appointment', backref='apppetter', lazy='dynamic')




class Prescription(db.Model):
    __tablename__ = 'pet_prescription'
    id = db.Column(db.Integer, primary_key=True)
    Pmedicine = db.Column(db.String(64), db.ForeignKey('pet_medicine.id'))#G
    Pnumber = db.Column(db.String(64))
    Pappointment = db.Column(db.String(64), db.ForeignKey('pet_appointment.id'))#G

    def __repr__(self):
        return '<Prescription {}>'.format(Prescription)


class Appointment(db.Model):
    __tablename__ = 'pet_appointment'
    id = db.Column(db.Integer, primary_key=True)
    Apet = db.Column(db.Integer, db.ForeignKey('pet_pet.id'))#
    Atype = db.Column(db.String(10), index=True)
    Alocation = db.Column(db.String(64), index=True)
    Adoc = db.Column(db.String(64), db.ForeignKey('pet_doctor.id'))#
    Ainfo = db.Column(db.String(1048))
    Adate = db.Column(db.DateTime, index=True)
    Acost = db.Column(db.String(64))
    Astart = db.Column(db.String(10), nullable=True)
    Acomplete = db.Column(db.String(10), index=True)
    Afinish = db.Column(db.String(10), nullable=True)
    Ostatus = db.Column(db.String(10), nullable=True)
    OperationStatus = db.Column(db.String(10), nullable=True)
    Hstatus = db.Column(db.String(10), nullable=True)
    HospitalizationStatus = db.Column(db.String(10), nullable=True)
    prescription = db.relationship('Prescription', backref='pappointment', lazy='dynamic')#
    Hospitalization  = db.relationship('Hospitalization', backref='happointment', lazy='dynamic')#
    Operation = db.relationship('Operation', backref='oappointment', lazy='dynamic')#
    def __repr__(self):
        return '<Appointment {}>'.format(Appointment)

class Order(db.Model):
    __tablename__ = 'pet_order'
    id = db.Column(db.Integer, primary_key=True)
    Obuyer = db.Column(db.Integer, db.ForeignKey('pet_customer.id'))
    Ogood = db.Column(db.Integer, db.ForeignKey('pet_good.id'))
    Ostate = db.Column(db.String(64), index=True)
    Oprice = db.Column(db.Integer)
    Odate = db.Column(db.DateTime, index=True)
    Onumber = db.Column(db.Integer)


class Good(db.Model):
    __tablename__ = 'pet_good'
    id = db.Column(db.Integer, primary_key=True)
    Gname = db.Column(db.String(70), index=True, unique=True)
    Ginfo = db.Column(db.String(1600), index=True, unique=True)
    Gimage = db.Column(db.String(120), index=True)
    Gprice = db.Column(db.Integer)
    Gadddate = db.Column(db.DateTime, index=True)
    Order = db.relationship('Order', backref='author', lazy='dynamic')

    def  __repr__(self):
            return '<Good is {}>'.format(self.Gname)

class Hospitalization(db.Model):
    __tablename__ = 'pet_hospitalization'
    id = db.Column(db.Integer, primary_key=True)
    Sappointment = db.Column(db.String(64), db.ForeignKey('pet_appointment.id'))
    Sdoc = db.Column(db.String(64), db.ForeignKey('pet_doctor.id'))
    Sroom = db.Column(db.String(64))
    Sstartdate = db.Column(db.DateTime, index=True)
    Senddate = db.Column(db.DateTime, index=True)
    Scost = db.Column(db.String(64))


class Operation(db.Model):
    __tablename__ = 'pet_operation'
    id = db.Column(db.Integer, primary_key=True)
    Oappiiontment = db.Column(db.Integer, db.ForeignKey('pet_appointment.id'))
    Odoc = db.Column(db.Integer, db.ForeignKey('pet_doctor.id'))
    Odate = db.Column(db.DateTime, index=True)
    Oinf = db.Column(db.String(1600))
    Ocost = db.Column(db.Integer)




class Employee(db.Model):
    __tablename__ = 'pet_employee'
    id = db.Column(db.Integer, primary_key=True, unique=True)
    Ename = db.Column(db.String(64), index=True)
    Egender = db.Column(db.String(10), index=True)
    EIDcard = db.Column(db.String(10))
    Epassword = db.Column(db.String(10))
    Ehiredate = db.Column(db.DateTime, index=True)
    Ephone = db.Column(db.String(64))
    Eemail = db.Column(db.String(120))


class Medicine(db.Model):
    __tablename__ = 'pet_medicine'
    id = db.Column(db.Integer, primary_key=True, unique=True)
    Mname = db.Column(db.String(64), index=True)
    Minf = db.Column(db.String(512))
    Mquantity = db.Column(db.Integer)
    prescription = db.relationship('Prescription', backref='medicine', lazy='dynamic')


class Hospital(db.Model):
    __tablename__ = 'pet_hospital'
    id = db.Column(db.Integer, primary_key=True)
    Hname = db.Column(db.String(64))
    Hposition = db.Column(db.String(512))
    Hinf = db.Column(db.String(512))
    doctor = db.relationship('Doctor', backref='hospital', lazy='dynamic')


class Doctor(db.Model):
    __tablename__ = 'pet_doctor'
    id = db.Column(db.Integer, primary_key=True)
    Dname = db.Column(db.String(64))
    department = db.Column(db.String(64))
    Dphone = db.Column(db.Integer)
    Dlevel = db.Column(db.Integer)
    Dinf = db.Column(db.String(512))
    Dhospital = db.Column(db.Integer, db.ForeignKey('pet_hospital.id'))
    hospitalization = db.relationship('Hospitalization', backref='sdoctor', lazy='dynamic')
    appointment = db.relationship('Appointment', backref='adoctor', lazy='dynamic')
    operation = db.relationship('Operation', backref='odoctor', lazy='dynamic')


class Post(db.Model):
    __tablename__ = 'pet_post'
    id = db.Column(db.Integer, primary_key=True)
    Ptopic = db.Column(db.String(1048), index=True)
    Pcontent = db.Column(db.String(1048), index=True)
    Pdate = db.Column(db.DateTime,index=True,default=datetime.now())
    Pcustomer = db.Column(db.Integer, db.ForeignKey('pet_customer.id'))
    Panswer = db.relationship('Answer', backref='answerer', lazy='dynamic')
    def __repr__(self):
        return '<Post:{}>'.format(self.Ptopic)

class Answer(db.Model):
    __tablename__ = 'pet_answer'
    id = db.Column(db.Integer, primary_key=True)
    Acontent = db.Column(db.String(1048), index=True)
    Adate = db.Column(db.DateTime,index=True,default=datetime.now())
    Apost = db.Column(db.Integer, db.ForeignKey('pet_post.id'))
    def __repr__(self):
        return '<Post:{}>'.format(self.Acontent)