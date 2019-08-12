import datetime

# import torch
from enum import Enum
from theano import function, config, shared, tensor

from corpus import *
from identification import identify, identifyWithMlpInLinear, identifyWithLinearInMlp, identifyWithBoth

allSharedtask1Lang = ['BG', 'CS', 'DE', 'EL', 'ES', 'FA', 'FR', 'HE', 'HU', 'IT',
                      'LT', 'MT', 'PL', 'PT', 'RO', 'SV', 'SL', 'TR']

allSharedtask2Lang = ['BG', 'DE', 'EL', 'EN', 'ES', 'EU', 'FA', 'FR', 'HE', 'HI',
                      'HR', 'HU', 'IT', 'LT', 'PL', 'PT', 'RO', 'SL', 'TR']

pilotLangs = ['BG', 'PT', 'TR']


def xp(langs, dataset, xpMode, division, xpNum=1, seeds=[0], title='',
       mlpInLinear=False, linearInMlp=False, complentary=False, outputCupt=True):
    initXp(xpMode, dataset, division, title, outputCupt)
    for lang in langs:
        for s in seeds:
            setSeed(s)
            for i in range(xpNum):
                runXp(lang, mlpInLinear, linearInMlp, complentary, s, cuptTitle=title)


def runXp(lang, mlpInLinear, linearInMlp, complentary, seed, cuptTitle=''):
    now = datetime.datetime.now()
    sys.stdout.write('XP Starts: %d/%d (%dh:%d)' % (now.day, now.month, now.hour, now.minute) + doubleSep)
    if mlpInLinear:
        corpus = identifyWithMlpInLinear(lang, tuning=configuration['others']['tuneCoop'])
        corpus.createMWEFiles(seed, title='mlpInSvm' + cuptTitle)
    elif linearInMlp:
        corpus = identifyWithLinearInMlp(lang, tuning=configuration['others']['tuneCoop'])
        corpus.createMWEFiles(seed, title='svmInMlp' + cuptTitle)
    elif complentary:
        corpus = identifyWithBoth(lang)
        corpus.createMWEFiles(seed, title='complementary' + cuptTitle)
    elif configuration['evaluation']['cv']:
        for j in range(configuration['others']['cvFolds']):
            sys.stdout.write('\t' + 'Iteration {0}'.format(j))
            corpus = identify(lang, foldId=j)
            corpus.createMWEFiles(seed, title='fold.{0}'.format(j) + cuptTitle)
    else:
        corpus = identify(lang)
        if corpus:
            corpus.createMWEFiles(seed, title=cuptTitle)
    now = datetime.datetime.now()
    sys.stdout.write('\t' + 'XP Ends: %d/%d (%d h:%d)' %
                     (now.day, now.month, now.hour, now.minute) + doubleSep)
    sys.stdout.flush()


def initXp(xpMode, dataset, division, title, outputCupt):
    setXPMode(xpMode)
    setDataSet(dataset)
    setTrainAndTest(division)
    debug = True
    for k in configuration['evaluation']:
        if configuration['evaluation'][k] == True:
            debug = False
    configuration['tmp']['outputCupt'] = False if debug else outputCupt
    if xpMode != XpMode.linear:
        verifyGPU()
    getParameters(xpMode)
    # reports.createHeader(title)


def setSeed(s):
    numpy.random.seed(s)
    random.seed(s)
    # torch.manual_seed(s)
    sys.stdout.write('# Seed: %d' % s + doubleSep)


def getParameters(xpMode, printTilte=True):
    titles, values = [], []
    for k in sorted(configuration['xp'].keys()):
        if configuration['xp'][k] and type(True) == type(configuration['xp'][k]):
            titles.append('xp')
            values.append(k)
    if not titles:
        titles.append('xp')
        if xpMode == XpMode.mlpWide:
            values.append('MLP Wide')
        values.append('MLP')
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
    if xpMode == XpMode.kiperwasser or xpMode == XpMode.kiperComp:
        for k in sorted(configuration['kiperwasser'].keys()):
            titles.append(k)
            values.append(configuration['kiperwasser'][k])
    elif xpMode == XpMode.multitasking:
        for k in sorted(configuration['multitasking'].keys()):
            titles.append(k)
            values.append(configuration['multitasking'][k])

    elif xpMode == XpMode.rmlp:
        for k in sorted(configuration['rnn'].keys()):
            titles.append(k)
            values.append(configuration['rnn'][k])
    elif xpMode == XpMode.linear:
        for k in sorted(configuration['features'].keys()):
            titles.append(k)
            values.append(configuration['features'][k])
    elif xpMode == XpMode.rmlpTree:
        for k in sorted(configuration['rmlpTree'].keys()):
            titles.append(k)
            values.append(configuration['rmlpTree'][k])
    elif xpMode == XpMode.mlpWide:
        for k in sorted(configuration['mlp'].keys()):
            titles.append(k)
            values.append(configuration['mlp'][k])
    elif xpMode == XpMode.mlpPhrase:
        for k in sorted(configuration['mlpPhrase'].keys()):
            titles.append(k)
            values.append(configuration['mlpPhrase'][k])
    elif xpMode == XpMode.chenManning:
        for k in sorted(configuration['chenParams'].keys()):
            titles.append(k)
            values.append(configuration['chenParams'][k])
    else:
        for k in sorted(configuration['mlp'].keys()):
            titles.append(k)
            values.append(configuration['mlp'][k])
    if xpMode != XpMode.linear:
        for k in sorted(configuration['embedding'].keys()):
            titles.append(k)
            values.append(configuration['embedding'][k])
        for k in sorted(configuration['nn'].keys()):
            titles.append(k)
            values.append(configuration['nn'][k])
    if printTilte:
        sys.stdout.write('# CTitles: ' + ', '.join(str(t) for t in titles))
        sys.stdout.write(doubleSep)
    for i in range(int(len(titles) / 5) + 1):
        for j in range(5):
            if i * 5 + j < len(titles):
                sys.stdout.write(str(titles[i * 5 + j][:15]) + ' ' * (
                    15 - len(titles[i * 5 + j]) if 50 - len(titles[i * 5 + j]) > 0 else 0) + ',')
        sys.stdout.write(seperator)
        for j in range(5):
            if i * 5 + j < len(values):
                sys.stdout.write(str(values[i * 5 + j]) + ' ' * (
                    15 - len(str(values[i * 5 + j])) if 50 - len(str(values[i * 5 + j])) > 0 else 0) + ',')
        sys.stdout.write(seperator)

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
    rmlp = 4
    rnnNonCompo = 5
    kiperComp = 6
    rmlpTree = 7
    multitasking = 8
    mlpWide = 9
    mlpPhrase = 10
    chenManning = 11


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
        'rmlpTree': True if v == XpMode.rmlpTree else False,
        'multitasking': True if v == XpMode.multitasking else False,
        'kiperwasser': True if v == XpMode.kiperwasser else False,
        'kiperComp': True if v == XpMode.kiperComp else False,
        'rnn': True if v == XpMode.rmlp else False,
        'rnnNonCompo': True if v == XpMode.rnnNonCompo else False,
        'mlpWide': True if v == XpMode.mlpWide else False,
        'mlpPhrase': True if v == XpMode.mlpPhrase else False,
        'chenManning': True if v == XpMode.chenManning else False,
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


def getST1TrainFiles():
    path = '/Users/halsaied/PycharmProjects/MWE.Identification/Results/SVM0-CV'
    configuration['tmp']['shuffleOrRedistribute'] = False
    for l in allSharedtask1Lang:
        corpus = Corpus(l)
        pointer = int(len(corpus.trainDataSet) * 2 / 10)
        for i in range(5):
            corpus.trainingSents = corpus.trainDataSet[0:i * pointer] + corpus.trainDataSet[(i + 1) * pointer:]
            corpus.testingSents = corpus.trainDataSet[i * pointer: (i + 1) * pointer]
            trainInConllU = corpus.toConllU(useCupt=True, train=True, gold=True)
            # testInConllU = corpus.toConllU(useCupt=True, train=False, gold=True)
            with open(os.path.join(path, l + str(i) + '.train.cupt'), 'w') as ff:
                ff.write(trainInConllU)
            #with open(os.path.join(path, l, l + str(i + 1) + '.gold.cupt'), 'w') as ff:
            #    ff.write(testInConllU)


def fromTSVtoCupt():
    path = '/Users/halsaied/PycharmProjects/MWE.Identification/Results/baseline-cv'

    for l in allSharedtask1Lang:
        for i in range(5):
            for fileTail in ['.gold.txt', '.txt']:#, '.train.txt']:
                filename = l + str(i + 1) + fileTail
                conll = '# global.columns = ID FORM LEMMA UPOS XPOS FEATS HEAD DEPREL DEPS MISC PARSEME:MWE\n'
                filePath = os.path.join(path, filename)
                with open(filePath, 'r') as ff:
                    for line in ff:
                        if len(line.split('\t')) != 4:
                            conll += line
                        else:
                            lineParts = line.split('\t')
                            x = lineParts[-1].replace(':', ':LVC.full')
                            if lineParts[-1] == '_\n':
                                x = '*\n'
                            conll += '\t'.join([lineParts[0], lineParts[1]] + (['_'] * 8) + [x])
                with open(os.path.join(path, filename + '.cupt'), 'w') as ff:
                    ff.write(conll)
