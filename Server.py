import json
import os
import random
import threading
import time
from http.server import HTTPServer, BaseHTTPRequestHandler

import requests

import BiliBili
import Response
import Api
import MySQL_Method.getTable


class Analyse(BaseHTTPRequestHandler):
    def do_POST(self):
        dataRaw = self.rfile.read(int(self.headers['content-length'])).decode()
        dataJson = json.loads(dataRaw)
        messageThread = MessageThread(dataJson)


class MessageThread(threading.Thread):
    def __init__(self, dataJson):
        """
        消息线程
        :param dataJson: 消息Json
        """
        threading.Thread.__init__(self)
        message = Response.MessageObject(dataJson)


class GlobThread(threading.Thread):
    def __init__(self, uid):
        threading.Thread.__init__(self)
        self.uid = uid

    def run(self):
        self.pushPubSay(self.uid)
        # for i in self.getAdmin():
        #     msg = BiliBili.getBiliGlob(self.uid, i)
        #     Api.Api_SendMsg('2327541179', '2', i, '', msg)
        #     time.sleep(3)

    @staticmethod
    def getAdmin():
        groupJson = Api.Api_GetGroupList_B('2327541179')['manage']
        groupList = []
        for i in groupJson:
            groupList.append(i['gc'])
        return groupList

    @staticmethod
    def pushPubSay(uid):
        msg, image = BiliBili.getPubSayGlob(uid)
        if len(image) == 0:
            Api.Api_PubSay('2327541179', msg)
        else:
            imageName = []
            imageStr = ''
            randName = str(random.randint(1, 1000))
            for i in range(len(image)):
                imageRequest = requests.get(image[i])
                url = os.path.abspath('./').replace('\\', '/') + '/' + randName + str(i) + '.jpg'
                imageName.append(url)
                file = open(url, 'wb')
                file.write(imageRequest.content)
                file.close()
                imageStr += url + '|'
            print(imageStr)
            Api.Api_PubSayAddImgBatch('2327541179', msg, imageStr)
            for i in imageName:
                os.remove(i)


class BiliBiliThread(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)

    def run(self):
        sql = MySQL_Method.getTable.MySQL()
        uidList = sql.getBilibiliUid()
        while True:
            for i in uidList:
                globTime_old = sql.getBilibiliTime(i)[0]
                globTime_new = BiliBili.getGlob(i)['data']['time']
                if not globTime_old == globTime_new:
                    try:
                        globTh = GlobThread(i)
                        globTh.start()
                        print('检测到 UID：' + str(i) + '发送新消息')
                        sql = MySQL_Method.getTable.MySQL()
                        sql.renewBiliTime(i, globTime_new)
                    except:
                        pass
            time.sleep(1)


class Server:
    def __init__(self, callPort, httpApiUrl, token):
        """
        创建本地服务器

        :param callPort: 回调接口
        :param httpApiUrl: httpApi接口
        :param token: Token
        """
        self.callPort = callPort
        self.httpApiUrl = httpApiUrl
        self.token = token

    def run(self):
        host = ('localhost', self.callPort)
        server = HTTPServer(host, Analyse)
        server.serve_forever()
