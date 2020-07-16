from app import db


class Rack(db.Model):
    __tablename__ = "rack"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(140), unique=True)
    location_id = db.Column(db.Integer, db.ForeignKey('location.id'))
    location = db.relationship('Location')

    def __repr__(self):
        return '<Rack {}>'.format(self.name)

    def to_dict(self):
        data = {
            'id': self.id,
            'name': self.name,
            'location_id': self.location_id,
            }
        return data

    def from_dict(self, data):
        from app.models import Location
        for field in ['name']:
            if field not in data:
                return {'msg': "must include field: %s" % field, 'success': False}
            else:
                setattr(self, field, data[field])

        if 'location_id' in data:
            location = Location.query.get(data['location_id'])
            if location is not None:
                setattr(self, 'location_id', location.id)
            else:
                return {'msg': "location not found via id", 'success': False}

        elif 'location_long_name' in data:
            for loc in Location.query.order_by(Location.id):
                if data['location_long_name'] == loc.longName():
                    setattr(self, 'location_id', loc.id)
        else:
            return {'msg': "location not set", 'success': False}

        return {'msg': "object loaded ok", 'success': True}

    def inventory_id(self):
        return '{}-{}'.format(self.__class__.__name__.lower(), self.id)

    def name_with_location(self):
        return '{} ({})'.format(self.name, self.location.longName())
