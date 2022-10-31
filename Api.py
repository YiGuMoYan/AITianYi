import configparser

import requests

config = configparser.ConfigParser()
config.read('E:\MyQQ\MyQQ\MyQQRobot\config.ini', encoding='utf-8')
httpApiUrl = config.get('MyQQ', 'HttpApiUrl')
token = int(config.get('MyQQ', 'Token'))


def Api_SendMsg(responseQQ, messageType, aimGroup, aimQQ, contain):
    """
    发送消息
    向对象、目标发送信息 支持好友 群 讨论组 群临时会话 讨论组临时会话
    :param responseQQ: 机器人QQ
    :param messageType: 1好友 2群 3讨论组 4群临时会话 5讨论组临时会话 6在线临时会话
    :param aimGroup: 发送群信息、讨论组信息、群临时会话信息、讨论组临时会话信息时填写
    :param aimQQ: 最终接收这条信息的对象QQ
    :param contain: 信息内容
    """
    data = {
        'function': 'Api_SendMsg',
        'token': token,
        'params': {
            'c1': responseQQ,
            'c2': messageType,
            'c3': aimGroup,
            'c4': aimQQ,
            'c5': contain
        }
    }
    requests.post(httpApiUrl, json=data)


def Api_WavToAmr(wavUrl, armUrl):
    """
    WavToAmr
    请确保bin目录有ffmpeg转码库(框架不自带)，成功返回amr文件完整路径，可直接调用上传语音api，失败返回空
    :param wavUrl: wav文件路径
    :param armUrl: amr文件路径
    :return: amr文件路径
    """
    data = {
        'function': 'Api_WavToAmr',
        'token': token,
        'params': {
            'c1': wavUrl,
            'c2': armUrl
        }
    }
    result = requests.post(httpApiUrl, json=data).json()
    return result['data']['ret']


def Api_UpLoadVoice(responseQQ, amrUrl):
    """
    上传语音
    上传QQ语音，成功返回语音GUID （只能发送群消息使用，不能好友） 失败返回空
    :param responseQQ: 	机器人QQ
    :param amrUrl: 语音文件路径（AMR Silk编码）
    :return: GUID
    """
    data = {
        'function': 'Api_UpLoadVoice',
        'token': token,
        'params': {
            'c1': responseQQ,
            'c2': amrUrl
        }
    }
    result = requests.post(httpApiUrl, json=data).json()
    return result['data']['ret']


def Api_SendVoice(responseQQ, aimQQ, amrUrl):
    """
    置好友语音上传
    发送好友语音 （成功返回真 失败返回假）
    :param responseQQ: 机器人QQ
    :param aimQQ: 接收语音人QQ
    :param amrUrl: 语音文件路径（AMR Silk编码）
    """
    data = {
        'function': 'Api_SendVoice',
        'token': token,
        'params': {
            'c1': responseQQ,
            'c2': aimQQ,
            'c3': amrUrl
        }
    }
    requests.post(httpApiUrl, json=data)


def Api_UpLoadPic(responseQQ, messageType, aimID, imageUrl):
    """
    上传图片
    上传图片，成功返回该图片GUID（格式为[pic={E9A12BBC-A5F9-1074-40D7-D1F229B4CA05}.png]），失败返回空
    :rtype: object
    :param responseQQ: 机器人QQ
    :param messageType: 1好友、临时会话 2群、讨论组 Ps：好友临时会话用类型 1，群讨论组用类型 2；当填写错误时，图片GUID发送不会成功
    :param aimID: 上传该图片所属的群号或QQ
    :param imageUrl: 本地路径或者网络图片地址
    """
    data = {
        'function': 'Api_UpLoadPic',
        'token': '666',
        'params': {
            'c1': responseQQ,
            'c2': messageType,
            'c3': aimID,
            'c4': imageUrl
        }
    }
    result = requests.post(httpApiUrl, json=data).json()
    return result['data']['ret']


def Api_GetAdminListEx(responseQQ, aimID):
    '''
    取包括群主在内的群管列表，返回json，其中oper=1代表接收群验证消息，owner=1代表是群主
    :param responseQQ: 	机器人QQ
    :param aimID: 欲取管理员列表群号
    :return:
    '''
    data = {
        'function': 'Api_GetAdminListEx',
        'token': '666',
        'params': {
            'c1': responseQQ,
            'c2': aimID,
        }
    }
    result = requests.post(httpApiUrl, json=data).json()
    return result['data']['ret']


def Api_GetGroupList_B(responseQQ):
    '''
    QQ群官网接口，取得群列表，返回获取到的原始JSON格式信息，需自行解析
    :param responseQQ: 机器人QQ
    :return:
    '''
    data = {
        'function': 'Api_GetGroupList_B',
        'token': '666',
        'params': {
            'c1': responseQQ,
        }
    }
    result = requests.post(httpApiUrl, json=data).json()
    return result['data']['ret']


def Api_PubSayAddImgBatch(responseQQ, content, image):
    data = {
        'function': 'Api_PubSayAddImgBatch',
        'token': '666',
        'params': {
            'c1': responseQQ,
            'c2': content,
            'c3': image
        }
    }
    result = requests.post(httpApiUrl, json=data).json()
    return result['data']['ret']


def Api_GetVoiceLink(responseQQ, guid):
    data = {
        'function': 'Api_GetVoiceLink',
        'token': '666',
        'params': {
            'c1': responseQQ,
            'c2': guid,
        }
    }
    result = requests.post(httpApiUrl, json=data).json()
    return result['data']['ret']


def Api_HandleFriendEvent(responseQQ, aimQQ, approach, message):
    data = {
        'function': 'Api_HandleFriendEvent',
        'token': '666',
        'params': {
            'c1': responseQQ,
            'c2': aimQQ,
            'c3': approach,
            'c4': message
        }
    }
    requests.post(httpApiUrl, json=data).json()


def Api_GetGroupName(responseQQ, aimID):
    data = {
        'function': 'Api_GetGroupName',
        'token': '666',
        'params': {
            'c1': responseQQ,
            'c2': aimID,
        }
    }
    result = requests.post(httpApiUrl, json=data).json()
    return result['data']['ret']


def Api_GetNick(responseQQ, aimQQ):
    data = {
        'function': 'Api_GetNick',
        'token': '666',
        'params': {
            'c1': responseQQ,
            'c2': aimQQ,
        }
    }
    result = requests.post(httpApiUrl, json=data).json()
    return result['data']['ret']


def Api_PubSay(responseQQ, msg):
    data = {
        'function': 'Api_GetNick',
        'token': '666',
        'params': {
            'c1': responseQQ,
            'c2': msg,
        }
    }
    requests.post(httpApiUrl, json=data).json()
