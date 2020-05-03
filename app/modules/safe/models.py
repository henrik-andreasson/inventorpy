from app import db


class Safe(db.Model):
    __tablename__ = "safe"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(140), unique=True)
    location_id = db.Column(db.Integer, db.ForeignKey('location.id'))
    location = db.relationship('Location')
    status = db.Column(db.String(20))
    comment = db.Column(db.String(255))

    def __repr__(self):
        return '<Safe {}>'.format(self.name)

    def to_dict(self):
        data = {
            'id': self.id,
            'name': self.name,
            'location_id': self.location_id,
            'status': self.status,
            'comment': self.comment
            }
        return data

    def from_dict(self, data, new_work=False):

        for field in ['name', 'location_id', 'status', 'comment']:
            if field in data:
                if field == 'location_id':
                    setattr(self, field, int(data[field]))
                else:
                    setattr(self, field, data[field])

    def inventory_id(self):
        return '{}-{}'.format(self.__class__.__name__.lower(), self.id)


class Compartment(db.Model):
    __tablename__ = "compartment"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(140), unique=True)
    safe = db.relationship('Safe')
    safe_id = db.Column(db.Integer, db.ForeignKey('safe.id'))
    user = db.relationship('User', foreign_keys='Compartment.user_id')
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    audit_status = db.Column(db.String(20))
    audit_comment = db.Column(db.String(255))
    audit_date = db.Column(db.DateTime)
    auditor = db.relationship('User', foreign_keys='Compartment.auditor_id')
    auditor_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    comment = db.Column(db.String(255))

    def __repr__(self):
        return '<Compartment {}>'.format(self.name)

    def to_dict(self):
        data = {
            'id': self.id,
            'name': self.name,
            'user_id': self.user_id,
            'safe_id': self.safe_id,
            'audit_status': self.audit_status,
            'audit_comment': self.audit_comment,
            'comment': self.comment,
            'audit_date': self.audit_date
            }
        return data

    def from_dict(self, data):
        for field in ['name', 'user_id', 'safe_id', 'audit_status', 'auditor_id', 'audit_date', 'comment']:
            if field in data:
                setattr(self, field, data[field])

    def inventory_id(self):
        return '{}-{}'.format(self.__class__.__name__.lower(), self.id)
