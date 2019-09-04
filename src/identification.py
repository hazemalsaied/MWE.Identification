import datetime
import logging

from nltk.parse import DependencyEvaluator

import modelChenManning
#
#import modelKiperwasser
import modelLinear
import modelMLP
import modelMlpPhrase
import modelMlpWide
import modelMultiTasking
import modelRMLP
import modelRMLPTree
import modelRnnNonCompo
import oracle
from corpus import *
from evaluation import evaluate, analyzePerformance
from parser import parse
from reports import STDOutTools


def identify(lang):
    corpus = Corpus(lang)
    oracle.parse(corpus)
    t = datetime.datetime.now()
    network, vectorizer = parseAndTrain(corpus)
    if configuration['tmp']['dontParse']:
        configuration['tmp']['dontParse'] = False
        return None
    STDOutTools.getExcutionTime('Training time', t)
    t = datetime.datetime.now()
    parse(corpus.testingSents, network, vectorizer)
    STDOutTools.getExcutionTime('Parsing time', t)
    evaluate(corpus.testingSents)
    analyzePerformance(corpus)
    return corpus


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
            sys.stdout.write('UAS = {0}\nLAS = {1}'.format(round(de.eval()[0] * 100, 1), round(de.eval()[1] * 100, 1)))
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
        #network = modelKiperwasser.train2(corpus)
        #network = modelKiperwasser.train(corpus, configuration)
        # import modelKiperKeras
        # network = modelKiperKeras.Network(corpus)
        import modelK
        network = modelK.run(corpus)
        # configuration['tmp']['dontParse'] = False
        return network, None

    if configuration['xp']['kiperComp']:
        import modelCompactKiper
        network = modelCompactKiper.train(corpus, configuration)
        return network, None

    if configuration['xp']['multitasking']:
        network = modelMultiTasking.Network(corpus)
        if configuration['tmp']['trainInTransfert']:
            network.trainInTransfert(corpus)
            configuration['tmp']['dontParse'] = True
            return network, None
        elif configuration['tmp']['trainJointly']:
            t = datetime.datetime.now()
            network.trainAll(corpus)
            STDOutTools.getExcutionTime('trainAll passed', t)
            t = datetime.datetime.now()
            configuration['multitasking']['testOnToken'] = True
            network.testTagging(corpus)
            STDOutTools.getExcutionTime('testTagging passed', t)
            t = datetime.datetime.now()
            configuration['multitasking']['testOnToken'] = False
            network.testTagging(corpus, title='POS tagging accuracy (MWEs)')
            STDOutTools.getExcutionTime('testTagging 2 passed', t)
            t = datetime.datetime.now()
            configuration['multitasking']['testOnToken'] = True
            network.evaluateDepParsing(corpus)
            STDOutTools.getExcutionTime('evaluateDepParsing 2 passed', t)
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


if __name__ == '__main__':
    reload(sys)
    sys.setdefaultencoding('utf8')
    logging.basicConfig(level=logging.WARNING)
