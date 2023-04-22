from flask import Flask
from flask_wtf import FlaskForm
from flask_wtf.file import FileRequired
from wtforms import EmailField, PasswordField, BooleanField, SubmitField, StringField, FileField
from wtforms.validators import DataRequired


class MedForm(FlaskForm):
    title = StringField('Название')
    price = StringField('Цена')
    quantity = StringField('Количество')
    picture = FileField('Картинка', validators=[FileRequired()])
    submit = SubmitField('Войти')