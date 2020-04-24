from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, TextAreaField
from wtforms.fields.html5 import DateTimeField
from wtforms.validators import DataRequired
from flask_babel import lazy_gettext as _l
from datetime import datetime
from app.models import Service, User
from app.modules.safe.models import Safe, Compartment
from app.modules.hsm.models import HsmDomain, HsmPed
from app.modules.server.models import Server
from flask_login import current_user


class HsmDomainForm(FlaskForm):
    name = StringField(_l('Name'), validators=[DataRequired()])
    service = SelectField(_l('Service'), validators=[DataRequired()], coerce=int)
    submit = SubmitField(_l('Submit'))
    cancel = SubmitField(_l('Cancel'))
    delete = SubmitField(_l('Delete'))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.service.choices = [(s.id, s.name) for s in Service.query.order_by(Service.name).all()]


class HsmPedForm(FlaskForm):
    keyno = StringField(_l('Key No.'), validators=[DataRequired()])
    keysn = StringField(_l('Key S/N'), validators=[DataRequired()])
    hsmdomain = SelectField(_l('HSM Domain'), coerce=int)
    compartment = SelectField(_l('Compartment'), coerce=int)
    user = SelectField(_l('User'), coerce=int)
    submit = SubmitField(_l('Submit'))
    cancel = SubmitField(_l('Cancel'))
    delete = SubmitField(_l('Delete'))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.compartment.choices = [(c.id, '{} ({})'.format(c.name, c.user.username)) for c in Compartment.query.all()]
        self.hsmdomain.choices = [(h.id, h.name) for h in HsmDomain.query.all()]
        self.user.choices = [(u.id, u.username) for u in User.query.all()]


class HsmPedUpdateForm(FlaskForm):
    keyno = StringField(_l('Key No.'),  render_kw={'readonly': True})
    keysn = StringField(_l('Key S/N'),  render_kw={'readonly': True})
    hsmdomain = SelectField(_l('HSM Domain'), coerce=int,  render_kw={'readonly': True})
    compartment = SelectField(_l('Compartment'), coerce=int,  render_kw={'readonly': True})
    user = SelectField(_l('User'), coerce=int,  render_kw={'readonly': True})
    requested_by = SelectField(_l('Requested by'),  render_kw={'readonly': True})
    approve = SubmitField(_l('Approve'))
    deny = SubmitField(_l('Deny'))
    postpone = SubmitField(_l('Postpone'))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.compartment.choices = [(c.id, '{} ({})'.format(c.name, c.user.username)) for c in Compartment.query.all()]
        self.hsmdomain.choices = [(h.id, h.name) for h in HsmDomain.query.all()]
        self.user.choices = [(u.id, u.username) for u in User.query.all()]
        self.requested_by.choices = [(current_user.username, current_user.username)]


class HsmPinForm(FlaskForm):
    ped = SelectField(_l('HSM PED'), coerce=int)
    compartment = SelectField(_l('Compartment'), coerce=int)
    submit = SubmitField(_l('Submit'))
    cancel = SubmitField(_l('Cancel'))
    delete = SubmitField(_l('Delete'))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.compartment.choices = [(c.id, c.name) for c in Compartment.query.order_by(Compartment.id).all()]
        self.ped.choices = [(p.id, '{} - {} - {}'.format(p.keyno, p.keysn, p.user.username)) for p in HsmPed.query.all()]


class HsmPciCardForm(FlaskForm):
    serial = StringField(_l('HSM PCI S/N'), validators=[DataRequired()])
    fbno = StringField(_l('HSM PCI FB No.'), validators=[DataRequired()],
                       default="FBxxxxxx")
    manufacturedate = DateTimeField(_l('Manufacture Date'), validators=[DataRequired()],
                                    format='%Y-%m-%d', default=datetime.now())
    model = SelectField(_l('HSM Model'), choices=[('luna6', 'Luna 6'),
                                                  ('luna7', 'Luna 7')])
    hsmdomain = SelectField(_l('HSM Domain'), coerce=int)
    server = SelectField(_l('Server'), coerce=int)
    compartment = SelectField(_l('Compartment'), coerce=int)
    submit = SubmitField(_l('Submit'))
    cancel = SubmitField(_l('Cancel'))
    delete = SubmitField(_l('Delete'))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.compartment.choices = [(c.id, c.name) for c in Compartment.query.order_by(Compartment.id).all()]
        self.hsmdomain.choices = [(h.id, h.name) for h in HsmDomain.query.all()]
        self.server.choices = [(s.id, s.hostname) for s in Server.query.all()]
        self.server.choices.insert(0, (0, 'None'))
        self.compartment.choices.insert(0, (0, 'None'))


class HsmBackupUnitForm(FlaskForm):
    name = StringField(_l('Name'), validators=[DataRequired()])
    serial = StringField(_l('Serial No.'), validators=[DataRequired()])
    model = StringField(_l('Model'), validators=[DataRequired()])
    manufacturedate = StringField(_l('Manufacture Date'), validators=[DataRequired()])
    fbno = StringField(_l('FB No.'), validators=[DataRequired()])
    hsmdomain = SelectField(_l('HSM Domain'), validators=[DataRequired()], coerce=int)
    safe = SelectField(_l('Safe'), validators=[DataRequired()], coerce=int)
    comment = TextAreaField(_l('Comment'))
    submit = SubmitField(_l('Submit'))
    cancel = SubmitField(_l('Cancel'))
    delete = SubmitField(_l('Delete'))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.safe.choices = [(s.id, s.name) for s in Safe.query.order_by(Safe.name).all()]
        self.hsmdomain.choices = [(h.id, h.name) for h in HsmDomain.query.order_by(HsmDomain.name).all()]
