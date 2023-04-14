import datetime
import sqlalchemy
from sqlalchemy import orm
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField
from wtforms import BooleanField, SubmitField
from wtforms.validators import DataRequired
from .db_session import SqlAlchemyBase


class News(SqlAlchemyBase):
    __tablename__ = 'medical'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    title = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    price = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)
    quantity = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)
    picture = sqlalchemy.Column(sqlalchemy.String, nullable=True)




class NewsForm(FlaskForm):
    title = StringField('Заголовок', validators=[DataRequired()])
    content = TextAreaField("Содержание")
    is_private = BooleanField("Личное")
    submit = SubmitField('Применить')

