import time
import random

import data
from fuckWords import FuckWords

if __name__ == '__main__':
    # 加载设置
    setting = data.loadSetting()
    token = setting['token']
    UA = setting['UA']
    stu = FuckWords(token, UA=UA)
    aimScore = random.randint(60, 85)  # 随机目标分数
    score = -1
    status = 1
    if setting['fastMode'] == 1:
        timeDelay = 1
    else:
        timeDelay = random.randint(465, 475)  # 随机做题时间

    while status == 1 or score != aimScore:
        status, score = stu.practice(timeDelay=timeDelay, score=aimScore)
