#-*- coding:utf-8 -*-
from flask_wtf import FlaskForm
from wtforms import HiddenField, PasswordField, StringField, TextAreaField, TextField
from wtforms.validators import DataRequired, Length, Optional


class LoginForm(FlaskForm):
    next = HiddenField()
    identidad = StringField('Usuario o e-mail',
                            validators=[DataRequired(), Length(3, 256)])
    contrasena = PasswordField(u'Contraseña',
                               validators=[DataRequired(), Length(8, 32)])


class UsuariosForm(FlaskForm):
    nombre = TextField('Nombre',
                       validators=[DataRequired(), Length(3, 256)])
    email = TextField('e-mail',
                      validators=[DataRequired(), Length(3, 256)])
    contrasena = PasswordField(u'Contraseña',
                               validators=[DataRequired(), Length(8, 32)])
    notas = TextAreaField('Notas',
                          validators=[Optional(), Length(max=8192)])
