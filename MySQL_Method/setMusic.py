import os
import MySQLdb

import MySQL_Method.getTable
from Api import *
from xpinyin import Pinyin

mySql = MySQL_Method.getTable.MySQL()

p = Pinyin()

url = os.path.abspath('../Voice/Music').replace('\\', '/') + '/'

mp3Url = url + 'MP3/'

amrUrl = url + 'AMR/'

dirAll = os.listdir(mp3Url)

mp3 = []
musicName = []
amr = []

for i in dirAll:
    if '.mp3' in i:
        mp3.append(i)
        musicName.append(i[0:len(i) - 4])

oldMusicName = mySql.getMusicList()
del mySql

newMusicName = [i for i in musicName if i not in oldMusicName]
newMusicMp3 = [i for i in mp3 if i[0:len(i) - 4] in newMusicName]

for i in range(len(newMusicMp3)):
    Api_WavToAmr(mp3Url + newMusicMp3[i], amrUrl + musicName[i] + '.amr')
    print(musicName[i] + '转化成功')

db = MySQLdb.connect(
    host='localhost',
    port=3306,
    user='MyQQ',
    passwd='123456',
    db='myqq',
)

cursor = db.cursor()

cursor.execute('use myqq')

cursor.execute('delete from music;')

for i in os.listdir(amrUrl):
    if '.amr' in i:
        print(i)
        amrU = amrUrl + i
        name = i[0:len(i) - 4]
        sql = 'insert into music(name, url) ' \
              'values(\'' + name + '\', \'' + amrU + '\');'
        print(name, amrU)
        cursor.execute(sql)
