import MySQLdb

db = MySQLdb.connect(
    host='localhost',
    port=3306,
    user='MyQQ',
    passwd='123456',
    db='myqq',
)

cursor = db.cursor()

cursor.execute('delete from welcomeNewNumber;')
cursor.execute('delete from welcomeNewGroup;')
cursor.execute('delete from welcomeFriend;')
cursor.execute('delete from bilibiliUid;')

textNumber = [
    'Hello，我是AI天依，是最后的梦制作组制作的同人AI！',
    '欢迎新同学，这里是AI天依',
    '很高兴认识你，希望我们彼此能够度过一个快乐的时光~',
    '终于等到你啦，我是AI天依，相互认识一下吧！',
    '又有新的小伙伴来啦！',
    'こんにちは， 我是AI天依，是你的新伙伴呦',
]

textGroup = [
    'みんな，我是AI天依，很高兴在这里认识大家。',
    'Hello，大家好，我是AI天依，是最后的梦制作组制作的同人AI！',
    '有幸在最好的时代在这里遇到大家，希望能和大家一同度过快乐的时光。',
    'こんにちは，我是AI天依，相互认识一下吧！',
    '嗨~大家好，我是AI天依。',
    '皆さん、こんにちは、AI天依で、ここで皆さんと知り合って嬉しいです。'
]

textFriend = [
    '你好，我是AI天依，很高兴认识你！',
    'こんにちは，我是AI天依~',
    '终于等到你啦，我是AI天依，相互认识一下吧！',
    '嗨~我是AI天依，相信我们会度过一个快乐的时光',
    'Hello，我是AI天依，是最后的梦制作组制作的同人AI！',
    '哼哼哼~你终于来啦'
]

textUID = [
    '36081646',
    '34782593',
    '406948276',
    '406949083',
    '406950978',
    '406948857',
    '406948651',
    '34727551',
    '10878474',
]

for i in textNumber:
    sql = 'insert into welcomeNewNumber(text) values(\'' + i + '\');'
    cursor.execute(sql)

for i in textGroup:
    sql = 'insert into welcomeNewGroup(text) values(\'' + i + '\');'
    cursor.execute(sql)

for i in textFriend:
    sql = 'insert into welcomeFriend(text) values(\'' + i + '\');'
    cursor.execute(sql)

for i in textUID:
    sql = 'insert into bilibiliUid(uid) values(\'' + i + '\');'
    cursor.execute(sql)