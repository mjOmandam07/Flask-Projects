from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField
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
    register_gender = SelectField('Gender', choices=[('Male'),('Female')], validate_choice = True)
    register_yearLvl = SelectField('Year Level', choices=[1,2,3,4,5], validate_choice = True)
    register_college = SelectField('College', choices=[], validate_choice = True)
    register_department = SelectField('Department', choices=[], validate_choice = True)
    register_course = SelectField('Course', choices=[], validate_choice = True)
    register_submit = SubmitField('Add New Student')


class updateForm(FlaskForm):
    update_id = StringField('I.D Number', validators=[DataRequired(), validate_id, Regexp(regex=r"^[0-9]{4}-[0-9]{4}$", message="Please input a valid I.D Number")])
    update_fname = StringField('First Name', validators=[DataRequired()])
    update_lname = StringField('Last Name', validators=[DataRequired()])
    update_gender = SelectField('Gender', choices=[('Male'),('Female')], validate_choice = True)
    update_yearLvl = SelectField('Year Level', choices=[1,2,3,4,5])
    update_college = SelectField('College', choices=[], validate_choice = True)
    update_department = SelectField('Department', choices=[], validate_choice = True)
    update_course = SelectField('Course', choices=[], validate_choice = True)
    update_submit = SubmitField('Update')

class filterForm(FlaskForm):
    filter_college = SelectField('College', choices=[], validate_choice = True)
    filter_department = SelectField('Department', choices=[], validate_choice = True)
    filter_course = SelectField('Course', choices=[], validate_choice = True)
    filter_arrange = SelectField('Arrange by', choices=['ID', 'Last Name', 'Course'], validate_choice = True)
    filter_submit = SubmitField('Submit Filter')

