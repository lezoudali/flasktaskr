from views import db
from datetime import datetime


class Task(db.Model):

    __tablename__ = 'tasks'

    task_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    due_date = db.Column(db.Date, nullable=False)
    priority = db.Column(db.Integer, nullable=False)
    status = db.Column(db.Integer)
    posted_at = db.Column(db.Date, default=datetime.utcnow())
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))

    def __init__(self, attributes):

        self.name = attributes["name"]
        self.due_date = attributes["due_date"]
        self.priority = attributes["priority"]
        self.status = attributes["status"]
        self.posted_at = attributes["posted_at"]
        self.user_id = attributes["user_id"]

    def __repr__(self):
        return "<name %r>" % (self.name)


class User(db.Model):

    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True, nullable=False)
    email = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)
    tasks = db.relationship('Task', backref='poster')

    def __init__(self, name=None, email=None, password=None):
        self.name = name
        self.email = email
        self.password = password

    def __repr__(self):
        return '<User %r>' % (self.name)
