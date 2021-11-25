from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.fields.simple import PasswordField
from wtforms.validators import InputRequired


class FeedbackForm(FlaskForm):
    """Form for giving some feedback"""
    username=StringField("username", validators=[InputRequired()])
    password=PasswordField("password", validators=[InputRequired()])
    email=StringField("email", validators=[InputRequired()])
    first_name=StringField("First name", validators=[InputRequired()])
    last_name=StringField("Last name", validators=[InputRequired()])

class LoginForm(FlaskForm):
    """Form for loging in"""
    username=StringField("username", validators=[InputRequired()])
    password=PasswordField("password", validators=[InputRequired()])

class FeedbackForm(FlaskForm):
    """Form for making some feedback"""
    title=StringField("title", validators=[InputRequired()])
    content=StringField("content", validators=[InputRequired()])


