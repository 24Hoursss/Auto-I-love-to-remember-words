import httpx
import datetime
import time
import random

import data


class FuckWords:
    def __init__(self, token, UA='FuckWords'):
        self.token = token
        self.headers = {
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
        self.headersOptions = {
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
        self.firstRun = 1  # 第一次访问（有options操作

    def get_current_week(self):
        # 返回当前的星期一和星期天的日期
        monday = datetime.date.today()
        one_day = datetime.timedelta(days=1)
        while monday.weekday() != 0:
            monday -= one_day
        return monday

    def getWithOptions(self, url):
        try:
            httpx.options(url, headers=self.headersOptions)
            return httpx.get(url, headers=self.headers)
        except:
            return self.getWithOptions(url)

    def postWithOptions(self, url, json):
        try:
            httpx.options(url, headers=self.headersOptions)
            return httpx.post(url, headers=self.headers, json=json)
        except:
            return self.postWithOptions(url, json)

    def practice(self, timeDelay=470, score=100):
        # 返回：状态码，得分
        if self.firstRun:
            # 今天所在的周
            weekToday = datetime.datetime.now().isocalendar(
            )[1]-datetime.date(2020, 9, 14).isocalendar()[1]+1
            # 模仿真人访问 前摇（狗头
            self.getWithOptions('https://skl.hdu.edu.cn/api/userinfo?type=')
            self.getWithOptions('https://skl.hdu.edu.cn/api/course?startTime=' +
                                str(self.get_current_week()))
            time.sleep(random.randint(1, 4)/2.0)
            self.getWithOptions(
                'https://skl.hdu.edu.cn/api/paper/list?type=0&week=' + str(weekToday) + '&schoolYear=&semester=')

        # 拿练习卷
        paper = self.getWithOptions(
            'https://skl.hdu.edu.cn/api/paper/new?type=0&week=' + str(weekToday))

        try:
            paperId = paper.json()['paperId']
        except:
            print('请检查token，有可能已经过期')
            return 1, 0

        # 准备答案
        answer = data.loadAnswer()
        paperUploaded = {}
        paperUploaded['paperId'] = paperId
        listTemp = []
        temp = {}
        recordedAnswer = 0  # 记录当前数据库中有题目答案的数量
        for paperDelail in paper.json()['list']:
            temp['paperDetailId'] = paperDelail['paperDetailId']
            temp['input'] = 'Z'  # 用Z来标记答案未知
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

        if recordedAnswer < score:
            print('当前题库完整度不足，可能无法达到预期分数，如有需要，请运行学习程序扩充题库（练习状态自动扩充题库）')
        elif recordedAnswer != 100 and recordedAnswer >= score:
            print('当前题库完整度可以达到预期分数或超出预期分数，但无法保证准确分数')
        elif recordedAnswer == 100:
            print('当前题库完整度已经可以覆盖本次测试所有题目')
        if recordedAnswer > score:
            print('当前分数高于目标分数，即将进行降分')
            changedList = []  # 记录已经改变过的题目
            while recordedAnswer-score != 0:
                randomNum = random.randint(0, 99)
                if randomNum not in changedList and paperUploaded['list'][randomNum]['input'] != 'Z':
                    _word = paperUploaded['list'][randomNum]['input']
                    paperUploaded['list'][randomNum]['input'] = chr(
                        (ord(_word)-ord('A')+random.randint(1, 3)) % 4+ord('A'))
                    recordedAnswer = recordedAnswer-1
                changedList.append(randomNum)
            print('降分完成 一看就是老演员了')

        # 将所有未知答案的题目做一下处理
        for _temp in paperUploaded['list']:
            if _temp['input'] == 'Z':
                _temp['input'] = 'A'
        for i in range(timeDelay):
            print('\r剩余等待时间：'+str(timeDelay-i)+'s', end='')
            time.sleep(1)
        print()
        # 提交卷子
        r = self.postWithOptions(
            'https://skl.hdu.edu.cn/api/paper/save', paperUploaded)
        score = r.json()['mark']
        print('本次得分' + str(score))

        # 抓答案
        answerRecived = self.getWithOptions(
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
        data.saveAnswer(answer)
        return 0, score
