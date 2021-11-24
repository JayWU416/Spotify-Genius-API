from enum import unique
import flask
from flask import Flask, render_template, flash, redirect, url_for
import requests
from main import get_song_data
import os
from flask_sqlalchemy import SQLAlchemy
import sqlalchemy
from flask_login import LoginManager, login_manager, UserMixin, current_user, login_required, login_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, ValidationError
from flask_migrate import Migrate
from werkzeug.security import generate_password_hash



app = flask.Flask(__name__)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = "thisisthesecretkey"

db = SQLAlchemy(app)
migrate = Migrate(app, db)
login = LoginManager()
login.init_app(app)
login.login_view = 'login'


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Sign In')

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Register')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()

        if user:
            raise ValidationError('Give me Another name')

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(), unique=True)
    password = db.Column(db.String())

    def __repr__(self):
        return '<User {}>'.format(self.username)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)



class ArtistIdForm(FlaskForm):
    artistid = StringField('ArtistId', validators=[DataRequired()])
    submit = SubmitField('Add artist')

class Artist(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String(64))
    person_name = db.Column(db.String(64))
    def __repr__(self):
        return '<Artist {}>'.format(self.body)

admin = User(username='admin', email='admin@example.com')
guest = User(username='guest', email='guest@example.com')
artist = Artist(body=102,person_name='admin')
db.session.add(admin)
db.session.add(guest)
db.session.add(artist)
db.session.commit()
User.query.all()
User.query.filter_by(username='admin').first()
Artist.query.filter_by(person_name='admin').first()
db.create_all()


@login.user_loader
def load_user(username):
    return User.query.get(username)

@app.route('/')
def home():
    return render_template("base.html")

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    return render_template("login.html", form=form)


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    return render_template("register.html", form=form)




@app.route("/main", methods=['GET','POST'])
def main():
    list = get_song_data()
    return flask.render_template(
        "index.html",
        songtitles = list["songtitles"],
        songartists = list["songartists"],
        songimgs = list["songimgs"],
        songprevs = list["songprevs"],
        songlyrics = list["songlyrics"]
    )

app.run(host='0.0.0.0', port = int(os.getenv("PORT", 8000)), debug=True)