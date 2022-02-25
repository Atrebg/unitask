# coding=utf-8
from flask import flash
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
    email = StringField('Email:', validators=[DataRequired(), Email()])
    name = StringField('Name:', validators=[DataRequired(), Length(min=3, max=25)])
    surname = StringField('Surname:', validators=[DataRequired(), Length(min=3, max=25)])
    description = StringField('Description:', validators=[Length(min=3)])
    type = SelectField("Select type of user:", choices=[('student', 'Student'), ('adult', 'Adult')])
    password = PasswordField('Password:', validators=[DataRequired(), Length(min=8, max=16)])
    passwordconf = PasswordField('Confirm Password:', validators=[DataRequired(), Length(min=8, max=16), EqualTo('password', message='Password must match')])
    submit = SubmitField('Register')

    @staticmethod
    def validate_email(self, email1):
        race = User.query.filter_by(email=email1.data).first()
        if race:
            raise ValidationError(flash('Email already exists.', category='error'))


class PosttaskForm(FlaskForm):
    tasktitle = StringField('Title:', validators=[DataRequired(message ='prova'), Length(min=3, max=25)])
    taskdescription = StringField('Description:', validators=[DataRequired(), Length(min=3, max=25)])
    amount = IntegerField("Payment (Euro):", validators=[DataRequired()])
    address = StringField('Address:', validators=[DataRequired(), Length(min=3, max=25)])
    spt = StringField('Apt, Suite, etc (optional):')
    state = StringField('State:', validators=[DataRequired(), Length(min=3, max=25)])
    zip = StringField('Zip:')
    country = StringField('Country:')
    date = DateField("Date", validators=[DataRequired()])
    dateexpire= DateField("Expiration Date",validators=[DataRequired()])
    submit = SubmitField('Post Task')


class ReviewForm(FlaskForm):
    reviewtitle = StringField('Titolo:', validators=[DataRequired(), Length(min=3, max=25)])
    reviewdescription = StringField('Description:', validators=[DataRequired(), Length(min=3, max=25)])
    submit = SubmitField('Review')


class UpdateAccountForm (FlaskForm):

    name = StringField('Name:', validators=[DataRequired(), Length(min=3, max=25)])
    surname = StringField('Surname:', validators=[DataRequired(), Length(min=3, max=25)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Update')


    def validate_email(self, email):
        race = User.query.filter_by(email=email.data).first()
        if race:
            raise ValidationError('Email already in use')

