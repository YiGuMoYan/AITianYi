import base64
import configparser
import os
import random
import re
import time
import BiliBili
from urllib import parse

import requests
from PIL import Image, ImageFont, ImageDraw

import Api
import MySQL_Method.getTable
import LyricsSolitaire.SQL
import LyricsSolitaire.game

config = configparser.ConfigParser()
config.read('config.ini', encoding='utf-8')
voiceUrl = config.get('MyQQ', 'VoiceUrl')
TianXingKey = config.get('TianXing', 'Key')
TianXingUrl = config.get('TianXing', 'Url')
VocalTTSUrl = config.get('VocalTTS', 'VocalTTSUrl')


class MessageObject:
    def __init__(self, dataJson):
        """
        初始化消息对象
        :param dataJson: 消息son
        """
        self.MQ_robot = dataJson['MQ_robot']
        self.MQ_type = dataJson['MQ_type']
        self.MQ_type_sub = dataJson['MQ_type_sub']
        self.MQ_fromID = dataJson['MQ_fromID']
        self.MQ_fromQQ = dataJson['MQ_fromQQ']
        self.MQ_passiveQQ = dataJson['MQ_passiveQQ']
        self.MQ_msg = parse.unquote(dataJson['MQ_msg'])
        self.MQ_msgSeq = dataJson['MQ_msgSeq']
        self.MQ_msgID = dataJson['MQ_msgID']
        self.MQ_msgData = dataJson['MQ_msgData']
        self.MQ_timestamp = dataJson['MQ_timestamp']

        if not self.MQ_fromQQ == '2854196310':
            if self.MQ_type == 1:
                print('[私聊]' + self.MQ_fromID + '(' + self.MQ_fromQQ + ')：' + self.MQ_msg)
                self.friend_keyWords()
                if self.MQ_msg == '获取动态':
                    self.friend_sendGlob()
                elif self.MQ_msg == '歌单' or self.MQ_msg == '唱歌':
                    self.friend_sendMusicList()
                elif self.isSong():
                    self.friend_sendMusic()
                elif '歌词接龙' in self.MQ_msg:
                    self.friend_keyWords()
                else:
                    self.friend_sendVoice()
            elif self.MQ_type == 2:
                print('[群聊]' + self.MQ_fromID + '(' + self.MQ_fromQQ + ')：' + self.MQ_msg)
                if '获取动态' in self.MQ_msg:
                    self.group_sendGlob()
                elif self.MQ_msg == '歌单' or self.MQ_msg == '唱歌':
                    self.group_sendMusicList()
                elif self.isAt():
                    if self.MQ_msg == '歌单' or self.MQ_msg == '唱歌':
                        self.group_sendMusicList()
                    elif self.isSong():
                        self.group_sendMusic()
                    elif self.isAdmin() and self.isSay():
                        print('管理')
                        self.group_sendVoice(typeNum=1)
                    elif '歌词接龙' in self.MQ_msg:
                        self.group_Lyrics()
                    else:
                        self.group_sendVoice()
                else:
                    self.group_keyWords()
            elif self.MQ_type == 20021 or self.MQ_type == 2002 or self.MQ_type == 2005:
                if self.MQ_passiveQQ == self.MQ_robot:
                    self.welcomeNewGroup()
                else:
                    self.welcomeNewNumber()
            elif self.MQ_type == 1000 or self.MQ_type == 1001:
                self.agreeFriend()

    def group_sendVoice(self, msg=None, typeNum=0):
        """
        向群聊发送语音
        :param msg: 语音消息内容（空则为 MQ_msg ）
        """
        TianXingReply = ''
        if typeNum == 0:
            TianXingReply = self.getTianXingReply(msg)
        else:
            TianXingReply = self.MQ_msg
        fileName = self.getTTS(TianXingReply)
        wavUrl = voiceUrl + fileName + '.wav'
        amrUrl = voiceUrl + fileName + '.amr'
        amrUrl = Api.Api_WavToAmr(wavUrl, amrUrl)
        Api.Api_SendVoice(self.MQ_robot, self.MQ_fromID, amrUrl)
        GUID = Api.Api_UpLoadVoice(self.MQ_robot, amrUrl)
        Api.Api_SendMsg(self.MQ_robot, 2, self.MQ_fromID, '', GUID)
        # Api.Api_SendMsg(self.MQ_robot, 2, self.MQ_fromID, '', TianXingReply)
        os.remove(wavUrl)
        os.remove(amrUrl)

    def group_sendGlob(self):
        """
        被动获取最新动态
        """
        globMsg = BiliBili.getBiliGlob(36081646, self.MQ_fromID)
        Api.Api_SendMsg(self.MQ_robot, 2, self.MQ_fromID, '', globMsg)

    def group_sendMusicList(self):
        url = self.setMusicUrl()
        musicUrl = '[pic=' + url + ']'
        sql = MySQL_Method.getTable.MySQL()
        msg = '如果想让AI天依唱歌\n请输入：唱 + 歌名\n例：唱' + random.choice(sql.getMusicList())
        Api.Api_SendMsg(self.MQ_robot, self.MQ_type, self.MQ_fromID, '', msg)
        Api.Api_SendMsg(self.MQ_robot, self.MQ_type, self.MQ_fromID, '', musicUrl)
        time.sleep(3)
        os.remove(url)

    def group_keyWords(self):
        for i in self.getKeyWords():
            if i in self.MQ_msg and random.randint(1, 2) % 3 == 0:
                reply = self.getTianXingReply(i)
                url = self.getImageUrl(i)
                guid = Api.Api_UpLoadPic(self.MQ_robot, 2, self.MQ_fromID, url)
                self.MQ_msg = reply
                self.group_sendVoice(reply, 1)
                Api.Api_SendMsg(self.MQ_robot, 2, self.MQ_fromID, '', guid)
                break

    def group_sendMusic(self):
        if self.isExistMusic():
            musicUrl = self.musicUrl()
            musicGUID = Api.Api_UpLoadVoice(self.MQ_robot, musicUrl)
            Api.Api_SendMsg(self.MQ_robot, 2, self.MQ_fromID, '', musicGUID)
        else:
            Api.Api_SendMsg(self.MQ_robot, 2, self.MQ_fromID, '', '天依暂时没有收录该曲目，小伙伴可以发送歌单获取信息呦！')

    def group_Lyrics(self):
        person = str(self.MQ_fromID) + '(2)'
        self.MQ_msg = self.MQ_msg.replace(' ', '')
        gameSave = LyricsSolitaire.SQL.getGameSave(person)
        if self.MQ_msg == '歌词接龙':
            if gameSave == -1:
                msg = '[歌词接龙]\n' \
                      '小伙伴的歌词接龙开始啦！\n' \
                      '歌词接龙指令：歌词接龙 歌词\n' \
                      '例子：歌词接龙 放逐泪光'
                Api.Api_SendMsg(self.MQ_robot, 2, self.MQ_fromID, '', msg)
            else:
                msg = '[歌词接龙]\n' \
                      '小伙伴正在歌词接龙中\n' \
                      '小伙伴的题目是：' + gameSave
                Api.Api_SendMsg(self.MQ_robot, 2, self.MQ_fromID, '', msg)
        elif self.MQ_msg[0: 4] == '歌词接龙':
            receiveWord = self.MQ_msg[4: len(self.MQ_msg)]
            getWord = LyricsSolitaire.game.botGame(receiveWord, person)
            if getWord == -1:
                msg = '[歌词接龙]\n' \
                      '天依检测到小伙伴的曲目并非中文VOCALOID曲目，请小伙伴检查曲目或是系管理员处理'
                Api.Api_SendMsg(self.MQ_robot, 2, self.MQ_fromID, '', msg)
            elif getWord == -2:
                msg = '[歌词接龙]\n' \
                      '小伙伴的前后内容不相互匹配哦，请检查歌词哦。\n小伙伴的题目是：' + LyricsSolitaire.SQL.getGameSave(person)
                Api.Api_SendMsg(self.MQ_robot, 2, self.MQ_fromID, '', msg)
            elif getWord == -3:
                msg = '[歌词接龙]\n' \
                      '小伙伴好厉害啊，这可把天依难住了，小伙伴重新开始一轮吧~'
                Api.Api_SendMsg(self.MQ_robot, 2, self.MQ_fromID, '', msg)
            else:
                Api.Api_SendMsg(self.MQ_robot, 2, self.MQ_fromID, '', getWord)
        else:
            msg = '[歌词接龙]\n' \
                  '* 歌词接龙 - 模板：歌词接龙 歌词（例：歌词接龙 放逐泪光）\n' \
                  '* 歌词接龙仅限于中文VOCALOID曲目，包括原唱、翻唱曲目，均来自网易云\n' \
                  '* 歌词数据库必然不全，还望谅解，若有需要添加的曲目，请联系最后的梦制作组。'
            Api.Api_SendMsg(self.MQ_robot, 2, self.MQ_fromID, '', msg)

    def friend_sendVoice(self, msg=None, typeNum=0):
        """
        向朋友发送语音
        :param typeNum:  类型
        :param msg: 语音消息内容（空则为 MQ_msg ）
        """
        TianXingReply = ''
        if typeNum == 0:
            TianXingReply = self.getTianXingReply(msg)
        else:
            TianXingReply = msg
        fileName = self.getTTS(TianXingReply)
        wavUrl = voiceUrl + fileName + '.wav'
        amrUrl = voiceUrl + fileName + '.amr'
        amrUrl = Api.Api_WavToAmr(wavUrl, amrUrl)
        Api.Api_SendVoice(self.MQ_robot, self.MQ_fromQQ, amrUrl)
        Api.Api_SendMsg(self.MQ_robot, 1, '', self.MQ_fromQQ, TianXingReply)
        os.remove(wavUrl)
        os.remove(amrUrl)

    def friend_sendGlob(self):
        """
        被动获取最新动态
        """
        globMsg = BiliBili.getBiliGlob(36081646, self.MQ_fromID)
        Api.Api_SendMsg(self.MQ_robot, 1, '', self.MQ_fromQQ, globMsg)

    def friend_sendMusicList(self):
        url = self.setMusicUrl()
        musicUrl = '[pic=' + url + ']'
        sql = MySQL_Method.getTable.MySQL()
        msg = '如果想让AI天依唱歌\n请输入：唱 + 歌名\n例：唱' + random.choice(sql.getMusicList())
        Api.Api_SendMsg(self.MQ_robot, 1, '', self.MQ_fromQQ, msg)
        Api.Api_SendMsg(self.MQ_robot, 1, '', self.MQ_fromQQ, musicUrl)
        os.remove(url)

    def friend_keyWords(self):
        for i in self.getKeyWords():
            if i in self.MQ_msg:
                url = self.getImageUrl(i)
                guid = Api.Api_UpLoadPic(self.MQ_robot, 1, self.MQ_fromQQ, url)
                Api.Api_SendMsg(self.MQ_robot, 1, '', self.MQ_fromQQ, guid)
                break

    def friend_sendMusic(self):
        if self.isExistMusic():
            musicUrl = self.musicUrl()
            musicGUID = Api.Api_SendVoice(self.MQ_robot, self.MQ_fromQQ, musicUrl)
            Api.Api_SendMsg(self.MQ_robot, 1, '', self.MQ_fromQQ, musicGUID)
        else:
            Api.Api_SendMsg(self.MQ_robot, 1, '', self.MQ_fromQQ, '天依暂时没有收录该曲目，小伙伴可以发送歌单获取信息呦！')

    def friend_Lyrics(self):
        person = str(self.MQ_fromID) + '(1)'
        self.MQ_msg = self.MQ_msg.replace(' ', '')
        gameSave = LyricsSolitaire.SQL.getGameSave(person)
        if self.MQ_msg == '歌词接龙':
            if gameSave == -1:
                msg = '[歌词接龙]\n' \
                      '小伙伴的歌词接龙开始啦！\n' \
                      '歌词接龙指令：歌词接龙 歌词\n' \
                      '例子：歌词接龙 放逐泪光'
                Api.Api_SendMsg(self.MQ_robot, 1, '', self.MQ_fromQQ, msg)
            else:
                msg = '[歌词接龙]\n' \
                      '小伙伴正在歌词接龙中\n' \
                      '小伙伴的题目是：' + gameSave
                Api.Api_SendMsg(self.MQ_robot, 1, '', self.MQ_fromQQ, msg)
        elif self.MQ_msg[0: 4] == '歌词接龙':
            receiveWord = self.MQ_msg[4: len(self.MQ_msg)]
            getWord = LyricsSolitaire.game.botGame(receiveWord, person)
            if getWord == -1:
                msg = '[歌词接龙]\n' \
                      '天依检测到小伙伴的曲目并非中文VOCALOID曲目，请小伙伴检查曲目或是系管理员处理'
                Api.Api_SendMsg(self.MQ_robot, 1, '', self.MQ_fromQQ, msg)
            elif getWord == -2:
                msg = '[歌词接龙]\n' \
                      '小伙伴的前后内容不相互匹配哦，请检查歌词哦。\n小伙伴的题目是：' + LyricsSolitaire.SQL.getGameSave(person)
                Api.Api_SendMsg(self.MQ_robot, 1, '', self.MQ_fromQQ, msg)
            elif getWord == -3:
                msg = '[歌词接龙]\n' \
                      '小伙伴好厉害啊，这可把天依难住了，小伙伴重新开始一轮吧~'
                Api.Api_SendMsg(self.MQ_robot, 1, '', self.MQ_fromQQ, msg)
            else:
                Api.Api_SendMsg(self.MQ_robot, 1, '', self.MQ_fromQQ, getWord)
        else:
            msg = '[歌词接龙]\n' \
                  '* 歌词接龙 - 模板：歌词接龙 歌词（例：歌词接龙 放逐泪光）\n' \
                  '* 歌词接龙仅限于中文VOCALOID曲目，包括原唱、翻唱曲目，均来自网易云\n' \
                  '* 歌词数据库必然不全，还望谅解，若有需要添加的曲目，请联系最后的梦制作组。'
            Api.Api_SendMsg(self.MQ_robot, 1, '', self.MQ_fromQQ, msg)

    def getTianXingReply(self, msg=None):
        """
        通过天行机器人获取回复
        :param msg: 请求内容
        :return: 回复内容
        """
        if msg is None:
            msg = self.MQ_msg
        data = {
            'key': TianXingKey,
            'question': msg,
            'uniqueid': str(self.MQ_fromID) + '(' + str(self.MQ_type) + ')'
        }
        result = requests.post(TianXingUrl, data=data).json()
        resultReply = result['newslist'][0]['reply']
        print(result)
        return resultReply

    def isAt(self):
        """
        群聊检测是否有 @ ，并删除
        :return: 是/否
        """
        if '[@2327541179]+' in self.MQ_msg:
            self.MQ_msg = self.MQ_msg.replace('[@2327541179]+', '')
            print('存在@')
            return True
        else:
            return False

    def setMusicUrl(self):
        sql = MySQL_Method.getTable.MySQL()
        musicName = sql.getMusicList()
        musicList = []
        for i in musicName:
            musicList.append('《' + i + '》')
        maxSize = 30
        tempSize = 0
        contentSize = 0
        title = '歌单：'
        content = ''
        for i in range(len(musicList)):
            content += musicList[i]
            tempSize += self.getMusicLen(musicList[i])
            if i < len(musicList) - 1:
                if maxSize < (tempSize + self.getMusicLen(musicList[i + 1])):
                    content += '\n'
                    tempSize = 0
                    contentSize += 1
        contentSize += 1
        lastSize = contentSize * 20 + 70 + 20 * 3
        lastContent = '如果想让AI天依唱歌\n请输入：唱 + 歌名\n例：唱' + random.choice(musicName)
        high = lastSize + 20 * 3 + 30
        imageBack = Image.new('RGB', (700, high), (225, 225, 225))
        draw = ImageDraw.Draw(imageBack)
        titleFont = ImageFont.truetype(os.path.join('', '华文琥珀.ttf'), 30)  # 字体与字大小
        contentFont = ImageFont.truetype(os.path.join('', 'simkai.ttf'), 20)  # 字体与字大小
        lastFont = ImageFont.truetype(os.path.join('', 'simkai.ttf'), 20)  # 字体与字大小
        draw.text((50, 30), title, font=titleFont, fill='#000000')  # 字位置与字颜色
        draw.text((50, 70), content, font=contentFont, fill='#000000')  # 字位置与字颜色
        draw.text((50, lastSize), lastContent, font=lastFont, fill='#000000')  # 字位置与字颜色
        url = os.path.abspath('./') + '\\歌单' + str(random.randint(1, 1000)) + '.jpg'
        imageBack.save(url)
        time.sleep(2)
        print(url)
        return url

    def isSong(self):
        if self.MQ_msg[0] == '唱':
            self.MQ_msg = self.MQ_msg[1: len(self.MQ_msg)]
            print(self.MQ_msg)
            return True
        else:
            return False

    def musicUrl(self):
        sql = MySQL_Method.getTable.MySQL()
        return sql.getMusicUrl(self.MQ_msg)

    @staticmethod
    def getImageUrl(key):
        sql = MySQL_Method.getTable.MySQL()
        imageUrl = sql.getImageUrl(key)
        return imageUrl

    @staticmethod
    def getKeyWords():
        """
        获取关键词
        :return: 关键词
        """
        sql = MySQL_Method.getTable.MySQL()
        keyWordsList = sql.getKeyWords()
        return keyWordsList

    @staticmethod
    def getTTS(text):
        """
        通过 VOCALTTS 获取音频
        :param text: 音频内容
        :return:  Wav文件路径
        """
        data = {
            'app': 'web',
            'pit': 0,
            'rand_str': "123456",
            'text': text,
            'time': time.time(),
            'token': "",
            'uid': "admin",
            'vel': 0,
            'voice_name': "lty",
            'voice_version': "t1",
            'vol': 0,
        }
        dosynth = requests.post(VocalTTSUrl, data=data).json()
        code64 = dosynth['data']
        code64 = code64.replace('data:audio/wav;base64,', '')
        code = base64.b64decode(code64)
        name = random.randint(1, 1000)
        tts = open(voiceUrl + str(name) + '.wav', 'wb')
        tts.write(code)
        tts.close()
        return str(name)

    @staticmethod
    def getMusicLen(name):
        worda = re.compile(r'[a-z]')
        wordA = re.compile(r'[A-Z]')
        num = re.compile(r'[0-9]')
        aLen = len(worda.findall(name))
        ALen = len(wordA.findall(name))
        numLen = len(num.findall(name))
        conLen = len(name) - aLen - ALen - numLen
        return conLen * 1 + aLen * 0.6 + ALen * 0.8 + numLen * 0.6

    def isExistMusic(self):
        sql = MySQL_Method.getTable.MySQL()
        if self.MQ_msg in sql.getMusicList():
            return True
        return False

    def welcomeNewNumber(self):
        sql = MySQL_Method.getTable.MySQL()
        msg = '[@' + self.MQ_passiveQQ + '] '
        msg += sql.getWelcomeNewNumber()
        Api.Api_SendMsg(self.MQ_robot, '2', self.MQ_fromID, '', msg)

    def welcomeNewGroup(self):
        sql = MySQL_Method.getTable.MySQL()
        msg = sql.getWelcomeNewGroup()
        Api.Api_SendMsg(self.MQ_robot, '2', self.MQ_fromID, '', msg)
        msg = '加入群聊：' + Api.Api_GetGroupName(self.MQ_robot, self.MQ_fromID) + '[' + str(self.MQ_fromID) + ']'
        Api.Api_SendMsg(self.MQ_robot, '1', '', '3194775246', msg)

    def agreeFriend(self):
        Api.Api_HandleFriendEvent(self.MQ_robot, self.MQ_fromQQ, 10, '')
        sql = MySQL_Method.getTable.MySQL()
        msg = sql.getWelcomeFriend()
        Api.Api_SendMsg(self.MQ_robot, '1', '', self.MQ_fromQQ, msg)
        msg = '添加好友：' + Api.Api_GetNick(self.MQ_robot, self.MQ_fromQQ) + '[' + str(self.MQ_fromQQ) + ']'
        Api.Api_SendMsg(self.MQ_robot, '1', '', '3194775246', msg)

    def isAdmin(self):
        adminStr = str(Api.Api_GetAdminListEx(self.MQ_robot, self.MQ_fromID))
        if self.MQ_fromQQ in adminStr:
            return True
        else:
            return False

    def isSay(self):
        if self.MQ_msg[0] == '说':
            self.MQ_msg = self.MQ_msg[1: len(self.MQ_msg)]
            return True
        else:
            return False
