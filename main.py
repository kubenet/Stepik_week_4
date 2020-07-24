from flask import Flask, render_template, request
from sqlalchemy import CheckConstraint
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField

app = Flask(__name__)
app.secret_key = "randomstring"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
# engine = create_engine('sqlite:///test.db', echo=True)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    email = db.Column(db.String, nullable=False)
    CheckConstraint("email LIKE '%@%'")
    pets = db.relationship("Pet")


class Pet(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    pets = db.Column(db.String, nullable=False)
    owner = db.relationship("User")
    owner_id = db.Column(db.Integer, db.ForeignKey("users.id"))


db.create_all()


def add_record(name, email):
    user = User(name=name, email=email)
    db.session.add(user)
    db.session.commit()
    return user.id


# создание формы
class OrderForm(FlaskForm):
    name = StringField("Имя")
    email = StringField("Email")


# # показываем форму
# @app.route('/')
# def index():
#     form = OrderForm()
#     return render_template("form.html", form=form)

@app.route('/')
def index():
    return render_template("index.html")


# принимаем форму
@app.route("/save/", methods=["POST"])
def save():
    form = OrderForm()
    name = form.name.data
    email = form.email.data
    id = add_record(name, email)

    return render_template("save.html", id=id, name=name, email=email)


app.run(debug=True)
