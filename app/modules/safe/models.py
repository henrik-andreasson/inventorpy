from app import db


class Safe(db.Model):
    __tablename__ = "safe"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(140), unique=True)
    location_id = db.Column(db.Integer, db.ForeignKey('location.id'))
    location = db.relationship('Location')

    def __repr__(self):
        return '<Safe {}>'.format(self.name)

    def to_dict(self):
        data = {
            'id': self.id,
            'name': self.name,
            'location_id': self.location_id,
            }
        return data

    def from_dict(self, data, new_work=False):

        for field in ['name', 'location_id']:
            if field == 'location_id':
                setattr(self, field, int(data[field]))
            else:
                setattr(self, field, data[field])


class Compartment(db.Model):
    __tablename__ = "compartment"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(140), unique=True)
    safe = db.relationship('Safe')
    safe_id = db.Column(db.Integer, db.ForeignKey('safe.id'))
    user = db.relationship('User')
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return '<Compartment {}>'.format(self.name)

    def to_dict(self):
        data = {
            'id': self.id,
            'name': self.name,
            'user_id': self.user_id,
            'safe_id': self.safe_id
            }
        return data

    def from_dict(self, data, new_work=False):
        for field in ['name', 'user_id', 'safe_id']:
            setattr(self, field, data[field])
