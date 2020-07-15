from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, TextAreaField
from wtforms.fields.html5 import DateTimeField
from wtforms.validators import DataRequired
from flask_babel import lazy_gettext as _l
from datetime import datetime
from app.models import Service
from app.modules.rack.models import Rack
from app.modules.network.models import Network
from app.modules.switch.models import Switch


class SwitchForm(FlaskForm):
    name = StringField(_l('Name'), validators=[DataRequired()])
    alias = StringField(_l('Alias'), validators=[DataRequired()])
    ipaddress = StringField(_l('IP Address'))
    serial = StringField(_l('Serial'))
    manufacturer = StringField(_l('Manufacturer'))
    model = StringField(_l('Model'))
    rack = SelectField(_l('Rack'), coerce=int)
    rack_position = StringField(_l('Rack position'))
    service = SelectField(_l('Service'), coerce=int)
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
    logs = SubmitField(_l('Logs'))
    ports = SubmitField(_l('SwitchPorts'))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.service.choices = [(s.id, s.name) for s in Service.query.order_by(Service.name).all()]
        self.rack.choices = [(r.id, r.name_with_location()) for r in Rack.query.order_by(Rack.name).all()]

 
class FilterSwitchListForm(FlaskForm):

    rack = SelectField(_l('Rack'), coerce=int)
    server = SelectField(_l('Server'), coerce=int)
    network = SelectField(_l('Network'), coerce=int)
    submit = SubmitField(_l('Filter List'))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        from app.modules.server.models import Server

        self.rack.choices = [(r.id, r.name_with_location()) for r in Rack.query.order_by(Rack.name).all()]
        self.rack.choices.insert(0, (-1, _l('None')))
        self.server.choices = [(s.id, '{} ({})'.format(s.hostname, s.rack.name)) for s in Server.query.order_by(Server.id).all()]
        self.server.choices.insert(0, (-1, _l('None')))
        self.network.choices = [(n.id, n.name) for n in Network.query.order_by(Network.id).all()]
        self.network.choices.insert(0, (-1, _l('None')))


class SwitchPortForm(FlaskForm):
    name = StringField(_l('Name'), validators=[DataRequired()])
    switch = SelectField(_l('Switch'), coerce=int)
    server = SelectField(_l('Server'), coerce=int)
    server_if = StringField(_l('Server Interface'))
    network = SelectField(_l('Network'), coerce=int)
    comment = TextAreaField(_l('Comment'))
    submit = SubmitField(_l('Submit'))
    cancel = SubmitField(_l('Cancel'))
    delete = SubmitField(_l('Delete'))
    logs = SubmitField(_l('Logs'))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        from app.modules.server.models import Server

        self.switch.choices = [(s.id, '{} {}'.format(s.name, s.alias)) for s in Switch.query.order_by(Switch.id).all()]
        self.server.choices = [(s.id, '{} ({})'.format(s.hostname, s.rack.name)) for s in Server.query.order_by(Server.id).all()]
        self.server.choices.insert(0, (-1, _l('Not Connected')))
        self.network.choices = [(n.id, n.name) for n in Network.query.order_by(Network.id).all()]
        self.network.choices.insert(0, (-1, _l('None')))
