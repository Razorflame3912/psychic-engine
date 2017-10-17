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
    db.close()

def getGrades(name):
    c.execute('SELECT name,code,mark,courses.id,students.id FROM courses,students WHERE courses.id = students.id AND name = "%s";' %(name))
    rows = c.fetchall()
    dic = {}
    for row in rows:
        dic[row[1]] = row[2]

    return dic

def getInfo(name):
    c.execute('SELECT name,code,mark,courses.id,students.id FROM courses,students WHERE courses.id = students.id AND name = "%s";' %(name))
    rows = c.fetchall()
    li = []
    

    

print getAvg('kruder')
print getGrades('kruder')
