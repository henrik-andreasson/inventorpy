from app import db
from datetime import datetime
from app.modules.server.models import Server
from app.models import Service, User
from app.modules.safe.models import Safe, Compartment
from app.models import PaginatedAPIMixin



class HsmDomain(PaginatedAPIMixin, db.Model):
    __tablename__ = "hsm_domain"
    __searchable__ = ['name']

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(140), unique=True)
    service_id = db.Column(db.Integer, db.ForeignKey('service.id'))
    service = db.relationship('Service')

    def __repr__(self):
        return '<HsmDomain {}>'.format(self.name)

    def to_dict(self):
        data = {
            'id': self.id,
            'name': self.name,
            'service_id': self.service_id,
            }
        return data

    def from_dict(self, data, new_work=False):
        if 'name' in data:
            setattr(self, 'name', data['name'])
        if 'service_name' in data:
            service = Service.query.filter_by(name=data['service_name']).first_or_404()
            setattr(self, 'service', service)
        elif 'service_id' in data:
            service = Service.query.get(data['service_id'])
            setattr(self, 'service', service)
        else:
            return {'msg': "nor service_name or service_id found a valid service", 'success': False}

        return {'msg': "object loaded ok", 'success': True}

    def inventory_id(self):
        return '{}-{}'.format(self.__class__.__name__.lower(), self.id)


class HsmPed(PaginatedAPIMixin, db.Model):
    __tablename__ = "hsm_ped"
    __searchable__ = ['type', 'keyno', 'keysn', 'hsmdomain_id', 'user_id', 'compartment_id', 'comment']
    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String(140))
    keyno = db.Column(db.String(140))
    keysn = db.Column(db.String(140))
    hsmdomain = db.relationship('HsmDomain')
    hsmdomain_id = db.Column(db.Integer, db.ForeignKey('hsm_domain.id'))
    user = db.relationship('User')
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    compartment = db.relationship('Compartment')
    compartment_id = db.Column(db.Integer, db.ForeignKey('compartment.id'))
    comment = db.Column(db.String(255))
    duplicate_of = db.Column(db.Integer, db.ForeignKey('hsm_ped.id'))

    def __repr__(self):
        return '<HsmPed {}>'.format(self.keyno)

    def to_dict(self):
        data = {
            'id': self.id,
            'type': self.type,
            'keyno': self.keyno,
            'keysn': self.keysn,
            'compartment_id': self.compartment_id,
            'user_id': self.user_id,
            'hsmdomain_id': self.hsmdomain_id
            }
        return data

    def from_dict(self, data):
        if data['type'] in ['blue', 'red', 'red2', 'orange', 'black']:
            setattr(self, 'type', data['type'])
        else:
            return {'msg': "type not of an allowed one blue, red, red2, orange or black", 'success': False}

        setattr(self, 'keyno', data['keyno'])
        setattr(self, 'keysn', data['keysn'])
        if 'hsmdomain_id' in data:
            hsmdomain = HsmDomain.query.get(data['hsmdomain_id'])
            if hsmdomain is None:
                return {'msg': "no hsmdomain found via id", 'success': False}
            setattr(self, 'hsmdomain_id', hsmdomain.id)

        elif 'hsmdomain_name' in data:
            hsmdomain = HsmDomain.query.filter_by(name=data['hsmdomain_name']).first()
            if hsmdomain is None:
                return {'msg': "no hsmdomain found via hsmdomain_name", 'success': False}
            setattr(self, 'hsmdomain_id', hsmdomain.id)

        else:
            return {'msg': "no hsmdomain found via hsmdomain_name nor id", 'success': False}

        if 'compartment_id' in data:
            compartment = Compartment.query.get(data['compartment_id'])
            if compartment is None:
                return {'msg': "no compartment found via id", 'success': False}
            setattr(self, 'compartment_id', compartment.id)

        elif 'compartment_name' in data:
            compartment = Compartment.query.filter_by(name=data['compartment_name']).first()
            if compartment is None:
                return {'msg': "no compartment found via compartment_name", 'success': False}
            setattr(self, 'compartment_id', compartment.id)

        else:
            return {'msg': "no compartment found via hsmdomain_name nor id", 'success': False}

        if 'user_id' in data:
            user = User.query.get(data['user_id'])
            if user is None:
                return {'msg': "no user found via id", 'success': False}
            setattr(self, 'user_id', user.id)

        elif 'user_name' in data:
            user = User.query.filter_by(username=data['user_name']).first()
            if user is None:
                return {'msg': "no user found via user_name", 'success': False}
            setattr(self, 'user_id', user.id)

        else:
            return {'msg': "no user found via user_name nor id", 'success': False}

        return {'msg': "Object created", 'success': True}

    def inventory_id(self):
        return '{}-{}'.format(self.__class__.__name__.lower(), self.id)


class HsmPedUpdates(PaginatedAPIMixin, db.Model):
    __tablename__ = "hsm_ped_updates"
    __searchable__ = ['type', 'keyno', 'keysn', 'hsmdomain_id', 'user_id', 'compartment_id']
    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String(140))
    keyno = db.Column(db.String(140))
    keysn = db.Column(db.String(140), unique=True)
    hsmdomain = db.relationship('HsmDomain')
    hsmdomain_id = db.Column(db.Integer, db.ForeignKey('hsm_domain.id'))
    user = db.relationship('User', foreign_keys='HsmPedUpdates.user_id')
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    requested_by = db.relationship('User', foreign_keys='HsmPedUpdates.requested_by_id')
    requested_by_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    compartment = db.relationship('Compartment')
    compartment_id = db.Column(db.Integer, db.ForeignKey('compartment.id'))

    def __repr__(self):
        return '<HsmPedUpdates {}>'.format(self.keyno)

    def to_dict(self):
        data = {
            'id': self.id,
            'type': self.type,
            'keyno': self.keyno,
            'keysn': self.keysn,
            'compartment_id': self.compartment_id,
            'user_id': self.user_id,
            'hsmdomain_id': self.hsmdomain_id
            }
        return data

    def from_dict(self, data):
        for field in ['keyno', 'keysn', 'hsmdomain_id', 'compartment_id', 'user_id', 'type']:
            setattr(self, field, data[field])


class HsmPin(PaginatedAPIMixin, db.Model):
    __tablename__ = "hsm_pin"
#    __searchable__ = ['ped_id', 'compartment_id']
    id = db.Column(db.Integer, primary_key=True)
    ped = db.relationship('HsmPed')
    ped_id = db.Column(db.Integer, db.ForeignKey('hsm_ped.id'))
    compartment = db.relationship('Compartment')
    compartment_id = db.Column(db.Integer, db.ForeignKey('compartment.id'))

    def __repr__(self):
        return '<HsmPin {}>'.format(self.id)

    def to_dict(self):
        data = {
            'id': self.id,
            'ped_id': self.ped_id,
            'compartment_id': self.compartment_id,
            }
        return data

    def from_dict(self, data):
        for field in ['ped_id', 'compartment_id']:
            setattr(self, field, data[field])

    def inventory_id(self):
        return '{}-{}'.format(self.__class__.__name__.lower(), self.id)


class HsmPciCard(PaginatedAPIMixin, db.Model):
    __tablename__ = "hsm_pci_card"
    __searchable__ = ['name', 'serial', 'fbno', 'model', 'status', 'comment']
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(140))
    serial = db.Column(db.String(140), unique=True)
    fbno = db.Column(db.String(140), unique=True)
    model = db.Column(db.String(140))
    manufacturedate = db.Column(db.DateTime)
    safe = db.relationship('Safe')
    safe_id = db.Column(db.Integer, db.ForeignKey('safe.id'))
    hsmdomain = db.relationship('HsmDomain')
    hsmdomain_id = db.Column(db.Integer, db.ForeignKey('hsm_domain.id'))
    server = db.relationship('Server')
    server_id = db.Column(db.Integer, db.ForeignKey('server.id'))
    status = db.Column(db.String(140))
    support_start = db.Column(db.DateTime)
    support_end = db.Column(db.DateTime)
    contract = db.Column(db.String(140))
    comment = db.Column(db.String(255))

    def __repr__(self):
        return '<HsmPciCard {}>'.format(self.serial)

    def to_dict(self):
        data = {
            'id': self.id,
            'name': self.name,
            'serial': self.serial,
            'fbno': self.fbno,
            'model': self.model,
            'manufacturedate': self.manufacturedate,
            'hsmdomain_id': self.hsmdomain_id,
            'server_id': self.server_id,
            'safe_id': self.safe_id,
            'status': self.status,
            'support_start': self.support_start,
            'support_end': self.support_end,
            'contract': self.contract,
            'comment': self.comment
            }
        return data

    def from_dict(self, data):
        for field in ['serial', 'model', 'fbno', 'name', 'status', 'contract', 'comment']:
            if field not in data:
                msg = 'must include field: %s' % field
                return {'msg': msg, 'success': False}
            setattr(self, field, data[field])

        for field in ['support_start', 'support_end', 'manufacturedate']:
            if field in data:
                date = datetime.strptime(data[field], "%Y-%m-%d")
                setattr(self, field, date)
            else:
                msg = f'must include field: {field}'
                return {'msg': msg, 'success': False}

        if 'server_id' in data:
            server = Server.query.get(data['server_id'])
            if server is None:
                return {'msg': "no server found via server_id", 'success': False}
            else:
                setattr(self, 'server_id', server.id)

        elif 'server_name' in data and data['server_name'] != "":
            server = Server.query.filter_by(hostname=data['server_name']).first()
            if server is None:
                return {'msg': "no server found via server_name nor id", 'success': False}
            else:
                setattr(self, 'server_id', server.id)

        elif 'safe_name' in data and data['safe_name'] != "":
            safe = Safe.query.filter_by(name=data['safe_name']).first()
            if safe is None:
                return {'msg': "no safe found via safe_name", 'success': False}
            else:
                setattr(self, 'safe_id', safe.id)

        elif 'safe_id' in data:
            safe = Safe.query.get(data['safe_id'])
            if safe is None:
                return {'msg': "no safe found via safe_id", 'success': False}
            else:
                setattr(self, 'safe_id', safe.id)
        else:
            return {'msg': "must supply valid physical location", 'success': False}

        if 'hsmdomain_id' in data:
            hsmdomain = HsmDomain.query.get(data['hsmdomain_id'])
            if hsmdomain is None:
                return {'msg': "no HSM Domain found via hsmdomain_id", 'success': False}
            else:
                setattr(self, 'hsmdomain_id', hsmdomain.id)

        elif 'hsmdomain_name' in data:
            hsmdomain = HsmDomain.query.filter_by(name=data['hsmdomain_name']).first()
            if hsmdomain is None:
                return {'msg': "no HSM Domain found via hsmdomain_id nor hsmdomain_name", 'success': False}
            else:
                setattr(self, 'hsmdomain_id', hsmdomain.id)

        return {'msg': "object loaded ok", 'success': True}

    def inventory_id(self):
        return '{}-{}'.format(self.__class__.__name__.lower(), self.id)


class HsmBackupUnit(PaginatedAPIMixin, db.Model):
    __tablename__ = "hsm_backup_unit"
    __searchable__ = ['name', 'serial', 'model', 'manufacturedate', 'fbno', 'hsmdomain_id', 'safe_id', 'comment']
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(140))
    serial = db.Column(db.String(140))
    model = db.Column(db.String(140))
    manufacturedate = db.Column(db.String(140))
    fbno = db.Column(db.String(140))
    safe = db.relationship('Safe')
    safe_id = db.Column(db.Integer, db.ForeignKey('safe.id'))
    hsmdomain = db.relationship('HsmDomain')
    hsmdomain_id = db.Column(db.Integer, db.ForeignKey('hsm_domain.id'))
    comment = db.Column(db.String(255))

    def __repr__(self):
        return '<HsmBackupUnit {}/{}>'.format(self.name, self.serial)

    def to_dict(self):
        data = {
            'id': self.id,
            'name': self.name,
            'serial': self.serial,
            'model': self.model,
            'manufacturedate': self.manufacturedate,
            'fbno': self.fbno,
            'hsmdomain_id': self.hsmdomain_id,
            'safe_id': self.safe_id
            }
        return data

    def from_dict(self, data):
        for field in ['name', 'serial', 'model', 'manufacturedate', 'fbno']:
            setattr(self, field, data[field])

        safe = None
        if 'safe_id' in data:
            safe = Safe.query.get(data['safe_id']).first()
        if 'safe_name' in data:
            safe = Safe.query.filter_by(name=data['safe_name']).first()
        else:
            return {'msg': "must supply valid safe via save_id or safe_name", 'success': False}

        if safe is None:
            return {'msg': "no safe found via safe_id/name", 'success': False}
        else:
            setattr(self, 'safe_id', safe.id)

        if 'hsmdomain_id' in data:
            hsmdomain = HsmDomain.query.get(data['hsmdomain_id'])
            if hsmdomain is None:
                return {'msg': "no HSM Domain found via hsmdomain_id", 'success': False}
            else:
                setattr(self, 'hsmdomain_id', hsmdomain.id)

        elif 'hsmdomain_name' in data:
            hsmdomain = HsmDomain.query.filter_by(name=data['hsmdomain_name']).first()
            if hsmdomain is None:
                return {'msg': "no HSM Domain found via hsmdomain_id nor hsmdomain_name", 'success': False}
            else:
                setattr(self, 'hsmdomain_id', hsmdomain.id)

        return {'msg': "object loaded ok", 'success': True}

    def inventory_id(self):
        return '{}-{}'.format(self.__class__.__name__.lower(), self.id)
