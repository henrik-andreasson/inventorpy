from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField
from wtforms.validators import DataRequired
from flask_babel import lazy_gettext as _l


class HsmDomainForm(FlaskForm):
    name = StringField(_l('Name'), validators=[DataRequired()])
    service = SelectField(_l('Service'), validators=[DataRequired()])
    submit = SubmitField(_l('Submit'))
    cancel = SubmitField(_l('Cancel'))
    delete = SubmitField(_l('Delete'))


class HsmPedForm(FlaskForm):
    keyno = StringField(_l('Key No.'), validators=[DataRequired()])
    keysn = StringField(_l('Key S/N'), validators=[DataRequired()])
    hsmdomain = SelectField(_l('HSM Domain'), validators=[DataRequired()])
#    safe = SelectField(_l('Safe'), validators=[DataRequired()])
    user = SelectField(_l('User'))
    submit = SubmitField(_l('Submit'))
    cancel = SubmitField(_l('Cancel'))
    delete = SubmitField(_l('Delete'))


class HsmPinForm(FlaskForm):
    ped = SelectField(_l('HSM PED'), coerce=int)
    safe = StringField(_l('Safe'), validators=[DataRequired()])
    submit = SubmitField(_l('Submit'))
    cancel = SubmitField(_l('Cancel'))
    delete = SubmitField(_l('Delete'))


class HsmPciCardForm(FlaskForm):
    serial = StringField(_l('HSM PCI S/N'), validators=[DataRequired()])
    model = StringField(_l('HSM PCI FB No.'), validators=[DataRequired()])
    manufacturedate = StringField(_l('Manufacture Date'), validators=[DataRequired()])
    fbno = StringField(_l('HSM PCI FB No.'), validators=[DataRequired()])
    hsmdomain = SelectField(_l('HSM Domain'), validators=[DataRequired()])
    server = SelectField(_l('Server'), validators=[DataRequired()])
    safe = SelectField(_l('Safe'), validators=[DataRequired()])
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
