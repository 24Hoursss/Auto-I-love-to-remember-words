import os


def saveAnswer(dic):
    saveDict(dic, '.\\awsNew.txt')


def loadAnswer():
    path = '.\\awsNew.txt'
    if not os.path.exists(path):
        print('题库文件不存在，即将创建')
        saveAnswer({})
        print('创建完成')
    return loadDict(path)


def loadSetting():
    return loadDict('.\\setting.txt')


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
