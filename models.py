class Order(db.Model):
    Oid = db.Column(db.Integer, primary_key=True)
    Obuyer = db.Column(db.Integer, db.ForeignKey('customer.Cid'))
    Ogood = db.Column(db.Integer, db.ForeignKey('good.Gid'))
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
    order = db.relationship('Order', backref='author', lazy='dynamic')

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



