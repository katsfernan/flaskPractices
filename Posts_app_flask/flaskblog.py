from flask import Flask, redirect, render_template, url_for, flash, request
from flask_sqlalchemy import SQLAlchemy
from forms import RegistrationForm, LoginForm
from datetime import datetime

app = Flask(__name__)

app.config['SECRET_KEY'] = '997e76e5d0b841f16a459b3ec98a6365'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'

db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_field = db.Column(db.String(20), nullable=False, default='default.jpg')
    password = db.Column(db.String(60), nullable=False)
    posts = db.relationship('Post', backref='author', lazy=True)

    def __repr__(self):
        return f"User ('{self.username}','{self.email}','{self.image_file}')" 

class Post(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(100), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)


    def __repr__(self):
        return f"Post ('{self.title}','{self.date_posted}')" 

posts = [
    {
        'title': 'Hello everybody',
        'author': 'Fernando Martinez',
        'date_posted' : '2022-06-07',
        'content': 'Blog app built in python flask'
    },
        {
        'title': 'Keep goin',
        'author': 'Stephanie Duarte',
        'date_posted' : '2022-06-07',
        'content': 'Blog app built in python django'
    }
]

@app.route("/")
def home():
    return render_template("home.html", posts = posts)

@app.route("/about/")
def about():
    return render_template("about.html")

@app.route("/register/", methods=['GET','POST'])
def register():
    form = RegistrationForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            print('ok')
            flash(f'Account created for {form.username.data}','success')
            return redirect(url_for('home'))
        else:
            flash(f'Error creating account!', 'error')
    return render_template("register.html", title='Register', form=form)

@app.route("/login/")
def login():
    form = LoginForm()
    return render_template("login.html", title='Login', form=form)

if __name__ == '__main__':
    app.run(debug=True)
