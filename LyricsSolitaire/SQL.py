import random
import re
import sqlite3


class MusicWordsObject:
    def __init__(self) -> None:
        self.id = ''
        self.word = ''
        self.pName = ''
        self.pinyin = ''
        self.precent = -1
        self.name = ''
        self.author = ''


def arrange(data):
    dataList = []
    for i in data:
        dataList.append(i[0])
    return dataList


def arrangeMusicWordsObject(data):
    dataList = []
    for i in data:
        musicObject = MusicWordsObject()
        musicObject.pinyin = i[0]
        musicObject.word = i[1]
        musicObject.id = i[2]
        dataList.append(musicObject)
    return dataList


def insertKey():
    wordsList = [
        '作词', '作曲', '编曲', '策划', 'PV', '混音', '曲绘', '调教', '和声', '鸣谢', '编调'
    ]
    connect = sqlite3.connect('./DataBase/KeyWords.db')
    cur = connect.cursor()
    sql = 'create table if not exists KeyWords(KeyWord text);'
    cur.execute(sql)
    sql = 'delete from KeyWords;'
    cur.execute(sql)
    for i in wordsList:
        sql = 'insert into KeyWords(KeyWord) values(\'' + str(i) + '\')'
        cur.execute(sql)
    connect.commit()
    connect.close


def getKeyWords():
    connect = sqlite3.connect('./DataBase/KeyWords.db')
    cur = connect.cursor()
    sql = 'select * from KeyWords;'
    result = cur.execute(sql)
    return arrange(result.fetchall())


def insertPinYin(p):
    connect = sqlite3.connect('./DataBase/MusicWords.db')
    cur = connect.cursor()
    sql = 'create table if not exists PinYinList(pinyin text);'
    cur.execute(sql)
    sql = 'select pinyin from PinYinList where pinyin = \'' + str(p) + '\''
    if not cur.execute(sql).fetchall():
        sql = 'insert into PinYinList(pinyin) values(\'' + str(p) + '\')'
        cur.execute(sql)
    connect.commit()
    connect.close


def insertMusicID(id):
    connect = sqlite3.connect('./DataBase/MusicWords.db')
    cur = connect.cursor()
    sql = 'create table if not exists MusciID(ID text);'
    cur.execute(sql)
    sql = 'select ID from MusciID where ID = \'' + str(id) + '\''
    if not cur.execute(sql).fetchall():
        sql = 'insert into MusciID(ID) values(\'' + str(id) + '\')'
        cur.execute(sql)
    connect.commit()
    connect.close


def insertMusic(word, id, pName, pinyin):
    connect = sqlite3.connect('./DataBase/MusicWords.db')
    cur = connect.cursor()
    sql = 'create table if not exists ' + pName + '(pinyin text, word text, id text);'
    cur.execute(sql)
    sql = 'select pinyin from ' + pName + ' where pinyin = \'' + str(pinyin) + '\''
    if not cur.execute(sql).fetchall():
        sql = 'insert into ' + pName + \
              '(pinyin, word, id) values(\'' + \
              str(pinyin) + '\', \'' + str(word) + '\', \'' + str(id) + '\')'
        cur.execute(sql)
    connect.commit()
    connect.close


def getpName():
    connect = sqlite3.connect('./DataBase/MusicWords.db')
    cur = connect.cursor()
    sql = 'select * from PinYinList'
    result = arrange(cur.execute(sql).fetchall())
    connect.close()
    return result


def getMusicWordsList(pName):
    connect = sqlite3.connect('./DataBase/MusicWords.db')
    cur = connect.cursor()
    sql = 'select * from \'' + str(pName) + '\''
    result = arrangeMusicWordsObject(cur.execute(sql).fetchall())
    connect.close()
    return result


def GameSave(word, person):
    connect = sqlite3.connect('./DataBase/GameSave.db')
    cur = connect.cursor()
    sql = 'create table if not exists gameSave(word text, person text);'
    cur.execute(sql)
    if getGameSave(person) == -1:
        sql = 'insert into gameSave(word, person) values(\'' + str(word) + '\', \'' + str(person) + '\');'
        cur.execute(sql)
        connect.commit()
    else:
        sql = 'update gameSave set word=\'' + str(word) + '\' where person = \'' + str(person) + '\''
        cur.execute(sql)
        connect.commit()
    connect.close()


def getGameSave(person):
    connect = sqlite3.connect('./DataBase/GameSave.db')
    cur = connect.cursor()
    sql = 'select word from gameSave where person = "' + str(person) + '";'
    result = cur.execute(sql).fetchall()
    connect.close()
    if len(result) == 0:
        return -1
    else:
        result = arrange(result)
        return result[0]


def getMessage(id):
    connect = sqlite3.connect('./DataBase/MusicWords.db')
    cur = connect.cursor()
    sql = 'select message from MusciID where id = \'' + str(id) + '\''
    result = arrange(cur.execute(sql).fetchall())
    msgList = result[0]
    msgList = re.split('#', msgList)
    msg = ''
    for i in msgList:
        msg += i + '\n'
    return msg


def setReplyMsg():
    connect = sqlite3.connect('./DataBase/ReplyMsg.db')
    cur = connect.cursor()
    sql = 'create table if not exists personReply(msg text);'
    cur.execute(sql)
    sql = 'create table if not exists tianReply(msg text);'
    cur.execute(sql)
    personList = [
        '锵锵，小伙伴给出的是：',
        '歌词接龙小伙伴给出的回复是：',
        '咦，小伙伴给出了：'
    ]
    for i in personList:
        sql = 'insert into personReply(msg) values(\'' + str(i) + '\');'
        cur.execute(sql)
        connect.commit()
    tianList = [
        '那么，天依给出的答案是：',
        '天依也要更加努力了，天依的回复是：',
        '啊嘞啊嘞，小伙伴这么厉害吗，看看天依的：'
    ]
    for i in tianList:
        sql = 'insert into tianReply(msg) values(\'' + str(i) + '\');'
        cur.execute(sql)
        connect.commit()
    connect.close()


def getPersonReplyMsg():
    connect = sqlite3.connect('./DataBase/ReplyMsg.db')
    cur = connect.cursor()
    sql = 'select msg from personReply;'
    result = arrange(cur.execute(sql))
    return random.choice(result)


def getTianReplyMsg():
    connect = sqlite3.connect('./DataBase/ReplyMsg.db')
    cur = connect.cursor()
    sql = 'select msg from tianReply;'
    result = arrange(cur.execute(sql))
    return random.choice(result)


def delMusicPerson(person):
    connect = sqlite3.connect('./DataBase/GameSave.db')
    cur = connect.cursor()
    sql = 'delete from gameSave where person = \'' + person + '\''
    cur.execute(sql)
    connect.commit()
    connect.close()
