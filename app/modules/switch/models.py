from app import db
from datetime import datetime
# from SQLAlchemy import Table, Base, Column, Integer, ForeignKey
#
# server_to_switch = Table('association', Base.metadata,
#                          Column('server_id', Integer, ForeignKey('server.id')),
#                          Column('switch_id', Integer, ForeignKey('switch.id'))
#                          )


class Switch(db.Model):
    __tablename__ = "switch"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(140), unique=True)
    ipaddress = db.Column(db.String(140))
    serial = db.Column(db.String(140))
    manufacturer = db.Column(db.String(140))
    model = db.Column(db.String(140))
    rack_id = db.Column(db.Integer, db.ForeignKey('rack.id'))
    rack = db.relationship('Rack')
    rack_position = db.Column(db.String(10))
    location_id = db.Column(db.Integer, db.ForeignKey('location.id'))
    location = db.relationship('Location')
    service_id = db.Column(db.Integer, db.ForeignKey('service.id'))
    service = db.relationship('Service')
    status = db.Column(db.String(140))
    support_start = db.Column(db.DateTime)
    support_end = db.Column(db.DateTime)
    comment = db.Column(db.String(2000))

    def __repr__(self):
        return '<Switch {}>'.format(self.name)

    def inventory_id(self):
        return '{}-{}'.format(self.__class__.__name__.lower(), self.id)

    def to_dict(self):
        data = {
            'id': self.id,
            'name': self.name,
            'ipaddress': self.ipaddress,
            'serial': self.serial,
            'manufacturer': self.manufacturer,
            'model': self.model,
            'rack_id': self.rack_id,
            'rack_position': self.rack_position,
            'location_id': self.location_id,
            'service_id': self.service_id,
            'status': self.status,
            'support_start': self.support_start,
            'support_end': self.support_end,
            'comment': self.comment,
            }
        return data

    def from_dict(self, data, new_work=False):
        for field in ['name', 'ipaddress', 'serial',
                      'model', 'manufacturer', 'status', 'comment',
                      'support_start', 'support_end']:
            if field == "support_start" or field == "support_end":
                date = datetime.strptime(data[field], "%Y-%m-%d")
                setattr(self, field, date)
            else:
                setattr(self, field, data[field])
