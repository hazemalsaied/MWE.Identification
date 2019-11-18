#!/usr/bin/python

from config import TrendConfig, BestConfig, LinearConf
from xpTools import *
import sys, getopt

"""
Scrip used for running tuning and evaluation 
"""
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


def evaluateFTBAndDimSumInLinear():
    configuration['others']['analyzePerformance'] = True
    # GPP closed Svm
    LinearConf.svm()
    xp(['FR'], Dataset.ftb, XpMode.linear, Evaluation.trainVsDev)
    LinearConf.svmFtb()
    xp(['FR'], Dataset.ftb, XpMode.linear, Evaluation.trainVsDev)
    LinearConf.svm()
    xp(['EN'], Dataset.dimsum, XpMode.linear, Evaluation.trainVsDev)
    LinearConf.svmDiMSUM()
    xp(['EN'], Dataset.dimsum, XpMode.linear, Evaluation.trainVsDev)


def evaluateFTB():
    configuration['others']['analyzePerformance'] = True
    # Before
    # GPP closed Svm
    # LinearConf.svm()
    # xp(['FR'], Dataset.ftb, XpMode.linear, Evaluation.corpus)
    # # GPP closed
    # BestConfig.mlp()
    # xp(['FR'], Dataset.ftb, None, Evaluation.corpus)
    # BestConfig.mlpOpen()
    # # GPP Open
    # xp(['FR'], Dataset.ftb, None, Evaluation.corpus)
    # # GT Open
    # TrendConfig.mlp()
    # xp(['FR'], Dataset.ftb, None, Evaluation.corpus)
    # # GT Closed
    # TrendConfig.mlp()
    # configuration['embedding']['pretrained'] = False
    # xp(['FR'], Dataset.ftb, None, Evaluation.corpus)

    # after
    # GPP closed Svm
    LinearConf.svmFtb()
    xp(['FR'], Dataset.ftb, XpMode.linear, Evaluation.trainVsDev)
    # GPP closed
    BestConfig.mlpFtbClosed()
    xp(['FR'], Dataset.ftb, None, Evaluation.trainVsDev)
    BestConfig.mlpFtbOpen()
    xp(['FR'], Dataset.ftb, None, Evaluation.trainVsDev)
    TrendConfig.mlpFtb()
    xp(['FR'], Dataset.ftb, None, Evaluation.trainVsDev)
    # TrendConfig.mlpFtb()
    # configuration['embedding']['pretrained'] = False
    # xp(['FR'], Dataset.ftb, None, Evaluation.trainVsDev)


def evaluateDiMSUM():
    configuration['others']['analyzePerformance'] = True
    # Before
    # GPP closed Svm
    # LinearConf.svm()
    # xp(['EN'], Dataset.dimsum, None, Evaluation.corpus)
    # # GPP closed
    # BestConfig.mlp()
    # xp(['EN'], Dataset.dimsum, None, Evaluation.corpus)
    # BestConfig.mlpOpen()
    # # GPP Open
    # xp(['EN'], Dataset.dimsum, None, Evaluation.corpus)
    # # GT Open
    # TrendConfig.mlp()
    # xp(['EN'], Dataset.dimsum, None, Evaluation.corpus)
    # # GT Closed
    # TrendConfig.mlp()
    # configuration['embedding']['pretrained'] = False
    # xp(['EN'], Dataset.dimsum, None, Evaluation.corpus)

    # after
    # GPP closed Svm
    LinearConf.svmDiMSUM()
    xp(['EN'], Dataset.dimsum, XpMode.linear, Evaluation.trainVsDev)
    # GPP closed
    BestConfig.mlpDimsumClosed()
    xp(['EN'], Dataset.dimsum, None, Evaluation.trainVsDev)
    BestConfig.mlpDimsumClosed()
    xp(['EN'], Dataset.dimsum, None, Evaluation.trainVsDev)
    TrendConfig.mlpDimsum()
    xp(['EN'], Dataset.dimsum, None, Evaluation.trainVsDev)
    # TrendConfig.mlpDimsum()
    # configuration['embedding']['pretrained'] = False
    # xp(['EN'], Dataset.dimsum, None, Evaluation.trainVsDev)


def evaluateDiMSUMAfterTunning():
    BestConfig.mlpDimsumClosed()
    xp(['EN'], Dataset.dimsum, None, Evaluation.corpus, seeds=range(2))
    # xp(['EN'], Dataset.dimsum, None, Evaluation.dev, seeds=range(2))
    TrendConfig.mlpDimsum()
    xp(['EN'], Dataset.dimsum, None, Evaluation.corpus, seeds=range(2))
    # xp(['EN'], Dataset.dimsum, None, Evaluation.dev, seeds=range(2))
    BestConfig.mlpDimsumClosed()
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
    rsg.runRSGAsynch(['BG'], Dataset.sharedtask2, None, Evaluation.fixedSize,
                     seeds=range(2), xpNum=1, xpNumByThread=200)


def tuneCompoRnn():
    import rsg
    rsg.runRSGAsynch(['BG'], Dataset.sharedtask2, XpMode.rmlpTree, Evaluation.fixedSize,
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

    BestConfig.mtPOSIdenOld()
    xp(langs, Dataset.sharedtask2,
       XpMode.multitasking, division, seeds=[0])

    TrendConfig.mtJoint()
    xp(langs, Dataset.sharedtask2,
       XpMode.multitasking, division, seeds=[0])


def evaluatePOSIden(langs=allSharedtask2Lang, division=Evaluation.trainVsDev):
    configuration['tmp']['createDepGraphs'] = False
    configuration['others']['analyzePerformance'] = True
    configuration['tmp']['trainTaggerAndIdentifier'] = True

    BestConfig.mtPOSIden()
    xp(langs, Dataset.sharedtask2,
       XpMode.multitasking, division, seeds=[0])

    TrendConfig.mtPOSIden()
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


def evaluateRMLP(langs=allSharedtask2Lang, xpMode=XpMode.rmlp):
    configuration['others']['analyzePerformance'] = True
    configuration['tmp']['createDepGraphs'] = False

    division = Evaluation.trainVsDev
    BestConfig.rmlpClosed()
    xp(langs[16:], Dataset.sharedtask2, xpMode, division, title='RMLP.CPP.Closed')
    BestConfig.rmlpOpen()
    xp(langs, Dataset.sharedtask2, xpMode, division, title='RMLP.CPP.Open')
    TrendConfig.rmlp()
    xp(langs, Dataset.sharedtask2, xpMode, division, title='RMLP.CT')

    # CORPUS
    division = Evaluation.corpus
    BestConfig.rmlpClosed()
    xp(langs, Dataset.sharedtask2, xpMode, division, title='RMLP.CPP.Closed')
    BestConfig.rmlpOpen()
    xp(langs, Dataset.sharedtask2, xpMode, division, title='RMLP.CPP.Open')
    TrendConfig.rmlp()
    xp(langs, Dataset.sharedtask2, xpMode, division, title='RMLP.CT')


def evaluateRMLPTree(langs=allSharedtask2Lang, xpMode=XpMode.rmlpTree):
    configuration['others']['analyzePerformance'] = True
    configuration['tmp']['createDepGraphs'] = False

    division = Evaluation.trainVsDev
    BestConfig.rmlpClosed()
    # xp(langs, Dataset.sharedtask2, xpMode, division, title='RMLP.Tree.CPP.Closed')
    BestConfig.rmlpOpen()
    # xp(langs, Dataset.sharedtask2, xpMode, division, title='RMLP.Tree.CPP.Open')
    TrendConfig.rmlp()
    xp(langs[16:], Dataset.sharedtask2, xpMode, division, title='RMLP.Tree.CT')

    # CORPUS
    division = Evaluation.corpus
    BestConfig.rmlpClosed()
    xp(langs, Dataset.sharedtask2, xpMode, division, title='RMLP.Tree.CPP.Closed')
    BestConfig.rmlpOpen()
    xp(langs, Dataset.sharedtask2, xpMode, division, title='RMLP.Tree.CPP.Open')
    TrendConfig.rmlp()
    xp(langs, Dataset.sharedtask2, xpMode, division, title='RMLP.Tree.CT')


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


def evaluateMLPOpen():
    configuration['others']['analyzePerformance'] = True
    configuration['tmp']['createDepGraphs'] = False
    TrendConfig.mlpOpen()
    # xp(allSharedtask2Lang, Dataset.sharedtask2, None, Evaluation.trainVsDev, seeds=range(1))
    xp(allSharedtask2Lang, Dataset.sharedtask2, None, Evaluation.corpus, seeds=range(1))


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


def analyzeResampling(langs=allSharedtask2Lang, xpMode=XpMode.linear,
                      division=Evaluation.trainVsDev, linear=True, xpNum=5):
    # without any resampling
    if linear:
        LinearConf.setSVMConf()
    else:
        TrendConfig.mlp()
        xpMode = None
    configuration['sampling'].update({
        'sampleWeight': False,
        'favorisationCoeff': 1,
        'focused': False,
        'overSampling': False,
        'importantSentences': False,
        'importantTransitions': False,
        'mweRepeition': 35
    })
    xp(langs, Dataset.sharedtask2, xpMode, division, xpNum=xpNum)

    # importantSentences  
    configuration['sampling'].update({
        'sampleWeight': False,
        'favorisationCoeff': 1,
        'focused': False,
        'overSampling': False,
        'importantSentences': True,
        'importantTransitions': False,
        'mweRepeition': 35
    })
    xp(langs, Dataset.sharedtask2, xpMode, division, xpNum=xpNum)

    # overSampling  
    configuration['sampling'].update({
        'sampleWeight': False,
        'favorisationCoeff': 1,
        'focused': False,
        'overSampling': True,
        'importantSentences': False,
        'importantTransitions': False,
        'mweRepeition': 35
    })
    xp(langs, Dataset.sharedtask2, xpMode, division, xpNum=xpNum)

    # focused  
    configuration['sampling'].update({
        'sampleWeight': False,
        'favorisationCoeff': 1,
        'focused': True,
        'overSampling': False,
        'importantSentences': False,
        'importantTransitions': False,
        'mweRepeition': 30
    })
    xp(langs, Dataset.sharedtask2, xpMode, division, xpNum=xpNum)

    # sampleWeight
    configuration['sampling'].update({
        'sampleWeight': True,
        'favorisationCoeff': 30,
        'focused': False,
        'overSampling': False,
        'importantSentences': False,
        'importantTransitions': False,
        'mweRepeition': 15
    })
    xp(langs, Dataset.sharedtask2, xpMode, division, xpNum=xpNum)

    # overSampling  + importantSentences
    configuration['sampling'].update({
        'sampleWeight': False,
        'favorisationCoeff': 1,
        'focused': False,
        'overSampling': True,
        'importantSentences': True,
        'importantTransitions': False,
        'mweRepeition': 35
    })
    xp(langs, Dataset.sharedtask2, xpMode, division, xpNum=xpNum)

    # overSampling  + importantSentences + focused
    configuration['sampling'].update({
        'sampleWeight': False,
        'favorisationCoeff': 1,
        'focused': True,
        'overSampling': True,
        'importantSentences': True,
        'importantTransitions': False,
        'mweRepeition': 30
    })
    xp(langs, Dataset.sharedtask2, xpMode, division, xpNum=xpNum)

    # overSampling  + importantSentences + sampleWeight
    configuration['sampling'].update({
        'sampleWeight': False,
        'favorisationCoeff': 1,
        'focused': True,
        'overSampling': True,
        'importantSentences': True,
        'importantTransitions': False,
        'mweRepeition': 30
    })
    xp(langs, Dataset.sharedtask2, xpMode, division, xpNum=xpNum)


def evaluateDepParsing():
    # depParsing.eval
    configuration['tmp']['trainDepParser'] = True
    configuration['tmp']['trainJointly'] = False
    configuration['tmp']['createDepGraphs'] = True
    configuration['others']['analyzePerformance'] = True
    TrendConfig.mtDepParsing()
    xp(allSynSharedtask2Lang, dataset=Dataset.sharedtask2, xpMode=XpMode.multitasking,
       division=Evaluation.trainVsDev)
    BestConfig.mtDepParsing()
    xp(allSynSharedtask2Lang, dataset=Dataset.sharedtask2, xpMode=XpMode.multitasking,
       division=Evaluation.trainVsDev)


def evaluateJointAvgJoint():
    # jointAvgJoint.eval
    configuration['tmp']['trainDepParser'] = False
    configuration['tmp']['trainJointly'] = True
    configuration['tmp']['createDepGraphs'] = True
    configuration['others']['analyzePerformance'] = True
    TrendConfig.jointAvgJoint()
    xp(allSynSharedtask2Lang, dataset=Dataset.sharedtask2, xpMode=XpMode.multitasking,
       division=Evaluation.trainVsDev)
    BestConfig.jointAvgJoint()
    xp(allSynSharedtask2Lang, dataset=Dataset.sharedtask2, xpMode=XpMode.multitasking,
       division=Evaluation.trainVsDev)


def evaluateIdentAvgJoint():
    # identAvgJoint.eval
    configuration['tmp']['trainDepParser'] = False
    configuration['tmp']['trainJointly'] = True
    configuration['tmp']['createDepGraphs'] = True
    configuration['others']['analyzePerformance'] = True
    TrendConfig.identAvgJoint()
    xp(allSynSharedtask2Lang, dataset=Dataset.sharedtask2, xpMode=XpMode.multitasking,
       division=Evaluation.trainVsDev)
    BestConfig.identAvgJoint()
    xp(allSynSharedtask2Lang, dataset=Dataset.sharedtask2, xpMode=XpMode.multitasking,
       division=Evaluation.trainVsDev)

def main(argv):
   inputfile = ''
   outputfile = ''
   try:
      opts, args = getopt.getopt(argv,"hi:o:",["ifile=","ofile="])
   except getopt.GetoptError:
      print 'test.py -i <inputfile> -o <outputfile>'
      sys.exit(2)
   for opt, arg in opts:
      if opt == '-h':
         print 'test.py -i <inputfile> -o <outputfile>'
         sys.exit()
      elif opt in ("-i", "--ifile"):
         inputfile = arg
      elif opt in ("-o", "--ofile"):
         outputfile = arg
   print 'Input file is "', inputfile
   print 'Output file is "', outputfile

if __name__ == "__main__":
    reload(sys)
    sys.setdefaultencoding('utf8')
    # main(sys.argv[1:])
    import argparse

    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('integers', metavar='N', type=int, nargs='+',
                        help='an integer for the accumulator')
    parser.add_argument('--sum', dest='accumulate', action='store_const',
                        const=sum, default=max,
                        help='sum the integers (default: find the max)')

    args = parser.parse_args()
    print args.accumulate(args.integers)

# if __name__ == '__main__':
#     reload(sys)
#     sys.setdefaultencoding('utf8')
#
#     configuration['tmp']['xpNonCompocreateDepGraphs'] = False
#     configuration['tmp']['trainTaggerAndIdentifier'] = True
#     TrendConfig.mtJoint()
#     xp(['BG', 'RO'], Dataset.sharedtask2, XpMode.multitasking, Evaluation.trainVsDev)
