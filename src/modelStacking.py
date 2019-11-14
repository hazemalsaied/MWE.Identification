import config
import modelLinear
import modelMLP
import oracle
from corpus import *
from evaluation import evaluate
from parser import parse
from reports import STDOutTools


def identifyWithLinearInMlp(lang, tuning=False):
    """
    A function for training and evaluating MLP model, feed by the predictions of a SVM model (trained with jackkniffing)
    :param lang:
    :param tuning:
    :return:
    """
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


def modifyConf(linear=False):
    """
    a fucntion for renversing the configurations and adapting them for training a SVM or a MLP model
    :param linear:
    :param tuning:
    :return:
    """
    if linear:
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
        if configuration['dataset']['ftb']:
            config.BestConfig.mlpFtbClosed()
        elif configuration['dataset']['dimsum']:
            config.BestConfig.mlpDimsumClosed()
        else:
            config.TrendConfig.mlp()
            configuration['embedding']['pretrained'] = False


def identifyWithMlpInLinear(lang, tuning=False):
    """
    A function for training and evaluating SVM model, feed by the predictions of a MLP model (trained with jackkniffing)
    :param lang:
    :param tuning:
    :return:
    """
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
    """
    5-fold kackkniffing function used for training auxiliary models (feeding principal model in stacked models)
    :param lang:
    :param linear:
    :return:
    """
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
    """
    fold kackkniffing function used for training a SVM or a MLP model on a given fold or on the whole training set
    :param lang:
    :param foldIdx: the given fold to train on
    :param linear: SVM? MLP?
    :param all: train on the whole training set
    :return:
    """
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
        network = modelMLP.Network(corpus)
        network.train(corpus)
    return network, vectorizer
