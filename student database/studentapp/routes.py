from flask import render_template, redirect, request, url_for, flash, jsonify
from studentapp import app
from studentapp.for_valid import current_id
from studentapp.forms import registerForm, updateForm
import studentapp.models as models



'''@app.route('/')
def land():
    return redirect(url_for('home', fltr='id'))'''
@app.route('/', methods=['GET', 'POST'])
@app.route('/home', methods=['GET', 'POST'])
def home():
    student = models.students()
    students = student.all()
    if request.method == "POST":
        if request.form["search"]:
            id = request.form["search"]
            return redirect(url_for('searched', id_number=id))
        else:
            flash('Please Enter an I.D Number', 'danger')
            return redirect(url_for('home'))
    else:
        return render_template('index.html', students=students)




@app.route('/register', methods=['GET','POST'])
def register():
    db = models.students()
    college = db.showCollege()
    form = registerForm()
    college_arr = [('','Choose...'),]
    for item in college:
        college_arr.append((item[0],("("+item[0]+")  "+item[1])))
    form.register_college.choices = [item for item in college_arr]
    if form.validate_on_submit() and request.method=='POST':
        yearLvl = int(form.register_yearLvl.data)
        db = models.students(id_number = form.register_id.data, 
                            firstname = form.register_fname.data, 
                            lastname = form.register_lname.data,
                            yearlvl = yearLvl, 
                            gender = form.register_gender.data , 
                            course = form.register_course.data)
        db.add()
        return redirect(url_for('home'))
    return render_template('register.html', banner='Add Student',title='Register', form=form)




@app.route('/update/<string:id_number>', methods=['GET', 'POST'])
def update(id_number):
    form = updateForm()
    current_id.clear()
    courses = []
    db = models.students(id_number=id_number)
    college = db.showCollege()
    college_arr = [('','Choose...'),]
    for item in college:
        college_arr.append((item[0],("("+item[0]+")  "+item[1])))
    form.update_college.choices = [item for item in college_arr]
    students = db.search()  
    banner_data = dict
    for item in students:
        banner_data = item
        current_id.append(item[0])
        if request.method=="POST" and form.validate_on_submit():
            yearLvl = int(form.update_yearLvl.data)
            db = models.students(id_number = form.update_id.data, 
                            firstname = form.update_fname.data, 
                            lastname = form.update_lname.data,
                            yearlvl = yearLvl, 
                            gender = form.update_gender.data , 
                            course = form.update_course.data,
                            id=id_number)
            db.update()
            return redirect(url_for('searched', id_number=form.update_id.data))

        elif request.method == "GET":
            curr_course = item[3]
            if item[6] != 'SGS':
                courses.clear()
                db_dept = models.students(college=item[6],dept=item[5])
                dept = db_dept.showDept()
                course = db_dept.showCourse()
                form.update_department.choices = [(item[1]) for item in dept]
                for i in course:
                    courses.append((i[1],(i[1]+" "+i[2])))
                form.update_course.choices = [(item) for item in courses]
            else:
                courses.clear()
                db_dept = models.students(college=item[6],dept=item[5])
                dept = db_dept.showSGSdept()
                course = db_dept.showSGScourse()
                form.update_department.choices = [(item[1]) for item in dept]
                for i in course:
                    courses.append((i[1],(i[1]+" "+i[2])))
                form.update_course.choices = [(item) for item in courses]

            form.update_fname.data = item[1]
            form.update_lname.data = item[2]
            form.update_id.data = item[0]
            form.update_gender.data =  item[9]
            form.update_college.data = item[6]
            form.update_yearLvl.data = str(item[4])
            form.update_department.data = item[5]
            form.update_course.data = curr_course

    banner = "Hi, " + banner_data[1]
    title = banner_data[1] + " " + banner_data[2]
    return render_template('update.html', banner=banner, title=title, form=form)


@app.route('/dept/<string:get_college>')
def deptByCollege(get_college):
    form = registerForm()

    if get_college != 'SGS':
        db = models.students(college=get_college)
        dept = db.showDept()
        form.register_department.choices = [(item[1]) for item in dept]

        deptArray = [{
          "college_code": "Choose...", 
          "id": 0, 
          "name": "Choose...", 
          "name_value": ""
        }]
        for item in dept:
            deptObj = {}
            deptObj['id'] = item[0]
            deptObj['name_value'] = item[1]
            deptObj['name'] = item[1]
            deptObj['college_code'] = item[2]
            deptArray.append(deptObj)
        return jsonify({'department':deptArray})
    else:
        db = models.students(college=get_college)
        dept = db.showSGSdept()
        form.register_department.choices = [(item[1]) for item in dept]
        deptArray = [{
          "college_code": "Choose...", 
          "id": 0, 
          "name": "Choose...", 
          "name_value": " "
        }]
        for item in dept:
            deptObj = {}
            deptObj['id'] = item[0]
            deptObj['name_value'] = item[1]
            deptObj['name'] = item[1]
            deptObj['college_code'] = item[2]
            deptArray.append(deptObj)
        return jsonify({'department':deptArray})


@app.route('/course/<string:get_college>/<string:get_dept>')
def courseByDept(get_college, get_dept):
    form = registerForm()
    if get_college != 'SGS':
        db = models.students(dept=get_dept)
        course = db.showCourse()
        
        courseArray = [{"code": "", 
          "college_code": "", 
          "department": "Choose...", 
          "name": "Choose..."
        }
        ]
        for item in course:
            courseObj = {}
            courseObj['department'] = item[0]
            courseObj['code'] = item[1]
            courseObj['name'] = item[2]
            courseObj['college_code'] = item[4]
            courseArray.append(courseObj)
        return jsonify({'course':courseArray})
    else:
        db = models.students(dept=get_dept)
        course = db.showSGScourse()
       
        courseArray = [{"code":"", 
          "college_code": "", 
          "department": "Choose...", 
          "name": "Choose..."
        }
        ]
        for item in course:
            courseObj = {}
            courseObj['department'] = item[0]
            courseObj['code'] = item[1]
            courseObj['name'] = item[2]
            courseObj['college_code'] = item[4]
            courseArray.append(courseObj)
        return jsonify({'course':courseArray})

   
 
       


@app.route('/searched/<string:id_number>', methods=['GET'])
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




@app.route('/colleges')
def colleges():
    return render_template('colleges.html', banner='Colleges')


@app.route('/<string:college>departments')
def department(college):
    if college != 'SGS':
        db = models.students(college=college)
        dept = db.showDept()
        return redirect (url_for('courses', college=college, dept=dept[0][1]))
    else:
        db = models.students()
        dept = db.showSGSdept()
        return redirect (url_for('courses', college=college, dept=dept[0][1]))

@app.route('/courses/<string:college>/<string:dept>')
def courses(college, dept):
    if college != 'SGS':
        course = models.students(dept=dept)
        courses = course.showCourse()
        department = models.students(college=college)
        depts = department.showDept()
        banner = "("+college+")"+" "+courses[0][3]
        return render_template('courses.html', course = courses, depts=depts, banner=banner, clg=college)
    else:
        course = models.students(dept=dept)
        courses = course.showSGScourse()
        department = models.students(college=college)
        depts = department.showSGSdept()
        banner = "("+college+")"+" "+courses[0][3]
        return render_template('courses.html', course = courses, depts=depts, banner=banner, clg=college)

