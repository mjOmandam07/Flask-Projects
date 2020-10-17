from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField
from wtforms.validators import DataRequired, ValidationError, Regexp
import studentapp.models as models
import re

def validate_id(FlaskForm, field):
    student = models.students(id_number=field.data)
    if student.validation():
        raise ValidationError('I.D Number already exists')




class registerForm(FlaskForm):
    register_id = StringField('I.D Number', validators=[DataRequired(), validate_id, Regexp(regex=r"^[0-9]{4}-[0-9]{4}$", message="Please input a valid I.D Number")])
    register_fname = StringField('First Name', validators=[DataRequired()])
    register_lname = StringField('Last Name', validators=[DataRequired()])
    register_course = StringField('Course', validators=[DataRequired(), Regexp(regex=r"^B[A-Z]+$", message="Course should in abbreviation form (e.g., BSCS, BSCET)")])
    register_submit = SubmitField('Add New Student')


class updateForm(FlaskForm):
    update_id = StringField('I.D Number', validators=[DataRequired(), validate_id, Regexp(regex=r"^[0-9]{4}-[0-9]{4}$", message="Please input a valid I.D Number")])
    update_fname = StringField('First Name', validators=[DataRequired()])
    update_lname = StringField('Last Name', validators=[DataRequired()])
    update_course = StringField('Course', validators=[DataRequired()])
    update_submit = SubmitField('Update')

