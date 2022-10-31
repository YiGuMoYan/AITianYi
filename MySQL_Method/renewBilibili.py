import MySQLdb
import requests
import BiliBili
import getTable


db = MySQLdb.connect(
    host='42.192.137.54',
    port=3306,
    user='MyQQ',
    passwd='123456',
    db='myqq',
)

cursor = db.cursor()
cursor.execute('select * from bilibiliuid')

print(cursor.fetchall())
sql = getTable.MySQL()
uidList = sql.getBilibiliUid()
for i in uidList:
    result = BiliBili.getGlob(i)
    print(result['data']['name'] + result['data']['time'])
    sql = 'update bilibiliuid set time=\'' + result['data']['time'] +  '\' where uid=\'' + str(i) + '\';'
    cursor.execute(sql)



