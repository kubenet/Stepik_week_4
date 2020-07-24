import json
from flask import Flask, render_template, request
from flask_wtf import FlaskForm
from wtforms import RadioField, StringField

app = Flask(__name__)
app.secret_key = 'key'

with open('data.json', 'r') as r:
    all_data = json.load(r)
    r.close()


# Запись нового запроса в файл all_requests.json
def add_request(name, phone, goal, times):
    with open('requests.json', 'r') as read_json:
        records = json.load(read_json)
    records.append({'name': name, 'phone': phone, 'goal': goal, 'times': times})
    read_json.close()
    with open('requests.json', 'w') as write_json:
        json.dump(records, write_json)
        write_json.close()


# Запись нового запроса в файл all_requests.json
def update_timetale_teacher(id_teacher, day, times, client_name, client_phone):
    with open('data.json', 'r') as read_json:
        records = json.load(read_json)
        records[1][int(id_teacher)]['free'][day][times] = False
        read_json.close()

    with open('data.json', 'w') as w:
        json.dump(records, w)
        w.close()

    with open('data.json', 'r') as r:
        global all_data
        all_data = json.load(r)
        r.close()

    with open('booking.json', 'r') as read_booking:
        records = json.load(read_booking)
        records.append([id_teacher, day, times, client_name, client_phone])
        read_booking.close()
        with open('booking.json', 'w') as write_booking:
            json.dump(records, write_booking)
            write_booking.close()




class RequestForm(FlaskForm):  # объявление класса формы для WTForms
    name = StringField('name')
    phone = StringField('phone')
    goal = RadioField("Какая цель занятий?", choices=[('0', 'Для путешествий'), ('1', 'Для школы'), ('2', 'Для работы'),
                                                      ('3', 'Для переезда')])
    time = RadioField("Сколько времени есть?",
                      choices=[('0', '1-2 часа в неделю'), ('1', '3-5 часов в неделю'), ('2', '5-7 часов в неделю'),
                               ('3', '7-10 часов в неделю')])


@app.route('/')  # главная
def index():
    return render_template("index.html", all_data=all_data)


@app.route('/techers/')  # все репетиторы
def techers():
    return render_template("techers.html", all_data=all_data)


@app.route('/goals/<goal>/')  # цель 'goal'
def goals(goal):
    return render_template("goals.html", goal=goal, all_data=all_data)


@app.route('/profiles/<int:id_techers>/')  # профиль репетитора <id учителя>
def profiles(id_techers):
    return render_template("profiles.html", id_techers=id_techers, all_data=all_data)


@app.route('/requests/')  #  заявка на подбор репетитора
def requests():
    form_request = RequestForm()  # Форма для страницы ('/request')
    return render_template("request.html", form=form_request, all_data=all_data)


@app.route('/request_done/', methods=['POST'])  # заявка на подбор отправлена
def request_done():
    form = RequestForm()
    name = form.name.data
    phone = form.phone.data
    goal = form.goal.data
    times = form.time.data

    goal_choices = {'0': 'Для путешествий', '1': 'Для школы', '2': 'Для работы', '3': 'Для переезда'}
    time_choices = {'0': '1-2 часа в неделю', '1': '3-5 часов в неделю', '2': '5-7 часов в неделю',
                    '3': '7-10 часов в неделю'}

    add_request(name, phone, goal_choices[goal], time_choices[times])
    return render_template("request_done.html", username=name, userphone=phone,
                           goal=goal_choices[goal], time=time_choices[times])


@app.route('/booking/<int:id_techers>/<day>/<time>/')  # здесь будет форма бронирования <id учителя>
def booking(id_techers, day, time):
    return render_template("booking.html", id_techers=id_techers, day=day, time=time, all_data=all_data)


@app.route('/booking_done/', methods=['POST'])  # заявка отправлена
def booking_done():
    # получаем даныне из формы
    client_weekday = request.form["clientWeekday"]
    client_time = request.form["clientTime"]
    client_teacher = request.form["clientTeacher"]
    client_name = request.form["clientName"]
    client_phone = request.form["clientPhone"]

    # Обновляем расписание свободного времени репетитора
    update_timetale_teacher(client_teacher, client_weekday, client_time, client_name, client_phone)

    return render_template("booking_done.html", clientName=client_name, clientPhone=client_phone,
                           clientTime=client_time, clientTeacher=client_teacher, clientWeekday=client_weekday)


app.run('0.0.0.0')
