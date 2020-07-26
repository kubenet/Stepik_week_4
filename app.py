import json
import hashlib
from flask import Flask, render_template, request
from flask_wtf import FlaskForm
from wtforms import RadioField, StringField
from sqlalchemy import CheckConstraint
from flask_sqlalchemy import SQLAlchemy

with open('data.json', 'r') as r:
    all_data = json.load(r)
    md5Hash = hashlib.md5(str(all_data).encode())
    md5Hashed = md5Hash.hexdigest()
    r.close()

app = Flask(__name__)
app.secret_key = md5Hashed
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Teachers(db.Model):
    """ Модель преподавателей """
    __tablename__ = 'teachers'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    about = db.Column(db.String, nullable=False)
    rating = db.Column(db.Float, nullable=False)
    price = db.Column(db.Integer, nullable=False)
    lesson_time = db.Column(db.String, nullable=False)
    # Ссылка на поле в модели цели (One-to-Many)
    goals = db.relationship("Goals", back_populates="goal")
    # Ссылка на поле в модели рассписание (One-to-Many)
    week_day = db.relationship("TimetableTeachers", back_populates="week")


class Goals(db.Model):
    """ Модель целей занятий """
    __tablename__ = 'goals'
    id = db.Column(db.Integer, primary_key=True)
    key = db.Column(db.String, nullable=False)
    # Ссылка на модель преподавателя (One-to-Many)
    teachers_id = db.Column(db.Integer, db.ForeignKey("teachers.id"))
    goal = db.relationship("Teachers", back_populates="goals", uselist=False)

    # Ссылка на поле в модели подбора преподавателя (One-to-Many)
    search_teacher = db.relationship("SearchTeacher", back_populates="goal", uselist=False)


class TimetableTeachers(db.Model):
    """ Модель расписания преподавателей на неделю """
    __tablename__ = 'timetables'
    id = db.Column(db.Integer, primary_key=True)
    day_times = db.Column(db.String, nullable=False)
    status = db.Column(db.Boolean, nullable=False)
    # ссылка на поле id в модели преподавателя (One-to-Many)
    teachers_id = db.Column(db.Integer, db.ForeignKey("teachers.id"))
    week = db.relationship("Teachers", back_populates="week_day", uselist=False)
    # ссылка на поле id в модели booking (One-to-Many)
    booking = db.relationship("Booking", back_populates='day_times', uselist=False)


class SearchTeacher(db.Model):
    """ Модель поиска преподавателя по критериям: цели и планируемое кол-во часов занятий в неделю """
    __tablename__ = 'search_teachers'
    id = db.Column(db.Integer, primary_key=True)
    how_time = db.Column(db.String(20), nullable=False)
    client_name = db.Column(db.String(25), nullable=False)
    client_phone = db.Column(db.String(10), nullable=False)
    # Ссылка на поле в модели цели (One-to-Many)
    goal_id = db.Column(db.Integer, db.ForeignKey("goals.id"))
    goal = db.relationship("Goals", back_populates="search_teacher", uselist=False)


class Booking(db.Model):
    """ Модель для записи на пробное занятие к преподавателю """
    __tablename__ = 'booking'
    id = db.Column(db.Integer, primary_key=True)
    client_name = db.Column(db.String(25), nullable=False)
    client_phone = db.Column(db.String(10), nullable=False)
    # ссылка на поле id в модели Teachers (One-to-Many)
    timetable_id = db.Column(db.Integer, db.ForeignKey("timetables.id"))
    # ссылка на поле free и day в модели TimetableTeachers (One-to-One)
    day_times = db.relationship("TimetableTeachers", back_populates="booking", uselist=False)


db.drop_all()
db.create_all()
teacher1 = Teachers(name='Ivan', about='about', rating=4.5, price=900, lesson_time='1')
teacher2 = Teachers(name='Fedor', about='about2', rating=4, price=9, lesson_time='13')
teacher3 = Teachers(name='Vasya', about='about3', rating=5, price=90, lesson_time='41')

b = Booking(client_name='Semyon', client_phone='4440009993322')
t1 = TimetableTeachers(day_times="8:00", status=False, booking=b, week=teacher3)

search_teacher = SearchTeacher(how_time='1-2 часа', client_name='Igor', client_phone='79993332211')

week = TimetableTeachers(day_times="8:00", status=False, week=teacher1)
week1 = TimetableTeachers(day_times="10:00", status=True, week=teacher1)
week2 = TimetableTeachers(day_times="12:00", status=True, week=teacher1)
week3 = TimetableTeachers(day_times="14:00", status=True, week=teacher1)
week4 = TimetableTeachers(day_times="16:00", status=True, week=teacher3)
week5 = TimetableTeachers(day_times="18:00", status=True, week=teacher3)
week6 = TimetableTeachers(day_times="20:00", status=True, week=teacher3)
week7 = TimetableTeachers(day_times="22:00", status=True, week=teacher3)
week8 = TimetableTeachers(day_times="21:00", status=True, week=teacher3)

goal1 = Goals(key='fly', goal=teacher1)
goal2 = Goals(key='learn', goal=teacher1)
goal3 = Goals(key='travel', goal=teacher1)
goal4 = Goals(key='travel', goal=teacher3)
goal_s = Goals(key='travel', search_teacher=search_teacher)

db.session.add(goal1)
db.session.add(goal2)
db.session.add(goal3)
db.session.add(goal4)
db.session.add(search_teacher)


db.session.add(b)
db.session.add(t1)

db.session.add(week)
db.session.add(week1)
db.session.add(week2)
db.session.add(week3)
db.session.add(week4)
db.session.add(week5)
db.session.add(week6)
db.session.add(week7)
db.session.add(week8)
db.session.add(teacher1)
db.session.add(teacher2)
db.session.add(teacher3)

db.session.commit()
t1 = Teachers.query.get(1)
print(t1.name)
print(t1.about)
print(t1.rating)
print(t1.price)
print(t1.lesson_time)
print(t1.goals[0].key)
print(t1.goals[1].key)
print(t1.goals[2].key)


def add_record(name, about, rating, price, goal, lesson_time):
    teacher = Teachers(name=name, about=about, rating=rating, price=price, goal=goal, lesson_time=lesson_time)
    db.session.add(teacher)
    db.session.commit()
    return teacher.id  # id нового преподавателя в БД


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


@app.route('/requests/')  # заявка на подбор репетитора
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


app.run('0.0.0.0', debug=True)
