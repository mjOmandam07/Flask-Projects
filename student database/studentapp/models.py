from studentapp import mysql
from studentapp.for_valid import current_id
class students(object):
    def __init__(self, id=None, id_number=None,
                        firstname=None, lastname=None, 
                        yearlvl=None, gender=None, 
                        course=None, filter=None, 
                        college=None, dept=None
                                                ):

        self.id = id

        self.id_number = id_number
        self.firstname = firstname
        self.lastname = lastname
        self.yearlvl = yearlvl
        self.gender = gender
        self.course = course

        self.filter = filter
        self.college = college
        self.dept = dept



    def add(self):
        cursor = mysql.connection.cursor()

        sql = """INSERT INTO student(id, firstName, lastName, yearLevel, gender, course)
             VALUES ('%s','%s','%s',%d,'%s','%s')""" % (self.id_number, 
                                                        self.firstname, 
                                                        self.lastname, 
                                                        self.yearlvl, 
                                                        self.gender, 
                                                        self.course)

        cursor.execute(sql)
        mysql.connection.commit()


    def search(self):
        cursor = mysql.connection.cursor()
        sql = """SELECT s.id, s.firstName, s.lastName, c.code, s.yearLevel, d.name, clg.code, clg.name, c.name, s.gender FROM
                    (((student AS s LEFT JOIN course AS c ON s.course = c.code)
                    LEFT JOIN department as d ON c.deptNo = d.id)
                    LEFT JOIN college AS clg ON c.college_code = clg.code ) WHERE s.id = '{}'""".format(self.id_number)

        cursor.execute(sql)

        display = cursor.fetchall()
        return display

    def update(self):
        cursor = mysql.connection.cursor()
        sql = """UPDATE student SET id = '%s', firstName = '%s', lastName = '%s', yearLevel = %d, gender = '%s', course = '%s'
                WHERE id = '%s'"""  % (self.id_number, 
                                        self.firstname, 
                                        self.lastname, 
                                        self.yearlvl, 
                                        self.gender, 
                                        self.course,
                                        self.id)

        cursor.execute(sql)
        mysql.connection.commit()


    def validation(self):
        cursor = mysql.connection.cursor()
        sql = "SELECT id FROM student WHERE id = '{}'".format(self.id_number)

        cursor.execute(sql)
        display = cursor.fetchall()
        for item in display:
            if item[0] == self.id_number and item[0] not in current_id:
                return True

    def delete(self):
        cursor = mysql.connection.cursor()
        sql = "DELETE FROM student WHERE id = '{}'".format(self.id_number)

        cursor.execute(sql)
        mysql.connection.commit()



    @classmethod
    def all(cls):
        cursor = mysql.connection.cursor()

        sql = """SELECT s.id, s.firstName, s.lastName, c.code, s.yearLevel, d.name, clg.code, clg.name FROM
                    (((student AS s LEFT JOIN course AS c ON s.course = c.code)
                    LEFT JOIN department as d ON c.deptNo = d.id)
                    LEFT JOIN college AS clg ON c.college_code = clg.code)"""


        cursor.execute(sql)
        display = cursor.fetchall()
        return display

    @classmethod
    def showCollege(cls):
        cursor = mysql.connection.cursor()

        sql = "SELECT * FROM college"

        cursor.execute(sql)
        display = cursor.fetchall()
        return display


    def showDept(self):
        cursor = mysql.connection.cursor()

        sql = """SELECT DISTINCT c.deptNo, d.name, d.college_code FROM course as c 
                JOIN department AS d  
                ON d.id = c.deptNo AND c.college_code != 'SGS' AND d.college_code = '{}'""".format(self.college)

        cursor.execute(sql)
        display = cursor.fetchall()
        return display

    def showCourse(self):
        cursor = mysql.connection.cursor()
        sql = """SELECT d.name, c.code,c.name, clg.name, clg.code FROM 
                ((department AS d JOIN course as c ON d.id = c.deptNo AND d.name = '{}' )
                JOIN college as clg ON c.college_code = clg.code AND clg.code != 'SGS')""".format(self.dept)

        cursor.execute(sql)
        display = cursor.fetchall()
        return display



    @classmethod
    def showSGSdept(cls):
        cursor = mysql.connection.cursor()

        sql ="""SELECT DISTINCT d.id, d.name, c.college_code
            FROM course as c, department as d
            WHERE c.deptNo = d.id AND c.college_code = 'SGS'"""

        cursor.execute(sql)
        display = cursor.fetchall()
        return display

    def showSGScourse(self):
        cursor = mysql.connection.cursor()

        sql ="""SELECT d.name, c.code, c.name, clg.name, clg.code FROM ((course as c JOIN department as d 
        ON c.deptNo = d.id AND d.name = '{}')
        JOIN college as clg ON c.college_code = clg.code AND c.college_code = 'SGS')""".format(self.dept)

        cursor.execute(sql)
        display = cursor.fetchall()
        return display


