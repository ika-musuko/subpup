from flask_wtf import FlaskForm
from flask_wtf.file import FileField
from wtforms import widgets, StringField, SelectField, SelectMultipleField, TextAreaField, SubmitField
from wtforms.fields.html5 import DateTimeLocalField, TimeField
from wtforms.validators import DataRequired

class MultiCheckboxField(SelectMultipleField):
    widget = widgets.ListWidget(prefix_label=False)
    option_widget = widgets.CheckboxInput()

class DogForm(FlaskForm):
    pic = FileField("Dog Picture")
    name = StringField("Dog Name", validators=[DataRequired()])
    breed = StringField("Dog Breed", validators=[DataRequired()])
    description = TextAreaField("About the Dog")
    availability_type = SelectField("Availability Type", choices=[("O", "One Time"), ("R", "Recurring")], validators=[DataRequired()])
    submit = SubmitField()

class OneTimeAvailabilityForm(FlaskForm):
    date_time = DateTimeLocalField("Date and Time",  format='%Y-%m-%dT%H:%M')

class RecurringAvailabilityForm(FlaskForm):
    day_of_week = MultiCheckboxField("Days of Week", choices=["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"])
    time = TimeField("Time")

