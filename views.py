from flask import Flask, request, session, redirect, \
    url_for, render_template, flash, g
import sqlite3
from functools import wraps
from forms import AddTaskForm


app = Flask(__name__)
app.config.from_object("config")


def connect_db():
    return sqlite3.connect(app.config["DATABASE"])


def login_required(action):
    @wraps(action)
    def wrap(*args, **kwargs):
        if "logged_in" in session:
            return action(*args, **kwargs)
        else:
            flash("You must login first")
            return redirect(url_for("login"))
    return wrap


@app.route('/', methods=["GET", "POST"])
def login():
    if request.method == "POST":
        if request.form["username"] != app.config["USERNAME"] or \
                request.form['password'] != app.config["PASSWORD"]:
            error = "Wrong Credentials. Please try again."
            return render_template("login.html", error=error)
        else:
            session["logged_in"] = True
            return redirect(url_for('tasks'))
    else:
        return render_template("login.html")


@app.route('/add/', methods=['POST'])
@login_required
def new_task():
    name = request.form['name']
    due_date = request.form['due_date']
    priority = request.form['priority']
    if not name or not due_date or not priority:
        flash("All fields are required. Please try again.")
        return redirect(url_for('tasks'))
    else:
        g.db = connect_db()
        g.db.execute(
            'INSERT INTO tasks (name, due_date, priority, status) \
             VALUES (?, ?, ?, 1)',
            [name, due_date, priority])
        g.db.commit()
        g.db.close()
        flash("New entry was successfully posted.")
        return redirect(url_for('tasks'))


@app.route('/complete/<int:task_id>/',)
@login_required
def complete(task_id):
    g.db = connect_db()
    g.db.execute('UPDATE tasks SET status=0 WHERE task_id = ' + str(task_id))
    g.db.commit()
    g.db.close()
    flash('The task was marked as complete')
    return redirect(url_for('tasks'))


@app.route('/delete/<int:task_id>/')
@login_required
def delete_entry(task_id):
    g.db = connect_db()
    g.db.execute('DELETE FROM tasks WHERE task_id = ' + str(task_id))
    g.db.commit()
    g.db.close()
    flash("The task was deleted.")
    return redirect(url_for('tasks'))


@app.route("/tasks/")
@login_required
def tasks():
    g.db = connect_db()
    curr = g.db.execute('SELECT name, due_date, priority, \
                         task_id FROM tasks WHERE status=1')
    open_tasks = [
        dict(name=row[0], due_date=row[1], priority=row[2],
             task_id=row[3]) for row in curr.fetchall()
    ]

    curr = g.db.execute('SELECT name, due_date, priority, \
                         task_id FROM tasks WHERE status=0')
    closed_tasks = [
        dict(name=row[0], due_date=row[1], priority=row[2],
             task_id=row[3]) for row in curr.fetchall()
    ]

    g.db.close()
    return render_template(
        "tasks.html",
        form=AddTaskForm(request.form),
        open_tasks=open_tasks,
        closed_tasks=closed_tasks
    )


@app.route("/logout/")
def logout():
    session.pop("logged_in", None)
    flash("You have successfully logged out")
    return redirect(url_for('login'))
