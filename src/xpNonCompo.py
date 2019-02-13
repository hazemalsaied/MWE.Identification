# from rsg import *
import config
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
    config.setOptimalRSGForMLP()
    configuration['sampling'].update({
        'importantSentences': False,
        'overSampling': False,
        'sampleWeight': False,
        'focused': False})
    xp(allSharedtask2Lang, Dataset.sharedtask2, None, Evaluation.fixedSize, seeds=[0], xpNum=3)


def evaluateST2EnFixed():
    config.setOptimalRSGForMLP()
    xp(allSharedtask2Lang, Dataset.sharedtask2, None, Evaluation.fixedSize, seeds=range(2))


def evaluateFTB():
    config.setOptimalRSGForMLP()
    xp(['FR'], Dataset.ftb, None, Evaluation.corpus, seeds=range(2))
    xp(['FR'], Dataset.ftb, None, Evaluation.fixedSize, seeds=range(2))
    config.setOptimalRSGForMLPTendance()
    xp(['FR'], Dataset.ftb, None, Evaluation.corpus, seeds=range(2))
    xp(['FR'], Dataset.ftb, None, Evaluation.fixedSize, seeds=range(2))


def evaluateDiMSUM():
    config.setOptimalRSGForMLP()
    xp(['EN'], Dataset.dimsum, None, Evaluation.corpus, seeds=range(2))
    xp(['EN'], Dataset.dimsum, None, Evaluation.dev, seeds=range(2))
    config.setOptimalRSGForMLPTendance()
    xp(['EN'], Dataset.dimsum, None, Evaluation.corpus, seeds=range(2))
    xp(['EN'], Dataset.dimsum, None, Evaluation.dev, seeds=range(2))


def evaluateCoop():
    # hours: 8
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

    evaluateFTB()
    evaluateDiMSUM()
    # configuration['tmp']['dontParse'] = True
    # xp(['FR'], Dataset.sharedtask2, XpMode.multitasking, None, seeds=range(1))
    # import config
    # config.setOptimalRSGForMLP()
    # xp(allSharedtask2Lang, Dataset.sharedtask2, None, Evaluation.fixedSize, seeds=range(2))
    # generateOarsub(xpNum=5, duration=30, tourNum=2, name='compo.rnn')
    # tuneCompoRnn()
    # tuneWithFB()

    # A. resamplingEffect()
    # B. evaluateST2EnFixed()
    # C. evaluateFTB()
    #    evaluateDiMSUM()
    # xp(allSharedtask2Lang[7:], Dataset.sharedtask2, None, Evaluation.corpus, seeds=range(2), mlpInLinear=True)
    # xp(allSharedtask2Lang[12:], Dataset.sharedtask2, None, Evaluation.fixedSize, seeds=range(2), mlpInLinear=True)
    # F. xp(allSharedtask2Lang, Dataset.sharedtask2, None, Evaluation.corpus, seeds=range(2), linearInMlp=True)
    # G. xp(allSharedtask2Lang, Dataset.sharedtask2, None, Evaluation.fixedSize, seeds=range(2), linearInMlp=True)
    # H. tuneWithFB()

    # xp(['FR'], Dataset.sharedtask2, None, None, seeds=range(1), linearInMlp=True)

    # xp(['FR'], Dataset.sharedtask2, XpMode.multitasking, None, seeds=range(1), complentary=False)

    # generateOarsub(xpNum=5, duration=20, tourNum=1, name='mlp.fb')
    # xp(['EN'], Dataset.dimsum, XpMode.linear, Evaluation.corpus)
    # setOptimalRSGFeaturesForFtbSVM()
    # xp(['FR'], Dataset.ftb, XpMode.linear, Evaluation.corpus)

    # import rsg
    # configuration['mlp']['trainable'] = False
    # configuration['tmp']['tunePretrained'] = True
    # rsg.runRSGSpontaneously(['BG'], Dataset.sharedtask2, None, Evaluation.fixedSize,
    #                           seeds=range(2), xpNum=1, xpNumByThread=150)
    # rsg.runRSGSpontaneously(pilotLangs, Dataset.sharedtask2, XpMode.compoRnn, Evaluation.fixedSize,
    #                         seeds=range(2), xpNum=1, xpNumByThread=200)

    # Ev.linInMLP
    # configuration['mlp'].update({
    #     'posEmb': 78,
    #     'tokenEmb': 327,
    #     'dense1UnitNumber': 113,
    #     'dense1Dropout': 0.25,
    # })
    # xp(allSharedtask2Lang, Dataset.sharedtask2, None, Evaluation.corpus, linearInMlp=True)
    # NoSampling5
    # setOptimalRSGForMLP()
    # configuration['sampling'].update({
    #     'importantSentences': False,
    #     'overSampling': False,
    #     'sampleWeight': False,
    #     'favorisationCoeff': 6,
    #     'focused': False})
    # xp(allSharedtask2Lang, Dataset.sharedtask2, None, Evaluation.corpus, xpNum=10)
