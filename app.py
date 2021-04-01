"""Flask project that works with DATABASE."""
from faker import Faker
from flask import Flask, jsonify, redirect, render_template, request, url_for
from flask_sqlalchemy import SQLAlchemy


fake = Faker()

# DATABASE = "users.db"
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
#
#
# def db_con():
#     cn = None
#     try:
#         cn = sqlite3.connect(DATABASE)
#     except Exception as e:
#         print(e)
#     return cn


app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'

db = SQLAlchemy(app)


class User(db.Model):
    """This class creates DATABASE of Users with fields id,name,email."""

    __tablename__ = 'users'
    idt = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)

    def __init__(self, *args, **kwargs):
        """Init global variables in this class."""
        super(User, self).__init__(*args, **kwargs)

    def __repr__(self):
        """Given a format of printing."""
        return '<User %r>' % self.name


@app.route("/")
def home():
    """Home page."""
    return "Welcome Home!"


@app.route("/users/all")
def users_all():
    """Thows all users."""
    result = User.query.all()
    users = [
        dict(id=user.idt, name=user.name, email=user.email) for user in result
    ]
    return jsonify(users)


@app.route("/users/gen")
def users_gen():
    """Generate one fake user."""
    usr = User(name=fake.name(), email=fake.email())
    db.session.add(usr)
    db.session.commit()
    return redirect(url_for("users_all"))


@app.route("/users/delete-all")
def users_del_all():
    """Delete all users."""
    db.session.query(User).delete()
    db.session.commit()
    return redirect(url_for('users_all'))


@app.route("/users/count")
def users_count():
    """Count how many users in DATABASE."""
    row = User.query.count()
    db.session.flush()
    db.session.commit()
    if row is None:
        return ValueError("Could not count users")
    return jsonify({"count": row})


@app.route("/users/add", methods=['GET', 'POST'])
def users_add():
    """Register a new user."""
    if request.method == "GET":
        return render_template("user_add.html")
    else:
        try:
            u = User(name=request.form["user_name"],
                     email=request.form["email"])
            db.session.add(u)
            db.session.flush()
            db.session.commit()
        except Exception:
            db.session.rollback()
            print("Ошибка добавления в БД")
    return redirect(url_for('users_all'))
