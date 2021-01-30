from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, TextAreaField
from wtforms.validators import DataRequired
from flask_babel import lazy_gettext as _l
from app.models import Location


class RackForm(FlaskForm):
    name = StringField(_l('Name'), validators=[DataRequired()])
    location = SelectField(_l('Location'), coerce=int)
    submit = SubmitField(_l('Submit'))
    cancel = SubmitField(_l('Cancel'))
    delete = SubmitField(_l('Delete'))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.location.choices = [(l.id, '{} / {} / {} / {}'.format(l.place, l.facillity, l.area, l.position)) for l in Location.query.order_by(Location.id).all()]


class AuditRackForm(FlaskForm):
    name = StringField(_l('Name'), render_kw={'readonly': True})
    location = StringField(_l('Location'), render_kw={'readonly': True})
    comment = TextAreaField(_l('Audit Comment'))
    approved = SubmitField(_l('Audit Approved'))
    failed = SubmitField(_l('Audit Failed'))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
