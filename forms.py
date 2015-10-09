from flask_wtf import Form
from wtforms import TextField, DateField, IntegerField, \
    SelectField
from wtforms.validators import DataRequired


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
