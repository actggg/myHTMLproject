from flask import Flask
from flask_wtf import FlaskForm
from wtforms import EmailField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired


class MedForm(FlaskForm):
    title = EmailField('Почта', validators=[DataRequired()])
    price = PasswordField('Пароль', validators=[DataRequired()])
    quantity = BooleanField('Запомнить меня')
    picture = SubmitField('Войти')