{% extends "base.html" %}

{% block content %}
<div class="login_form">
<h1>Укажите место куда вам доставить товар</h1>
<form action="" method="post">
    {{ form.hidden_tag() }}
    <p>
        {{ form.city.label }}<br>
            <select class="form-control" id="classSelect" name="city">
              {% for city in cities %}
              <option>{{ city }}</option>
              {% endfor %}

            </select>
    </p>
    <dialog id="myDialog">
  <h1>Закрой меня! 🙏</h1>
  <p>Результат этих кнопок одинаковый</p>

  <button type="button" onclick="window.myDialog.close();">
    Close
  </button>

      <form method="dialog" >
        <button type="button" class="btn btn-primary" onclick="window.location='http://127.0.0.1:8123/minus/{{id}}/place'">OK</button>
      </form>
    </dialog>
    <p>
        {{ form.street.label }}<br>
        {{ form.street(class="form-control") }}<br>
    </p>
    <p>
        {{ form.house_number.label }}<br>
        {{ form.house_number(class="form-control") }}<br>
    </p>
    <p>
        {{ form.apartment_number.label }}<br>
        {{ form.apartment_number(class="form-control") }}<br>
    </p>
    <p>
        {{ form.quantity.label }}<br>
        {{ form.quantity(class="form-control") }}<br>
    </p>
    <p onclick="window.myDialog.show();">
        {{ form.submit(type="submit", class="btn btn-primary") }}
        {{message}}
    </p>
</form>
</div>
<link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0-alpha3/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-KK94CHFLLe+nY2dmCWGMq91rCGa5gtU4mk92HdvYe+M/SXH301p5ILy+dN9+nJOZ" crossorigin="anonymous">
<script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0-alpha3/dist/js/bootstrap.bundle.min.js" integrity="sha384-ENjdO4Dr2bkBIFxQpeoTz1HIcje39Wm4jDKdf19U8gI4ddQ3GYNS7NTKfAdVQSZe" crossorigin="anonymous"></script>
{% endblock %}
