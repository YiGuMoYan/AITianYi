import random

import MySQLdb
from PIL import Image,ImageFont,ImageDraw
import os
import re

db = MySQLdb.connect(
    host='localhost',
    port=3306,
    user='MyQQ',
    passwd='123456',
    db='myqq',
)

cursor = db.cursor()

cursor.execute('use myqq')

cursor.execute('select name from music;')

data = cursor.fetchall()

musicList = []
musicName = []

for i in data:
    musicName.append(i[0])
    musicList.append('《' + i[0] + '》')

maxSize = 30
tempSize = 0
contentSize = 0

def getLen(name):
    worda = re.compile(r'[a-z]')
    wordA = re.compile(r'[A-Z]')
    num = re.compile(r'[0-9]')
    aLen = len(worda.findall(name))
    ALen = len(wordA.findall(name))
    numLen = len(num.findall(name))
    conLen = len(name) - aLen - ALen - numLen
    return conLen * 1 + aLen * 0.6 + ALen * 0.8 + numLen * 0.6


title = '歌单：'

content = ''

for i in range(len(musicList)):
    print(content)
    content += musicList[i]
    tempSize += getLen(musicList[i])
    if i < len(musicList) - 1:
        if maxSize < (tempSize + getLen(musicList[i+1])):
            content += '\n'
            tempSize = 0
            contentSize += 1

contentSize += 1

lastSize = contentSize * 20 + 70 + 20 * 3

lastContent = '如果想让AI天依唱歌\n请输入：唱 + 歌名\n例：唱' + random.choice(musicList)

high = lastSize + 20 * 3 + 30

imageBack = Image.new('RGB', (700, high), (225, 225, 225))

draw = ImageDraw.Draw(imageBack)

titleFont = ImageFont.truetype(os.path.join('', 'STHUPO.TTF'), 30) # 字体与字大小
contentFont = ImageFont.truetype(os.path.join('', 'simkai.ttf'), 20) # 字体与字大小
lastFont = ImageFont.truetype(os.path.join('', 'STXINWEI.TTF'), 20) # 字体与字大小

draw.text((50, 30), title, font=titleFont, fill='#000000') # 字位置与字颜色
draw.text((50, 70), content, font=contentFont, fill='#000000') # 字位置与字颜色
draw.text((50, lastSize), lastContent, font=lastFont, fill='#000000') # 字位置与字颜色

imageBack.save('../Image/歌单.jpg') # 保存

print(contentSize)