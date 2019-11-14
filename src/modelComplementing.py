import config
import oracle
from corpus import *
from evaluation import evaluate
from identification import parseAndTrain
from modelStacking import modifyConf
from parser import parse
from reports import STDOutTools


def identifyWithBoth(lang):
    """
    A function for a complementary training of SVM and MLP models
    The result is based on either the intersection or the
    :param lang:
    :return:
    """
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
    """
    removes identified MWEs that are not annotated by the both models in  a complementary method of identification
    :param corpus:
    :return:
    """
    for s in corpus.testingSents:
        nonCorrectMWEIdxs = []
        for v in s.identifiedVMWEs:
            if v.predictingModel == 'linear' or v.predictingModel == 'mlp':
                nonCorrectMWEIdxs.append(s.identifiedVMWEs.index(v))
        for idx in sorted(nonCorrectMWEIdxs, reverse=True):
            s.identifiedVMWEs.pop(idx)


def getMWEsAccFrequency(corpus):
    """
    removes barely and partially seen MWEs from the identified MWEs by a complementary method
    :param corpus:
    :return:
    """
    for s in corpus.testingSents:
        nonCorrectMWEIdxs = []
        for v in s.identifiedVMWEs:
            partiallySeen = v.getLemmaString() not in corpus.mweDictionary
            barelySeen = v.getLemmaString() in corpus.mweDictionary and corpus.mweDictionary[v.getLemmaString()] <= 5
            if v.predictingModel in ['linear', 'mlp'] and (partiallySeen or barelySeen):
                nonCorrectMWEIdxs.append(s.identifiedVMWEs.index(v))
        for idx in sorted(nonCorrectMWEIdxs, reverse=True):
            s.identifiedVMWEs.pop(idx)
