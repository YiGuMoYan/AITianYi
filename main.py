import configparser
from Server import *

if __name__ == '__main__':
    config = configparser.ConfigParser()
    config.read('config.ini', encoding='utf-8')
    callPort = int(config.get('MyQQ', 'CallPort'))
    httpApiUrl = config.get('MyQQ', 'HttpApiUrl')
    token = int(config.get('MyQQ', 'Token'))
    biliTh = BiliBiliThread()
    biliTh.start()
    server = Server(callPort, httpApiUrl, token)
    server.run()