from app import db
from datetime import datetime


class Firewall(db.Model):
    __tablename__ = "firewall"
    __searchable__ = ['name', 'alias', 'status', 'serial', 'manufacturer', 'model', 'status', 'comment']
# TODO: add ipaddress
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
        from app.modules.rack.models import Rack
        from app.models import Service

        for field in ['name', 'alias', 'ipaddress', 'serial',
                      'model', 'manufacturer', 'status', 'comment']:
            if field not in data:
                return {'msg': "must include field: %s" % field, 'success': False}
            else:
                setattr(self, field, data[field])

        for field in ['support_start', 'support_end']:
            if field not in data:
                return {'msg': "must include field: %s" % field, 'success': False}
            else:
                date = datetime.strptime(data[field], "%Y-%m-%d")
                setattr(self, field, date)

        if 'rack_id' in data:
            rack = Rack.query.get(data['rack_id'])
        elif 'rack_name' in data:
            rack = Rack.query.filter_by(name=data['rack_name']).first()

        if rack is None:
            return {'msg': "no rack found via rack_name nor id", 'success': False}
        else:
            setattr(self, 'rack_id', rack.id)

        if 'service_id' in data:
            service = Service.query.get(data['service_id'])
        elif 'service_name' in data:
            service = Service.query.filter_by(name=data['service_name']).first()

        if service is None:
            return {'msg': "no service found via service_name nor id", 'success': False}
        else:
            setattr(self, 'service_id', service.id)

        return {'msg': "object loaded ok", 'success': True}


class FirewallPort(db.Model):
    __tablename__ = "firewall_port"
    __searchable__ = ['name', 'firewall_id', 'switch_id', 'server_id', 'network_id', 'comment']

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(140))
    firewall = db.relationship('Firewall')
    firewall_id = db.Column(db.Integer, db.ForeignKey('firewall.id'))
    switch = db.relationship('Switch')
    switch_id = db.Column(db.Integer, db.ForeignKey('switch.id'))
    server = db.relationship('Server')
    # , back_populates="firewall_ports")
    server_id = db.Column(db.Integer, db.ForeignKey('server.id'))
    server_if = db.Column(db.String(140))
    network = db.relationship('Network')
    # , back_populates="firewall_ports")
    network_id = db.Column(db.Integer, db.ForeignKey('network.id'))
    comment = db.Column(db.String(255))

    def __repr__(self):
        return '<SwitchPort {} -> {}>'.format(self.name, self.server.hostname)

    def to_dict(self):
        data = {
            'id': self.id,
            'name': self.name,
            'firewall_id': self.wirewall_id,
            'switch_id': self.switch_id,
            'server_id': self.server_id,
            'server_if': self.server_if,
            'network_id': self.network_id,
            'comment': self.comment,
            }
        return data

    def from_dict(self, data):
        for field in ['name', 'firewall_id', 'switch_id', 'server_id', 'server_if', 'network_id', 'comment']:
            if field not in data:
                return {'msg': "must include field: %s" % field, 'success': False}
            else:
                setattr(self, field, data[field])

    def inventory_id(self):
        return '{}-{}'.format(self.__class__.__name__.lower(), self.id)
