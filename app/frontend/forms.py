from flask.ext.wtf import Form
from flask.ext.wtf import (HiddenField, BooleanField, TextField,
        PasswordField, SubmitField)
from flask.ext.wtf import Required, Length, EqualTo, Email

from ..utils import (PASSWORD_LEN_MIN, PASSWORD_LEN_MAX,
        USERNAME_LEN_MIN, USERNAME_LEN_MAX)


class LoginForm(Form):
    next = HiddenField()
    login = TextField('Username (or email)', [Required()])
    password = PasswordField('Password', [Required(),
        Length(PASSWORD_LEN_MIN, PASSWORD_LEN_MAX)],)
    remember = BooleanField('Remember me')
    submit = SubmitField('Sign in')


class RegisterForm(Form):
    next = HiddenField()
    username = TextField('Username', [Required(), Length(USERNAME_LEN_MIN, USERNAME_LEN_MAX)],)
    email = TextField('Email', [Required(), Email()])
    password = PasswordField('Password', [Required(),
        EqualTo('confirm', message='Passwords must match'),
        Length(PASSWORD_LEN_MIN, PASSWORD_LEN_MAX)],)
    confirm = PasswordField('Repeat Password')
    submit = SubmitField('Sign up')
