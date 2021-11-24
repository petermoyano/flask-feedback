from flask import Flask, render_template, redirect, flash, session, request
from flask_debugtoolbar import DebugToolbarExtension
from flask_sqlalchemy import SQLAlchemy
from models import db, connect_db, User
from forms import FeedbackForm, LoginForm
from sqlalchemy.exc import IntegrityError



app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///feedback_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = "secret"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

app.debug = DebugToolbarExtension
app.debug = True
toolbar = DebugToolbarExtension(app)

connect_db(app)

@app.route("/secret")
def home():
    return "This is the secret page!"

@app.route("/register", methods=["GET", "POST"])
def register():
    """Show a form that when submitted will register/create a user. 
    This form should accept a username, password, email, first_name, and last_name.
    """
    form = FeedbackForm()
    if form.validate_on_submit():
        username=form.username.data
        password=form.password.data
        email=form.email.data
        first_name=form.first_name.data
        last_name=form.last_name.data
        
        current_user = User.register(username=username, password=password, email=email, first_name=first_name, last_name=last_name)
        db.session.add(current_user)

        try:
            db.session.commit()
        except IntegrityError:
            form.username.errors.append("Registration failed")
            return render_template("/register", form=form)

        session["username"] = username
        return redirect("/secret")
    else:
        return render_template("register.html", form=form)


@app.route("/login", methods=['GET', 'POST'])
def login():
    """Handle login requests and submissions"""
    form=LoginForm()
    if form.validate_on_submit():
        username=form.username.data
        password=form.password.data
        current_user = User.authenticate(username, password)

        if current_user:
            session["username"] = username
            return redirect("/secret")
        else:
            form.username.errors = ["Incorrect credentials"]
            return render_template("login.html", form=form)
    else:
        return render_template("login.html", form=form)


