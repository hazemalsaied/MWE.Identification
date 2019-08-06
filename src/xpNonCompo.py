# from rsg import *
from config import TrendConfig, BestConfig, LinearConf
from xpTools import *
from identification import getST1TrainFiles

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


def getPOSTagEffect():
    """
        On Parseme 1.0 in cross validation with golden and
        automatically predicted version of pos tags
    """
    LinearConf.setMinimalFeatures()
    # configuration['others']['autoData'] = False
    # xp(['HU', 'PL', 'CS'], None, XpMode.linear, Evaluation.cv)
    configuration['others']['autoData'] = True
    # , 'CS'
    xp(['HU', 'PL'], None, XpMode.linear, Evaluation.cv)


def resamplingEffect():
    BestConfig.mlp()
    configuration['sampling'].update({
        'importantSentences': False,
        'overSampling': False,
        'sampleWeight': False,
        'focused': False})
    xp(allSharedtask2Lang, Dataset.sharedtask2, None, Evaluation.corpus, seeds=[0, 1], xpNum=3, outputCupt=False)
    TrendConfig.mlp()
    configuration['sampling'].update({
        'importantSentences': False,
        'overSampling': False,
        'sampleWeight': False,
        'focused': False})
    xp(allSharedtask2Lang, Dataset.sharedtask2, None, Evaluation.corpus, seeds=[0, 1], xpNum=3, outputCupt=False)


def evaluateST2EnFixed():
    BestConfig.mlp()
    xp(allSharedtask2Lang, Dataset.sharedtask2, None, Evaluation.fixedSize, seeds=range(2))


def evaluateFTB():
    BestConfig.mlp()
    xp(['FR'], Dataset.ftb, None, Evaluation.corpus, seeds=range(2))
    xp(['FR'], Dataset.ftb, None, Evaluation.fixedSize, seeds=range(2))
    TrendConfig.mlp()
    xp(['FR'], Dataset.ftb, None, Evaluation.corpus, seeds=range(2))
    xp(['FR'], Dataset.ftb, None, Evaluation.fixedSize, seeds=range(2))
    BestConfig.mlpOpen()
    xp(['FR'], Dataset.ftb, None, Evaluation.corpus, seeds=range(2))
    xp(['FR'], Dataset.ftb, None, Evaluation.fixedSize, seeds=range(2))


def evaluateDiMSUM():
    BestConfig.mlp()
    xp(['EN'], Dataset.dimsum, None, Evaluation.corpus, seeds=range(2))
    # xp(['EN'], Dataset.dimsum, None, Evaluation.dev, seeds=range(2))
    TrendConfig.mlp()
    xp(['EN'], Dataset.dimsum, None, Evaluation.corpus, seeds=range(2))
    # xp(['EN'], Dataset.dimsum, None, Evaluation.dev, seeds=range(2))
    BestConfig.mlpOpen()
    xp(['EN'], Dataset.dimsum, None, Evaluation.corpus, seeds=range(2))
    # xp(['EN'], Dataset.dimsum, None, Evaluation.dev, seeds=range(2))


def evaluateDiMSUMAfterTunning():
    BestConfig.mlpDimsum()
    xp(['EN'], Dataset.dimsum, None, Evaluation.corpus, seeds=range(2))
    # xp(['EN'], Dataset.dimsum, None, Evaluation.dev, seeds=range(2))
    TrendConfig.mlpDimsum()
    xp(['EN'], Dataset.dimsum, None, Evaluation.corpus, seeds=range(2))
    # xp(['EN'], Dataset.dimsum, None, Evaluation.dev, seeds=range(2))
    BestConfig.mlpDimsum()
    configuration['mlp']['tokenEmb'] = 300
    configuration['embedding']['pretrained'] = True
    xp(['EN'], Dataset.dimsum, None, Evaluation.corpus, seeds=range(2))
    # xp(['EN'], Dataset.dimsum, None, Evaluation.dev, seeds=range(2))


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
    rsg.runRSGSpontaneously(['BG'], Dataset.sharedtask2, XpMode.rmlpTree, Evaluation.fixedSize,
                            seeds=range(1), xpNum=1, xpNumByThread=50)


def evaluateMultitasking(langs=allSharedtask2Lang, division=Evaluation.trainVsDev):
    evaluatePosInMultitasking(langs, division)
    evaluateIdenInMultitasking(langs, division)
    evaluateJointIdent(langs, division)


def evaluatePosInMultitasking(langs=allSharedtask2Lang, division=Evaluation.trainVsDev):
    configuration['tmp']['trainJointly'] = False
    configuration['tmp']['trainIden'] = False

    BestConfig.mtPos()
    xp(langs, Dataset.sharedtask2,
       XpMode.multitasking, division, seeds=[0])

    TrendConfig.mtPos()
    xp(langs, Dataset.sharedtask2,
       XpMode.multitasking, division, seeds=[0])


def evaluateIdenInMultitasking(langs=allSharedtask2Lang, division=Evaluation.trainVsDev):
    configuration['others']['analyzePerformance'] = True
    configuration['tmp']['trainJointly'] = False
    configuration['tmp']['trainIden'] = True

    BestConfig.mtIdent()
    xp(langs, Dataset.sharedtask2,
       XpMode.multitasking, division, seeds=[0])

    TrendConfig.mtIden()
    xp(langs, Dataset.sharedtask2,
       XpMode.multitasking, division, seeds=[0])


def evaluateJointIdent(langs=allSharedtask2Lang, division=Evaluation.trainVsDev):
    configuration['others']['analyzePerformance'] = True
    configuration['tmp']['trainIden'] = False
    configuration['tmp']['trainJointly'] = True

    BestConfig.mtJoint()
    xp(langs, Dataset.sharedtask2,
       XpMode.multitasking, division, seeds=[0])

    TrendConfig.mtJoint()
    xp(langs, Dataset.sharedtask2,
       XpMode.multitasking, division, seeds=[0])


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


def evaluateMLPPhrase():
    configuration['others']['analyzePerformance'] = True
    configuration['tmp']['createDepGraphs'] = False
    # BestConfig.mlpPhrase()
    # xp(allSharedtask2Lang, Dataset.sharedtask2, XpMode.mlpPhrase, Evaluation.trainVsDev, seeds=range(1))
    TrendConfig.mlpPhrase()
    xp(allSharedtask2Lang, Dataset.sharedtask2, XpMode.mlpPhrase, Evaluation.trainVsDev, seeds=range(1))
    BestConfig.mlpPhrase()
    xp(allSharedtask2Lang, Dataset.sharedtask2, XpMode.mlpPhrase, Evaluation.corpus, seeds=range(1))
    TrendConfig.mlpPhrase()
    xp(allSharedtask2Lang, Dataset.sharedtask2, XpMode.mlpPhrase, Evaluation.corpus, seeds=range(1))


def evaluateMLPWide():
    configuration['others']['analyzePerformance'] = True
    configuration['tmp']['createDepGraphs'] = False
    BestConfig.mlpWide()
    xp(allSharedtask2Lang, Dataset.sharedtask2, XpMode.mlpWide, Evaluation.trainVsDev, seeds=range(1))
    TrendConfig.mlpWide()
    xp(allSharedtask2Lang, Dataset.sharedtask2, XpMode.mlpWide, Evaluation.trainVsDev, seeds=range(1))
    BestConfig.mlpWide()
    xp(allSharedtask2Lang, Dataset.sharedtask2, XpMode.mlpWide, Evaluation.corpus, seeds=range(1))
    TrendConfig.mlpWide()
    xp(allSharedtask2Lang, Dataset.sharedtask2, XpMode.mlpWide, Evaluation.corpus, seeds=range(1))


def evaluateMLPWideOnClosed():
    configuration['others']['analyzePerformance'] = True
    configuration['tmp']['createDepGraphs'] = False
    BestConfig.mlpWide()
    configuration['embedding']['pretrained'] = False
    xp(allSharedtask2Lang, Dataset.sharedtask2, XpMode.mlpWide, Evaluation.trainVsDev, seeds=range(1))
    TrendConfig.mlpWide()
    configuration['embedding']['pretrained'] = False
    xp(allSharedtask2Lang, Dataset.sharedtask2, XpMode.mlpWide, Evaluation.trainVsDev, seeds=range(1))
    BestConfig.mlpWide()
    configuration['embedding']['pretrained'] = False
    xp(allSharedtask2Lang, Dataset.sharedtask2, XpMode.mlpWide, Evaluation.corpus, seeds=range(1))
    TrendConfig.mlpWide()
    configuration['embedding']['pretrained'] = False
    xp(allSharedtask2Lang, Dataset.sharedtask2, XpMode.mlpWide, Evaluation.corpus, seeds=range(1))



if __name__ == '__main__':
    reload(sys)
    sys.setdefaultencoding('utf8')

    getST1TrainFiles()
    # rmlpTree
    # import rsg
    # configuration['others']['analyzePerformance'] = False
    # rsg.runRSGSpontaneously(pilotLangs, Dataset.sharedtask2, XpMode.rmlpTree, Evaluation.fixedSize, xpNumByThread=200)

    # rmlp
    # import rsg
    # configuration['others']['analyzePerformance'] = False
    # rsg.runRSGSpontaneously(pilotLangs, Dataset.sharedtask2, XpMode.rmlp, Evaluation.fixedSize, xpNumByThread=200)

    # configuration['embedding']['pretrained'] = False
    # configuration['tmp']['trainJointly'] = True
    # configuration['nn']['jointLearningEpochs'] = 10
    # xp(['FR'], Dataset.sharedtask2, XpMode.multitasking, None) # Evaluation.trainVsDev


