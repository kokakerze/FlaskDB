import sqlite3

from flask import Flask, jsonify, request, redirect, url_for, render_template
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func
from faker import Faker


fake = Faker()

DATABASE = "users.db"
# connection = sqlite3.connect(DATABASE)
# cursor = connection.cursor()
# cursor.execute(
#     """
#     CREATE TABLE IF NOT EXISTS users (
#         id INTEGER PRIMARY KEY,
#         name TEXT NOT NULL,
#         email TEXT NOT NULL
#     )
#     """
# )


# def db_con():
#     cn = None
#     try:
#         cn = sqlite3.connect(DATABASE)
#     except Exception as e:
#         print(e)
#     return cn
#

app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'

db = SQLAlchemy(app)


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)

    def __init__(self, *args, **kwargs):
        super(User, self).__init__(*args, **kwargs)

    def __repr__(self):
        return '<User %r>' % self.name


@app.route("/")
def home():
    return "Welcome Home!"


@app.route("/users/all")
def users_all():
    cur = db.session.execute("select * from users")
    users = [
        dict(id=row[0], name=row[1], email=row[2])
        for row in cur.fetchall()
    ]
    return jsonify(users)


@app.route("/users/gen")
def users_gen():
    usr = User(name=fake.name(), email=fake.email())
    db.session.add(usr)
    db.session.commit()
    return redirect(url_for('users_all'))


@app.route("/users/delete-all")
def users_del_all():
    db.session.query(User).delete()
    db.session.commit()
    return redirect(url_for('users_all'))


@app.route("/users/count")
def users_count():
    cur = db.session.execute("select count(1) as cnt from users")
    row = cur.fetchone()
    db.session.flush()
    db.session.commit()
    if row is None:
        return ValueError("Could not count users")
    return jsonify({"count": row[0]})





@app.route("/users/add", methods=['GET', 'POST'])
def users_add():
    if request.method == "GET":
        return render_template("user_add.html")
    else:
        try:
            u = User(name=request.form["user_name"], email=request.form["email"])
            db.session.add(u)
            db.session.flush()
            db.session.commit()
        except:
            db.session.rollback()
            print("Ошибка добавления в БД")
    return redirect(url_for('users_all'))

