import datetime
import logging

from nltk.parse import DependencyEvaluator

import config
import modelChenManning
import modelCompactKiper
import modelKiperwasser
import modelLinear
import modelMLP
import modelMlpPhrase
import modelMlpWide
import modelMultiTasking
import modelRMLP
import modelRMLPTree
import modelRnnNonCompo
import oracle
import reports
from corpus import *
from evaluation import evaluate, analyzePerformance
from parser import parse
from transitions import TransitionType


def identify(lang, foldId=-1):
    corpus = Corpus(lang, foldId=foldId)
    getDimsumStats(corpus)
    oracle.parse(corpus)
    startTime = datetime.datetime.now()
    network, vectorizer = parseAndTrain(corpus)
    if configuration['tmp']['dontParse']:
        configuration['tmp']['dontParse'] = False
        return None
    getExcutionTime('Training time', startTime)
    startTime = datetime.datetime.now()
    parse(corpus.testingSents, network, vectorizer)
    getExcutionTime('Parsing time', startTime)
    evaluate(corpus.testingSents)
    analyzePerformance(corpus)
    if configuration['tmp']['outputDimsum']:
        dimSum = corpus.toDiMSUM()
        with open(os.path.join(configuration['path']['projectPath'], 'ressources/dimsum/scripts/EN.pred'), 'w') as ff:
            ff.write(dimSum)
    if configuration['tmp']['testOut']:
        for s in corpus.testingSents:
            s.initialTransition = None
            sys.stdout.write(str(s))
    return corpus




def getTransDistribution(corpus):
    shNum, rdNum, mgNum, mkNum = 0, 0, 0, 0
    importantSents = 0
    for s in corpus.trainingSents:
        if s.vMWEs:
            importantSents += 1
        t = s.initialTransition
        while t.next:
            if t.type == TransitionType.SHIFT:
                shNum += 1
            elif t.type == TransitionType.REDUCE:
                rdNum += 1
            elif t.type == TransitionType.MERGE:
                mgNum += 1
            else:
                mkNum += 1
            t = t.next
    print len(corpus.trainingSents), importantSents
    print shNum, rdNum, mgNum, mkNum, (shNum + rdNum + mgNum + mkNum)
    return


def getDimsumStats(corpus):
    if not configuration['tmp']['dimsulStats']:
        return
    sys.stdout.write('# MWEs\n')
    for k in corpus.mweDictionary:
        sys.stdout.write('{0} : {1}\n'.format(k, corpus.mweDictionary[k]))
    seenToks, nonSeenToks = set(), set()
    for s in corpus.testingSents:
        for w in s.vMWEs:
            for t in w.tokens:
                if t.getLemma() in corpus.mweTokenDictionary:
                    seenToks.add(t.getLemma())
                else:
                    nonSeenToks.add(t.getLemma())
    sys.stdout.write('# seen tokens\n')
    for t in seenToks:
        sys.stdout.write('{0}\n' % t)
    sys.stdout.write('# non seen tokens\n')
    for t in nonSeenToks:
        sys.stdout.write('{0}\n' % t)


def identifyWithBoth(lang):
    from xpTools import setXPMode, XpMode
    setXPMode(XpMode.linear)
    corpus = Corpus(lang)
    oracle.parse(corpus)
    startTime = datetime.datetime.now()
    modifyConf(linear=True, tuning=False)
    linearModel, linearVectorizer = parseAndTrain(corpus)
    getExcutionTime('Training time', startTime)
    setXPMode(None)
    config.BestConfig.mlp()
    startTime = datetime.datetime.now()
    mlpModel, mlpVectorizer = parseAndTrain(corpus)
    getExcutionTime('Training time', startTime)
    startTime = datetime.datetime.now()
    setXPMode(XpMode.linear)
    parse(corpus.testingSents, linearModel, linearVectorizer)
    setXPMode(None)
    parse(corpus.testingSents, mlpModel, mlpVectorizer, initialize=False)
    getExcutionTime('Parsing time', startTime)
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


def getMWEsAccFrequency(corpus):
    for s in corpus.testingSents:
        nonCorrectMWEIdxs = []
        for v in s.identifiedVMWEs:
            partiallySeen = v.getLemmaString() not in corpus.mweDictionary
            barelySeen = v.getLemmaString() in corpus.mweDictionary and corpus.mweDictionary[v.getLemmaString()] <= 5
            if v.predictingModel in ['linear', 'mlp'] and (partiallySeen or barelySeen):
                nonCorrectMWEIdxs.append(s.identifiedVMWEs.index(v))
        for idx in sorted(nonCorrectMWEIdxs, reverse=True):
            s.identifiedVMWEs.pop(idx)


def identifyWithLinearInMlp(lang, tuning=False, seed=0):
    linearModels, linearVecs = jackknifing(lang, True)
    configuration['xp']['linear'] = False
    modifyConf(linear=False, tuning=tuning)
    corpus = Corpus(lang)
    oracle.parse(corpus)
    startTime = datetime.datetime.now()
    model = modelMLP.Network(corpus, linearInMLP=True)
    model.train(corpus, linearModels=linearModels, linearNormalizers=linearVecs)
    getExcutionTime('Training time', startTime)
    startTime = datetime.datetime.now()
    parse(corpus.testingSents, model, linearModels=linearModels, linearVecs=linearVecs)
    getExcutionTime('Parsing time', startTime)
    evaluate(corpus.testingSents)
    configuration['xp']['linear'] = False
    return corpus


def modifyConf(linear=False, tuning=False):
    if linear:
        if tuning:
            config.Generator.svm()
        else:
            if configuration['dataset']['ftb']:
                config.LinearConf.setSvmFtbConf()
            elif configuration['dataset']['dimsum']:
                config.LinearConf.setSvmDiMSUMConf()
            else:
                config.LinearConf.setSVMConf()
        configuration['sampling'].update({
            'overSampling': False,
            'importantSentences': False,
        })
    else:
        if tuning:
            config.Generator.mlp()
        else:
            if configuration['dataset']['ftb']:
                config.BestConfig.mlpFtb()
            elif configuration['dataset']['dimsum']:
                config.BestConfig.mlpDimsum()
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
    getExcutionTime('Linear training time', startTime)
    configuration['xp']['linear'] = True
    startTime = datetime.datetime.now()
    parse(corpus.testingSents, linearModel, linearVec, mlpModels=mlpModels)
    getExcutionTime('Parsing time', startTime)
    evaluate(corpus.testingSents)
    configuration['xp']['linear'] = False
    return corpus


def getExcutionTime(label, start):
    sys.stdout.write('{0}{1}: {2} minutes {3}'.format(reports.tabs,
                                                      label.upper(),
                                                      round((datetime.datetime.now() - start).seconds / 60., 2),
                                                      reports.doubleSep))


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


def parseAndTrain(corpus):
    if configuration['xp']['linear']:
        return modelLinear.train(corpus)
    if configuration['xp']['rnn']:
        network = modelRMLP.Network(corpus)
        network.train(corpus)
        return network, None
    if configuration['xp']['mlpWide']:
        network = modelMlpWide.Network(corpus)
        network.train(corpus)
        return network, None
    if configuration['xp']['mlpPhrase']:
        network = modelMlpPhrase.train(corpus)
        return network, None
    if configuration['xp']['chenManning']:
        if configuration['tmp']['nltk']:
            modelChenManning.NLTKParser.evaluate(corpus)
            configuration['tmp']['dontParse'] = True
            return None, None
        else:
            network = modelChenManning.Network(corpus)
            network.train()
            result = network.parse(corpus)
            configuration['tmp']['dontParse'] = True
            de = DependencyEvaluator(corpus.testDepGraphs, result)
            print 'UAS = {0}\nLAS = {1}'.format(round(de.eval()[0] * 100, 1), round(de.eval()[1] * 100, 1))
            return network, None
    if configuration['xp']['rmlpTree']:
        network = modelRMLPTree.Network(corpus)
        modelRMLPTree.train(network, corpus)
        return network, None
    if configuration['xp']['rnnNonCompo']:
        network = modelRnnNonCompo.Network(corpus)
        modelRnnNonCompo.train(network, corpus)
        return network, None
    if configuration['xp']['kiperwasser']:
        network = modelKiperwasser.train(corpus, configuration)
        return network, None
    if configuration['xp']['kiperComp']:
        network = modelCompactKiper.train(corpus, configuration)
        return network, None

    if configuration['xp']['multitasking']:
        network = modelMultiTasking.Network(corpus)
        if configuration['tmp']['trainInTransfert']:
            network.trainInTransfert(corpus)
            configuration['tmp']['dontParse'] = True
            return network, None
        elif configuration['tmp']['trainJointly']:
            network.trainAll(corpus)
            configuration['multitasking']['testOnToken'] = True
            network.testTagging(corpus)
            configuration['multitasking']['testOnToken'] = False
            network.testTagging(corpus, title='POS tagging accuracy (MWEs)')
            configuration['multitasking']['testOnToken'] = True
            network.evaluateDepParsing(corpus)
            return network, None
        elif configuration['tmp']['trainTaggerAndIdentifier']:
            network.trainTaggerAndIdentifier(corpus)
            # parse(corpus.testingSents, network, None)
            configuration['multitasking']['testOnToken'] = True
            network.testTagging(corpus)
            configuration['multitasking']['testOnToken'] = False
            network.testTagging(corpus, title='POS tagging accuracy (MWEs)')
            configuration['multitasking']['testOnToken'] = True
            network.evaluateDepParsing(corpus)
            return network, None
        elif configuration['tmp']['trainIden']:
            network.trainIden(corpus)
            # parse(corpus.testingSents, network, None)
            # network.testIden(corpus)
        elif configuration['tmp']['trainDepParser']:
            network.trainDepParser()
            network.evaluateDepParsing(corpus)
            configuration['tmp']['dontParse'] = True
            return network, None
        else:
            network.trainTagging(corpus)
            configuration['multitasking']['testOnToken'] = True
            network.testTagging(corpus)
            configuration['multitasking']['testOnToken'] = False
            network.testTagging(corpus, title='POS tagging accuracy (MWEs)')
            configuration['multitasking']['testOnToken'] = True
            configuration['tmp']['dontParse'] = True
        return network, None
    network = modelMLP.Network(corpus)
    network.train(corpus)
    return network, None


def analyzeCorporaAndOracle(langs):
    header = 'Non recognizable,Interleaving,Embedded,Distributed Embedded,Left Embedded,Right Embedded,Middle Embedded'
    analysisReport = header + '\n'
    for lang in langs:
        sys.stdout.write('Language = {0}\n'.format(lang))
        corpus = Corpus(lang)
        analysisReport += corpus.getVMWEReport() + '\n'
        oracle.parse(corpus)
        oracle.validate(corpus)
    with open('../Results/VMWE.Analysis.csv', 'w') as ff:
        ff.write(analysisReport)


if __name__ == '__main__':
    reload(sys)
    sys.setdefaultencoding('utf8')
    logging.basicConfig(level=logging.WARNING)
