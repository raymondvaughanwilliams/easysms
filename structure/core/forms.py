from flask_wtf import FlaskForm
from wtforms import BooleanField, StringField, PasswordField, validators , ValidationError, HiddenField,FloatField,IntegerField,SubmitField,SelectField,SelectMultipleField,TextAreaField,FileField,Form,DateTimeField,TimeField
from wtforms.validators import DataRequired, Email, EqualTo
from wtforms import ValidationError
from flask_wtf.file import FileField,FileAllowed
from wtforms_components import TimeField
from wtforms.fields.html5 import DateField,DateTimeField
import datetime
from flask_login import current_user
from structure.models import User

class MessageForm(FlaskForm):
    message = TextAreaField('Message',validators=[DataRequired()])
    destination = TextAreaField('Destination')
    contacts = FileField('Upload Contacts', validators=[FileAllowed(['csv'])])
    date = DateField('Choose Date', [validators.DataRequired()] ,format='%Y-%m-%d',default=datetime.datetime.now)
    time  = TimeField('Time',default=datetime.datetime.now)
    phonebook = SelectField('Phonebook', choices=[])
    amount = IntegerField('Amount',validators=[DataRequired()])

    submit = SubmitField('Submit')


class ContactForm(FlaskForm):
    name = StringField('Name',validators=[DataRequired()])
    number = StringField('Number')
    phonebook = SelectField('Phonebook', choices=[])
    contacts = FileField('Upload Contacts', validators=[FileAllowed(['csv'])])


    # contacts = FileField('Upload Contacts', validators=[FileAllowed(['csv'])])

    submit = SubmitField('Submit')


class PhonebookForm(FlaskForm):
    name = StringField('Name',validators=[DataRequired()])
    number = StringField('Number')
    phonebook = SelectField('Phonebook', choices=[])

    submit = SubmitField('Submit')


class SenderIDForm(FlaskForm):
    name = StringField('Name',validators=[DataRequired()])
    description = StringField('Description',validators=[DataRequired()])
    submit = SubmitField('Submit')


class RatesForm(FlaskForm):
    code = StringField('Code',validators=[DataRequired()])
    cost = FloatField('Cost',validators=[DataRequired()])
    country = StringField('Country',validators=[DataRequired()])
    route = SelectField('Route',validators=[DataRequired()],choices=[('routems', 'Routesms'), ('Mnotify', 'Mnotify')])
    uploadfile = FileField('Upload Contacts', validators=[FileAllowed(['csv'])])
    submit = SubmitField('Submit')