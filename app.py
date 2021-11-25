from flask import Flask, render_template, redirect, flash, session, request
from flask_debugtoolbar import DebugToolbarExtension
from flask_sqlalchemy import SQLAlchemy
from models import Feedback, db, connect_db, User
from forms import FeedbackForm, LoginForm
from sqlalchemy.exc import IntegrityError
from werkzeug.exceptions import Unauthorized


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

@app.route("/")
def home():
    """Home page"""
    if session["username"]:
        current_user = session["username"]
        flash("redirected to your user profile page")
        return redirect(f"/users/{current_user}")
    else:
        return render_template("base.html")

@app.route("/users/<username>")
def user_info(username):
    """Displays information about the current user"""
    current_user = session["username"]
    if current_user == username:
        current_user = User.query.get_or_404(username)
        return render_template("users.html", current_user=current_user)
    else:
        flash("Please check your credentials and permissions, redirected to your user profile")
        return redirect(f"/users/{current_user}")

@app.route("/register", methods=["GET", "POST"])
def register():
    """Show a form that when submitted will register/create a user"""
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
        return redirect(f"/users/{username}")
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
            return redirect(f"/users/{username}")
        else:
            form.username.errors = ["Incorrect credentials"]
            return render_template("login.html", form=form)
    else:
        return render_template("login.html", form=form)

@app.route("/logout", methods=["POST"])
def log_out():
    """Remove current user from session"""
    session.pop("username")
    return redirect("/login")



@app.route("/users/<username>/delete", methods=["POST"])
def delete_user(username):
    """Delete a user if it coincides with the one in the session"""
    if "username" not in session or username != session['username']:
        raise Unauthorized()

    user = User.query.get(username)
    db.session.delete(user)
    db.session.commit()
    session.pop("username")

    return redirect("/login")

@app.route("/users/<username>/feedback/add", methods=["POST", "GET"])
def feedback(username):
    """ Display a form to add feedback"""
    form=FeedbackForm()
    if form.validate_on_submit():
        title=form.title.data
        content=form.content.data
        if session["username"] == username:
            fb = Feedback(title=title, content=content, username=username)
            db.session.add(fb)
            db.session.commit()
            return redirect(f"/users/{username}")
        else:
            form.username.errors = ["Cannot create a feedback using another username"]
            return render_template(f"/users/{username}")
    else:
        return render_template("feedback.html", form=form)

@app.route("/feedback/<id>/update", methods=["GET", "POST"])
def edit_feedback(id):
    """Display a form to edit feedback """
    fb = Feedback.query.get_or_404(id)
    current_user = session["username"]
    form=FeedbackForm(obj=fb)
    if fb.username == current_user:
        if  form.validate_on_submit():
            fb.title = form.title.data
            fb.content = form.content.data
            db.session.commit()
            current_user = User.query.get(session["username"])
            flash("Your feedback has been updated!")
            return redirect(f"/users/{current_user}")
        else:
            return render_template("edit_feedback.html", form=form, current_user=current_user)
    else:
        flash("Cannot edit other users feedback")
        return redirect(f"/users/{current_user}")

@app.route("/feedback/id/delete", methods=["POST"])
def delete_feedback(id):
    """Delete a certain feedback"""
    fb = Feedback.query.get_or_404(id)
    current_user = session["username"]
    if fb.username == current_user:
        db.session.delete(id)
        db.session.commit()
        flash("Feedback deleted!")
        return redirect(f"/users/{current_user}")
    else:
        flash("You cannot delete other people's feedback.")
        return redirect(f"/users/{current_user}")



