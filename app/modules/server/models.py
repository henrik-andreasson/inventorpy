from app import db


class Server(db.Model):
    __tablename__ = "server"
    id = db.Column(db.Integer, primary_key=True)
    hostname = db.Column(db.String(140))
    status = db.Column(db.String(140))
    ipaddress = db.Column(db.String(140))
    netmask = db.Column(db.String(140))
    gateway = db.Column(db.String(140))
    memory = db.Column(db.String(140))
    cpu = db.Column(db.String(140))
    location = db.Column(db.String(140))
    service_id = db.Column(db.Integer, db.ForeignKey('service.id'))
    service = db.relationship('Service')

    def __repr__(self):
        return '<Server {}>'.format(self.hostname)

    def to_dict(self):
        data = {
            'id': self.id,
            'hostname': self.hostname,
            'ipaddress': self.ipaddress,
            'netmask': self.netmask,
            'gateway': self.gateway,
            'memory': self.memory,
            'cpu': self.cpu,
            'location': self.location,
            'service_id': self.service_id,
            'status': self.status,
            }
        return data

    def from_dict(self, data, new_work=False):
        for field in ['hostname', 'ipaddress', 'netmask', 'gateway', 'memory', 'cpu', 'location', 'service_id', 'status']:
            setattr(self, field, data[field])
