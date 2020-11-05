from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField
from wtforms.validators import DataRequired, ValidationError, Regexp
import studentapp.models as models
import re

def validate_id(FlaskForm, field):
    student = models.students(id_number=field.data)
    if student.validation():
        raise ValidationError('I.D Number already exists')
def validate_selectField(FlaskForm, field):
    if field.data == 'Choose...' or field.data == '':
        raise ValidationError('Please Select one of the options provided')




class myCustomSelectField(SelectField):
    def pre_validate(self, form):
        pass


class registerForm(FlaskForm):
    register_fname = StringField('First Name', validators=[DataRequired()])
    register_lname = StringField('Last Name', validators=[DataRequired()])
    register_id = StringField('I.D Number', validators=[DataRequired(), validate_id, Regexp(regex=r"^[0-9]{4}-[0-9]{4}$", message="Please input a valid I.D Number")])


    register_gender = myCustomSelectField('Gender', choices=[('','Choose...'),('Male','Male'),('Female','Female')], validators=[DataRequired(), validate_selectField])
    register_yearLvl = myCustomSelectField('Year Level', choices=[('','Choose...'),(1,1),(2,2),(3,3),(4,4),(5,5)], validators=[DataRequired(), validate_selectField])
    register_college = myCustomSelectField('College', choices=[], validators=[DataRequired(), validate_selectField])
    register_department = myCustomSelectField('Department', choices=[], validators=[DataRequired(), validate_selectField])
    register_course = myCustomSelectField('Course', choices=[], validators=[DataRequired(), validate_selectField])

    register_submit = SubmitField('Add New Student')




class updateForm(FlaskForm):
    update_fname = StringField('First Name', validators=[DataRequired()])
    update_lname = StringField('Last Name', validators=[DataRequired()])
    update_id = StringField('I.D Number', validators=[DataRequired(), validate_id, Regexp(regex=r"^[0-9]{4}-[0-9]{4}$", message="Please input a valid I.D Number")])


    update_gender = myCustomSelectField('Gender', choices=[('','Choose...'),('Male','Male'),('Female','Female')], validators=[DataRequired(), validate_selectField])
    update_yearLvl = myCustomSelectField('Year Level', choices=[('','Choose...'),(1,1),(2,2),(3,3),(4,4),(5,5)], validators=[DataRequired(), validate_selectField])
    update_college = myCustomSelectField('College', choices=[], validators=[DataRequired(), validate_selectField])
    update_department = myCustomSelectField('Department', choices=[], validators=[DataRequired(), validate_selectField])
    update_course = myCustomSelectField('Course', choices=[], validators=[DataRequired(), validate_selectField])

    update_submit = SubmitField('Update')

class filterForm(FlaskForm):
    filter_college = SelectField('College', choices=[], validators=[DataRequired()])
    filter_department = SelectField('Department', choices=[], validators=[DataRequired()])
    filter_course = SelectField('Course', choices=[], validators=[DataRequired()])
    filter_arrange = SelectField('Arrange by', choices=['ID', 'Last Name', 'Course'], validators=[DataRequired()])
    filter_submit = SubmitField('Submit Filter')



