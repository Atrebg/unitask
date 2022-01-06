from flask_wtf import FlaskForm, Form
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField, IntegerField, RadioField, \
    FormField, FieldList, SelectField
from wtforms.fields.html5 import DateField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError, Optional
from flask_login import current_user
from website.models import User


class LoginForm(FlaskForm):
    email = StringField('Email:', validators=[DataRequired(), Email()])
    password = PasswordField('Password:', validators=[Length(min=8, max=16), DataRequired()])
    submit = SubmitField('Login')


class SignupForm(FlaskForm):
    email = StringField('E-mail:', validators=[DataRequired(), Email()])
    name = StringField('Name:', validators=[DataRequired(), Length(min=3, max=25)])
    surname = StringField('Surname:', validators=[DataRequired(), Length(min=3, max=25)])
    type = SelectField("Select type of user:", choices=[('student', 'Student'), ('adult', 'Adult')])
    password = PasswordField('Password:', validators=[DataRequired(), Length(min=8, max=16)])
    passwordconf = PasswordField('Confirm Password:', validators=[DataRequired(), Length(min=8, max=16)])
    submit = SubmitField('Register')

    def validate_email(self, email):
        race = User.query.filter_by(email=email.data).first()
        if race:
            raise ValidationError('Email already in use, please follow password recovery procedure')


class PosttaskForm(FlaskForm):
    tasktitle = StringField('Titolo:')
    taskdescription = StringField('Description:')
    date = DateField()
    submit = SubmitField('Post Task')


class ReviewForm(FlaskForm):
    reviewtitle = StringField('Titolo:')
    reviewdescription = StringField('Description:')
    submit = SubmitField('Review')


class UpdateAccountForm (FlaskForm):

    name = StringField('Name:', validators=[DataRequired(), Length(min=3, max=25)])
    surname = StringField('Surname:', validators=[DataRequired(), Length(min=3, max=25)])

    email = StringField('Email',
                        validators=[DataRequired(), Email()])

    submit = SubmitField('Update')


    def validate_email(self, email):
        race = User.query.filter_by(email=email.data).first()
        if race:
            raise ValidationError('Email already in use, please follow password recovery procedure')

