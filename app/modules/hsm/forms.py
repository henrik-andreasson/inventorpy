from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField
from wtforms.fields.html5 import DateTimeField
from wtforms.validators import DataRequired
from flask_babel import lazy_gettext as _l
from datetime import datetime


class HsmDomainForm(FlaskForm):
    name = StringField(_l('Name'), validators=[DataRequired()])
    service = SelectField(_l('Service'), validators=[DataRequired()])
    submit = SubmitField(_l('Submit'))
    cancel = SubmitField(_l('Cancel'))
    delete = SubmitField(_l('Delete'))


class HsmPedForm(FlaskForm):
    keyno = StringField(_l('Key No.'), validators=[DataRequired()])
    keysn = StringField(_l('Key S/N'), validators=[DataRequired()])
    hsmdomain = SelectField(_l('HSM Domain'), coerce=int)
    compartment = SelectField(_l('Compartment'), coerce=int)
    user = SelectField(_l('User'), coerce=int)
    submit = SubmitField(_l('Submit'))
    cancel = SubmitField(_l('Cancel'))
    delete = SubmitField(_l('Delete'))


class HsmPinForm(FlaskForm):
    ped = SelectField(_l('HSM PED'), coerce=int)
    compartment = SelectField(_l('Compartment'), coerce=int)
    submit = SubmitField(_l('Submit'))
    cancel = SubmitField(_l('Cancel'))
    delete = SubmitField(_l('Delete'))


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


class HsmBackupUnitForm(FlaskForm):
    serial = StringField(_l('Serial No.'), validators=[DataRequired()])
    model = StringField(_l('Model'), validators=[DataRequired()])
    manufacturedate = StringField(_l('Manufacture Date'), validators=[DataRequired()])
    fbno = StringField(_l('FB No.'), validators=[DataRequired()])
    hsmdomain = SelectField(_l('HSM Domain'), validators=[DataRequired()])
    server = SelectField(_l('Server'), validators=[DataRequired()])
    safe = SelectField(_l('Safe'), validators=[DataRequired()])
    submit = SubmitField(_l('Submit'))
    cancel = SubmitField(_l('Cancel'))
    delete = SubmitField(_l('Delete'))
