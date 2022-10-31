import os
import MySQLdb
from xpinyin import Pinyin

db = MySQLdb.connect(
    host='localhost',
    port=3306,
    user='MyQQ',
    passwd='123456',
    db='myqq',
)

cursor = db.cursor()

cursor.execute('use myqq')

cursor.execute('select * from keywords;')

data = cursor.fetchall()

key = []

for i in data:
    key.append(i[0])

dirAll = os.listdir('../Image')

dirFile = []
dirIndex = []

for i in dirAll:
    if os.path.isfile('../Image/' + i):
        dirFile.append(i)
    elif os.path.isdir('../Image/' + i):
        dirIndex.append(i)


def delName(name):
    return name[0: len(name) - 4]


dirFileName = []

for i in dirFile:
    i = delName(i)
    dirFileName.append(i)

data = {}

p = Pinyin()

for i in range(len(dirFileName)):
    data[p.get_pinyin(dirFileName[i], '_')] = os.path.abspath('../Image/' + dirFile[i]).replace('\\', '/')

# 进行单一图片的写入
for key, value in data.items():
    sql = 'create table if not exists ' + key + ' (url varchar(64));'
    cursor.execute(sql)
    cursor.execute('delete from ' + key + ';')
    sql = 'insert into ' + key + '(url) values (\'' + value + '\');'
    cursor.execute(sql)

# 多图片写入
for i in dirIndex:
    imageList = os.listdir(os.path.abspath('../Image/' + i).replace('\\', '/'))
    sql = 'create table if not exists ' + p.get_pinyin(i, '_') + ' (url varchar(64));'
    cursor.execute(sql)
    cursor.execute('delete from ' + p.get_pinyin(i, '_') + ';')
    for j in imageList:
        url = os.path.abspath('../Image/' + i + '/' + j).replace('\\', '/')
        sql = 'insert into ' + p.get_pinyin(i, '_') + '(url) values (\'' + url + '\');'
        cursor.execute(sql)

print(dirFile)
