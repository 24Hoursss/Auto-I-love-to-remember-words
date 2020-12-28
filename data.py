localPath = '.'


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
