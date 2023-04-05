from flask import Flask, url_for, request

app = Flask(__name__)


@app.route("/choice")
def choice():
    return '''
    <h1>Миссия Колонизация Марса</h1>
    <h2>dddd</h1>
            '''


@app.route("/index")
def index():
    return "<h1>И на Марсе будут яблони цвести!</h1>"


@app.route("/promotion")
def promotion():
    return f"""<link rel="stylesheet" type="text/css" href="{url_for('static', filename='css/style.css')}" />
        <form class="login_form" method="post">
        <h2>Человечество вырастает из детства.<h2> </br>
            <h2>Человечеству мала одна планета.<h2> </br>
            <h2>Мы сделаем обитаемыми безжизненные пока планеты.<h2> </br>
            <h2>И начнем с Марса!<h2> </br>
            <h2>Присоединяйся!<h2>
    """


@app.route('/image_mars')
def image_mars():
    return f'''<h2>Жди нас, Марс!<h2> </br>
    <img src="{url_for('static', filename='img/400624.jpg')}" alt="здесь должна была быть картинка, но не нашлась">'''


@app.route("/")
@app.route('/astronaut_selection', methods=['POST', 'GET'])
def astronaut_selection():
    if request.method == 'GET':
        return f'''<!doctype html>
                        <html lang="en">
                          <head>
                            <meta charset="utf-8">
                            <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
                            <link rel="stylesheet"
                            href="https://cdn.jsdelivr.net/npm/bootstrap@5.0.0-beta1/dist/css/bootstrap.min.css"
                            integrity="sha384-giJF6kkoqNQ00vy+HMDP7azOuL0xtbfIcaT9wjKHr8RbDVddVHyTfAAsrekwKmP1"
                            crossorigin="anonymous">
                            <link rel="stylesheet" type="text/css" href="{'style.css'}" />
                            <title>Пример формы</title>
                          </head>
                          <body>
                            <h1 class='center'>Анкета претендента</h1>
                            <h2 class='center'>на участие в миссии</h2>
                            <div>
                                <form class="login_form" method="post">
                                    <input class="form-control" aria-describedby="emailHelp" placeholder="Введите фамилию"><br>
                                    <input class="form-control" placeholder="Введите имя" name="password"><br><br>
                                    <input type="email" class="form-control" id="email" aria-describedby="emailHelp" placeholder="Введите адрес почты" name="email"><br>
                                    <div class="form-group">
                                        <label for="classSelect">Какое у Вас образование?</label><br>
                                            <select class="form-control" id="classSelect" name="class">
                                              <option>Начальное</option>
                                              <option>Среднее</option>
                                              <option>Высшее</option>
                                            </select>
                                    </div>
                                    <br>
                                    <text>Какие у Вас профессии?</text>
                                        <div class="form-group form-check">
                                            <input type="checkbox" id="happy" name="happy" value="yes"> <label for="happy">Инженер-исследователь</label><br>
                                            <input type="checkbox" id="happy" name="happy" value="yes"> <label for="happy">Пилот</label><br>
                                            <input type="checkbox" id="happy" name="happy" value="yes"> <label for="happy">Строитель</label><br>
                                            <input type="checkbox" id="happy" name="happy" value="yes"> <label for="happy">Экзобиолог</label><br>
                                            <input type="checkbox" id="happy" name="happy" value="yes"> <label for="happy">Врач</label><br>
                                            <input type="checkbox" id="happy" name="happy" value="yes"> <label for="happy">Инженер по терраформированию</label><br>
                                            <input type="checkbox" id="happy" name="happy" value="yes"> <label for="happy">Климатолог</label><br>
                                            <input type="checkbox" id="happy" name="happy" value="yes"> <label for="happy">Специалист по радиационной защите</label><br>
                                        </div>
                                    <br><br>
                                        <label>Укажите пол</label><br>
                                        <div class="form-check">
                                          <input class="form-check-input" type="radio" name="sex" id="male" value="male" checked>
                                          <label class="form-check-label" for="male">Мужской</label>
                                        </div>
                                        <div class="form-check">
                                          <input class="form-check-input" type="radio" name="sex" id="female" value="female">
                                          <label class="form-check-label" for="female">Женский</label>
                                        </div>
                                        <br>
                                            <label for="about">Немного о себе</label><br>
                                            <textarea class="form-control" id="about" rows="3" name="about"></textarea>
                                        <div>
                                            <label for="photo">Приложите фотографию</label><br>
                                            <input type="file" class="form-control-file" id="photo" name="file">
                                        </div>
                                        <br>
                                        <div class="form-group form-check">
                                            <label>
                                                <input type="checkbox" id="happy" name="happy" value="yes">
                                                <label for="happy">Готовы ли остаться на Марсе?</label>
                                            </label>
                                        </div>
                                        <button type="submit" class="btn btn-primary">Отправить</button>
                                </form>
                            </div>
                          </body>
                        </html>'''
    elif request.method == 'POST':
        return "Форма отправлена"


app.run(port=8080)
