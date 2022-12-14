import random
import re

import requests

import SQL
from xpinyin import Pinyin


class MusicWordsObject:
    def __init__(self) -> None:
        self.id = ''
        self.word = ''
        self.pName = ''
        self.pinyin = ''
        self.precent = -1
        self.name = ''
        self.author = ''


def isHave(word):
    p = Pinyin()
    pName = p.get_pinyin(word[0])
    pinyin = re.split('_', p.get_pinyin(word, '_'))
    if pName in SQL.getpName():
        wordList = SQL.getMusicWordsList(pName)
        mayList = []
        for i in wordList:
            pinyinList = re.split('_', i.pinyin)
            num = len(set(pinyinList).intersection(set(pinyin)))
            precent = num / len(pinyinList)
            if precent > 0.5:
                i.precent = precent
                mayList.append(i)
        if len(mayList) == 0:
            return -1
        maxPrecent = MusicWordsObject()
        maxPrecent.precent = 100
        for i in mayList:
            if abs(i.precent - 1) < maxPrecent.precent and pName == re.split('_', i.pinyin)[0]:
                maxPrecent.precent = abs(i.precent - 1)
                maxPrecent.id = i.id
                maxPrecent.word = i.word
        return maxPrecent
    else:
        return -1


def reply(word):
    p = Pinyin()
    pName = p.get_pinyin(word[-1])
    if pName in SQL.getpName():
        musicList = SQL.getMusicWordsList(pName)
        return random.choice(musicList)
    else:
        return -1


def isNext(first, last):
    p = Pinyin()
    firstP = p.get_pinyin(first[0])
    lastP = p.get_pinyin(last[-1])
    if firstP == lastP:
        return True
    else:
        return False


def game(word) -> MusicWordsObject:
    result = isHave(word)
    if not result == -1:
        message(result)
        printMessage(result, 0)
        print('\n')
        music = reply(result.word)
        if not music == -1:
            message(music)
            printMessage(music, 1)
            return music
        else:
            return -1
    else:
        return -1


def printMessage(music: MusicWordsObject, type):
    if type == 0:
        print('?????????')
    elif type == 1:
        print('?????????')

    print('???????????????\t' + str(music.word))
    print('??????id???\t\t' + str(music.id))
    print('???????????????\t' + str(music.name))
    print('???????????????\t' + str(music.author))


def message(music: MusicWordsObject):
    url = 'http://music.cyrilstudio.top/song/detail?ids=' + str(music.id)
    result = requests.get(url).json()
    music.name = result['songs'][0]['name']
    try:
        for i in result['songs'][0]['ar']:
            music.author += i['name'] + '/'
        music.author = music.author[0: len(music.author) - 1]
    except:
        music.author = '??????'


def botGame(word, person):
    music = isHave(word)
    if music == -1:
        # ???????????? ??????-1
        return -1
    lastMusic = SQL.getGameSave(person)
    # ???????????? ????????????
    if not lastMusic == -1:
        # ????????????
        if isNext(word, lastMusic):
            result = reply(word)
            if result == -1:
                # ???????????????
                return -3
            # ????????????????????????
            SQL.GameSave(result.word, person)
        else:
            # ??????????????? ??????-2
            return -2
    else:
        result = reply(word)
        SQL.GameSave(result.word, person)
    replyMsg = SQL.getPersonReplyMsg() + '\n' + word + '\n' + SQL.getMessage(
        music.id) + '\n\n' + SQL.getTianReplyMsg() + '\n' + result.word + '\n' + SQL.getMessage(result.id)
    return replyMsg


msg = input('?????????')
botResult = botGame(msg, 'test1')
if botResult == -1:
    print('?????????')
elif botResult == -2:
    print('???????????????')
elif botResult == -3:
    print('???????????????')
else:
    print(botResult)
