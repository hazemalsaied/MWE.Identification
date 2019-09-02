from corpus import *
from xpTools import xp, XpMode
from config import Generator

def runRSGSpontaneously(langs, dataset, xpMode, division,
                        seeds=[0], xpNumByThread=50, xpNum=1,
                        mlpInLinear=False,
                        linearInMlp=False,
                        complentary=False,
                        dontParse=False):
    configs = []
    for i in range(xpNumByThread):
        generateConf(xpMode)
        configs.append(copy.deepcopy(configuration))
    for i in range(xpNumByThread):
        configuration.update(configs[i])

        # configuration['multitasking'].update({
        #     'useCapitalization': False,
        #     'useSymbols': True,
        #     'useB1': True,
        #     'useBx': True,
        # })
        if dontParse:
            configuration['tmp']['dontParse'] = True
        xp(langs, dataset, xpMode, division, xpNum=xpNum, seeds=seeds,
           mlpInLinear=mlpInLinear, linearInMlp=linearInMlp,
           complentary=complentary, outputCupt=False)


def runRSG(langs, dataset, xpMode, division, fileName,
           xpNumByThread=50, xpNum=1,
           mlpInLinear=False,
           linearInMlp=False,
           complentary=False):
    exps = getGrid(fileName)
    threadConf = []
    for i in range(len(exps)):
        exp = exps[i]
        if not exp[0]:
            for j in range(i, i + xpNumByThread):
                exps[j][0] = True
                threadConf.append(exps[j][1])
            break
    with open(os.path.join(configuration['path']['projectPath'], 'ressources/RSG', fileName), 'wb') as ff:
        pickle.dump(exps, ff)
    for i in range(len(threadConf)):
        configuration.update(threadConf[i])
        xp(langs, dataset, xpMode, division, xpNum=xpNum,
           mlpInLinear=mlpInLinear, linearInMlp=linearInMlp,
           complentary=complentary)

def generateConf(xpMode):
    if xpMode == XpMode.rmlp:
        Generator.rmlp()
    elif xpMode == XpMode.linear:
        Generator.svm()
    elif xpMode == XpMode.kiperwasser:
        Generator.kiper()
    elif xpMode == XpMode.rmlpTree:
        Generator.rmlpTree()
    elif xpMode == XpMode.multitasking:
        Generator.mt()
    elif xpMode == XpMode.mlpPhrase:
        Generator.mlpPhrase()
    elif xpMode == XpMode.chenManning:
        Generator.chenManning()
    else:
        if configuration['tmp']['tunePretrained']:
            Generator.mlpOpen()
        else:
            Generator.mlp()


def createRSG(fileName, xpMode, xpNum=1000):
    resultDic = dict()
    for i in range(xpNum):
        generateConf(xpMode)
        resultDic[i] = [False, copy.deepcopy(configuration)]
        # resultDic[0] == resultDic[1]:
    pickle.dump(resultDic, open(os.path.join(configuration['path']['projectPath'],'ressources/RSG', fileName), 'wb'))


def getGrid(fileName):
    randomSearchGridPath = os.path.join(configuration['path']['projectPath'], 'ressources/RSG', fileName)
    with open(randomSearchGridPath, 'rb') as ff:
        xps = pickle.load(ff)
        return xps





def hasCloseValue(value, generatedValues, step=0.001):
    for v in generatedValues:
        if abs(v - value) <= step:
            return True
    return False


def generateValueWithFavorisation(plage, importantPlage, favorisationRate=60, continousPlage=False):
    useImportantPlage = random.randint(0, 100) < favorisationRate
    if useImportantPlage:
        if continousPlage:
            return random.uniform(importantPlage[0], importantPlage[-1])
        else:
            return importantPlage[random.randint(0, len(importantPlage) - 1)]
    else:
        if continousPlage:
            leftRange = [plage[0], importantPlage[0]]
            leftRangeLegth = importantPlage[0] - plage[0]
            rightRange = [importantPlage[-1], plage[-1]]
            rightRangeLenght = plage[-1] - importantPlage[-1]
            percentage = (float(leftRangeLegth) / (leftRangeLegth + rightRangeLenght))
            useLeftRange = random.uniform(0, 1) < percentage
            return random.uniform(leftRange[0], leftRange[-1]) if useLeftRange else \
                random.uniform(rightRange[0], rightRange[-1])

        else:
            for item in importantPlage:
                plage.remove(item)
            return plage[random.randint(0, len(plage) - 1)]


def createLRGrid(xpNum=150):
    lrs = dict()
    for i in range(xpNum):
        while True:
            lr = round(Generator.generateValue([.001, .2], True, True), 3)
            if lr not in lrs.keys() and not hasCloseValue(lr, lrs):
                lrs[lr] = False
                break
    pickle.dump(lrs, open(os.path.join(configuration['path']['projectPath'],
                                       'ressources/RSG', 'lrGrid.p'), 'wb'))
