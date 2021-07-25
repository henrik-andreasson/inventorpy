from app import db
from datetime import datetime
from app.modules.rack.models import Rack
from app.models import Service
from app.modules.network.models import Network


class Server(db.Model):
    __tablename__ = "server"
    __searchable__ = ['hostname', 'role', 'status', 'ipaddress', 'serial', 'memory',
                      'cpu', 'psu', 'model', 'os_name', 'manufacturer', 'comment',
                      'environment']
    id = db.Column(db.Integer, primary_key=True)
    hostname = db.Column(db.String(140), unique=True)
    role = db.Column(db.String(140))
    status = db.Column(db.String(140))
    ipaddress = db.Column(db.String(140))
    network_id = db.Column(db.Integer, db.ForeignKey('network.id'))
    network = db.relationship('Network')
    memory = db.Column(db.String(140))
    cpu = db.Column(db.String(140))
    psu = db.Column(db.String(140))
    hd = db.Column(db.String(140))
    serial = db.Column(db.String(140))
    model = db.Column(db.String(140))
    os_name = db.Column(db.String(140))
    os_version = db.Column(db.String(140))
    manufacturer = db.Column(db.String(140))
    rack = db.relationship('Rack')
    rack_id = db.Column(db.Integer, db.ForeignKey('rack.id'))
    rack_position = db.Column(db.String(10))
    service_id = db.Column(db.Integer, db.ForeignKey('service.id'))
    service = db.relationship('Service')
    comment = db.Column(db.String(2000))
    support_start = db.Column(db.DateTime)
    support_end = db.Column(db.DateTime)
    environment = db.Column(db.String(140))
    switch_ports = db.relationship("SwitchPort", back_populates="server")
    virtual_guests = db.relationship("VirtualServer", back_populates="hosting_server")
    virtual_host = db.Column(db.String(10))

    def __repr__(self):
        return '<Server {}>'.format(self.hostname)

    def inventory_id(self):
        return '{}-{}'.format(self.__class__.__name__.lower(), self.id)

    def to_dict(self):
        data = {
            'id': self.id,
            'hostname': self.hostname,
            'role': self.role,
            'status': self.status,
            'ipaddress': self.ipaddress,
            'network_id': self.network_id,
            'memory': self.memory,
            'cpu': self.cpu,
            'psu': self.psu,
            'hd': self.hd,
            'serial': self.serial,
            'model': self.model,
            'os_name': self.os_name,
            'os_version': self.os_version,
            'manufacturer': self.manufacturer,
            'rack_id': self.rack_id,
            'rack_position': self.rack_position,
            'service_id': self.service_id,
            'comment': self.comment,
            'support_start': self.support_start,
            'support_end': self.support_end,
            'environment': self.environment,
            'virtual_host': self.virtual_host
            }
        return data

    def from_dict(self, data):

        for field in ['hostname', 'ipaddress',  'memory', 'cpu', 'psu', 'hd', 'os_name', 'os_version', 'serial',
                      'model', 'manufacturer', 'status', 'comment', 'role', 'environment', 'virtual_host']:
            if field not in data:
                return {'msg': "must include field: %s" % field, 'success': False}
            else:
                setattr(self, field, data[field])

        for field in ['support_start', 'support_end']:
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

        if 'network_id' in data:
            network = Network.query.get(data['network_id'])
        elif 'network_name' in data:
            network = Network.query.filter_by(name=data['network_name']).first()
            if network is None:
                return {'msg': "no network found via network_name nor id", 'success': False}
        else:
            setattr(self, 'network_id', network.id)

        return {'msg': "object loaded ok", 'success': True}


class VirtualServer(db.Model):
    __tablename__ = "virtual_server"
    __searchable__ = ['hostname', 'role', 'status', 'ipaddress', 'memory',
                      'cpu', 'psu', 'os_name', 'os_version',
                      'comment', 'environment']
    id = db.Column(db.Integer, primary_key=True)
    hostname = db.Column(db.String(140), unique=True)
    role = db.Column(db.String(140))
    status = db.Column(db.String(140))
    ipaddress = db.Column(db.String(140))
    network_id = db.Column(db.Integer, db.ForeignKey('network.id'))
    network = db.relationship('Network')
    memory = db.Column(db.String(140))
    cpu = db.Column(db.String(140))
    psu = db.Column(db.String(140))
    hd = db.Column(db.String(140))
    os_name = db.Column(db.String(140))
    os_version = db.Column(db.String(140))
    service_id = db.Column(db.Integer, db.ForeignKey('service.id'))
    service = db.relationship('Service')
    comment = db.Column(db.String(2000))
    environment = db.Column(db.String(140))
    hosting_server = db.relationship("Server", back_populates="virtual_guests")
    hosting_server_id = db.Column(db.Integer, db.ForeignKey('server.id'))

    def __repr__(self):
        return '<VirtualServer {}>'.format(self.hostname)

    def inventory_id(self):
        return '{}-{}'.format(self.__class__.__name__.lower(), self.id)

    def to_dict(self):
        data = {
            'id': self.id,
            'hostname': self.hostname,
            'role': self.role,
            'status': self.status,
            'ipaddress': self.ipaddress,
            'network_id': self.network_id,
            'memory': self.memory,
            'cpu': self.cpu,
            'hd': self.hd,
            'os_name': self.os_name,
            'os_version': self.os_version,
            'service_id': self.service_id,
            'comment': self.comment,
            'environment': self.environment,
            'hsoting_server_id': self.hosting_server_id
            }
        return data

    def from_dict(self, data):

        for field in ['hostname', 'ipaddress',  'memory', 'cpu', 'psu', 'hd',
                      'os_name', 'os_version', 'status', 'comment', 'role', 'environment']:
            if field not in data:
                return {'msg': "must include field: %s" % field, 'success': False}
            else:
                setattr(self, field, data[field])

        service = None
        if 'service_id' in data:
            service = Service.query.get(data['service_id'])
        elif 'service_name' in data:
            service = Service.query.filter_by(name=data['service_name']).first()

        if service is None:
            return {'msg': "no service found via service_name nor id", 'success': False}
        else:
            setattr(self, 'service_id', service.id)

        network = None
        if 'network_id' in data:
            network = Network.query.get(data['network_id'])
        elif 'network_name' in data:
            network = Network.query.filter_by(name=data['network_name']).first()
        if network is None:
            return {'msg': "no network found via network_name nor id", 'success': False}
        else:
            setattr(self, 'network_id', network.id)

        hosting_server = None
        if 'hosting_server_id' in data:
            hosting_server = Server.query.get(data['hosting_server_id'])
        elif 'hosting_server_name' in data:
            hosting_server = Server.query.filter_by(hostname=data['hosting_server_name']).first()
        if hosting_server is None:
            return {'msg': "no hosting_server found via name nor id", 'success': False}
        else:
            setattr(self, 'hosting_server_id', hosting_server.id)

        return {'msg': "object loaded ok", 'success': True}
