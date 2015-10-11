from flask_wtf import Form
from wtforms import TextField, DateField, IntegerField, \
    SelectField, PasswordField
from wtforms.validators import DataRequired, Length, EqualTo


class AddTaskForm(Form):
    task_id = IntegerField()
    name = TextField('Task Name', validators=[DataRequired()])
    due_date = DateField('Date Due (mm/dd/yyyy)',
                         validators=[DataRequired()],
                         format='%m/%d/%Y')
    priority = SelectField(
        'Priority',
        validators=[DataRequired()],
        choices=[(str(i), str(i)) for i in range(1, 11)]
    )
    status = IntegerField('Status')


class RegisterForm(Form):
    id = IntegerField()
    name = TextField('Username', validators=[DataRequired(),
                                             Length(min=5, max=25)])
    email = TextField('Email', validators=[DataRequired(),
                                           Length(min=6, max=40)])
    password = PasswordField('Password', validators=[DataRequired(),
                                                     Length(min=5, max=40)])
    confirm = PasswordField(
        'Confirm Password',
        validators=[DataRequired(),
                    EqualTo('password', message='Passwords must match')]
    )


class LoginForm(Form):
    username = TextField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
