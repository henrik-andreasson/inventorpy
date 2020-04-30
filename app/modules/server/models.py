from app import db
from datetime import datetime


class Server(db.Model):
    __tablename__ = "server"
    id = db.Column(db.Integer, primary_key=True)
    hostname = db.Column(db.String(140), unique=True)
    status = db.Column(db.String(140))
    ipaddress = db.Column(db.String(140))
    netmask = db.Column(db.String(140))
    gateway = db.Column(db.String(140))
    memory = db.Column(db.String(140))
    cpu = db.Column(db.String(140))
    psu = db.Column(db.String(140))
    hd = db.Column(db.String(140))
    serial = db.Column(db.String(140))
    model = db.Column(db.String(140))
    os_name = db.Column(db.String(140))
    os_version = db.Column(db.String(140))
    manufacturer = db.Column(db.String(140))
    rack_id = db.Column(db.Integer, db.ForeignKey('rack.id'))
    rack = db.relationship('Rack')
    location_id = db.Column(db.Integer, db.ForeignKey('location.id'))
    location = db.relationship('Location')
    service_id = db.Column(db.Integer, db.ForeignKey('service.id'))
    service = db.relationship('Service')
    comment = db.Column(db.String(2000))
    support_start = db.Column(db.DateTime)
    support_end = db.Column(db.DateTime)
    rack_position = db.Column(db.String(10))

    def __repr__(self):
        return '<Server {}>'.format(self.hostname)

    def inventory_id(self):
        return '{}-{}'.format(self.__class__.__name__.lower(), self.id)

    def to_dict(self):
        data = {
            'id': self.id,
            'hostname': self.hostname,
            'ipaddress': self.ipaddress,
            'netmask': self.netmask,
            'gateway': self.gateway,
            'memory': self.memory,
            'cpu': self.cpu,
            'psu': self.psu,
            'hd': self.hd,
            'os_name': self.os_name,
            'os_version': self.os_version,
            'serial': self.serial,
            'model': self.model,
            'manufacturer': self.manufacturer,
            'rack_id': self.rack_id,
            'rack_position': self.rack_position,
            'location_id': self.location_id,
            'service_id': self.service_id,
            'status': self.status,
            'comment': self.comment,
            'support_start': self.support_start,
            'support_end': self.support_end,
            }
        return data

    def from_dict(self, data, new_work=False):
        for field in ['hostname', 'ipaddress', 'netmask', 'gateway', 'memory',
                      'cpu', 'psu', 'hd', 'os_name', 'os_version', 'serial',
                      'model', 'manufacturer', 'status', 'comment',
                      'support_start', 'support_end']:
            if field == "support_start" or field == "support_end":
                date = datetime.strptime(data[field], "%Y-%m-%d")
                setattr(self, field, date)
            else:
                setattr(self, field, data[field])
