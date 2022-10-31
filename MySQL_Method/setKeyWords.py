import os

import MySQLdb

db = MySQLdb.connect(
    host='localhost',
    port=3306,
    user='MyQQ',
    passwd='123456',
    db='myqq',
)

cursor = db.cursor()

cursor.execute('use myqq')


# cursor.execute('delete from keywords;')

def delName(name):
    return name[0: len(name) - 4]


keyWords = []

dirAll = os.listdir('../Image')
dirFile = []
dirIndex = []

for i in dirAll:
    if os.path.isfile('../Image/' + i):
        dirFile.append(i)
    elif os.path.isdir('../Image/' + i):
        dirIndex.append(i)

for i in dirFile:
    i = delName(i)
    keyWords.append(i)

for i in dirIndex:
    keyWords.append(i)

cursor.execute('delete from keywords;')

data = cursor.fetchall()

key = []

for i in data:
    key.append(i[0])

for i in keyWords:
    if i not in key:
        sql = '''
            insert into keywords(keywords)
                values('%s');
        ''' % i
        cursor.execute(sql)

cursor.execute('select * from keywords;')

data = cursor.fetchall()

print(data)
