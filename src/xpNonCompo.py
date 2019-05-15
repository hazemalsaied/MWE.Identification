# from rsg import *
import config
from config import setMLPConf, setMlpOpenConf, setMlpTendanceConf, setSVMConf
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
        sys.stdout.write('oarsub -p "GPU<>\'NO\'" -q production -l nodes=1,walltime={0} '
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


if __name__ == '__main__':
    reload(sys)
    sys.setdefaultencoding('utf8')
    # generateOarsub(xpNum=5,duration=25,tourNum=1,name='mlp.dimsum')

    setSVMConf()
    xp(['TR'], Dataset.sharedtask2, XpMode.linear, Evaluation.corpus, seeds=[0], xpNum=1,
        outputCupt=True, title='')
    # setMlpTendanceConf()
    # configuration['sampling']['overSampling'] = False
    # configuration['sampling']['importantSentences'] = False
    # configuration['embedding']['pretrained'] = False
    # xp(allSharedtask2Lang, Dataset.sharedtask2, None, Evaluation.trainVsDev, seeds=[0], xpNum=1,
    #    outputCupt=True, title='tendy.closed.sampling')

    # configuration['tmp']['transOut'] = True
    # configuration['tmp']['markObligatory'] = False
    # configuration['tmp']['addTokens'] = False
    # setSVMConf()
    # configuration['tmp']['cleanSents'] = True
    # configuration['tmp']['onGroup'] = False
    # configuration['tmp']['group'] = 'tweebank'
    # # configuration['sampling']['overSampling'] = True
    # xp(['EN'], Dataset.dimsum, XpMode.linear, Evaluation.trainVsDev, seeds=[0], xpNum=1,
    #     outputCupt=False, title='tendy.sampling')

    # setMlpTendanceConf()
    # configuration['sampling']['importantSentences'] = False
    # configuration['sampling']['overSampling'] = False
    # xp(allSharedtask2Lang, Dataset.sharedtask2, None, Evaluation.trainVsDev, seeds=[0], xpNum=1,
    #    outputCupt=False, title='tendy.sampling')

    # import rsg
    # rsg.runRSGSpontaneously(['EN'], Dataset.dimsum, None, Evaluation.dev, seeds=range(1), xpNumByThread=500)

    # configuration['tmp']['dontParse'] = True
    # configuration['others']['debugTrainNum'] = 2000
    # xp(['FR'], Dataset.sharedtask2, XpMode.multitasking, None, seeds=range(1))
    # resamplingEffect()
    # setOptimalRSGForMLP()
    # xp(allSharedtask2Lang, Dataset.sharedtask2, None, Evaluation.fixedSize, seeds=range(1))
    # setOptimalRSGForMLPTendance()
    # xp(allSharedtask2Lang, Dataset.sharedtask2, None, Evaluation.fixedSize, seeds=range(1))
