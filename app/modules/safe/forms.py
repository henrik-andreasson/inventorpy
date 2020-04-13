from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField
from wtforms.validators import DataRequired
from flask_babel import lazy_gettext as _l
from app.modules.safe.models import Safe
from app.models import User, Location


class SafeForm(FlaskForm):
    name = StringField(_l('Name'), validators=[DataRequired()])
    location = SelectField(_l('Location'), coerce=int)
    submit = SubmitField(_l('Submit'))
    cancel = SubmitField(_l('Cancel'))
    delete = SubmitField(_l('Delete'))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.location.choices = [(l.id, '{} / {} / {} / {}'.format(l.place, l.facillity, l.area, l.position)) for l in Location.query.order_by(Location.id).all()]


class CompartmentForm(FlaskForm):
    name = StringField(_l('Name'), validators=[DataRequired()])
    safe = SelectField(_l('Safe'), coerce=int)
    user = SelectField(_l('User'), coerce=int)
    submit = SubmitField(_l('Submit'))
    cancel = SubmitField(_l('Cancel'))
    delete = SubmitField(_l('Delete'))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.safe.choices = [(s.id, s.name) for s in Safe.query.order_by(Safe.name).all()]
        self.user.choices = [(u.id, u.username) for u in User.query.order_by(User.username).all()]
