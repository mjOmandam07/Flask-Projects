from flask import render_template, redirect, request, url_for, flash
from studentapp import app
from studentapp.for_valid import current_id
from studentapp.forms import registerForm, updateForm
import studentapp.models as models



@app.route('/')
def land():
    return redirect(url_for('home', fltr='id'))

@app.route('/home/filterBY<string:fltr>', methods=['GET', 'POST'])
def home(fltr):
    student = models.students(filter=fltr)
    students = student.all()
    if request.method == "POST":
        if request.form["search"]:
            id = request.form["search"]
            return redirect(url_for('searched', id_number=id))
        else:
            flash('Please Enter an I.D Number', 'danger')
            return redirect(url_for('home'), fltr='id')
    else:
        return render_template('index.html', students=students)




@app.route('/register', methods=['GET','POST'])
def register():
    form = registerForm()
    if request.method == "POST" and form.validate_on_submit():
        student = models.students(id_number=form.register_id.data, firstname=form.register_fname.data, lastname=form.register_lname.data, course=form.register_course.data)
        student.add()
        return redirect(url_for('searched', id_number=form.register_id.data))
    else:
        return render_template('register.html', banner='Add Student',title='Register', form=form)




@app.route('/update/<string:id_number>', methods=['GET', 'POST'])
def update(id_number):
    current_id.clear()
    student = models.students(id_number=id_number)
    students = student.search()
    form = updateForm()
    banner_data = dict
    for item in students:
        banner_data = item
        current_id.append(item[0])
        if request.method=="POST" and form.validate_on_submit():
            student = models.students(id_number=form.update_id.data, firstname=form.update_fname.data, lastname=form.update_lname.data, course=form.update_course.data, id=id_number)
            student.update()
            return redirect(url_for('searched', id_number=form.update_id.data))
        elif request.method == "GET":
            form.update_id.data = item[0]
            form.update_fname.data = item[1]
            form.update_lname.data = item[2]
            form.update_course.data = item[3]


    banner = "Hi, " + banner_data[1]
    title = banner_data[1] + " " + banner_data[2]
    return render_template('update.html', banner=banner, title=title, form=form)



@app.route('/searched/<string:id_number>', methods=['GET', 'POST'])
def searched(id_number):
    if request.method == "POST":
        if request.form["search"]:
            id = request.form["search"]
            return redirect(url_for('searched', id_number=id))
    student = models.students(id_number=id_number)
    students = student.search()
    try:
        return render_template('searched.html', banner = "Searched Student", title='Search', students=students)
    except Exception:
        flash('Sorry student not found', 'danger')
        return redirect(url_for('home', fltr='id'))

            




@app.route('/delete/<string:id_number>', methods=['GET'])
def delete(id_number):
    students = models.students(id_number=id_number)
    students = students.delete()
    flash('Student data has been deleted', 'success')
    return redirect(url_for('home', fltr='id'))
