from app import db
from datetime import datetime


class Switch(db.Model):
    __tablename__ = "switch"
    __searchable__ = ['name', 'comment', 'status', 'model', 'manufacturer', 'ipaddress', 'alias', 'serial']
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(140), unique=True)
    alias = db.Column(db.String(140), unique=True)
    ipaddress = db.Column(db.String(140))
    serial = db.Column(db.String(140))
    manufacturer = db.Column(db.String(140))
    model = db.Column(db.String(140))
    rack_id = db.Column(db.Integer, db.ForeignKey('rack.id'))
    rack = db.relationship('Rack')
    rack_position = db.Column(db.String(10))
    service_id = db.Column(db.Integer, db.ForeignKey('service.id'))
    service = db.relationship('Service')
    status = db.Column(db.String(140))
    support_start = db.Column(db.DateTime)
    support_end = db.Column(db.DateTime)
    comment = db.Column(db.String(2000))

    def __repr__(self):
        return '<Switch {} ({})>'.format(self.name, self.alias)

    def inventory_id(self):
        return '{}-{}'.format(self.__class__.__name__.lower(), self.id)

    def to_dict(self):
        data = {
            'id': self.id,
            'name': self.name,
            'alias': self.alias,
            'ipaddress': self.ipaddress,
            'serial': self.serial,
            'manufacturer': self.manufacturer,
            'model': self.model,
            'rack_id': self.rack_id,
            'rack_position': self.rack_position,
            'service_id': self.service_id,
            'status': self.status,
            'support_start': self.support_start,
            'support_end': self.support_end,
            'comment': self.comment,
            }
        return data

    def from_dict(self, data, new_work=False):
        for field in ['name', 'alias', 'ipaddress', 'serial',
                      'model', 'manufacturer', 'status', 'comment',
                      'support_start', 'support_end']:
            if field == "support_start" or field == "support_end":
                date = datetime.strptime(data[field], "%Y-%m-%d")
                setattr(self, field, date)
            else:
                setattr(self, field, data[field])


class SwitchPort(db.Model):
    __tablename__ = "switch_port"
    __searchable__ = ['name', 'server.hostname', 'switch.name', 'network.name']
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(140))
    switch = db.relationship('Switch')
    switch_id = db.Column(db.Integer, db.ForeignKey('switch.id'))
    server = db.relationship('Server', back_populates="switch_ports")
    server_id = db.Column(db.Integer, db.ForeignKey('server.id'))
    server_if = db.Column(db.String(140))
    network = db.relationship('Network', back_populates="switch_ports")
    network_id = db.Column(db.Integer, db.ForeignKey('network.id'))
    comment = db.Column(db.String(255))

    def __repr__(self):
        return '<SwitchPort {} -> {}>'.format(self.name, self.server.hostname)

    def to_dict(self):
        data = {
            'id': self.id,
            'name': self.name,
            'switch_id': self.switch_id,
            'server_id': self.server_id,
            'server_if': self.server_if,
            'network_id': self.network_id,
            'comment': self.comment,
            }
        return data

    def from_dict(self, data):
        for field in ['name', 'switch_id', 'server_id', 'server_if', 'network_id', 'comment']:
            if field in data:
                setattr(self, field, data[field])

    def inventory_id(self):
        return '{}-{}'.format(self.__class__.__name__.lower(), self.id)
