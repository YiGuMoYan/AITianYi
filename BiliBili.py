import json
import time

import requests


def getGlob(uid):
    url = 'https://api.vc.bilibili.com/dynamic_svr/v1/dynamic_svr/space_history?host_uid=' + str(uid)
    result = requests.get(url).json()
    # print(result)
    data = result['data']['cards'][0]
    globName = data['desc']['user_profile']['info']['uname']
    globType = data['desc']['type']
    globTime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(data['desc']['timestamp']))
    # print(globTime)
    # print(time.localtime(data['desc']['timestamp']))
    if globType == 1 or globType == 4:
        globTypeName = '[转发]'
        globContent = json.loads(data['card'])['item']['content']
        globUrl = 'https://t.bilibili.com/' + data['desc']['dynamic_id_str']
        globImage = []
        try:
            imageUrl = json.loads(json.loads(data['card'])['origin'])['pic']
            globImage.append(imageUrl)
        except:
            pass
        ret = {
            'name': globName,
            'type': globTypeName,
            'time': globTime,
            'content': globContent,
            'url': globUrl,
            'image': globImage
        }
        retJson = {
            'code': 200,
            'msg': '成功',
            'data': ret
        }
        return retJson
    elif globType == 2:
        globTypeName = '[动态]'
        globContent = json.loads(data['card'])['item']['description']
        globUrl = 'https://t.bilibili.com/' + data['desc']['dynamic_id_str']
        globImage = []
        try:
            imageList = json.loads(data['card'])['item']['pictures']
            for i in imageList:
                globImage.append(i['img_src'])
        except:
            pass
        ret = {
            'name': globName,
            'type': globTypeName,
            'time': globTime,
            'content': globContent,
            'url': globUrl,
            'image': globImage
        }
        retJson = {
            'code': 200,
            'msg': '成功',
            'data': ret
        }
        return retJson
    elif globType == 8:
        globTypeName = '[视频]'
        globContent = json.loads(data['card'])['title'] + '\n\n' + json.loads(data['card'])['dynamic'] + '\n' + json.loads(data['card'])['desc']
        globImage = [json.loads(data['card'])['pic']]
        globUrl = json.loads(data['card'])['short_link']
        ret = {
            'name': globName,
            'type': globTypeName,
            'time': globTime,
            'content': globContent,
            'url': globUrl,
            'image': globImage
        }
        retJson = {
            'code': 200,
            'msg': '成功',
            'data': ret
        }
        return retJson
    elif globType == 64:
        globTypeName = '[专栏]'
        globContent = json.loads(data['card'])['title'] + '\n\n' + json.loads(data['card'])['summary']
        globImage = []
        try:
            globImage = [json.loads(data['card'])['image_urls']]
        except:
            pass
        globUrl = 'https://t.bilibili.com/' + data['desc']['dynamic_id_str']
        ret = {
            'name': globName,
            'type': globTypeName,
            'time': globTime,
            'content': globContent,
            'url': globUrl,
            'image': globImage
        }
        retJson = {
            'code': 200,
            'msg': '成功',
            'data': ret
        }
        return retJson

def getBiliGlob(uid, aimID):
    print('开始获取动态')
    result = getGlob(uid)
    resultData = result['data']
    name = resultData['name']
    typeName = resultData['type']
    globTime = resultData['time']
    content = resultData['content']
    globUrl = resultData['url']
    imageList = resultData['image']
    msg = name + '动态\n\n' + typeName + '\n' + '时间：' + globTime + '\n\n' + content + '\n\n' + '传送门：' + globUrl + '\n' + '目标ID:' + str(
        aimID)
    for i in imageList:
        msg += '[pic=' + i + ']\n'
    return msg


def getPubSayGlob(uid):
    print('开始获取动态')
    result = getGlob(uid)
    resultData = result['data']
    name = resultData['name']
    typeName = resultData['type']
    globTime = resultData['time']
    content = resultData['content']
    globUrl = resultData['url']
    imageList = resultData['image']
    msg = name + '动态\n\n' + typeName + '\n' + '时间：' + globTime + '\n\n' + content + '\n\n' + '传送门：' + globUrl
    image = ''
    return msg, imageList
