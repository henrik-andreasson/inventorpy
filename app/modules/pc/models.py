from app import db
from datetime import datetime
from app.modules.rack.models import Rack
from app.models import Service
from app.modules.network.models import Network


class Pc(db.Model):
    __tablename__ = "pc"
    __searchable__ = ['status', 'serial', 'memory',
                      'cpu', 'model', 'os_name', 'manufacturer', 'comment',
                      'environment']
    id = db.Column(db.Integer, primary_key=True)
    status = db.Column(db.String(140))
    network_id = db.Column(db.Integer, db.ForeignKey('network.id'))
    network = db.relationship('Network')
    memory = db.Column(db.String(140))
    cpu = db.Column(db.String(140))
    hd = db.Column(db.String(140))
    serial = db.Column(db.String(140))
    model = db.Column(db.String(140))
    os_name = db.Column(db.String(140))
    os_version = db.Column(db.String(140))
    manufacturer = db.Column(db.String(140))
    service_id = db.Column(db.Integer, db.ForeignKey('service.id'))
    service = db.relationship('Service')
    comment = db.Column(db.String(2000))
    support_start = db.Column(db.DateTime)
    support_end = db.Column(db.DateTime)
    environment = db.Column(db.String(140))
#    switch_port_id = db.Column(db.Integer, db.ForeignKey('switch_port.id'))

    def __repr__(self):
        return '<Pc {}>'.format(self.id)

    def inventory_id(self):
        return '{}-{}'.format(self.__class__.__name__.lower(), self.id)

    def to_dict(self):
        data = {
            'id': self.id,
            'status': self.status,
            'network_id': self.network_id,
            'memory': self.memory,
            'cpu': self.cpu,
            'hd': self.hd,
            'serial': self.serial,
            'model': self.model,
            'os_name': self.os_name,
            'os_version': self.os_version,
            'manufacturer': self.manufacturer,
            'service_id': self.service_id,
            'comment': self.comment,
            'support_start': self.support_start,
            'support_end': self.support_end,
            'environment': self.environment,
            }
        return data

    def from_dict(self, data):

        for field in ['memory', 'cpu', 'hd', 'os_name', 'os_version', 'serial',
                      'model', 'manufacturer', 'status', 'comment', 'environment']:
            if field not in data:
                return {'msg': "must include field: %s" % field, 'success': False}
            else:
                setattr(self, field, data[field])

        for field in ['support_start', 'support_end']:
            date = datetime.strptime(data[field], "%Y-%m-%d")
            setattr(self, field, date)

        if 'service_id' in data:
            service = Service.query.get(data['service_id'])
        elif 'service_name' in data:
            service = Service.query.filter_by(
                name=data['service_name']).first()

        if service is None:
            return {'msg': "no service found via service_name nor id", 'success': False}
        else:
            setattr(self, 'service_id', service.id)

        if 'network_id' in data:
            network = Network.query.get(data['network_id'])
        elif 'network_name' in data:
            network = Network.query.filter_by(
                name=data['network_name']).first()
            if network is None:
                return {'msg': "no network found via network_name nor id", 'success': False}
        else:
            setattr(self, 'network_id', network.id)

        return {'msg': "object loaded ok", 'success': True}
