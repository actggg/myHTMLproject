import math
import os

import requests
from bs4 import BeautifulSoup
from flask import Flask, render_template, redirect
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from werkzeug.utils import secure_filename

from data import db_session
from data import users
from data.medandusers import Med
from data.news import News
from data.users import User, LoginForm, RegisterForm
from forms.med import MedForm
from forms.place import PlaceForm

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
login_manager = LoginManager()
login_manager.init_app(app)


@app.route("/")
def base():
    return render_template("base.html")


def index():
    db_sess = db_session.create_session()
    if current_user.is_authenticated:
        news = db_sess.query(News).filter(
            (News.user == current_user) | (News.is_private != True))
    else:
        news = db_sess.query(News).filter(News.is_private != True)
    return render_template("index.html", news=news)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(users.User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/")
        return render_template('login.html',
                               message="Неправильный логин или пароль",
                               form=form)
    return render_template('login.html', title='Авторизация', form=form)


@app.route('/add_med', methods=['GET', 'POST'])
def add_med():
    form = MedForm()
    return render_template('med.html', title='Авторизация', form=form)


@app.route('/register', methods=['GET', 'POST'])
def reqister():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Пароли не совпадают")
        db_sess = db_session.create_session()
        if db_sess.query(User).filter(User.email == form.email.data).first():
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Такой пользователь уже есть")
        user = User(
            name=form.name.data,
            email=form.email.data,
            about=form.about.data
        )
        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()
        return redirect('/login')
    return render_template('register.html', title='Регистрация', form=form)


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


@app.route('/catalog', methods=['GET', 'POST'])
def catalog():
    db_sess = db_session.create_session()
    medicines = db_sess.query(News).all()
    return render_template('catalog.html', title='Каталог', med=medicines)


@login_required
@app.route('/basket', methods=['GET', 'POST'])
def basket():
    x = []
    db_sess = db_session.create_session()
    medicines = db_sess.query(Med).filter(Med.id_user.like(current_user.id)).all()
    for i in medicines:
        x.append(db_sess.query(News).filter(News.id.like(i.id_med)).first())
    return render_template('basket.html', title='Корзина', med=x)


@login_required
@app.route('/minus/<u>/<where>', methods=['GET', 'POST'])
def minus(u, where):
    form = PlaceForm()
    cities = pars()
    if form.validate_on_submit():
        if way_to_home(f'{form.city.data}{form.street.data}{form.house_number.data}') != False:
            db_session.global_init("db/blogs.db")
            session = db_session.create_session()
            x = session.query(News).filter(News.id.like(u)).first()
            u = session.query(User).filter(User.id.like(current_user.id)).first()
            if x.quantity - int(form.quantity.data) < 0:
                return render_template('place_form.html', title='Анкета заказа', form=form, cities=cities, id=u)
            else:
                u.money -= int(
                    round(way_to_home(f'{form.city.data}{form.street.data}{form.house_number.data}') / 20, 0))
                u.money -= int(form.quantity.data) * x.price
                x.quantity = x.quantity - int(form.quantity.data)
                session.commit()
                return basket()
        else:
            return render_template('place_form.html', title='Анкета заказа', form=form, cities=cities, id=u)
    return render_template('place_form.html', title='Анкета заказа', form=form, cities=cities, id=u)


@login_required
@app.route('/plus/<u>', methods=['GET', 'POST'])
def plus(u):
    db_session.global_init("db/blogs.db")
    session = db_session.create_session()
    if session.query(Med).filter(Med.id_user.like(current_user.id) & Med.id_med.like(u)).first():
        session.query(Med).filter(Med.id_user.like(current_user.id) & Med.id_med.like(u)).first().quantity += 1
    else:
        m = Med()
        m.id_user = current_user.id
        m.id_med = u
        m.quantity = 1
        session.add(m)
        session.commit()
    db_sess = db_session.create_session()
    medicines = db_sess.query(News).all()
    return render_template('catalog.html', title='Каталог', med=medicines)


@login_required
@app.route('/delete/<u>', methods=['GET', 'POST'])
def delete(u):
    db_sess = db_session.create_session()
    med = db_sess.query(Med).filter(Med.id_user.like(current_user.id) & Med.id_med.like(u)).first()
    if med:
        db_sess.delete(med)
        db_sess.commit()
    return basket()


@login_required
@app.route('/accept/<id>/<quantity>', methods=['GET', 'POST'])
def accept(id, quantity):
    db_sess = db_session.create_session()
    price = db_sess.query(News).filter(News.id.like(id)).first().price
    all_price = price * quantity
    return render_template('price.html', price=all_price, id=id)


@app.route('/add_item', methods=['GET', 'POST'])
def add_item():
    form = MedForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        all = db_sess.query(News).all().title
        if form.title.data not in all:
            f = form.picture.data
            filename = secure_filename(f.filename)
            f.save(os.path.join(
                './static/img/лекарства', filename
            ))
            new_med(form.title.data, int(form.price.data), int(form.quantity.data), filename)
            return catalog()
        else:
            u = db_sess.query(News).filter(News.title.like(form.title.data))
            u.quantity = int(form.quantity.data)
    return render_template('add_item.html', form=form)


def pars():
    cities = []
    link = 'https://ru.wikipedia.org/wiki/Список_городов_России'
    resp = requests.get(link)
    if 300 > resp.status_code >= 200:
        bs = BeautifulSoup(resp.text, "html5lib")
        anArticle = BeautifulSoup(" ".join([p.text for p in bs.find_all("p")]), "html5lib").get_text().replace(
            "\xa0", " ")
        anArticle = anArticle.replace('↑', '')
        count = 0
        for link in anArticle.split('\n'):
            if link == ' Москва, столица России':
                cities.append('Москва')
                count = 1
            elif count != 0 and count != 15:
                count += 1
                cities.append(link[1:])
        return cities


def if_in_table(name):
    db_session.global_init("db/blogs.db")
    session = db_session.create_session()
    if session.query(News).filter(News.title.like(name)).all():
        return False
    return True


def new_med(title, price, quantity, picture):
    if if_in_table(title):
        m = News()
        m.title = title
        m.price = price
        m.quantity = quantity
        m.picture = picture
        session = db_session.create_session()
        session.add(m)
        session.commit()


def way_to_home(address):
    def lonlat_distance(a, b):

        degree_to_meters_factor = 111 * 1000  # 111 километров в метрах
        a_lon, a_lat = a
        b_lon, b_lat = b

        # Берем среднюю по широте точку и считаем коэффициент для нее.
        radians_lattitude = math.radians((a_lat + b_lat) / 2.)
        lat_lon_factor = math.cos(radians_lattitude)

        dx = abs(a_lon - b_lon) * degree_to_meters_factor * lat_lon_factor
        dy = abs(a_lat - b_lat) * degree_to_meters_factor

        distance = math.sqrt(dx * dx + dy * dy)

        return distance

    home = f'http://geocode-maps.yandex.ru/1.x/?apikey=40d1649f-0493-4b70-98ba-98533de7710b&geocode=Малый Знаменский переулок, 7/10 стр. 5&format=json'
    school = f'http://geocode-maps.yandex.ru/1.x/?apikey=40d1649f-0493-4b70-98ba-98533de7710b&geocode={address}&format=json'
    response_1 = requests.get(home)
    response_2 = requests.get(school)
    if response_1 and response_2:
        json_response_1 = response_1.json()
        json_response_2 = response_2.json()
        home_coord = json_response_1["response"]["GeoObjectCollection"]["featureMember"][0]["GeoObject"]['Point'][
            'pos'].split()
        school_coord = json_response_2["response"]["GeoObjectCollection"]["featureMember"][0]["GeoObject"]['Point'][
            'pos'].split()
        home_coord[0] = float(home_coord[0])
        home_coord[1] = float(home_coord[1])
        school_coord[0] = float(home_coord[0])
        school_coord[1] = float(school_coord[1])
        return lonlat_distance(home_coord, school_coord)
    else:
        return False


def main():
    db_session.global_init("db/blogs.db")
    # app.run()
    session = db_session.create_session()
    new_med("Венарус", 100, 50, "Венарус.png")
    new_med("Лизобакт", 299, 50, "Лизобакт.jpg")
    new_med("Супрастин", 223, 50, "Супрастин.jpg")
    new_med("Ринофлуимуцил", 554, 50, "Ринофлуимуцил.jpg")
    new_med("Йодомарин", 224, 50, "Йодомарин.png")
    new_med("Эспумизан", 354, 25, "Эспумизан.jpg")
    app.run(port=8127, host='127.0.0.1')


if __name__ == '__main__':
    main()
