from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, TextAreaField
from wtforms.fields.html5 import DateTimeField
from wtforms.validators import DataRequired
from flask_babel import lazy_gettext as _l
from datetime import datetime
from app.models import Location, Service
from app.modules.rack.models import Rack
from app.modules.network.models import Network


class ServerForm(FlaskForm):
    hostname = StringField(_l('Hostname'), validators=[DataRequired()])
    role = StringField(_l('Host Role (FE1)'))
    ipaddress = StringField(_l('IP Address'), validators=[DataRequired()])
    network = SelectField(_l('Network'), coerce=int)
    memory = StringField(_l('Memory'))
    cpu = StringField(_l('CPU'))
    psu = StringField(_l('PSU'))
    hd = StringField(_l('Hard drive'))
    os_name = StringField(_l('OS Name'))
    os_version = StringField(_l('OS Version'))
    serial = StringField(_l('Serial'))
    manufacturer = StringField(_l('Manufacturer'))
    model = StringField(_l('Model'))
    rack = SelectField(_l('Rack'), coerce=int)
    rack_position = StringField(_l('Rack position'))
    location = SelectField(_l('Location'), coerce=int)
    service = SelectField(_l('Service'), coerce=int)
    environment = SelectField(_l('Environment'), choices=[('dev', 'Development'),
                                                          ('tools', 'Tools'),
                                                          ('cicd', 'CI/CD'),
                                                          ('st', 'System Testing'),
                                                          ('at', 'Acceptance Testing'),
                                                          ('prod', 'Production'),
                                                          ])

    status = SelectField(_l('Status'), choices=[('pre-op', 'Pre Operation'),
                                                ('operation', 'Operation'),
                                                ('post-op', 'Post Operation'),
                                                ('removed', 'Removed')])
    support_start = DateTimeField(_l('Start support'), validators=[DataRequired()],
                                  format='%Y-%m-%d', default=datetime.now())
    support_end = DateTimeField(_l('End of support'),
                                validators=[DataRequired()], format='%Y-%m-%d',
                                default=datetime.now())
    comment = TextAreaField(_l('Comment'))
    submit = SubmitField(_l('Submit'))
    cancel = SubmitField(_l('Cancel'))
    delete = SubmitField(_l('Delete'))
    copy = SubmitField(_l('Copy'))
    logs = SubmitField(_l('Logs'))
    hsm = SubmitField(_l('HSMs'))
    switchport = SubmitField(_l('Switch ports'))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.location.choices = [(l.id, '{} / {} / {} / {}'.format(l.place, l.facillity, l.area, l.position)) for l in Location.query.order_by(Location.id).all()]
        self.service.choices = [(s.id, s.name) for s in Service.query.order_by(Service.name).all()]
        self.rack.choices = [(r.id, r.name_with_location()) for r in Rack.query.order_by(Rack.name).all()]
        self.network.choices = [(n.id, n.name) for n in Network.query.order_by(Network.id).all()]
        self.network.choices.insert(0, (-1, _l('None')))
