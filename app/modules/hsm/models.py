from app import db
from datetime import datetime


class HsmDomain(db.Model):
    __tablename__ = "hsm_domain"
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
        for field in ['name', 'service_id']:
            setattr(self, field, data[field])

    def inventory_id(self):
        return '{}-{}'.format(self.__class__.__name__.lower(), self.id)


class HsmPed(db.Model):
    __tablename__ = "hsm_ped"
    id = db.Column(db.Integer, primary_key=True)
    keyno = db.Column(db.String(140))
    keysn = db.Column(db.String(140), unique=True)
    hsmdomain = db.relationship('HsmDomain')
    hsmdomain_id = db.Column(db.Integer, db.ForeignKey('hsm_domain.id'))
    user = db.relationship('User')
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    compartment = db.relationship('Compartment')
    compartment_id = db.Column(db.Integer, db.ForeignKey('compartment.id'))

    def __repr__(self):
        return '<HsmPed {}>'.format(self.keyno)

    def to_dict(self):
        data = {
            'id': self.id,
            'keyno': self.keyno,
            'keysn': self.keysn,
            'compartment_id': self.compartment_id,
            'user_id': self.user_id,
            'hsmdomain_id': self.hsmdomain_id
            }
        return data

    def from_dict(self, data):
        for field in ['keyno', 'keysn', 'hsmdomain_id', 'compartment_id', 'user_id']:
            setattr(self, field, data[field])

    def inventory_id(self):
        return '{}-{}'.format(self.__class__.__name__.lower(), self.id)


class HsmPedUpdates(db.Model):
    __tablename__ = "hsm_ped_updates"
    id = db.Column(db.Integer, primary_key=True)
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
            'keyno': self.keyno,
            'keysn': self.keysn,
            'compartment_id': self.compartment_id,
            'user_id': self.user_id,
            'hsmdomain_id': self.hsmdomain_id
            }
        return data

    def from_dict(self, data):
        for field in ['keyno', 'keysn', 'hsmdomain_id', 'compartment_id', 'user_id']:
            setattr(self, field, data[field])


class HsmPin(db.Model):
    __tablename__ = "hsm_pin"
    id = db.Column(db.Integer, primary_key=True)
    ped = db.relationship('HsmPed')
    ped_id = db.Column(db.Integer, db.ForeignKey('hsm_ped.id'))
    compartment = db.relationship('Compartment')
    compartment_id = db.Column(db.Integer, db.ForeignKey('compartment.id'))

    def __repr__(self):
        return '<HsmPin {}>'.format(self.keyno)

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


class HsmPciCard(db.Model):
    __tablename__ = "hsm_pci_card"
    id = db.Column(db.Integer, primary_key=True)
    serial = db.Column(db.String(140), unique=True)
    fbno = db.Column(db.String(140), unique=True)
    model = db.Column(db.String(140))
    manufacturedate = db.Column(db.DateTime)
    compartment = db.relationship('Compartment')
    compartment_id = db.Column(db.Integer, db.ForeignKey('compartment.id'))
    hsmdomain = db.relationship('HsmDomain')
    hsmdomain_id = db.Column(db.Integer, db.ForeignKey('hsm_domain.id'))
    server = db.relationship('Server')
    server_id = db.Column(db.Integer, db.ForeignKey('server.id'))

    def __repr__(self):
        return '<HsmPciCard {}>'.format(self.serial)

    def to_dict(self):
        data = {
            'id': self.id,
            'serial': self.serial,
            'fbno': self.fbno,
            'model': self.model,
            'manufacturedate': self.manufacturedate,
            'hsmdomain_id': self.hsmdomain_id,
            'server_id': self.server_id,
            'compartment_id': self.compartment_id
            }
        return data

    def from_dict(self, data, new_work=False):
        for field in ['serial', 'model', 'manufacturedate', 'fbno', 'hsmdomain_id', 'server_id', 'compartment_id']:
            setattr(self, field, data[field])
            if field == "manufacturedate":
                date = datetime.strptime(data[field], "%Y-%m-%d")
                setattr(self, field, date)
            else:
                setattr(self, field, data[field])

    def inventory_id(self):
        return '{}-{}'.format(self.__class__.__name__.lower(), self.id)


class HsmBackupUnit(db.Model):
    __tablename__ = "hsm_backup_unit"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(140))
    serial = db.Column(db.String(140))
    model = db.Column(db.String(140))
    manufacturedate = db.Column(db.String(140))
    fbno = db.Column(db.String(140))
    hsmdomain = db.Column(db.String(140))
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
        for field in ['name', 'serial', 'model', 'manufacturedate', 'fbno', 'hsmdomain_id', 'safe_id']:
            setattr(self, field, data[field])

    def inventory_id(self):
        return '{}-{}'.format(self.__class__.__name__.lower(), self.id)
