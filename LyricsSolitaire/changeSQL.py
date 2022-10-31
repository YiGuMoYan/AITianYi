import sqlite3
import threading

import requests


def arrange(data):
    dataList = []
    for i in data:
        dataList.append(i[0])
    return dataList


def message(id):
    url = 'http://music.cyrilstudio.top/song/detail?ids=' + str(id)
    print(url)
    result = requests.get(url).json()
    name = result['songs'][0]['name']
    author = ''
    for i in result['songs'][0]['ar']:
        author += i['name'] + '/'
    author = author[0: len(author) - 1]
    msg = '歌曲id：' + str(id) + '#歌曲昵称：' + name + '#歌曲作者：' + author
    return msg


connect = sqlite3.connect('./DataBase/MusicWords.db')
cur = connect.cursor()
sql = 'select * from MusciID'
result = arrange(cur.execute(sql).fetchall())
connect.close()
del cur
del connect


class myThread(threading.Thread):
    def __init__(self, numList, first, end):
        threading.Thread.__init__(self)
        self.wordList = numList
        self.firstNum = first
        self.endNum = end

    def run(self):
        self.wordList = self.wordList[self.firstNum: self.endNum]
        connectTh = sqlite3.connect('./DataBase/MusicWords.db')
        curTh = connectTh.cursor()
        for i in self.wordList:
            try:
                msg = message(i)
                sql = 'update MusciID set message = \'%s\' where ID = \'%s\';' % (msg, str(i))
                print(sql)
                curTh.execute(sql)
                connectTh.commit()
            except:
                pass
            print(str(i) + ' - 加载完成')


th1 = myThread(result, 0, 670)
th2 = myThread(result, 670, 1340)
th3 = myThread(result, 1340, 2010)
th4 = myThread(result, 2010, len(result))
th1.start()
th2.start()
th3.start()
th4.start()
