from hospitalapp import db


class Customer(db.Model):
    Cid = db.Column(db.Integer, primary_key=True)
    Cname = db.Column(db.String(70), index=True, unique=True)
    Cpassword = db.Column(db.Integer, unique=True)
    Cphone = db.Column(db.String(64, index = True))
    Cemail = db.Column(db.String(255))
    Order = db.relationship('Order', backref='author', lazy='dynamic')#
    Pet = db.relationship('Pet', backref='owner', lazy='dynamic')#

    def __repr__(self):
        return '<Customer {}>'.format(Customer)


class Pet(db.Model):
    Pid = db.Column(db.Integer, primary_key=True)
    Pname = db.Column(db.String(70), index=True, unique=True)
    Page = db.Column(db.Integer)
    Psex = db.Column(db.Integer)
    Pspecies = db.Column(db.String(64), index=True, unique=True)
    Powner = db.Column(db.Integer, db.ForeignKey('Customer.Cid'))#G
    Pinfo = db.Column(db.String(1048))

    def __repr__(self):
        return '<Pet {}>'.format(Pet)


class Prescription(db.Model):
    Pid = db.Column(db.Integer, primary_key=True)
    Pmedicine = db.Column(db.Integer, db.ForeignKey('Medicine.Mid'))#G
    Pnumber = db.Column(db.Integer, unique=True)
    Pappointment = db.Column(db.Integer, db.ForeignKey('Appointment.Aid'))#G

    def __repr__(self):
        return '<Prescription {}>'.format(Prescription)


class Appointment(db.Model):
    Aid = db.Column(db.Integer, primary_key=True)
    Apet = db.Column(db.Integer, db.ForeignKey('Pet.Pid'))#
    Atype = db.Column(db.String(64))
    Adoc = db.Column(db.Integer, db.ForeignKey('Doctor.Did'))#
    Acomplete = db.Column(db.Boolean)
    Ainfo = db.Column(db.String(1048))
    Adate = db.Column(db.Date)
    Acost = db.Column(db.Integer)
    prescription = db.relationship('Prescription', backref='Pappointment', lazy='dynamic')#
    Hospitalization  = db.relationship('Hospitalization', backref='Happointment', lazy='dynamic')#
    Operation = db.relationship('Operation', backref='Oappointment', lazy='dynamic')#
    def __repr__(self):
        return '<Appointment {}>'.format(Appointment)

class Order(db.Model):
    Oid = db.Column(db.Integer, primary_key=True)
    Obuyer = db.Column(db.Integer, db.ForeignKey('Customer.Cid'))
    Ogood = db.Column(db.Integer, db.ForeignKey('Good.Gid'))
    Ostate = db.Column(db.String(64), index=True)
    Oprice = db.Column(db.Integer)
    Odate = db.Column(db.DateTime, index=True)
    Onumber = db.Column(db.Integer)

    def __repr__(self):
            return '<Ordered by {}>'.format(self.Oid)

class Good(db.Model):
    Gid = db.Column(db.Integer, primary_key=True)
    Gname = db.Column(db.String(70), index=True, unique=True)
    Ginfo = db.Column(db.String(1600), index=True, unique=True)
    Gimage = db.Column(db.Integer)
    Gprice = db.Column(db.Integer)
    Gadddate = db.Column(db.DateTime, index=True)
    Order = db.relationship('Order', backref='author', lazy='dynamic')

    def  __repr__(self):
            return '<Good is {}>'.format(self.Gname)

class Hospitalization(db.Model):
    Sid = db.Column(db.Integer, primary_key=True)
    Sappointment = db.Column(db.Integer, db.ForeignKey('appointment.Aid'))
    Sdoc = db.Column(db.Integer, db.ForeignKey('doctor.Did'))
    Sroom = db.Column(db.Integer)
    Sstartdate = db.Column(db.DateTime, index=True)
    Senddate = db.Column(db.DateTime, index=True)
    Scost = db.Column(db.Integer)

    def __repr__(self):
            return 'Hospitalization {} is run by doctor {}'.format(self.Sid, self.Sdoc)

class Operation(db.Model):
    OPid = db.Column(db.Integer, primary_key=True)
    OPappiiontment = db.Column(db.Integer, db.ForeignKey('appointment.Aid'))
    OPdoc = db.Column(db.Integer, db.ForeignKey('doctor.Did'))
    OPdate = db.Column(db.DateTime, index=True)
    OPinf = db.Column(db.String(1600))
    OPcost = db.Column(db.Integer)

    def __repr__(self):
            return 'Operated by doc {}'.format(self.OPdoc)


class Employee(db.Model):
    Eid = db.Column(db.Integer, primary_key=True)
    Ename = db.Column(db.String(64), index=True, unique=True)
    Egender = db.Column(db.Integer)
    EIDcard = db.Column(db.String(10), index=True)
    Epassword = db.Column(db.String(10), index=True)
    Ehiredate = db.Column(db.DateTime)
    Ephone = db.Column(db.String(64, index = True))
    Eemail = db.Column(db.Strin(120))


class Medicine(db.Model):
    Mid = db.Column(db.Integer, primary_key=True)
    Mname = db.Column(db.String(64), index=True, unique=True)
    Minf = db.Column(db.String(512))
    Mquantity = db.Column(db.Integer)
    prescription = db.relationship('Prescription', backref='medicine', lazy='dynamic')


class hospital(db.Model):
    Hid = db.Column(db.Integer, primary_key=True)
    Hname = db.Column(db.String(64), index=True, unique=True)
    Hposition = db.Column(db.String(512), index=True, unique=True)
    Hinf = db.Column(db.String(512), index=True, unique=True)
    doctor = db.relationship('Doctor', backref='hospital', lazy='dynamic')


class doctor(db.Model):
    Did = db.Column(db.Integer, primary_key=True)
    Dname = db.Column(db.String(64), index=True, unique=True)
    department = db.Column(db.String(64), index=True, unique=True)
    Dphone = db.Column(db.Integer)
    Dlevel = db.Column(db.Integer)
    Dinf = db.Column(db.String(512), index=True, unique=True)
    Dhospital = db.Column(db.Integer, db.ForeignKey('hospital.Hid'))
    hospitalization = db.relationship('Hospitalization', backref='Sdoctor', lazy='dynamic')
    appointment = db.relationship('Appointment', backref='Adoctor', lazy='dynamic')
    operation = db.relationship('Operation', backref='Odoctor', lazy='dynamic')
