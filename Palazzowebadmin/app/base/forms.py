# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from flask_wtf import FlaskForm
from wtforms import BooleanField,TextField, PasswordField,FieldList,SubmitField,SelectField,StringField,TextAreaField,IntegerField,FormField,DateField
from wtforms.validators import DataRequired, Email, EqualTo, InputRequired, Length, Regexp, ValidationError
from wtforms.widgets.html5 import ColorInput
## login and registration
from flask_wtf.file import FileField, FileRequired
from app.base.models import User



class LoginForm(FlaskForm):
    username = TextField    ('Username', id='username_login'   , validators=[DataRequired()])
    password = PasswordField('Password', id='pwd_login'        , validators=[DataRequired()])

class CreateAccountForm(FlaskForm):
    username = TextField('Username'     , id='username_create' , validators=[DataRequired()])
    email    = TextField('Email'        , id='email_create'    , validators=[DataRequired(), Email()])
    password = PasswordField('Password' , id='pwd_create'      , validators=[DataRequired()])



class RegistrationForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Length(1, 64),
                                             Email()])
    username = StringField('Username', validators=[
        DataRequired(), Length(1, 64),
        Regexp('^[A-Za-z][A-Za-z0-9_.]*$', 0,
               'Usernames must have only letters, numbers, dots or '
               'underscores')])
    password = PasswordField('Password', validators=[
        DataRequired(), EqualTo('password2', message='Passwords must match.')])
    password2 = PasswordField('Confirm password', validators=[DataRequired()])
    roles       = SelectField('select filed')
    submit = SubmitField('Register')

    def validate_email(self, field):
        if User.query.filter_by(email=field.data.lower()).first():
            raise ValidationError('Email already registered.')

    def validate_username(self, field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError('Username already in use.')


class prioritizeForm(FlaskForm):
    status                      = BooleanField('Promotion status',validators=[DataRequired()])
    idev                        = IntegerField('idev',validators=[DataRequired()])
    privior                     = IntegerField('Priority',validators=[DataRequired()])

    submit                       =SubmitField('Change')
class prioritizeListForm(FlaskForm):
    select_entries = FieldList(FormField(prioritizeForm))
class EventsForm(FlaskForm):
    eventname                   = StringField('Promotion name',validators=[DataRequired() ,Length(1, 15)])
    ENTitle                     = StringField('Title of Promotion by English',validators=[DataRequired(),Length(1, 50)])
    CNTitle                     = StringField('Title of Promotion by Chinese',validators=[DataRequired()])
    KRTitle                     = StringField('Title of Promotion by Korean',validators=[DataRequired()])
    ENdetail                    = StringField('Detail of Promotion by English',validators=[DataRequired()])
    CNdetail                    = StringField('Detail of Promotion by Chinese',validators=[DataRequired()])
    KRdetail                    = StringField('Detail of Promotion by Korean',validators=[DataRequired()])
    ENdescription               = TextAreaField('Description of Promotion by English', validators=[DataRequired()])
    CNdescription               = TextAreaField('Description of Promotion by Chinese', validators=[DataRequired()])
    KRdescription               = TextAreaField('Description of Promotion by Korean', validators=[DataRequired()])
    ENimagebase64               = FileField('Upload English Image',validators=[FileRequired()])
    CNimagebase64               = FileField('Upload Chinese Image',validators=[FileRequired()])
    KRimagebase64               = FileField('Upload Korean Image',validators=[FileRequired()])
    color                       = StringField(widget=ColorInput())
    urldetail                   = TextAreaField('Url detail', validators=[DataRequired()])
    submit                      = SubmitField('Submit')

class footerdataForm(FlaskForm):
    value                       = StringField('Value', validators=[DataRequired()])
    Submit                      = SubmitField('Submit')

class footerForm(FlaskForm):
    name                        = StringField('Name', validators=[DataRequired()])
    value                       = StringField('Value', validators=[DataRequired()])
    status                      = BooleanField('status',validators=[DataRequired()])
    ordinal                     = SelectField('Ordinal', choices=['top','middle'])
    side                        = SelectField('osition', choices=['Left','Right'])
    submit                      = SubmitField('Submit')

class DaysofEvent(FlaskForm):
    Daysofevent                 = StringField('Select Days of Promotion', required=True)
    submit                      = SubmitField('Submit')

class datepickerform(FlaskForm):
    days                        = StringField("select date", validators=[DataRequired()])
    submit                      = SubmitField('Submit')
class EventssofDay(FlaskForm):
    dayCalendar                 = DateField('Select day', required=False)
    prioritizeEvent             = StringField('prioritize of Promotion', required=False)
    EventssofDay                = StringField('Promotions of Day', required=True)
    submit                      = SubmitField('Submit')
