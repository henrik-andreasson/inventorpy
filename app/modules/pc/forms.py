from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, TextAreaField, BooleanField, DateTimeField
from wtforms.validators import DataRequired, NumberRange
from flask_babel import lazy_gettext as _l
from datetime import datetime, timedelta
from app.models import Location, Service
from app.modules.rack.models import Rack
from app.modules.network.models import Network
from app.modules.switch.models import SwitchPort
from app.modules.server.models import Server
from app.models import User


class PcForm(FlaskForm):
    user = SelectField(_l('User'))
    name = StringField(_l('Name'),default="1")
    memory = StringField(_l('Memory'),default="4GB")
    cpu = StringField(_l('CPU'),default="4 core")
    hd = StringField(_l('Hard drive'),default="SSD 100GB")
    os_name = StringField(_l('OS Name'),default="Debian")
    os_version = StringField(_l('OS Version'),default="12")
    serial = StringField(_l('Serial'), validators=[DataRequired()])
    manufacturer = StringField(_l('Manufacturer'),default="Lenovo")
    model = StringField(_l('Model'),default="Thinkstation")
    service = SelectField(_l('Service'), coerce=int)
    switchport = SelectField(_l('Switch port'), coerce=int)
    network = SelectField(_l('Network'), coerce=int, validators=[
                          NumberRange(1, None, _l('Must select a Network'))])
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
                                default=(datetime.now() + timedelta(days=365)))
    comment = TextAreaField(_l('Comment'))
    submit = SubmitField(_l('Submit'))
    cancel = SubmitField(_l('Cancel'))
    delete = SubmitField(_l('Delete'))
    copy = SubmitField(_l('Copy'))
    logs = SubmitField(_l('Logs'))
    switchport_list = SubmitField(_l('List Switch ports'))
    switchport_add = SubmitField(_l('Add Switch port'))
    qrcode = SubmitField(_l('QR Code'))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.service.choices = [(s.id, s.name)
                                for s in Service.query.order_by(Service.name).all()]
        self.user.choices = [(u.id, u.username)
                            for u in User.query.order_by(User.username).all()]
        self.network.choices = [(n.id, n.name)
                                for n in Network.query.order_by(Network.name).all()]
        self.switchport.choices = [(s.id, s.name)
                                  for s in SwitchPort.query.order_by(SwitchPort.name).all()]
        self.network.choices.insert(0, (-1, _l('None')))
        self.user.choices.insert(0, (-1, _l('None')))


class FilterPcListForm(FlaskForm):
    service = SelectField(_l('Service'), coerce=int)
    environment = SelectField(_l('Environment'))
    submit = SubmitField(_l('Filter List'))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.service.choices = [(s.id, s.name)
                                for s in Service.query.order_by(Service.name).all()]
        self.service.choices.insert(0, (-1, _l('All')))
        self.environment.choices = [('all', 'All'),
                                    ('dev', 'Development'),
                                    ('tools', 'Tools'),
                                    ('cicd', 'CI/CD'),
                                    ('st', 'System Testing'),
                                    ('at', 'Acceptance Testing'),
                                    ('prod', 'Production'),
                                    ]
