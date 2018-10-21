from flask_wtf import FlaskForm
from flask_wtf.file import FileField
from wtforms import widgets, StringField, SelectField, SelectMultipleField, TextAreaField, SubmitField
from wtforms.fields.html5 import TimeField, DateField
from wtforms.validators import DataRequired

class MultiCheckboxField(SelectMultipleField):
    widget = widgets.ListWidget(prefix_label=False)
    option_widget = widgets.CheckboxInput()

class DogForm(FlaskForm):
    pic = FileField("Dog Picture")
    name = StringField("Dog Name", validators=[DataRequired()])
    breed = StringField("Dog Breed", validators=[DataRequired()])
    description = TextAreaField("About the Dog")
    date = DateField("Date Available")
    start_time = TimeField("Start Time")
    end_time = TimeField("End Time")
    submit = SubmitField()

