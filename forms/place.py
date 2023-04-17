from flask import Flask
from flask_wtf import FlaskForm
from wtforms import EmailField, PasswordField, BooleanField, SubmitField, StringField
from wtforms.validators import DataRequired


class PlaceForm(FlaskForm):
    city = StringField('Город')
    street = StringField('Улица')
    house_number = StringField('Номер дома')
    apartment_number = StringField('Номер квартиры')
    quantity = StringField('Номер квартиры')
    submit = SubmitField('Заказать')