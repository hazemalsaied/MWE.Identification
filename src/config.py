import math
import os
import random

configuration = {
    'multitasking':{
        'windowSize': 3,
        'tokenDim': 64,
        'affixeDim': 16,
        'capitalDim': 3,
        'symbolDim': 8,
        'taggingDenseUnits': 128,
        'useCapitalization': True,
        'useSymbols': True,
        'testOnToken': True
    },'xp': {
        'linear': False,
        'compo': False,
        'kiperwasser': False,
        'kiperComp': False,
        'rnn': False,
        'rnnNonCompo': False,
        'compoRnn': False,
        'multitasking': False
    }, 'dataset': {
        'sharedtask2': False,
        'ftb': False,
        'dimsum': False
    }, 'evaluation': {
        'cv': False,
        'corpus': False,
        'fixedSize': False,
        'dev': False,
        'trainVsDev': False,
        'trainVsTest': False
    }, 'embedding': {
        'manual': True,
        'keras': False,
        'pretrained': False,
        'average': True,
        'compactVocab': False,
        'lemma': True,
        'dynamicVocab': False,
        'useB1': 1,
        'useB-1': 1
    }, 'mlp': {
        'posEmb': 42,
        'tokenEmb': 480,
        'trainable': True,
        'batchSize': 64,
        'lr': 0.059,
        'dense1UnitNumber': 60,
        'dense1Dropout': 0.4
    }, 'compoRnn': {
        'posEmb': 42,
        'tokenEmb': 480,
        'trainable': True,
        'batchSize': 64,
        'lr': 0.059,
        'denseUnitNumber': 60,
        'denseDropout': 0.4,
        'stackPadding': 4,
        'wordRnnUnitNum': 50,
        'posRnnUnitNum': 15,
        'rnnSequence': False,
        'rnnDropout': .2,
        'gru': True,
        'shuffle': True
    }, 'tmp': {
        'dontParse': False,
        'cleanSents': False,
        'transOut': False,
        'tunePretrained': False,
        'deleteNumericalExpressions': False,
        'testOut': False,
        'outputDimsum': False,
        'dimsulStats': False,
        'outputCupt': False
    }, 'others': {
        'tuneCoop': False,
        'cvFolds': 5,
        'currentIter': -1,
        'shuffleTrain': False,
        'debugTrainNum': 25,
        'test': 0.2,
        'tokenAvg': 270000,
        'testTokenAvg': 43000,
        'importantWordThShold': 5,
        'universalPOS': True,
        'svm': True,
        'svmScikit': True,
        'bufferElements': 5,
        'verbose': True,
        'replaceNumbers': False,
        'removeFtbMWT': True,
        'logReg': False,
        'svc': False,
        'traitDeformedLemma': True,
        'minimal': False,
        'complInter': False,
        'complFreq': False,
        'dimsumAsCupt': False,
        'debugOnDev': False,
        'autoData': True,
        'analyzePerformance': True
    }, 'kiperwasser': {
        'wordDim': 25,
        'posDim': 5,
        'layerNum': 2,
        'optimizer': 'adagrad',
        'lr': 0.07,
        'dropout': .3,
        'batch': 1,
        'dense1': 25,
        'denseActivation': 'tanh',
        'denseDropout': 0,
        'rnnUnitNum': 8,
        'rnnDropout': 0.3,
        'rnnLayerNum': 2,
        'focusedElemNum': 8,
        'file': 'kiper.p',
        'earlyStop': False,
        'verbose': True,
        'eager': True,
        'gru': True,
        'trainValidationSet': True
    }, 'rnn': {
        'focusedElements': 7,
        'wordDim': 50,
        'posDim': 15,
        'gru': True,
        'wordRnnUnitNum': 16,
        'posRnnUnitNum': 5,
        'rnnDropout': .3,
        'useDense': True,
        'denseDropout': .3,
        'denseUnitNum': 25,
        'lr': .05,
        'batchSize': 64,
        'earlyStop': True,
        's0TokenNum': 4,
        's1TokenNum': 2,
        'bTokenNum': 1,
        'shuffle': False,
        'rnnSequence': False
    }, 'nn': {
        'loss': 'categorical_crossentropy',
        'optimizer': 'adagrad',
        'epochs': 40,
        'earlyStop': True,
        'checkPoint': False,
        'minDelta': .2,
        'patience': 4,
        'dense1Activation': 'relu',
        'predictVerbose': False,
        'validationSplit': .2
    }, 'mlp2': {
        'features': False,
        'dense2': False,
        'dense2UnitNumber': 0,
        'dense2Activation': 'relu',
        'dense2Dropout': 0,
    }, 'mlpNonLexicl': {
        'bPadding': 2,
        's0Padding': 5,
        's1Padding': 5,
        'inputItems': 3,
    }, 'initialisation': {
        'active': False,
        'oneHotPos': False,
        'pos': True,
        'token': True,
        'Word2VecWindow': 3,
        'type': 'frWac200'
        # 'dataFR.profiles.min.250'  # 'frWac200'
    }, 'sampling': {
        'sampleWeight': False,
        'favorisationCoeff': 1,
        'focused': False,
        'overSampling': False,
        'importantSentences': False,
        'importantTransitions': False,
        'mweRepeition': 35
    }, 'features': {
        'superSense': False,
        'reduced': False,
        'lemma': True,
        'token': False,
        'pos': True,
        'suffix': False,
        'b1': False,
        's0b2': False,
        'bigram': True,
        'trigram': False,
        'syntax': False,
        'syntaxAbstract': False,
        'dictionary': False,
        's0TokenIsMWEToken': False,
        's0TokensAreMWE': False,
        'history1': False,
        'history2': False,
        'history3': False,
        'stackLength': False,
        'distanceS0s1': False,
        'distanceS0b0': False,
        'numeric': False
    }, 'path': {
        'results': 'Results',
        'errorAnalysis': 'Results/ErrorAnalysis',
        'output': 'Results/Output',
        'projectPath': '',
        'corpusFolder': 'ressources/sharedtask',
        'checkPointPath': 'best_model.h5'

    }, 'files': {
        'bestWeights': 'bestWeigths.hdf5',
        'train': {
            'conllu': 'train.conllu',
            'posAuto': 'train.conllu.autoPOS',
            'depAuto': 'train.conllu.autoPOS.autoDep'
        }, 'test': {
            'conllu': 'test.conllu',
            'posAuto': 'test.conllu.autoPOS',
            'depAuto': 'test.conllu.autoPOS.autoDep'
        }, 'embedding': {
            'frWac200': 'ressources/WordEmb/frWac/frWac_non_lem_no_postag_no_phrase_200_cbow_cut100.bin',
            'dataFR.profiles.min.250': 'ressources/WordEmb/dataFR.profiles.min',
            'frWiki50': 'ressources/WordEmb/vecs50-linear-frwiki'
        }, 'reports': {
            'summary': 'summary.json',
            'normaliser': 'normaliser.pkl',
            'config': 'setting.txt',
            'scores': 'scores.csv',
            'schema': 'schema.png',
            'history': 'history.pkl',
            'model': 'model.hdf5'
        }
    }, 'constants': {
        'unk': '*unknown*',
        'empty': '*empty*',
        'number': '*number*',
        'alpha': 0.5
    }
}

configuration['path']['projectPath'] = os.path.dirname(__file__)[:-len(os.path.basename(os.path.dirname(__file__)))]


def resetFRStandardFeatures():
    conf = {
        'lemma': True,
        'token': True,
        'pos': True,
        'suffix': False,
        'b1': True,
        'bigram': True,
        's0b2': True,
        'trigram': False,
        'syntax': False,
        'syntaxAbstract': False,
        'dictionary': True,
        's0TokenIsMWEToken': False,
        's0TokensAreMWE': False,
        'history1': False,
        'history2': False,
        'history3': False,
        'stackLength': False,
        'distanceS0s1': True,
        'distanceS0b0': True
    }
    configuration['features'].update(conf)


def resetStandardFeatures(v=False):
    configuration['features'].update({
        'lemma': v,
        'token': v,
        'pos': v,
        'suffix': v,
        'b1': v,
        'bigram': v,
        's0b2': v,
        'trigram': v,
        'syntax': v,
        'syntaxAbstract': v,
        'dictionary': v,
        's0TokenIsMWEToken': v,
        's0TokensAreMWE': v,
        'history1': v,
        'history2': v,
        'history3': v,
        'stackLength': v,
        'distanceS0s1': v,
        'distanceS0b0': v
    })


def resetNonLexicalFeatures(value=False):
    conf = {
        'lemma': True,
        'pos': True,
        'token': value,
        'suffix': value,
        'b1': value,
        'bigram': value,
        's0b2': value,
        'trigram': value,
        'syntax': value,
        'syntaxAbstract': value,
        'dictionary': value,
        's0TokenIsMWEToken': value,
        's0TokensAreMWE': value,
        'history1': value,
        'history2': value,
        'history3': value,
        'stackLength': value,
        'distanceS0s1': value,
        'distanceS0b0': value
    }
    configuration['features'].update(conf)


def setMinimalFeatures():
    conf = {
        'lemma': True,
        'token': False,
        'pos': True,
        'suffix': False,
        'b1': False,
        'bigram': True,
        's0b2': False,
        'trigram': False,
        'syntax': False,
        'syntaxAbstract': False,
        'dictionary': False,
        's0TokenIsMWEToken': False,
        's0TokensAreMWE': False,
        'history1': False,
        'history2': False,
        'history3': False,
        'stackLength': False,
        'distanceS0s1': False,
        'distanceS0b0': False
    }
    configuration['features'].update(conf)


def setOptimalRSGFeaturesByLogReg():
    conf = {
        'lemma': True,
        'token': False,
        'pos': True,
        'suffix': False,
        'b1': False,
        'bigram': True,
        's0b2': False,
        'trigram': True,
        'syntax': False,
        'syntaxAbstract': False,
        'dictionary': False,
        's0TokenIsMWEToken': False,
        's0TokensAreMWE': False,
        'history1': True,
        'history2': True,
        'history3': True,
        'stackLength': False,
        'distanceS0s1': True,
        'distanceS0b0': True
    }
    configuration['features'].update(conf)


def setOptimalRSGFeaturesForSVM():
    configuration['features'].update({
        'lemma': True,
        'token': True,
        'pos': True,
        'suffix': False,
        'b1': True,
        'bigram': True,
        's0b2': True,
        'trigram': True,
        'syntax': False,
        'syntaxAbstract': False,
        'dictionary': True,
        's0TokenIsMWEToken': True,
        's0TokensAreMWE': False,
        'history1': True,
        'history2': False,
        'history3': True,
        'stackLength': False,
        'distanceS0s1': True,
        'distanceS0b0': True
    })


def setOptimalRSGFeaturesForDimsumSVM():
    conf = {
        'lemma': True,
        'token': False,
        'pos': True,
        'suffix': False,
        'b1': True,
        'bigram': True,
        's0b2': False,
        'trigram': True,
        'syntax': False,
        'syntaxAbstract': False,
        'dictionary': True,
        's0TokenIsMWEToken': False,
        's0TokensAreMWE': False,
        'history1': True,
        'history2': False,
        'history3': True,
        'stackLength': False,
        'distanceS0s1': False,
        'distanceS0b0': True
    }
    configuration['features'].update(conf)


def setOptimalRSGFeaturesForFtbSVM():
    conf = {
        'lemma': True,
        'token': True,
        'pos': True,
        'suffix': False,
        'b1': False,
        'bigram': True,
        's0b2': False,
        'trigram': True,
        'syntax': False,
        'syntaxAbstract': False,
        'dictionary': True,
        's0TokenIsMWEToken': False,
        's0TokensAreMWE': False,
        'history1': False,
        'history2': False,
        'history3': False,
        'stackLength': True,
        'distanceS0s1': True,
        'distanceS0b0': True
    }
    configuration['features'].update(conf)


def setOptimalRSGForMlpFTB():
    samling = configuration['sampling']
    samling['importantSentences'] = True
    samling['overSampling'] = True
    samling['sampleWeight'] = True
    samling['favorisationCoeff'] = 3
    samling['focused'] = True

    configuration['nn']['optimizer'] = 'adagrad'
    configuration['mlp']['lr'] = 0.059

    configuration['embedding']['lemma'] = True
    configuration['mlp']['posEmb'] = 103
    configuration['mlp']['tokenEmb'] = 410
    configuration['embedding']['compactVocab'] = True

    configuration['mlp']['dense1UnitNumber'] = 167
    configuration['mlp']['dense1Dropout'] = 0.16


def setOptimalRSGForMlpDiMSUM():
    samling = configuration['sampling']
    samling['importantSentences'] = True
    samling['overSampling'] = True
    samling['sampleWeight'] = True
    samling['favorisationCoeff'] = 13
    samling['focused'] = True

    configuration['nn']['optimizer'] = 'adagrad'
    configuration['mlp']['lr'] = 0.059

    configuration['embedding']['lemma'] = True
    configuration['mlp']['posEmb'] = 118
    configuration['mlp']['tokenEmb'] = 326
    configuration['embedding']['compactVocab'] = True

    configuration['mlp']['dense1UnitNumber'] = 172
    configuration['mlp']['dense1Dropout'] = 0.38


def setOptimalRSGForMLP():
    configuration['sampling'].update({
        'importantSentences': True,
        'overSampling': True,
        'sampleWeight': False,
        'favorisationCoeff': 2,
        'focused': False})
    configuration['embedding'].update({
        'useB1': 1,
        'useB-1': 1,
        'manual': True,
        'keras': False,
        'pretrained': False,
        'average': False,
        'compactVocab': True,
        'lemma': True,
        'dynamicVocab': False
    })
    configuration['mlp'].update({
        'posEmb': 147,
        'tokenEmb': 157,
        'dense1UnitNumber': 85,
        'dense1Dropout': 0.3,
        'lr': 0.017,
        'trainable': True,
        'batchSize': 128,
    })

    # configuration['sampling'].update({
    #     'importantSentences': True,
    #     'overSampling': True,
    #     'sampleWeight': True,
    #     'favorisationCoeff': 6,
    #     'focused': True})
    # configuration['embedding'].update({
    #     'lemma': True,
    #     'compactVocab': False,
    #     'dynamicVocab': False,
    #     'useB-1': 0,
    #     'useB1': 1
    # })
    # configuration['mlp'].update({
    #     'posEmb': 42,
    #     'tokenEmb': 480,
    #     'dense1UnitNumber': 58,
    #     'dense1Dropout': 0.429,
    #     'lr': 0.059,
    #     'optimizer': 'adagrad',
    #     'trainable': True,
    #     'batchSize': 64,
    #
    # })


def setOptimalRSGForMLPTendance():
    configuration['sampling'].update({
        'importantSentences': True,
        'overSampling': True,
        'sampleWeight': False,
        'favorisationCoeff': 2,
        'focused': False})
    configuration['embedding'].update({
        'useB1': 1,
        'useB-1': 1,
        'manual': False,
        'keras': False,
        'pretrained': True,
        'average': True,
        'compactVocab': True,
        'lemma': True,
        'dynamicVocab': False
    })
    configuration['mlp'].update({
        'posEmb': 35,
        'tokenEmb': 300,
        'dense1UnitNumber': 75,
        'dense1Dropout': 0.4,
        'lr': 0.03,
        'trainable': True,
        'batchSize': 48,
    })

    # configuration['sampling'].update({
    #     'importantSentences': True,
    #     'overSampling': True,
    #     'sampleWeight': True,
    #     'favorisationCoeff': 6,
    #     'focused': True})
    # configuration['embedding'].update({
    #     'lemma': True,
    #     'compactVocab': False,
    #     'dynamicVocab': False,
    #     'useB-1': 0,
    #     'useB1': 1
    # })
    # configuration['mlp'].update({
    #     'posEmb': 42,
    #     'tokenEmb': 480,
    #     'dense1UnitNumber': 58,
    #     'dense1Dropout': 0.429,
    #     'lr': 0.059,
    #     'optimizer': 'adagrad',
    #     'trainable': True,
    #     'batchSize': 64,
    #
    # })


def setOptimalRSGForRNN():
    configuration['rnn']['gru'] = True
    configuration['rnn']['useDense'] = True
    configuration['embedding']['compactVocab'] = True
    configuration['embedding']['lemma'] = True

    configuration['sampling']['importantSentences'] = True
    configuration['sampling']['overSampling'] = True

    configuration['rnn']['wordDim'] = 410
    configuration['rnn']['posDim'] = 54
    configuration['rnn']['denseUnitNum'] = 51
    configuration['rnn']['denseDropout'] = 0.1
    configuration['rnn']['wordRnnUnitNum'] = 25
    configuration['rnn']['posRnnUnitNum'] = 15
    configuration['rnn']['rnnDropout'] = 0.1
    configuration['rnn']['batchSize'] = 16


def generateCompoRnnConf():
    configuration['sampling'].update({
        'overSampling': True,
        'importantSentences': True,
        'importantTransitions': False,
        'sampleWeight': generateValue([True, False], continousPlage=False, uniform=True),
        'favorisationCoeff': int(generateValue([1, 40], continousPlage=True, uniform=False)),
        'focused': generateValue([True, False], continousPlage=False, uniform=True),
        'mweRepeition': generateValue([5, 10, 15, 20, 30], continousPlage=False, uniform=True)
    })
    configuration['embedding'].update({
        'pretrained': generateValue([True, False], continousPlage=False, uniform=True),
        'manual': True,
        'average': generateValue([True, False], continousPlage=False, uniform=False),
        'compactVocab': generateValue([True, False], uniform=True),
        'lemma': generateValue([True, False], continousPlage=False, uniform=False),
        'dynamicVocab': generateValue([False, True], continousPlage=False, uniform=False),
        'useB1': generateValue([1, 0], continousPlage=False, uniform=False),
        'useB-1': generateValue([1, 0], continousPlage=False, uniform=False)
    })

    if configuration['embedding']['pretrained']:
        configuration['embedding']['manual'] = False
    configuration['compoRnn'].update({
        'wordRnnUnitNum': int(generateValue([25, 200], uniform=False, continousPlage=True)),
        'posRnnUnitNum': int(generateValue([25, 200], uniform=False, continousPlage=True)),
        'rnnDropout': float(generateValue([.1, .2, .3, .4, .5, .6], continousPlage=False, uniform=True)),
        'gru': generateValue([True, False], continousPlage=False, uniform=False),
        'posEmb': int(generateValue([15, 150], uniform=False, continousPlage=True)),
        'tokenEmb': 300 if configuration['embedding']['pretrained'] else
        int(generateValue([100, 600], uniform=False, continousPlage=True)),
        'denseUnitNumber': int(generateValue([25, 600], uniform=False, continousPlage=True)),
        'denseDropout': float(generateValue([.1, .2, .3, .4, .5, .6], continousPlage=False, uniform=True)),
        'batchSize': generateValue([16, 32, 48, 64, 128], continousPlage=False, uniform=True),
        'lr': round(generateValue([.01, .2], continousPlage=True, uniform=False), 3),
        'shuffle': generateValue([True, False], continousPlage=False, uniform=False),
    })


# def generateMLPConf():
#     configuration['sampling'].update({
#         'overSampling': True,
#         'importantSentences': True,
#         'importantTransitions': False,
#         'sampleWeight': generateValue([True, False], continousPlage=False, uniform=True),
#         'favorisationCoeff': int(generateValue([1, 40], continousPlage=True, uniform=False)),
#         'focused': generateValue([True, False], continousPlage=False, uniform=True),
#         'mweRepeition': generateValue([5, 10, 15, 20, 30], continousPlage=False, uniform=True)
#     })
#     configuration['embedding'].update({
#         'pretrained': True,  # generateValue([True, False], continousPlage=False, uniform=True),
#         'manual': False,  # True
#         'average': True,  # generateValue([True, False], continousPlage=False, uniform=False),
#         'compactVocab': False,  # generateValue([True, False], uniform=True),
#         'lemma': generateValue([True, False], continousPlage=False, uniform=True),
#         # generateValue([True, False], continousPlage=False, uniform=False),
#         'dynamicVocab': False,  # generateValue([False, True], continousPlage=False, uniform=False),
#         'useB1': True,  # generateValue([1, 0], continousPlage=False, uniform=False),
#         'useB-1': True,  # generateValue([1, 0], continousPlage=False, uniform=False)
#     })
#     if configuration['embedding']['pretrained']:
#         configuration['embedding']['manual'] = False
#     configuration['mlp'].update({
#         'posEmb': int(generateValue([15, 100], uniform=False, continousPlage=True)),
#         'tokenEmb': 300 if configuration['embedding']['pretrained'] else
#         int(generateValue([100, 400], uniform=False, continousPlage=True)),
#         'dense1UnitNumber': int(generateValue([25, 600], uniform=False, continousPlage=True)),
#         'dense1Dropout': float(generateValue([.1, .2, .3, .4], continousPlage=False, uniform=True)),
#         'batchSize': generateValue([16, 32, 48, 64, 128], continousPlage=False, uniform=True),
#         'lr': round(generateValue([.01, .07], continousPlage=True, uniform=False), 3),
#     })


def generateMLPConf():
    configuration['sampling'].update({
        'overSampling': True,
        'importantSentences': True,
        'importantTransitions': False,
        'sampleWeight': generateValue([True, False], continousPlage=False, uniform=True),
        'favorisationCoeff': int(generateValue([1, 40], continousPlage=True, uniform=False)),
        'focused': generateValue([True, False], continousPlage=False, uniform=True),
        'mweRepeition': generateValue([5, 10, 15, 20, 30], continousPlage=False, uniform=True)
    })
    configuration['embedding'].update({
        'pretrained': generateValue([True, False], continousPlage=False, uniform=True),
        'manual': True,
        'average': generateValue([True, False], continousPlage=False, uniform=False),
        'compactVocab': generateValue([True, False], uniform=True),
        'lemma': generateValue([True, False], continousPlage=False, uniform=False),
        'dynamicVocab': generateValue([False, True], continousPlage=False, uniform=False),
        'useB1': generateValue([1, 0], continousPlage=False, uniform=False),
        'useB-1': generateValue([1, 0], continousPlage=False, uniform=False)
    })
    if configuration['embedding']['pretrained']:
        configuration['embedding']['manual'] = False
    configuration['mlp'].update({
        'posEmb': int(generateValue([15, 150], uniform=False, continousPlage=True)),
        'tokenEmb': 300 if configuration['embedding']['pretrained'] else
        int(generateValue([100, 600], uniform=False, continousPlage=True)),
        'dense1UnitNumber': int(generateValue([25, 600], uniform=False, continousPlage=True)),
        'dense1Dropout': float(generateValue([.1, .2, .3, .4, .5, .6], continousPlage=False, uniform=True)),
        'batchSize': generateValue([16, 32, 48, 64, 128], continousPlage=False, uniform=True),
        'lr': round(generateValue([.01, .1], continousPlage=True, uniform=False), 3),
    })


def generateMLPConfForPretrained():
    configuration['sampling'].update({
        'overSampling': True,
        'importantSentences': True,
        'importantTransitions': False,
        'sampleWeight': generateValue([True, False], continousPlage=False, uniform=True),
        'favorisationCoeff': int(generateValue([1, 40], continousPlage=True, uniform=False)),
        'focused': generateValue([True, False], continousPlage=False, uniform=True),
        'mweRepeition': generateValue([5, 10, 15, 20, 30], continousPlage=False, uniform=True)
    })
    configuration['embedding'].update({
        'pretrained': True,
        'manual': False,
        'average': True,
        'compactVocab': False,
        'lemma': generateValue([True, False], continousPlage=False, uniform=True),
        'dynamicVocab': False,
        'useB1': True,
        'useB-1': True,
    })
    if configuration['embedding']['pretrained']:
        configuration['embedding']['manual'] = False

    configuration['mlp'].update({
        'posEmb': int(generateValue([15, 100], uniform=False, continousPlage=True)),
        'tokenEmb': 300 if configuration['embedding']['pretrained'] else
        int(generateValue([100, 400], uniform=False, continousPlage=True)),
        'dense1UnitNumber': int(generateValue([25, 600], uniform=False, continousPlage=True)),
        'dense1Dropout': float(generateValue([.1, .2, .3, .4], continousPlage=False, uniform=True)),
        'batchSize': generateValue([16, 32, 48, 64, 128], continousPlage=False, uniform=True),
        'lr': round(generateValue([.01, .07], continousPlage=True, uniform=False), 3),
    })


def generateRNNConf():
    configuration['rnn']['wordDim'] = int(generateValue([250, 600], True, True))
    configuration['rnn']['posDim'] = int(generateValue([25, 100], True, True))

    configuration['rnn']['gru'] = True  # generateValue([True, False], False, False)
    configuration['rnn']['wordRnnUnitNum'] = int(generateValue([25, 200], True, True))
    configuration['rnn']['posRnnUnitNum'] = int(generateValue([25, 200], True, True))
    configuration['rnn']['rnnDropout'] = round(generateValue([0, .3], True, True), 1)

    configuration['rnn']['useDense'] = True  # generateValue([True, False], False, False)
    configuration['rnn']['denseDropout'] = 0  # round(generateValue([0, .5], True, True), 1)
    configuration['rnn']['denseUnitNum'] = int(generateValue([5, 200], True, True))
    configuration['rnn']['batchSize'] = 64  # generateValue([16, 32, 64, 128], False, True)
    configuration['nn']['compactVocab'] = generateValue([True, False], False, False)


def generateLinearConf():
    configuration['features'].update({
        'lemma': True,
        'token': generateValue([True, False], favorisationTaux=.3),
        'pos': True,
        'suffix': False,
        'b1': generateValue([True, False], favorisationTaux=.5),
        'bigram': True,
        's0b2': generateValue([True, False], favorisationTaux=.5),
        'trigram': generateValue([True, False], favorisationTaux=.5),
        'syntax': False,
        'syntaxAbstract': False,
        'dictionary': generateValue([True, False], favorisationTaux=.5),
        's0TokenIsMWEToken': generateValue([True, False], favorisationTaux=.5),
        's0TokensAreMWE': False,
        'history1': generateValue([True, False], favorisationTaux=.5),
        'history2': generateValue([True, False], favorisationTaux=.5),
        'history3': generateValue([True, False], favorisationTaux=.5),
        'stackLength': generateValue([True, False], favorisationTaux=.5),
        'distanceS0s1': generateValue([True, False], favorisationTaux=.5),
        'distanceS0b0': generateValue([True, False], favorisationTaux=.5)
    })


def generateKiperwasserConf():
    kiperConf = configuration['kiperwasser']
    kiperConf['wordDim'] = int(generateValue([50, 500], True))
    kiperConf['posDim'] = int(generateValue([15, 150], True))
    kiperConf['denseActivation'] = 'tanh'  # str(generateValue(['tanh', 'relu'], False))
    configuration['nn']['optimizer'] = 'adagrad'  # str(generateValue(['adam', 'adagrad'], False))
    kiperConf['lr'] = 0.07
    kiperConf['dense1'] = int(generateValue([10, 350], True))
    kiperConf['rnnDropout'] = round(generateValue([.1, .4], True), 2)
    kiperConf['rnnUnitNum'] = int(generateValue([20, 250], True))
    kiperConf['rnnLayerNum'] = 1  # generateValue([1, 2], False)

    configuration['embedding']['compactVocab'] = generateValue([True, False], False)
    configuration['embedding']['lemma'] = True  # generateValue([True, False], False)


def generateValue(plage, continousPlage=False, uniform=False, favorisationTaux=0.7):
    if continousPlage:
        if uniform:
            return random.uniform(plage[0], plage[-1])
        else:
            return pow(2, random.uniform(math.log(plage[0], 2), math.log(plage[-1], 2)))
    else:
        if not uniform and len(plage) == 2:
            alpha = random.uniform(0, 1)
            if alpha < favorisationTaux:
                return plage[0]
            return plage[random.randint(1, len(plage) - 1)]
        else:
            return plage[random.randint(0, len(plage) - 1)]
