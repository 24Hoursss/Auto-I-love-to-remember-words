import httpx
import datetime
import time
import random

localPath = '.'
answer = {}


def saveAnswer(dic):
    saveDict(dic, localPath + '\\awsNew.txt')


def loadAnswer():
    return loadDict(localPath + '\\awsNew.txt')


def loadSetting():
    return loadDict(localPath + '\\setting.txt')


def saveDict(dic, path):
    f = open(path, 'w')
    f.write(str(dic))
    f.close()
    print("字典保存成功")


def loadDict(path):
    f = open(path, 'r')
    _dic = eval(f.read())
    f.close()
    print("字典载入成功")
    return _dic


def get_current_week():
    # 返回当前的星期一和星期天的日期
    monday = datetime.date.today()
    one_day = datetime.timedelta(days=1)
    while monday.weekday() != 0:
        monday -= one_day
    return monday


def getWithOptions(url):
    try:
        httpx.options(url, headers=headers)
        return httpx.get(url, headers=headers)
    except:
        return getWithOptions(url)


def postWithOptions(url, json):
    try:
        httpx.options(url, headers=headers)
        return httpx.post(url, headers=headers, json=json)
    except:
        return postWithOptions(url, json)


# 加载设置
setting = loadSetting()
token = setting['token']
UA = setting['UA']
headers = {
    'Host': 'skl.hdu.edu.cn',
    'Origin': 'https://skl.hduhelp.com',
    'X-Auth-Token': token,
    'Connection': 'keep-alive',
    'Accept': 'application/json, text/plain, */*',
    'User-Agent': UA,
    'Accept-Language': 'zh-cn',
    'Referer': 'https://skl.hduhelp.com/',
    'Accept-Encoding': 'gzip, deflate, br',
}
headersOptions = {
    'Host': 'skl.hdu.edu.cn',
    'Origin': 'https://skl.hduhelp.com',
    'Access-Control-Request-Method': 'GET',
    'Content-Length': '0',
    'Access-Control-Request-Headers': 'x-auth-token',
    'Connection': 'keep-alive',
    'Accept': '*/*',
    'User-Agent': UA,
    'Referer': 'https://skl.hduhelp.com/',
    'Accept-Language': 'zh-cn',
    'Accept-Encoding': 'gzip, deflate, br',
}

# 加载现有答案
answer = loadAnswer()

# 今天所在的周
weekToday = datetime.datetime.now().isocalendar(
)[1]-datetime.date(2020, 9, 14).isocalendar()[1]+1
# 模仿真人访问 前摇（狗头
getWithOptions('https://skl.hdu.edu.cn/api/userinfo?type=')
getWithOptions('https://skl.hdu.edu.cn/api/course?startTime=' +
               str(get_current_week()))
time.sleep(random.randint(1, 4))
getWithOptions(
    'https://skl.hdu.edu.cn/api/paper/list?type=0&week=' + str(weekToday) + '&schoolYear=&semester=')

score = 0
while score != 100:
    # 拿练习卷
    paper = getWithOptions(
        'https://skl.hdu.edu.cn/api/paper/new?type=0&week=' + str(weekToday))

    try:
        paperId = paper.json()['paperId']
    except:
        print('请检查token，有可能已经过期')
        break

    # 准备答案
    paperUploaded = {}
    paperUploaded['paperId'] = paperId
    listTemp = []
    temp = {}
    recordedAnswer = 0  # 记录当前数据库中有题目答案的数量
    for paperDelail in paper.json()['list']:
        temp['paperDetailId'] = paperDelail['paperDetailId']
        temp['input'] = 'A'
        if paperDelail['title'] in answer:
            if paperDelail['answerA'] in answer[paperDelail['title']]:
                temp['input'] = 'A'
                recordedAnswer = recordedAnswer + 1
            if paperDelail['answerB'] in answer[paperDelail['title']]:
                temp['input'] = 'B'
                recordedAnswer = recordedAnswer + 1
            if paperDelail['answerC'] in answer[paperDelail['title']]:
                temp['input'] = 'C'
                recordedAnswer = recordedAnswer + 1
            if paperDelail['answerD'] in answer[paperDelail['title']]:
                temp['input'] = 'D'
                recordedAnswer = recordedAnswer + 1
        # 下面做一下转换处理 保证字典成功加入数组
        tempStr = str(temp)
        _temp = eval(tempStr)
        listTemp.append(_temp)
    paperUploaded['list'] = listTemp
    print('当前题库覆盖率：' + str(recordedAnswer) + '%')
    # print(paperUploaded)

    if setting['fastMode'] == 0:
        time.sleep(random.randint(1, 5))

    # 提交卷子
    r = postWithOptions('https://skl.hdu.edu.cn/api/paper/save', paperUploaded)
    score = r.json()['mark']
    print('本次得分' + str(score))

    # 抓答案
    answerRecived = getWithOptions(
        'https://skl.hdu.edu.cn/api/paper/detail?paperId=' + paperId).json()
    for _answer in answerRecived['list']:
        _temp = []
        if _answer['title'] in answer:
            if _answer['answer'+_answer['answer']] in answer[_answer['title']]:
                # 如果答案已经登记
                continue
            _temp = answer[_answer['title']]  # 读出已有的答案列表
        _temp.append(_answer['answer'+_answer['answer']])  # 取出答案
        answer[_answer['title']] = _temp
    print('当前已收录答案数量：' + str(len(answer)))
    saveAnswer(answer)
