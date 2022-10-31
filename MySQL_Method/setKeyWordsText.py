import json

import MySQLdb
from xpinyin import Pinyin


def arrangeData(data):
    if data == 0:
        return []
    print(data)
    dataList = []
    for i in data:
        dataList.append(i[0])
    return dataList


db = MySQLdb.connect(
    host='localhost',
    port=3306,
    user='MyQQ',
    passwd='123456',
    db='myqq',
)
cursor = db.cursor()
cursor.execute('use myqq')
p = Pinyin()
cursor.execute('select * from keywords;')
data = arrangeData(cursor.fetchall())
dirData = {}
for i in data:
    tableName = p.get_pinyin(i, '_') + '_text'
    sql = 'create table if not exists ' + tableName + ' (text varchar(64));'
    cursor.execute(sql)
    # data[i] = arrangeData(cursor.execute('select * from ' + tableName + ';'))
    dirData[i] = []


file = open('keyWords.json' , 'w+')
file.write(json.dumps(dirData, indent=4, ensure_ascii=False))
file.close()

