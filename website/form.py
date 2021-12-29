from flask_wtf import FlaskForm, Form
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField, IntegerField, RadioField, \
    FormField, FieldList
from wtforms.fields.html5 import DateField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError, Optional
from flask_login import current_user
from website.models import User


class LoginForm(FlaskForm):
    email = StringField('Email:', validators=[DataRequired(), Email()])
    password = PasswordField('Password:', validators=[Length(min=8, max=16), DataRequired()])
    submit = SubmitField('Login')


class PosttaskForm(FlaskForm):
    tasktitle = StringField('Titolo:')
    taskdescription = StringField('Description:')
    date = DateField()
    submit = SubmitField('Post Task')


class ReviewForm(FlaskForm):
    reviewtitle = StringField('Titolo:')
    reviewdescription = StringField('Description:')
    submit = SubmitField('Review')
