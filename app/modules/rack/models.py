from app import db


class Rack(db.Model):
    __tablename__ = "rack"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(140), unique=True)
    location_id = db.Column(db.Integer, db.ForeignKey('location.id'))
    location = db.relationship('Location')

    def __repr__(self):
        return '<Rack {}>'.format(self.name)

    def to_dict(self):
        data = {
            'id': self.id,
            'name': self.name,
            'location_id': self.location_id,
            }
        return data

    def from_dict(self, data, new_work=False):
        for field in ['name', 'location_id']:
            setattr(self, field, data[field])

    def inventory_id(self):
        return '{}-{}'.format(self.__class__.__name__.lower(), self.id)
