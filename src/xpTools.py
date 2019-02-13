import datetime

import torch
from enum import Enum
from theano import function, config, shared, tensor

import reports
from corpus import *
from identification import identify, identifyWithMlpInLinear, identifyWithLinearInMlp, identifyWithBoth

allSharedtask1Lang = ['BG', 'CS', 'DE', 'EL', 'ES', 'FA', 'FR', 'HE', 'HU', 'IT',
                      'LT', 'MT', 'PL', 'PT', 'RO', 'SV', 'SL', 'TR']

allSharedtask2Lang = ['BG', 'DE', 'EL', 'EN', 'ES', 'EU', 'FA', 'FR', 'HE', 'HI',
                      'HR', 'HU', 'IT', 'LT', 'PL', 'PT', 'RO', 'SL', 'TR']

pilotLangs = ['BG', 'PT', 'TR']


def xp(langs, dataset, xpMode, division, xpNum=1, seeds=[0], title='',
       mlpInLinear=False, linearInMlp=False, complentary=False, outputCupt=False):
    initXp(xpMode, dataset, division, title, outputCupt)
    for lang in langs:
        for s in seeds:
            setSeed(s)
            for i in range(xpNum):
                runXp(lang, mlpInLinear, linearInMlp, complentary, s)


def runXp(lang, mlpInLinear, linearInMlp, complentary, seed):
    now = datetime.datetime.now()
    sys.stdout.write('XP Starts: %d/%d (%dh:%d)' % (now.day, now.month, now.hour, now.minute) + doubleSep)
    if mlpInLinear:
        corpus = identifyWithMlpInLinear(lang, tuning=configuration['others']['tuneCoop'])
        corpus.createMWEFiles(seed, 'mlpInSvm')
    elif linearInMlp:
        corpus = identifyWithLinearInMlp(lang, tuning=configuration['others']['tuneCoop'])
        corpus.createMWEFiles(seed, 'svmInMlp')
    elif complentary:
        corpus = identifyWithBoth(lang)
        corpus.createMWEFiles(seed, 'complementary')
    elif configuration['evaluation']['cv']:
        for j in range(configuration['others']['cvFolds']):
            sys.stdout.write(reports.tabs + 'Iteration {0}'.format(j))
            corpus = identify(lang, foldId=j)
            corpus.createMWEFiles(seed, 'fold.{0}'.format(j))
    else:
        corpus = identify(lang)
        corpus.createMWEFiles(seed)
    now = datetime.datetime.now()
    sys.stdout.write(reports.tabs +'XP Ends: %d/%d (%d h:%d)' %
                     (now.day, now.month, now.hour, now.minute) + doubleSep)
    sys.stdout.flush()


def initXp(xpMode, dataset, division, title, outputCupt):
    configuration['tmp']['outputCupt'] = outputCupt
    setXPMode(xpMode)
    setDataSet(dataset)
    setTrainAndTest(division)
    if xpMode != XpMode.linear:
        verifyGPU()
    getParameters(xpMode)
    reports.createHeader(title)


def setSeed(s):
    numpy.random.seed(s)
    random.seed(s)
    torch.manual_seed(s)
    sys.stdout.write('# Seed: %d' % s + doubleSep)


def getParameters(xpMode, printTilte=True):
    titles, values = [], []
    for k in sorted(configuration['xp'].keys()):
        if configuration['xp'][k] and type(True) == type(configuration['xp'][k]):
            titles.append('xp')
            values.append(k)
    if not titles:
        titles.append('xp')
        values.append('NonCompo')
    for k in sorted(configuration['dataset'].keys()):
        if configuration['dataset'][k] and type(True) == type(configuration['dataset'][k]):
            titles.append('Dataset')
            values.append(k)
    for k in sorted(configuration['evaluation'].keys()):
        if configuration['evaluation'][k] and type(True) == type(configuration['evaluation'][k]):
            titles.append('Evaluation')
            values.append(k)
    if len(titles) == 2:
        titles.append('evaluation')
        values.append('Debug')
    for k in sorted(configuration['sampling'].keys()):
        titles.append(k)
        values.append(configuration['sampling'][k])
    if xpMode != XpMode.linear:
        for k in sorted(configuration['embedding'].keys()):
            titles.append(k)
            values.append(configuration['embedding'][k])
    if xpMode == XpMode.kiperwasser or xpMode == XpMode.kiperComp:
        for k in sorted(configuration['kiperwasser'].keys()):
            titles.append(k)
            values.append(configuration['kiperwasser'][k])
    elif xpMode == XpMode.rnn:
        for k in sorted(configuration['rnn'].keys()):
            titles.append(k)
            values.append(configuration['rnn'][k])
    elif xpMode == XpMode.linear:
        for k in sorted(configuration['features'].keys()):
            titles.append(k)
            values.append(configuration['features'][k])
    elif xpMode == XpMode.compoRnn:
        for k in sorted(configuration['compoRnn'].keys()):
            titles.append(k)
            values.append(configuration['compoRnn'][k])
    else:
        for k in sorted(configuration['mlp'].keys()):
            titles.append(k)
            values.append(configuration['mlp'][k])
    if printTilte:
        sys.stdout.write('# CTitles: ' + ', '.join(str(t) for t in titles))
        sys.stdout.write(doubleSep)
    sys.stdout.write('# Configs: ' + ', '.join(str(v) for v in values))
    sys.stdout.write(doubleSep)


class Dataset(Enum):
    sharedtask2 = 0
    ftb = 1
    dimsum = 2


class Evaluation(Enum):
    cv = 0
    corpus = 1
    fixedSize = 2
    dev = 3
    trainVsDev = 4
    trainVsTest = 5


class XpMode(Enum):
    linear = 0
    compo = 1
    pytorch = 2
    kiperwasser = 3
    rnn = 4
    rnnNonCompo = 5
    kiperComp = 6
    compoRnn = 7
    multitasking = 8


def setTrainAndTest(v):
    configuration['evaluation'].update({
        'cv': True if v == Evaluation.cv else False,
        'corpus': True if v == Evaluation.corpus else False,
        'fixedSize': True if v == Evaluation.fixedSize else False,
        'dev': True if v == Evaluation.dev else False,
        'trainVsDev': True if v == Evaluation.trainVsDev else False,
        'trainVsTest': True if v == Evaluation.trainVsTest else False,
    })
    trues, evaluation = 0, 'DEBUG'
    for k in configuration['evaluation'].keys():
        if configuration['evaluation'][k] and type(True) == type(configuration['evaluation'][k]):
            evaluation = k.upper()
            trues += 1
    assert trues <= 1, 'There are more than one evaluation settings!'
    sys.stdout.write(tabs + 'Division: {0}'.format(evaluation) + doubleSep)


def setXPMode(v):
    configuration['xp'].update({
        'linear': True if v == XpMode.linear else False,
        'compo': True if v == XpMode.compo else False,
        'compoRnn': True if v == XpMode.compoRnn else False,
        'multitasking': True if v == XpMode.multitasking else False,
        'kiperwasser': True if v == XpMode.kiperwasser else False,
        'kiperComp': True if v == XpMode.kiperComp else False,
        'rnn': True if v == XpMode.rnn else False,
        'rnnNonCompo': True if v == XpMode.rnnNonCompo else False,
    })
    trues, mode = 0, 'NON.COMPO'
    for k in configuration['xp'].keys():
        if configuration['xp'][k] and type(True) == type(configuration['xp'][k]):
            mode = k.upper()
            trues += 1
    assert trues <= 1, 'There are more than one experimentation mode!'
    sys.stdout.write(tabs + 'Mode: {0}'.format(mode) + doubleSep)


def setDataSet(v):
    configuration['dataset'].update(
        {
            'sharedtask2': True if v == Dataset.sharedtask2 else False,
            'ftb': True if v == Dataset.ftb else False,
            'dimsum': True if v == Dataset.dimsum else False
        })
    trues, ds = 0, ''
    for k in configuration['dataset'].keys():
        if configuration['dataset'][k] and type(True) == type(configuration['dataset'][k]):
            ds = k.upper()
            trues += 1
    assert trues <= 1, 'Ambigious data set definition!'
    ds = 'ParseMe 1.0' if not ds else ds
    sys.stdout.write(tabs + 'Dataset: {0}'.format(ds) + doubleSep)


def verifyGPU():
    vlen = 10 * 30 * 768
    rng = numpy.random.RandomState(22)
    x = shared(numpy.asarray(rng.rand(vlen), config.floatX))
    f = function([], tensor.exp(x))
    if numpy.any([isinstance(x.op, tensor.Elemwise) and
                  ('Gpu' not in type(x.op).__name__)
                  for x in f.maker.fgraph.toposort()]):
        sys.stdout.write(tabs + 'Attention: CPU used' + doubleSep)
    else:
        sys.stdout.write(tabs + 'GPU Enabled' + doubleSep)
