from studentapp import mysql
from studentapp.for_valid import current_id
class students(object):
    def __init__(self, id=None, id_number=None, firstname=None, lastname=None, course=None, filter=None):
        self.id = id
        self.id_number = id_number
        self.firstname = firstname
        self.lastname = lastname
        self.course = course
        self.filter = filter



    def add(self):
        cursor = mysql.connection.cursor()
        input = (self.id_number, self.firstname, self.lastname, self.course)

        sql = "INSERT INTO students(id_number, firstname, lastname, course) VALUES (%s,%s,%s,%s)"

        cursor.execute(sql, input)
        mysql.connection.commit()


    def search(self):
        cursor = mysql.connection.cursor()
        sql = "SELECT * FROM students WHERE id_number = '{}'".format(self.id_number)

        cursor.execute(sql)

        display = cursor.fetchall()
        return display

    def update(self):
        input = (self.id_number, self.firstname, self.lastname, self.course, self.id)
        cursor = mysql.connection.cursor()
        sql = '''UPDATE students SET 
                id_number = %s,
                firstname = %s,
                lastname = %s,
                course = %s
                WHERE id_number = %s'''

        cursor.execute(sql, input)
        mysql.connection.commit()


    def validation(self):
        cursor = mysql.connection.cursor()
        sql = "SELECT id_number FROM students WHERE id_number = '{}'".format(self.id_number)

        cursor.execute(sql)
        display = cursor.fetchall()
        for item in display:
            if item[0] == self.id_number and item[0] not in current_id:
                return True

    def delete(self):
        cursor = mysql.connection.cursor()
        sql = "DELETE FROM students WHERE id_number = '{}'".format(self.id_number)

        cursor.execute(sql)
        mysql.connection.commit()




    def all(self):
        cursor = mysql.connection.cursor()

        if self.filter == 'id':
            sql = "SELECT * FROM students ORDER BY id_number ASC"

        elif self.filter == 'lname':
            sql = "SELECT * FROM students ORDER BY lastname ASC"

        elif self.filter == 'course':
            sql = "SELECT * FROM students ORDER BY course ASC"


        cursor.execute(sql)
        display = cursor.fetchall()
        return display



