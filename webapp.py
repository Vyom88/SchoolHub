from flask import Flask, render_template, request, Response, redirect, url_for
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import copy

app = Flask(__name__)
Bootstrap(app)

class MetaSchool(type): 
    def __iter__(cls): 
        return iter(cls._objs)

class School(metaclass=MetaSchool):
    _objs = []
    def __init__(self, name):
        School._objs.append(self)
        self.school = name
        self.teachers = []
        self.students = []
        self.clubs = []
    
    def addTeacher(self, teacher):
        self.teachers.append(teacher)

    def addStudent(self, student):
        self.students.append(student)

    def addClub(self, club):
        self.clubs.append(club)
    


all_schools = [
    {
        "name: " : "A. Y. Jackson Secondary School", 
    }, 
    {
        "name: " : "Agincourt Collegiate Institute", 
    }, 
    {   
       "name: " : "Albert Campbell Collegiate Institute", 
    }, 
    {
        "name: " : "Birchmount Park Collegiate Institute"
    }, 
    {   
       "name: " : "Bloor Collegiate Institute", 
    },
    {   
       "name: " : "C. W. Jefferys Collegiate Institute", 
    },       
    {   
       "name: " : "Cedarbrae Collegiate Institute", 
    },
    {   
       "name: " : "Central Technical School", 
    },
    {   
       "name: " : "Central Toronto Academy", 
    },
    {   
       "name: " : "Danforth Collegiate and Technical Institute", 
    },
    {   
       "name: " : "David and Mary Thomson Collegiate Institute", 
    },
    {   
       "name: " : "Don Mills Collegiate Institute", 
    },
    {   
       "name: " : "Downsview Secondary School", 
    },
    {   
       "name: " : "Dr Norman Bethune Collegiate Institute", 
    },
    {   
       "name: " : "Earl Haig Secondary School", 
    },
    {   
       "name: " : "East York Collegiate Institute", 
    },
    {   
       "name: " : "Emery Collegiate Institute", 
    },
    {   
       "name: " : "Etobicoke Collegiate Institute", 
    },
    {   
       "name: " : "Etobicoke School of the Arts", 
    },
    {   
       "name: " : "Forest Hill Collegiate Institute", 
    },
    {   
       "name: " : "George Harvey Collegiate Institute", 
    },
    {   
       "name: " : "George S. Henry Academy", 
    },
    {   
       "name: " : "Georges Vanier Secondary School", 
    },
    {   
       "name: " : "Harbord Collegiate Institute", 
    },
    {   
       "name: " : "Humberside Collegiate Institute", 
    },
    {   
       "name: " : "Jarvis Collegiate Institute", 
    },
    {   
       "name: " : "SATEC @ WA Porter", 
    },
]

all_districts = [

    {
        
    }
]

with open("text/boards.txt", "r") as a_file:
  for line in a_file:
    stripped_line = line.strip()
    dictionary = {"name: " : stripped_line}
    all_districts.append(dictionary)

class MetaTeach(type): 
    def __iter__(cls): 
        return iter(cls.teachers)

teachers = []
class Teacher(metaclass=MetaTeach):
    global teachers
    def __init__(self, email, password, school):
        self.email = email
        self.password = password
        self.clubs = []
        self.wasteEmail = ""
        teachers.append(self)
        for _school in School:
            if _school.school == school:
                self.school = _school
                _school.addTeacher(self)
                break
    
    def addWasteEmail(self, email):
        self.wasteEmail = email

    def makeClub(self, name, description):
        Club(name, description, self, self.school)
        for _club in clubs:
            if _club.name == name:
                self.clubs.append(_club)
                break
    
    def joinClub(self, club):
        club.addTeacher(self)
        self.clubs.append(club)


class MetaClub(type):
    def __iter__(cls): 
        return iter(cls.clubs)

clubs = []
class Club():
    global clubs

    def __init__(self, name, description, teacher, school):
        self.teachers = []
        self.announcments = []
        self.events = []
        self.name = name
        self.description = description
        self.memebers = []
        self.presidents = []
        self.teachers.append(teacher)
        clubs.append(self)
        school.addClub(self)

    def addMember(self, student):
        self.memebers.append(student)
    
    def changeMemberToPresident(self, student):
        self.memebers.remove(student)
        self.presidents.append(student)
    
    def addTeacher(self, teacher):
        self.teachers.append(teacher)
    
    def addAnnouncment(self, title, description):
        x = datetime.now()
        str_x = str(x)[:16] # THIS IS THE STRING FORMAT OF THE TIME THAT DOES NOT INCLUDE THE SECONDS
        self.announcments.append([title, description, str_x])

    def addEvent(self, title, description, time):
        self.events.append([title, description, time])


class MetaStud(type): 
    def __iter__(cls): 
        return iter(cls.students)


class Student(metaclass=MetaStud):
    students = []
    def __init__(self, email, password, school):
        self.email = email
        self.password = password
        self.clubs = []
        self.wasteEmail = ""
        self.students.append(self)
        for _school in School:
            if _school.school == school:
                self.school = _school
                _school.addStudent(self)
                break
    
    def addWasteEmail(self, email):
        self.wasteEmail = email
    
    def joinClub(self, club):
        club.addMember(self)
        self.clubs.append(club)

        

mainAnnouncments =[]
mainEvents = []

app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///data.db" 
db = SQLAlchemy(app)


class Data(db.Model): 
    student_number = db.Column(db.Integer, primary_key=True)
    password =  db.Column(db.String(200), nullable=False)
    school = db.Column(db.String(200), nullable=False)
    board = db.Column(db.Text(400), nullable=False)

    def __repr__(self): 
        str1 = "Student number: " + str(self.student_number) + "\nPassword: " + str(self.password)
        str2 = "\nSchool: " + str(self.school) + "\nBoard: " + str(self.board)
        return str1 + str2


@app.route('/', methods=['GET', 'POST']) 
def signIn():
    error = ""
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]
        invalid = False
        waste = email.find('@')
        if waste == -1:
            invalid = True
            error = "* Please enter a valid email"
        else:
            teacher = False
            request.form.get("district")
            school = request.form.get("school")
            try:
                waste2 = None
                for _school in School:
                    if _school.name == school:
                        waste2 = _school
                        break
                if waste2 == None:
                    wa = 10/0
            except:
                School(school)

            if email[waste+1] == "s":
                teacher = False
                stu = None
                for _stud in Student:
                    if _stud.email == email:
                        stu = _stud
                        break
                
                if stu == None:
                    Student(email, password, school)
            elif email[waste+1] == "t":
                teacher = True
                tea = None
                for _teach in teachers:
                    if _teach.email == email:
                        tea = _teach
                        break
                
                if tea == None:
                    Teacher(email, password, school)
            else:
                invalid = True
                error = "* Please enter a valid email"
        if not invalid:
            if teacher == True:
                for _teach in teachers:
                    if _teach.email == email:
                        tea = _teach
                        break
                
                if email.find('.') == -1:
                    url =  email[:((email.find('@'))-1)]
                    if url[-1] == '.' or url[-1] == '@':
                        url = url[:-2]

                else:
                    url = email[:(min(email.find('.'), email.find('@'))-2)]
                    if url[-1] == '.' or url[-1] == '@': 
                        url = url[:-2]
                
                tea.addWasteEmail(url)
                return redirect(url_for('.teacherHome', email=url))
            else:
                for _stud in Student:
                    if _stud.email == email:
                        stu = _stud
                        break
                
                if email.find('.') == -1:
                    url =  email[:((email.find('@'))-1)]
                    if url[-1] == '.' or url[-1] == '@':
                        url = url[:-2]

                else:
                    url = email[:(min(email.find('.'), email.find('@'))-2)]
                    if url[-1] == '.' or url[-1] == '@':
                        url = url[:-2]
                
                stu.addWasteEmail(url)
                return redirect(url_for('.studentHome', email=url))
                
    return render_template("start.html", error=error, schools=all_schools, districts=all_districts)


@app.route('/teacher/home/<email>', methods=['POST', 'GET']) 
def teacherHome(email):
    waste = len(email)
    for _teach in teachers:
        if _teach.wasteEmail == email:
            teacher = _teach
            break

    if request.method == "POST":
        if request.form['button'] == "announcement":
            return redirect(url_for(".makeMainAnnouncment", email=email))
        
        if request.form['button'] == "club":
            return redirect(url_for(".teacherClubs", email=email))
        
        if request.form['button'] == "event":
            return redirect(url_for(".makeMainEvent", email=email))

    waste = teacher.clubs
    if len(waste) > 3:
        waste = waste[:3]
    return render_template("TeacherHome.html", school = teacher.school.school, announcments = mainAnnouncments, events=mainEvents, clubs=waste)

@app.route('/student/home/<email>', methods=['POST', 'GET']) 
def studentHome(email):
    waste = len(email)
    for _stud in Student:
        if _stud.wasteEmail == email:
            student = _stud
            break
    
    if request.method == "POST":
        return redirect(url_for(".studentAllClubs", email=email))

    waste = student.clubs
    if len(waste) > 3:
        waste = waste[:3]

    return render_template("StudentHome.html", school=student.school.school, announcments = mainAnnouncments, events=mainEvents, clubs=waste)

def wasteee(wa, x):
    for i in range(len(wa)):
        if wa[i].name == x.name:
            del wa[i]
            break

@app.route('/studentAllClubs/<email>', methods=['POST', 'GET']) 
def studentAllClubs(email):
    global clubs
    waste = len(email)
    for _stud in Student.students:
        if _stud.wasteEmail == email:
            student = _stud
            break
    
    wa = copy.deepcopy(clubs)
    try:
        for x in student.clubs:
            try:
                wasteee(wa, x)
            except:
                pass
    except:
        pass

    if request.method == "POST":
        for x in student.clubs:
            if request.form['go'] == x.name+'g':
                return redirect(url_for(".PacClub_Student_view", clubname = x.name, email=email))
            
        for x in wa:
            if request.form['go'] == x.name+'j':
                student.joinClub(x)
                return redirect(url_for(".PacClub_Student_view", clubname = x.name, email=email))
        
        if request.form['go'] == "home":
            return redirect(url_for(".studentHome", email=email))

    for x in range(len(wa)):
        if wa[x].name == None or wa[x].name == "":
            try:
                wa.remove(wa[x])
                clubs.remove(wa[x])
            except:
                pass
    
    
    return render_template("studentClubs.html", yourClubs=student.clubs, allClubs=wa)


@app.route('/student/<clubname>/<email>', methods=['POST', 'GET'])
def PacClub_Student_view(clubname, email):
    global clubs
    for x in clubs:
        if x.name == clubname:
            club = x
            break
    
    if request.method == "POST":
        if request.form['button'] == "home":
            return redirect(url_for(".studentHome", email=email))

        return redirect(url_for(".studentAllClubs", email=email))
    

    return render_template("PacClub_Student_view.html", name = clubname, announcments=club.announcments, events=club.events, members=club.memebers)

@app.route('/teacher/clubs/<email>', methods=['POST', 'GET'])
def teacherClubs(email):
    waste = len(email)
    for _teach in teachers:
        if _teach.wasteEmail == email:
            teacher = _teach
            break

    if request.method == 'POST':
        try:
            for club in teacher.clubs:
                if request.form["button"] == club.name:
                    return redirect(url_for(".teacherInClub", clubname=club.name))

        finally:
            name = request.form["email"]
            description = request.form["description"]
            
            teacher.makeClub(name, description)
        
        if request.form['button'] == "home":
            return redirect(url_for(".teacherHome", email=email))

    

    for x in range(len(teacher.clubs)):
        if teacher.clubs[x].name == None or teacher.clubs[x].name == "":
            teacher.clubs.remove(teacher.clubs[x])

    waste = copy.deepcopy(teacher.clubs)

    waste2 = copy.deepcopy(clubs)
    for x in teacher.clubs:
        try:
            waste2.remove(x)
        except:
            pass

    return render_template("clubs.html", yourClubs=waste, allClubs=waste2, lenlen = len(waste2))

@app.route('/teacher/<clubname>', methods=['POST', 'GET'])
def teacherInClub(clubname):
    
    for x in clubs:
        if x.name == clubname:
            club = x
            break

    teacher = club.teachers[0]
    email = teacher.wasteEmail
    if request.method == "POST":
        if request.form['button'] == "announcement":
            return redirect(url_for(".makeClubAnnouncment", clubname=club.name))
        
        if request.form['button'] == "club":
            return redirect(url_for(".teacherClubs", email=email))
        
        if request.form['button'] == "event":
            return redirect(url_for(".makeClubEvent", clubname=club.name))
        
        if request.form['button'] == "clubMembers":
            pass
            #return redirect(url_for(""))
        
        if request.form['button'] == "home":
            return redirect(url_for(".teacherHome", email=email))
    
    wa = []
    
    for x in club.memebers:
        wa.append(x.email[:x.find('.')])

    return render_template("PacClub.html", name=club.name, announcments = club.announcments, events=club.events, members=wa, otherClubs=teacher.clubs)



@app.route('/makeMainEvent/<email>', methods=['POST', 'GET'])
def makeMainEvent(email):
    if request.method == "POST":
        if request.form['button'] == "home":
            return redirect(url_for(".teacherHome", email=email))

        title = request.form['email']
        description = request.form['description']
        time = request.form['time']


        mainEvents.append([title, description, time])
        
        return redirect(url_for(".teacherHome", email=email))
    
    return render_template("event.html")


@app.route('/makeMainAnnouncement/<email>', methods=['POST', 'GET'])
def makeMainAnnouncment(email):
    if request.method == "POST":
        if request.form['button'] == "home":
            return redirect(url_for(".teacherHome", email=email))

        title = request.form['email']
        description = request.form['description']
        time = datetime.now()


        mainAnnouncments.append([title, description, time.strftime("%c")])
        
        return redirect(url_for(".teacherHome", email=email))
    
    return render_template("ann.html")



@app.route('/makeClubAnnouncement/<clubname>', methods=['POST', 'GET'])
def makeClubAnnouncment(clubname):

    for x in clubs:
        if x.name == clubname:
            club = x
            break

    if request.method == "POST":
        email = club.teachers[0].wasteEmail
        if request.form['button'] == "home":
            return redirect(url_for(".teacherHome", email=email))
        title = request.form['email']
        description = request.form['description']
        time = datetime.now()


        club.addAnnouncment(title, description)
        
        return redirect(url_for(".teacherInClub", clubname=club.name))
    
    return render_template("ann.html")

@app.route('/makeClubEvent/<clubname>', methods=['POST', 'GET'])
def makeClubEvent(clubname):

    for x in clubs:
        if x.name == clubname:
            club = x
            break

    if request.method == "POST":
        email = club.teachers[0].wasteEmail
        if request.form['button'] == "home":
            return redirect(url_for(".teacherHome", email=email))
        title = request.form['email']
        description = request.form['description']
        time = request.form['time']


        club.addEvent(title, description, time)
        
        return redirect(url_for(".teacherInClub", clubname=club.name))
    
    return render_template("event.html")


if __name__ == '__main__':
    app.run(debug=True, port=8778)


