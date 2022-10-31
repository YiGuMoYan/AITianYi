import random

import MySQLdb
from xpinyin import Pinyin


class MySQL:
    def __init__(self):
        self.db = MySQLdb.connect(
            host='42.192.137.54',
            port=3306,
            user='MyQQ',
            passwd='123456',
            db='myqq',
        )
        self.cursor = self.db.cursor()
        self.cursor.execute('use myqq')
        self.p = Pinyin()

    @staticmethod
    def arrangeData(data):
        dataList = []
        for i in data:
            dataList.append(i[0])
        return dataList

    def getKeyWords(self):
        sql = 'select * from keywords;'
        self.cursor.execute(sql)
        data = self.cursor.fetchall()
        return self.arrangeData(data)

    def getImageUrl(self, tableName):
        sql = 'select * from ' + self.p.get_pinyin(tableName, '_') + ';'
        self.cursor.execute(sql)
        data = self.cursor.fetchall()
        data = self.arrangeData(data)
        return random.choice(data)

    def getMusicList(self):
        sql = 'select name from music;'
        self.cursor.execute(sql)
        data = self.cursor.fetchall()
        data = self.arrangeData(data)
        return data

    def getMusicUrl(self, name):
        sql = 'select url from music where name=\'' + name + '\';'
        self.cursor.execute(sql)
        data = self.cursor.fetchall()
        data = self.arrangeData(data)
        return data

    def getBilibiliUid(self):
        sql = 'select uid from bilibiliuid;'
        self.cursor.execute(sql)
        data = self.cursor.fetchall()
        data = self.arrangeData(data)
        return data

    def getBilibiliTime(self, uid):
        sql = 'select time from bilibiliuid where uid=\'' + uid + '\';'
        self.cursor.execute(sql)
        data = self.cursor.fetchall()
        data = self.arrangeData(data)
        return data

    def renewBiliTime(self, uid, time):
        sql = 'update bilibiliuid set time=\'' + str(time) +  '\' where uid=\'' + str(uid) + '\';'
        self.cursor.execute(sql)

    def getWelcomeNewNumber(self):
        sql = 'select * from welcomeNewNumber;'
        self.cursor.execute(sql)
        data = self.cursor.fetchall()
        data = self.arrangeData(data)
        return random.choice(data)

    def getWelcomeNewGroup(self):
        sql = 'select * from welcomeNewGroup;'
        self.cursor.execute(sql)
        data = self.cursor.fetchall()
        data = self.arrangeData(data)
        return random.choice(data)

    def getWelcomeFriend(self):
        sql = 'select * from welcomeFriend;'
        self.cursor.execute(sql)
        data = self.cursor.fetchall()
        data = self.arrangeData(data)
        return random.choice(data)