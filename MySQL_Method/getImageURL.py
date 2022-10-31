import os
import MySQLdb
from xpinyin import Pinyin
import random

db = MySQLdb.connect(
    host='localhost',
    port=3306,
    user='MyQQ',
    passwd='123456',
    db='myqq',
)
cursor = db.cursor()


def arrangeData(data):
    dataList = []
    for i in data:
        dataList.append(i[0])
    return dataList


p = Pinyin()


def getImageUrl(tableName):
    sql = 'select * from ' + p.get_pinyin(tableName, '_') + ';'
    cursor.execute(sql)
    data = cursor.fetchall()
    data = arrangeData(data)
    print(random.choice(data))


getImageUrl('rua')
