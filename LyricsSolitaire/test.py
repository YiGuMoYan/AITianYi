import sqlite3
person = 'test1'
connect = sqlite3.connect('./DataBase/GameSave.db')
cur = connect.cursor()
sql = 'select word from gameSave where person = \'' + str(person) + '\';'
print(sql)
result = cur.execute(sql).fetchall()
print('result - ' + str(result))
