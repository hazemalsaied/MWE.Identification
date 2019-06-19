# from rsg import *
import config
from config import setMLPConf, setMlpOpenConf, setMlpTendanceConf, \
    setBestMTConfForIden, setBestMTConfForJoint, setBestMTConfForPOS, \
    setTrendMTConfForIden, setTrendMTConfForJoint, setTrendMTConfForPOS
from xpTools import *


def debug():
    configuration['embedding'].update({
        'manual': True,
        'keras': False,
        'pretrained': True,
        'average': True,
        'lemma': False,
        'compactVocab': True,
        'dynamicVocab': False,
        'useB-1': 1,
        'useB1': 1,
    })
    configuration['sampling'].update({
        'sampleWeight': True,
        'favorisationCoeff': 1,
        'focused': True,
        'overSampling': True,
        'importantSentences': True,
        'importantTransitions': False,
        'mweRepeition': 30
    })

    configuration['mlp'].update({
        'batchSize': 64,
        'dense1Dropout': .5,
        'dense1UnitNumber': 280,
        'lr': 0.193,
        'posEmb': 43,
        'tokenEmb': 300,
        'trainable': True,

    })
    configuration['others']['debugTrainNum'] = 50
    configuration['others']['debugOnDev'] = False

    xp(['FR'], Dataset.sharedtask2, None, None)


def generateOarsub(xpNum=21, duration=100, tourNum=1, name='mlp'):
    for i in range(1, xpNum + 1):
        sys.stdout.write('oarsub -p "GPU_MODEL <> \'NO\'" -q production -l nodes=1,walltime={0} '
                         '"NNIdenSys/Scripts/nonCompo.sh" -n {3}{1}.{2} '
                         '-O Reports/{3}{1}.{2} -E Reports/{3}{1}.{2}\n'.
                         format(duration, tourNum, i, name))


def getPOSTagEffect():
    """
        On Parseme 1.0 in cross validation with golden and
        automatically predicted version of pos tags
    """
    config.setMinimalFeatures()
    # configuration['others']['autoData'] = False
    # xp(['HU', 'PL', 'CS'], None, XpMode.linear, Evaluation.cv)
    configuration['others']['autoData'] = True
    # , 'CS'
    xp(['HU', 'PL'], None, XpMode.linear, Evaluation.cv)


def resamplingEffect():
    setMLPConf()
    configuration['sampling'].update({
        'importantSentences': False,
        'overSampling': False,
        'sampleWeight': False,
        'focused': False})
    xp(allSharedtask2Lang, Dataset.sharedtask2, None, Evaluation.corpus, seeds=[0, 1], xpNum=3, outputCupt=False)
    setMlpTendanceConf()
    configuration['sampling'].update({
        'importantSentences': False,
        'overSampling': False,
        'sampleWeight': False,
        'focused': False})
    xp(allSharedtask2Lang, Dataset.sharedtask2, None, Evaluation.corpus, seeds=[0, 1], xpNum=3, outputCupt=False)


def evaluateST2EnFixed():
    setMLPConf()
    xp(allSharedtask2Lang, Dataset.sharedtask2, None, Evaluation.fixedSize, seeds=range(2))


def evaluateFTB():
    setMLPConf()
    xp(['FR'], Dataset.ftb, None, Evaluation.corpus, seeds=range(2))
    xp(['FR'], Dataset.ftb, None, Evaluation.fixedSize, seeds=range(2))
    setMlpTendanceConf()
    xp(['FR'], Dataset.ftb, None, Evaluation.corpus, seeds=range(2))
    xp(['FR'], Dataset.ftb, None, Evaluation.fixedSize, seeds=range(2))
    setMlpOpenConf()
    xp(['FR'], Dataset.ftb, None, Evaluation.corpus, seeds=range(2))
    xp(['FR'], Dataset.ftb, None, Evaluation.fixedSize, seeds=range(2))


def evaluateDiMSUM():
    setMLPConf()
    xp(['EN'], Dataset.dimsum, None, Evaluation.corpus, seeds=range(2))
    xp(['EN'], Dataset.dimsum, None, Evaluation.dev, seeds=range(2))
    setMlpTendanceConf()
    xp(['EN'], Dataset.dimsum, None, Evaluation.corpus, seeds=range(2))
    xp(['EN'], Dataset.dimsum, None, Evaluation.dev, seeds=range(2))
    setMlpOpenConf()
    xp(['EN'], Dataset.dimsum, None, Evaluation.corpus, seeds=range(2))
    xp(['EN'], Dataset.dimsum, None, Evaluation.dev, seeds=range(2))


def evaluateCoop():
    xp(allSharedtask2Lang, Dataset.sharedtask2, None, Evaluation.corpus, seeds=range(2), mlpInLinear=True)
    xp(allSharedtask2Lang, Dataset.sharedtask2, None, Evaluation.fixedSize, seeds=range(2), mlpInLinear=True)

    xp(allSharedtask2Lang, Dataset.sharedtask2, None, Evaluation.corpus, seeds=range(2), linearInMlp=True)
    xp(allSharedtask2Lang, Dataset.sharedtask2, None, Evaluation.fixedSize, seeds=range(2), linearInMlp=True)

    xp(allSharedtask2Lang, Dataset.sharedtask2, None, Evaluation.corpus, seeds=range(2), complentary=True)
    xp(allSharedtask2Lang, Dataset.sharedtask2, None, Evaluation.fixedSize, seeds=range(2), complentary=True)


def tuneWithFB():
    import rsg
    configuration['mlp']['trainable'] = False
    configuration['tmp']['tunePretrained'] = True
    rsg.runRSGSpontaneously(['BG'], Dataset.sharedtask2, None, Evaluation.fixedSize,
                            seeds=range(2), xpNum=1, xpNumByThread=200)


def tuneCompoRnn():
    import rsg
    rsg.runRSGSpontaneously(['BG'], Dataset.sharedtask2, XpMode.compoRnn, Evaluation.fixedSize,
                            seeds=range(1), xpNum=1, xpNumByThread=50)


def evaluateMultitasking(langs=allSharedtask2Lang, division=Evaluation.trainVsDev):
    evaluatePosInMultitasking(langs, division)
    evaluateIdenInMultitasking(langs, division)
    evaluateJointIdent(langs, division)


def evaluatePosInMultitasking(langs=allSharedtask2Lang, division=Evaluation.trainVsDev):
    configuration['tmp']['trainJointly'] = False
    configuration['tmp']['trainIden'] = False

    setBestMTConfForPOS()
    xp(langs, Dataset.sharedtask2,
       XpMode.multitasking, division, seeds=[0])

    setTrendMTConfForPOS()
    xp(langs, Dataset.sharedtask2,
       XpMode.multitasking, division, seeds=[0])


def evaluateIdenInMultitasking(langs=allSharedtask2Lang, division=Evaluation.trainVsDev):
    configuration['others']['analyzePerformance'] = True
    configuration['tmp']['trainJointly'] = False
    configuration['tmp']['trainIden'] = True

    setBestMTConfForIden()
    xp(langs, Dataset.sharedtask2,
       XpMode.multitasking, division, seeds=[0])

    setTrendMTConfForIden()
    xp(langs, Dataset.sharedtask2,
       XpMode.multitasking, division, seeds=[0])


def evaluateJointIdent(langs=allSharedtask2Lang, division=Evaluation.trainVsDev):
    configuration['others']['analyzePerformance'] = True
    configuration['tmp']['trainIden'] = False
    configuration['tmp']['trainJointly'] = True

    setBestMTConfForJoint()
    xp(langs, Dataset.sharedtask2,
       XpMode.multitasking, division, seeds=[0])

    setTrendMTConfForJoint()
    xp(langs, Dataset.sharedtask2,
       XpMode.multitasking, division, seeds=[0])


def depParse():
    from depBaselineParser import parse
    initXp(XpMode.linear, Dataset.sharedtask2, Evaluation.trainVsDev, None, None)  # Evaluation.trainVsDev
    for l in allSharedtask2Lang:
        if l != 'LT':
            parse(l)


def createConllFiles(langs=allSharedtask2Lang):
    for l in langs:
        datasetConf, pathConf = configuration['dataset'], configuration['path']
        sharedtaskVersion = '.2'
        path = os.path.join(pathConf['projectPath'], pathConf['corpusFolder'] + sharedtaskVersion, l)
        for p in ['train.cupt', 'dev.cupt', 'test.cupt']:
            allPath = os.path.join(path, p)
            if os.path.exists(allPath):
                conll = cuptToConllU(allPath)
                pp = p.replace('cupt', 'conll')
                with open(os.path.join(path, pp), 'w') as ff:
                    ff.write(conll)


if __name__ == '__main__':
    reload(sys)
    sys.setdefaultencoding('utf8')
    # evaluateIdenInMultitasking()
    # evaluateJointIdent() # ['FR'], None)
    # configuration['others']['analyzePerformance'] = True
    #
    # configuration['tmp']['createDepGraphs'] = False
    # evaluateMultitasking(['FR'], None)

    # configuration['tmp']['trainIden'] = False
    # configuration['tmp']['trainJointly'] = False
    # configuration['tmp']['trainDepParser'] = True
    generateOarsub(xpNum=10, duration=50, tourNum=1, name='mlpPhrase')
    import rsg

    configuration['others']['analyzePerformance'] = False
    rsg.runRSGSpontaneously(pilotLangs, Dataset.sharedtask2, XpMode.mlpPhrase, Evaluation.fixedSize,
                           seeds=[0], xpNumByThread=120)

    # rsg.def runRSGSpontaneously(['BG', 'PT', 'TR'], Dataset.sharedtask2,
    #                        XpMode.multitasking, Evaluation.fixedSize, [0],
    #                        xpNumByThread=300)
    # xp(['FR'], Dataset.sharedtask2, XpMode.multitasking, None)# Evaluation.trainVsDev)
    # xp(['FR'], Dataset.sharedtask2, XpMode.mlpPhrase, None)  # Evaluation.trainVsDev)
