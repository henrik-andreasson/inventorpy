from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField
from wtforms.validators import DataRequired
from flask_babel import lazy_gettext as _l
from app.models import Location, Service


class NetworkForm(FlaskForm):
    name = StringField(_l('Net name'), validators=[DataRequired()])
    network = StringField(_l('IP Network'), validators=[DataRequired()])
    netmask = StringField(_l('Netmask'), validators=[DataRequired()])
    gateway = StringField(_l('Gateway'), validators=[DataRequired()])
    location = SelectField(_l('Location'), coerce=int)
    service = SelectField(_l('Service'), coerce=int)
    vlan = StringField(_l('VLAN'))
    submit = SubmitField(_l('Submit'))
    cancel = SubmitField(_l('Cancel'))
    delete = SubmitField(_l('Delete'))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.location.choices = [(l.id, '{} / {} / {} / {}'.format(l.place, l.facillity, l.area, l.position)) for l in Location.query.order_by(Location.id).all()]
        self.service.choices = [(s.id, s.name) for s in Service.query.order_by(Service.name).all()]
