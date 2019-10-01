import config
import modelLinear
import modelMLP
import modelRMLP
import oracle
from corpus import *
from evaluation import evaluate
from identification import parseAndTrain
from parser import parse
from reports import STDOutTools
from stats import getMWEsAccFrequency


def identifyWithBoth(lang):
    from xpTools import setXPMode, XpMode
    setXPMode(XpMode.linear)
    corpus = Corpus(lang)
    oracle.parse(corpus)
    startTime = datetime.datetime.now()
    modifyConf(linear=True, tuning=False)
    linearModel, linearVectorizer = parseAndTrain(corpus)
    STDOutTools.getExcutionTime('Training time', startTime)
    setXPMode(None)
    config.BestConfig.mlp()
    startTime = datetime.datetime.now()
    mlpModel, mlpVectorizer = parseAndTrain(corpus)
    STDOutTools.getExcutionTime('Training time', startTime)
    startTime = datetime.datetime.now()
    setXPMode(XpMode.linear)
    parse(corpus.testingSents, linearModel, linearVectorizer)
    setXPMode(None)
    parse(corpus.testingSents, mlpModel, mlpVectorizer, initialize=False)
    STDOutTools.getExcutionTime('Parsing time', startTime)
    if configuration['others']['complInter']:
        getIntersectedMWEs(corpus)
    elif configuration['others']['complFreq']:
        getMWEsAccFrequency(corpus)
    evaluate(corpus.testingSents)
    return corpus


def getIntersectedMWEs(corpus):
    for s in corpus.testingSents:
        nonCorrectMWEIdxs = []
        for v in s.identifiedVMWEs:
            if v.predictingModel == 'linear' or v.predictingModel == 'mlp':
                nonCorrectMWEIdxs.append(s.identifiedVMWEs.index(v))
        for idx in sorted(nonCorrectMWEIdxs, reverse=True):
            s.identifiedVMWEs.pop(idx)


def identifyWithLinearInMlp(lang, tuning=False):
    linearModels, linearVecs = jackknifing(lang, True)
    configuration['xp']['linear'] = False
    modifyConf(linear=False, tuning=tuning)
    corpus = Corpus(lang)
    oracle.parse(corpus)
    startTime = datetime.datetime.now()
    model = modelMLP.Network(corpus, linearInMLP=True)
    model.train(corpus, linearModels=linearModels, linearNormalizers=linearVecs)
    STDOutTools.getExcutionTime('Training time', startTime)
    startTime = datetime.datetime.now()
    parse(corpus.testingSents, model, linearModels=linearModels, linearVecs=linearVecs)
    STDOutTools.getExcutionTime('Parsing time', startTime)
    evaluate(corpus.testingSents)
    configuration['xp']['linear'] = False
    return corpus


def modifyConf(linear=False, tuning=False):
    if linear:
        if tuning:
            config.Generator.svm()
        else:
            if configuration['dataset']['ftb']:
                config.LinearConf.svmFtb()
            elif configuration['dataset']['dimsum']:
                config.LinearConf.svmDiMSUM()
            else:
                config.LinearConf.svm()
        configuration['sampling'].update({
            'overSampling': False,
            'importantSentences': False,
        })
    else:
        if tuning:
            config.Generator.mlp()
        else:
            if configuration['dataset']['ftb']:
                config.BestConfig.mlpFtbClosed()
            elif configuration['dataset']['dimsum']:
                config.BestConfig.mlpDimsumClosed()
            else:
                config.TrendConfig.mlp()
                configuration['embedding']['pretrained'] = False


def identifyWithMlpInLinear(lang, tuning=False):
    mlpModels, mlpNormalizers = jackknifing(lang, False)
    modifyConf(linear=True, tuning=tuning)
    corpus = Corpus(lang)
    oracle.parse(corpus)
    startTime = datetime.datetime.now()
    linearModel, linearVec = modelLinear.train(corpus, mlpModels=mlpModels)
    STDOutTools.getExcutionTime('Linear training time', startTime)
    configuration['xp']['linear'] = True
    startTime = datetime.datetime.now()
    parse(corpus.testingSents, linearModel, linearVec, mlpModels=mlpModels)
    STDOutTools.getExcutionTime('Parsing time', startTime)
    evaluate(corpus.testingSents)
    configuration['xp']['linear'] = False
    return corpus


def jackknifing(lang, linear=True):
    sys.stdout.write('Jacknfing:' + doubleSep)
    configuration['others']['verbose'] = False
    configuration['xp']['linear'] = linear
    modifyConf(linear=linear, tuning=False)
    models, normalizers = dict(), dict()
    for i in range(5):
        models[i], normalizers[i] = jackknifingAFold(lang, i, linear=linear)
        sys.stdout.write('Finished training the fold {0}\n'.format(i))
    models[5], normalizers[5] = jackknifingAFold(lang, linear=linear, all=True)
    sys.stdout.write('Jacknfing Finshed' + doubleSep)
    configuration['others']['verbose'] = True
    return models, normalizers


def jackknifingAFold(lang, foldIdx=-1, linear=True, all=False):
    corpus = Corpus(lang)
    if not all:
        foldLength = int(len(corpus.trainingSents) / 5)
        foldStart = foldIdx * foldLength
        foldEnd = foldStart + foldLength
        corpus.testingSents = corpus.trainingSents[foldStart:foldEnd]
        corpus.trainingSents = corpus.trainingSents[:foldStart] + corpus.trainingSents[foldEnd:]
    if not linear:
        configuration['sampling']['importantSentences'] = True
        corpus.trainingSents = corpus.filterImportatntSents()
    oracle.parse(corpus)
    vectorizer = None
    if linear:
        network, vectorizer = modelLinear.train(corpus)
    else:
        network = modelRMLP.Network(corpus)
        network.train(corpus)
    # parse(corpus.testingSents, network, vectorizer)
    # evaluate(corpus.testingSents)
    # corpus.testingSents = corpus.trainingSents
    # parse(corpus.testingSents, network, vectorizer)
    # evaluate(corpus.testingSents)

    return network, vectorizer
