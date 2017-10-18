import sqlite3;

db = sqlite3.connect('database.db');
c = db.cursor()


def getAvg(name):
    dic = getGrades(name)

    classnum = 0.0
    total = 0.0
    for course in dic:
        classnum+=1
        total += dic[course]
    return total/classnum

def getGrades(name):
    c.execute('SELECT name,code,mark,courses.id,students.id FROM courses,students WHERE courses.id = students.id AND name = "%s";' %(name))
    rows = c.fetchall()
    dic = {}
    for row in rows:
        dic[row[1]] = row[2]

    return dic

def getInfo(name):
    c.execute('SELECT name,id FROM students WHERE name = "%s";' %(name))
    rows = c.fetchall()
    dic = {}
    for row in rows:
        dic['name'] = row[0]
        dic['id'] = row[1]
        dic['average'] = getAvg(name)
    return dic
        
def createAvgTable():
    c.execute('SELECT name,id FROM students;')
    rows = c.fetchall()
    c.execute('DROP TABLE IF EXISTS peeps_avg;')
    c.execute('CREATE TABLE peeps_avg(id NUMERIC PRIMARY KEY, avg NUMERIC);')
    for row in rows:
         idnum = row[1]
         avg = getInfo(row[0])['average']
         c.execute('INSERT INTO peeps_avg VALUES(%d,%f);' %(idnum,avg))
    db.commit()

def updateAvg():
    c.execute('SELECT name,students.id,avg,peeps_avg.id FROM students,peeps_avg WHERE students.id = peeps_avg.id')
    rows = c.fetchall()
    for row in rows:
        c.execute('UPDATE peeps_avg SET avg = %f WHERE avg != %f AND id = %d' %(getAvg(row[0]),getAvg(row[0]),row[1]))

def addCourse(course,mark,idnum):
    c.execute('INSERT INTO courses VALUES("%s",%d,%d);'%(course,mark,idnum))
    db.commit()
   

    

print "Kruder's Average: %d\n" %(getAvg('kruder'))
print "Kruder's Grades: " + str(getGrades('kruder')) + '\n'
print "Kruder's Info: " + str(getInfo('kruder')) + '\n'

print 'Creating averages table...\n'
createAvgTable()

c.execute('SELECT * FROM peeps_avg;')
rows = c.fetchall()
for row in rows:
    print row

print '\nAdding new courses...'
addCourse('ceramics',90,5)
addCourse('greatbooks',75,8)
addCourse('systems',60,9)

print '\nUpdating averages...'
updateAvg()

c.execute('SELECT * FROM peeps_avg;')
rows = c.fetchall()
for row in rows:
    print row



db.close()
