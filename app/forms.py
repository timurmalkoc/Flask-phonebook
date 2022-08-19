from flask_wtf import FlaskForm
from wtforms import StringField,SubmitField,PasswordField
from wtforms.validators import InputRequired, EqualTo


class AddressRegister(FlaskForm):
    name = StringField('Name', validators=[InputRequired()])
    phone = StringField('Phone', validators=[InputRequired()])
    street = StringField('Address', validators=[InputRequired()])
    zipcode = StringField('Zipcode', validators=[InputRequired()])
    submit = SubmitField()

class UserRegister(FlaskForm):
    email = StringField('Email', validators=[InputRequired()])
    username = StringField('Username', validators=[InputRequired()])
    password = PasswordField('Password', validators=[InputRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[InputRequired(), EqualTo('password')])
    submit = SubmitField()

class Login(FlaskForm):
    username = StringField('Username', validators=[InputRequired()])
    password = PasswordField('Passowrd', validators=[InputRequired()])
    submit = SubmitField()
