from fuckWords import FuckWords
import random

headers = {
    'Accept': 'application/json, text/plain, */*',
    'Accept - Encoding': 'gzip, deflate, br',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Connection': 'keep-alive',
    'Host': 'skl.hdu.edu.cn',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'cross-site',
    'Origin': 'https://skl.hduhelp.com',
    'Referer': 'https://skl.hduhelp.com/',
    'X-Auth-Token' : token,
    'User-Agent': UA,
}
headersOptions = {
#i don't know
}

if __name__ == '__main__':
    setting = data.loadSetting()
    token = setting['token']
    UA = setting['UA']
    targetscore = setting['targetscore']
    stu = FuckWords(token, UA=UA)
    exam_time = random.uniform(460,470)