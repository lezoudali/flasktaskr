from flask import Flask, request, session, redirect, \
    url_for, render_template, flash
from functools import wraps
from forms import AddTaskForm, RegisterForm, LoginForm
from flask.ext.sqlalchemy import SQLAlchemy
from datetime import datetime


app = Flask(__name__)
app.config.from_object("config")
db = SQLAlchemy(app)

from models import Task, User


def login_required(action):
    @wraps(action)
    def wrap(*args, **kwargs):
        if "logged_in" in session:
            return action(*args, **kwargs)
        else:
            flash("You must login first")
            return redirect(url_for("login"))
    return wrap


def flash_errors(form):
    for field, errors in form.errors.items():
        for error in errors:
            flash(u"Error in the %s field - %s" % (
                getattr(form, field).label.text,
                error
            ))


@app.route('/register/', methods=["GET", "POST"])
def register():
    form = RegisterForm(request.form)
    if request.method == "POST":
        if form.validate_on_submit():
            new_user = User(
                form.name.data,
                form.email.data,
                form.password.data
            )
            db.session.add(new_user)
            db.session.commit()
            flash("Thanks for registering. Please login.")
            return redirect(url_for('login'))
    flash_errors(form)
    return render_template('register.html', form=form)


@app.route('/', methods=["GET", "POST"])
def login():
    form = LoginForm(request.form)
    if request.method == "POST":
        if form.validate_on_submit():
            u = User.query.filter_by(name=form.username.data,
                                     password=form.password.data).first()
            if u is None:
                error = "Invalid username or password."
                return render_template('login.html', form=form, error=error)
            session["logged_in"] = True
            session["user_id"] = u.id
            flash("You are logged in.")
            return redirect(url_for("tasks"))
    return render_template("login.html", form=form)


@app.route('/add/', methods=['GET', 'POST'])
@login_required
def new_task():
    form = AddTaskForm(request.form)
    if request.method == 'POST':
        if form.validate_on_submit():
            task = Task({
                "name": form.name.data,
                "due_date": form.due_date.data,
                "priority": form.priority.data,
                "posted_at": datetime.utcnow(),
                "user_id": session['user_id'],
                "status": 1
            })
            db.session.add(task)
            db.session.commit()
            flash("New entry was successfully posted.")
    return redirect(url_for('tasks'))


@app.route('/complete/<int:task_id>/',)
@login_required
def complete(task_id):
    new_id = task_id
    db.session.query(Task).filter_by(task_id=new_id).update({"status": "0"})
    db.session.commit()
    flash('The task was marked as complete')
    return redirect(url_for('tasks'))


@app.route('/delete/<int:task_id>/')
@login_required
def delete_entry(task_id):
    new_id = task_id
    db.session.query(Task).filter_by(task_id=new_id).delete()
    db.session.commit()
    flash("The task was deleted.")
    return redirect(url_for('tasks'))


@app.route("/tasks/")
@login_required
def tasks():
    form = AddTaskForm(request.form)
    open_tasks = db.session.query(Task).filter_by(status='1'). \
        order_by(Task.due_date.asc())
    closed_tasks = db.session.query(Task).filter_by(status='0'). \
        order_by(Task.due_date.asc())

    return render_template(
        "tasks.html",
        form=form,
        open_tasks=open_tasks,
        closed_tasks=closed_tasks
    )


@app.route("/logout/")
def logout():
    session.pop("logged_in", None)
    session.pop("user_id", None)
    flash("You have successfully logged out")
    return redirect(url_for('login'))
