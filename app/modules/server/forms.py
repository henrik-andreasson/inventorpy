from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField
from wtforms.validators import DataRequired
from flask_babel import lazy_gettext as _l

 
class ServerForm(FlaskForm):
    hostname = StringField(_l('Hostname'), validators=[DataRequired()])
    ipaddress = StringField(_l('IP Address'), validators=[DataRequired()])
    netmask = StringField(_l('Netmask'), validators=[DataRequired()])
    gateway = StringField(_l('Gateway'), validators=[DataRequired()])
    memory = StringField(_l('Memory'), validators=[DataRequired()])
    cpu = StringField(_l('CPU'), validators=[DataRequired()])
    location = SelectField(_l('Location'), validators=[DataRequired()])
    service = SelectField(_l('Service'), validators=[DataRequired()])
    status = SelectField(_l('Status'), choices=[('pre-op', 'Pre Operation'),
                                                ('operation', 'Operation'),
                                                ('post-op', 'Post Operation'),
                                                ('removed', 'Removed')])
    submit = SubmitField(_l('Submit'))
    cancel = SubmitField(_l('Cancel'))
    delete = SubmitField(_l('Delete'))
