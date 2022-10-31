# # import datetime
# #
import requests
# #
# import Api
# # import time
# #
# # msg = '生日快乐呀[next]虽然说因为种种原因不能在生日这天当面给你庆祝[next]只能用这样的方式庆祝[next]马上你就又要出国了[next]不过好在在这之前咱们还能见上一面[next]到时候一定要将这段时间的遗憾全部弥补回来[next]（我相信我绝对是最按时的一个）[next]n[pic=E:MyQQMyQQMyQQRobot1.jpg]'
# # nowTime = datetime.datetime.now()
# # print('当前时间：' + str(nowTime))
# # nextTime = datetime.datetime.strptime(
# #     str(nowTime.date().year) + "-" + str(nowTime.date().month) + "-" + str(nowTime.date().day) + " 23:59:59",
# #     "%Y-%m-%d %H:%M:%S")
# # print('目标时间：' + str(nextTime))
# # timer_start_time = (nextTime - nowTime).total_seconds()
# # print('间隔时间：' + str(timer_start_time) + '秒')
# # time.sleep(timer_start_time)
# # startTime = time.time()
# # Api.Api_SendMsg('3194775246', 1, '', 924923549, msg)
# # finishTime = time.time()
# # print(finishTime - startTime)
#
# # url = 'http://api.tianapi.com/robot/index'
# #
# # data = {
# #     'key': '8c83ce5c37e43ff20479ab503567f2fe',
# #     'question': '你好'
# # }
# #
# # print(requests.post(url, data=data).json())
#
# # a = '唱123'
# # print(a[1 : len(a)])
#
# # print(Api.Api_GetGroupList_B('2327541179'))
#
#
# # data = {
# #         'function': 'Api_PubSayAddImgBatch',
# #         'token': '666',
# #         'params': {
# #             'c1': '2327541179',
# #             'c2': '测试',
# #             'c3': 'E:MyQQMyQQMyQQRobotImage变态.jpg|E:MyQQMyQQMyQQRobotImage冒泡.jpg|E:MyQQMyQQMyQQRobotImage光明.jpg|',
# #         }
# # }
# # result = requests.post('http://localhost:1003/MyQQHTTPAPI', json=data).json()
# # print(result)
#
# a = '123456'
# print(a[1 : len(a)])

# aurl = 'https://www.gaokao.cn/special/172?sort=2&special_type=3&schoolflag=&argschtype=%E6%99%AE%E9%80%9A%E6%9C%AC%E7%A7%91'
#
# data = {
#     'user-agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36',
# }
#
# print(requests.get(url, headers=data).text.encode('raw_unicode_escape').decode())
#

# url = 'http://music.cyrilstudio.top/song/detail?ids='
# result = requests.get(url)
# print(result.text)
# print(1)

msg = [1, 2, 5, 4, 7, 5, 5, 4, 1]
print(msg[5 : len(msg)])
