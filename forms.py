from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField
from wtforms.validators import DataRequired, Email, Length

class MessageForm(FlaskForm):
    """form for adding/editing messages"""
    text=TextAreaField("text",validators=[DataRequired()])

class AddUserForm(FlaskForm):
    """form to add user to db"""
    username=StringField("Username",validators=[DataRequired()])
    password=PasswordField("Password",validators=[Length(min=6)])
    email=StringField("E-mail", validators=[DataRequired(),Email()])
    image_url=StringField('(Optional) Image URL')

class LoginForm(FlaskForm):
    """Login form"""
    username=StringField("Username",validators=[DataRequired()])
    password=PasswordField("Password",validators=[Length(min=6)])