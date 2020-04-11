from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, TextAreaField
from wtforms.fields.html5 import DateTimeField
from wtforms.validators import DataRequired
from flask_babel import lazy_gettext as _l
from datetime import datetime


class ServerForm(FlaskForm):
    hostname = StringField(_l('Hostname'), validators=[DataRequired()])
    ipaddress = StringField(_l('IP Address'), validators=[DataRequired()])
    netmask = StringField(_l('Netmask'), validators=[DataRequired()])
    gateway = StringField(_l('Gateway'), validators=[DataRequired()])
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
