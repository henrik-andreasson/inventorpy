from app import db


class Network(db.Model):
    __tablename__ = "network"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(140), unique=True)
    network = db.Column(db.String(140))
    netmask = db.Column(db.String(140))
    gateway = db.Column(db.String(140))
    location_id = db.Column(db.Integer, db.ForeignKey('location.id'))
    location = db.relationship('Location')
    service_id = db.Column(db.Integer, db.ForeignKey('service.id'))
    service = db.relationship('Service')

    def __repr__(self):
        return '<Network {}>'.format(self.name)

    def to_dict(self):
        data = {
            'id': self.id,
            'name': self.name,
            'network': self.network,
            'netmask': self.netmask,
            'gateway': self.gateway,
            'location_id': self.location_id,
            'service_id': self.service_id,
            }
        return data

    def from_dict(self, data):
        for field in ['name', 'network', 'netmask', 'gateway', 'location_id', 'service_id']:
            setattr(self, field, data[field])
