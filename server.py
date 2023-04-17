import requests
from bs4 import BeautifulSoup
from flask import Flask, render_template, redirect
from flask_login import LoginManager, login_user, login_required, logout_user, current_user

from data import db_session
from data import users
from data.news import News
from data.medandusers import Med
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
@app.route('/minus/<u>', methods=['GET', 'POST'])
def minus(u):
    form = PlaceForm()
    cities = pars()
    if form.validate_on_submit():
        db_session.global_init("db/blogs.db")
        session = db_session.create_session()
        x = session.query(News).filter(News.id.like(u)).first()
        x.quantity = x.quantity - int(form.quantity.data)
        session.commit()
        db_sess = db_session.create_session()
        medicines = db_sess.query(News).all()
        return basket()
    return render_template('place_form.html', title='Анкета заказа', form=form, cities=cities)


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
    app.run(port=8122, host='127.0.0.1')


if __name__ == '__main__':
    main()
