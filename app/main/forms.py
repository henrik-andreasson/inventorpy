from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, \
    SelectMultipleField, SelectField
from wtforms.validators import ValidationError, DataRequired, Length
from flask_babel import _, lazy_gettext as _l
from app.models import User


class EditProfileForm(FlaskForm):
    username = StringField(_l('Username'), validators=[DataRequired()])
    about_me = TextAreaField(_l('About me'),
                             validators=[Length(min=0, max=140)])
    submit = SubmitField(_l('Submit'))
    cancel = SubmitField(_l('Cancel'))

    def __init__(self, original_username, *args, **kwargs):
        super(EditProfileForm, self).__init__(*args, **kwargs)
        self.original_username = original_username

    def validate_username(self, username):
        if username.data != self.original_username:
            user = User.query.filter_by(username=self.username.data).first()
            if user is not None:
                raise ValidationError(_('Please use a different username.'))


class ServiceForm(FlaskForm):
    name = StringField(_l('name'), validators=[DataRequired()])
    color = StringField(_l('color'), validators=[DataRequired()])
    users = SelectMultipleField(_l('Users'), validators=[DataRequired()])
    submit = SubmitField(_l('Submit'))
    cancel = SubmitField(_l('Cancel'))
    delete = SubmitField(_l('Delete'))


class LocationForm(FlaskForm):
    place = StringField(_l('Place (City/Region)'), validators=[DataRequired()])
    facillity = StringField(_l('Facillity (House/Complex)'), validators=[DataRequired()])
    area = StringField(_l('Area (Room/Rack/Safe)'), validators=[DataRequired()])
    position = StringField(_l('Position'), validators=[DataRequired()])
    type = SelectField(_l('Type of Facillity'), choices=[('dc', 'Data Centre'),
                                                         ('office', 'Office'),
                                                         ('customer', 'Customer')])
    submit = SubmitField(_l('Submit'))
    cancel = SubmitField(_l('Cancel'))
    delete = SubmitField(_l('Delete'))
