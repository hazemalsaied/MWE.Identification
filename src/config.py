import math
import os
import random

configuration = {
    'chenParams': {
        'tokenEmb': 100,
        'posEmb': 15,
        'synLabelEmb': 10,
        'dense1UnitNumber': 100,
        'dense1Activation': 'relu',
        'dense1Dropout': .5,
        'lr': .02,
        'batchSize': 32,
        'unlabeled': True,
        'l2': 10e-8,
        'regularizer': False,
        'cubeActivation': False,
        'pretrained': False,
        'earlyStopping': True,
        'epochs': 50,
        'minDelta': .01,
        'patience': 4,
        'monitor': 'val_loss',
        'validationSplit': .2
    },
    'chenConstant': {
        'confElements': 18,
        'synLabelNum': 12,
        'transNumber': 3
    },
    'multitasking': {
        'windowSize': 3,
        'tokenDim': 64,
        'affixeDim': 16,
        'capitalDim': 3,
        'symbolDim': 8,
        'taggingDenseUnits': 128,
        'IdenDenseUnitNumber': 64,
        'depParsingDenseUnitNumber': 64,
        'useCapitalization': True,
        'useSymbols': True,
        'testOnToken': True,
        'useB1': True,
        'useBx': True,
        'taggingBatchSize': 32,
        'identBatchSize': 32,
        'depParserBatchSize': 32,
        'initialEpochs': 1,
        'jointLearningEpochs': 100,
        'sytacticLabelDim': 25,
        'lr': 0.02
    },
    'xp': {
        'linear': False,
        'compo': False,
        'kiperwasser': False,
        'kiperComp': False,
        'mlpPhrase': False,
        'rnn': False,
        'rnnNonCompo': False,
        'compoRnn': False,
        'multitasking': False,
        'mlpWide': False,
        'chenManning': False
    },
    'dataset': {
        'sharedtask2': False,
        'ftb': False,
        'dimsum': False
    },
    'evaluation': {
        'cv': False,
        'corpus': False,
        'fixedSize': False,
        'dev': False,
        'trainVsDev': False,
        'trainVsTest': False
    },
    'embedding': {
        'manual': True,
        'keras': False,
        'pretrained': False,
        'average': True,
        'compactVocab': False,
        'lemma': True,
        'dynamicVocab': False,
        'useB1': 1,
        'useB-1': 1
    },
    'mlpPhrase': {
        'phraseMaxLength': 50,
        'phraseTokenEmb': 75,
        'phrasePosEmb': 15,
        'gru': True,
        'wordRnnUnitNum': 100,
        'useB1': True,
        'useB-1': True,
        'transPosEmb': 15,
        'transTokenEmb': 75,
        'denseUnitNumber': 100,
        'lr': .02
    },
    'mlp': {
        'posEmb': 42,
        'tokenEmb': 480,
        'trainable': True,
        'batchSize': 64,
        'lr': 0.059,
        'dense1UnitNumber': 60,
        'dense1Dropout': 0.4,
        'posWindow': 3
    },
    'compoRnn': {
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
    },
    'tmp': {
        'createDepGraphs': True,
        'dontParse': False,
        'trainIden': False,
        'trainDepParser': False,
        'trainJointly': False,
        'cleanSents': False,
        'transOut': False,
        'tunePretrained': False,
        'deleteNumericalExpressions': False,
        'testOut': False,
        'outputDimsum': False,
        'dimsulStats': False,
        'outputCupt': False,
        'markObligatory': False,
        'addTokens': False,
        'onGroup': False,
        'group': 'tweebank'
    },
    'others': {
        'tuneCoop': False,
        'cvFolds': 5,
        'currentIter': -1,
        'shuffleTrain': False,
        'debugTrainNum': 100,
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
        'tokenBased': False,
        'analyzePerformance': True
    },
    'kiperwasser': {
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
        'trainValidationSet': True,
        'sampling': True
    },
    'rnn': {
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
    },
    'mlp2': {
        'features': False,
        'dense2': False,
        'dense2UnitNumber': 0,
        'dense2Activation': 'relu',
        'dense2Dropout': 0,
    },
    'mlpNonLexicl': {
        'bPadding': 2,
        's0Padding': 5,
        's1Padding': 5,
        'inputItems': 3,
    },
    'initialisation': {
        'active': False,
        'oneHotPos': False,
        'pos': True,
        'token': True,
        'Word2VecWindow': 3,
        'type': 'frWac200'
        # 'dataFR.profiles.min.250'  # 'frWac200'
    },
    'sampling': {
        'sampleWeight': False,
        'favorisationCoeff': 1,
        'focused': False,
        'overSampling': False,
        'importantSentences': False,
        'importantTransitions': False,
        'mweRepeition': 35
    },
    'features': {
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
    },
    'path': {
        'results': 'Results',
        'errorAnalysis': 'Results/ErrorAnalysis',
        'output': 'Results/Output',
        'projectPath': '',
        'corpusFolder': 'ressources/sharedtask',
        'checkPointPath': 'best_model.h5'

    },
    'files': {
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
    },
    'constants': {
        'unk': '*unknown*',
        'empty': '*empty*',
        'number': '*number*',
        'alpha': 0.5
    }
}

configuration['path']['projectPath'] = os.path.dirname(__file__)[:-len(os.path.basename(os.path.dirname(__file__)))]


class TendConfig:

    def mlpWide():
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
            'pretrained': False,
            'average': False,
            'compactVocab': True,
            'lemma': True,
            'dynamicVocab': False
        })
        configuration['mlp'].update({
            'posEmb': 60,
            'tokenEmb': 300,
            'dense1UnitNumber': 215,
            'dense1Dropout': 0.3,
            'lr': 0.03,
            'trainable': True,
            'batchSize': 60,
            'posWindow': 3
        })

    @staticmethod
    def mlpPhrase():
        configuration['mlpPhrase'].update({
            'phraseMaxLength': 50,
            'phraseTokenEmb': 80,
            'phrasePosEmb': 18,
            'gru': False,
            'wordRnnUnitNum': 110,
            'useB1': True,
            'useB-1': False,
            'transPosEmb': 15,
            'transTokenEmb': 95,
            'denseUnitNumber': 115,
            'lr': .05
        })
        configuration['embedding']['lemma'] = True
        configuration['sampling']['importantSentences'] = True
        configuration['sampling']['overSampling'] = True

    @staticmethod
    def setTrendMTConfForPOS():
        configuration['multitasking'].update({
            'tokenDim': 69,
            'affixeDim': 13,
            'capitalDim': 3,
            'symbolDim': 9,
            'taggingDenseUnits': 89,
            'IdenDenseUnitNumber': 88,
            'useCapitalization': True,
            'useSymbols': True,
            'testOnToken': True,
            'useB1': True,
            'useBx': True,
            'taggingBatchSize': 51,
            'lr': 0.04
        })
        configuration['embedding']['lemma'] = True
        configuration['sampling']['importantSentences'] = True
        configuration['sampling']['overSampling'] = True

    @staticmethod
    def setTrendMTConfForIden():
        configuration['multitasking'].update({
            'tokenDim': 89,
            'affixeDim': 13,
            'capitalDim': 3,
            'symbolDim': 9,
            'taggingDenseUnits': 87,
            'IdenDenseUnitNumber': 81,
            'useCapitalization': True,
            'useSymbols': True,
            'testOnToken': True,
            'useB1': True,
            'useBx': True,
            'identBatchSize': 32,  # 51,
            'lr': .02  # 0.04
        })
        configuration['embedding']['lemma'] = True
        configuration['sampling']['importantSentences'] = True
        configuration['sampling']['overSampling'] = True

    @staticmethod
    def setTrendMTConfForJoint():
        configuration['multitasking'].update({
            'tokenDim': 83,
            'affixeDim': 13,
            'capitalDim': 3,
            'symbolDim': 8,
            'taggingDenseUnits': 90,
            'IdenDenseUnitNumber': 64,
            'useCapitalization': True,
            'useSymbols': True,
            'testOnToken': True,
            'useB1': True,
            'useBx': True,
            'identBatchSize': 41,
            'taggingBatchSize': 39,
            'initialEpochs': 2,
            'jointLearningEpochs': 100,
            'lr': 0.04
        })
        configuration['embedding']['lemma'] = True
        configuration['sampling']['importantSentences'] = True
        configuration['sampling']['overSampling'] = True

    @staticmethod
    def setMlpTendanceConf():
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


class Standard:
    @staticmethod
    def setChenManningParameters():
        configuration['chenParams']['dense1Dropout'] = .5
        configuration['chenParams']['lr'] = .01
        configuration['chenParams']['dense1UnitNumber'] = 200
        configuration['chenParams']['regularizer'] = True
        configuration['chenParams']['l2'] = 10e-8
        configuration['chenParams']['tokenEmb'] = 300
        configuration['chenParams']['posEmb'] = 50
        configuration['chenParams']['synLabelEmb'] = 50
        configuration['chenParams']['batchSize'] = 32
        configuration['chenParams']['cubeActivation'] = True
        configuration['chenParams']['pretrained'] = True
        configuration['chenParams']['earlyStopping'] = True
        configuration['chenParams']['epochs'] = 50


class BestConfig:
    @staticmethod
    def mlpWide():
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
            'pretrained': False,
            'average': True,
            'compactVocab': True,
            'lemma': True,
            'dynamicVocab': False
        })
        configuration['mlp'].update({
            'posEmb': 50,
            'tokenEmb': 300,
            'dense1UnitNumber': 200,
            'dense1Dropout': 0.6,
            'lr': 0.04,
            'trainable': True,
            'batchSize': 128,
            'posWindow':2
        })
    @staticmethod
    def mlpPhrase():
        configuration['mlpPhrase'].update({
            'phraseMaxLength': 50,
            'phraseTokenEmb': 43,
            'phrasePosEmb': 6,
            'gru': True,
            'wordRnnUnitNum': 415,
            'useB1': True,
            'useB-1': False,
            'transPosEmb': 5,
            'transTokenEmb': 36,
            'denseUnitNumber': 35,
            'lr': .03
        })
        configuration['embedding']['lemma'] = True
        configuration['sampling']['importantSentences'] = True
        configuration['sampling']['overSampling'] = True

    @staticmethod
    def setBestMTConfForJoint():
        configuration['multitasking'].update({
            'tokenDim': 140,
            'affixeDim': 14,
            'capitalDim': 1,
            'symbolDim': 5,
            'taggingDenseUnits': 78,
            'IdenDenseUnitNumber': 30,
            'useCapitalization': False,
            'useSymbols': True,
            'testOnToken': True,
            'useB1': True,
            'useBx': True,
            'identBatchSize': 37,
            'taggingBatchSize': 21,
            'initialEpochs': 3,
            'jointLearningEpochs': 100,
            'lr': 0.05
        })
        configuration['embedding']['lemma'] = True
        configuration['sampling']['importantSentences'] = True
        configuration['sampling']['overSampling'] = True

    @staticmethod
    def setMlpFtbConf():
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

    @staticmethod
    def setMlpDiMSUMConf():
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

    @staticmethod
    def setMLPConf():
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

    @staticmethod
    def setMlpOpenConf():
        configuration['sampling'].update({
            'importantSentences': True,
            'overSampling': True,
            'sampleWeight': False,
            'favorisationCoeff': 2,
            'focused': False})
        configuration['embedding'].update({
            'useB1': 1,
            'useB-1': 0,
            'manual': False,
            'keras': False,
            'pretrained': True,
            'average': True,
            'compactVocab': False,
            'lemma': True,
            'dynamicVocab': False
        })
        configuration['mlp'].update({
            'posEmb': 132,
            'tokenEmb': 300,
            'dense1UnitNumber': 56,
            'dense1Dropout': 0.1,
            'lr': 0.095,
            'trainable': True,
            'batchSize': 16,
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

    @staticmethod
    def setOptimalRSGForMLPFTB():
        configuration['sampling'].update({
            'importantSentences': True,
            'overSampling': True,
            'sampleWeight': False,
            'favorisationCoeff': 2,
            'mweRepeition': 10,
            'focused': True})
        configuration['embedding'].update({
            'useB1': 1,
            'useB-1': 1,
            'manual': True,
            'keras': False,
            'pretrained': False,
            'average': True,
            'compactVocab': True,
            'lemma': True,
            'dynamicVocab': False
        })
        configuration['mlp'].update({
            'posEmb': 15,
            'tokenEmb': 383,
            'dense1UnitNumber': 174,
            'dense1Dropout': 0.3,
            'lr': 0.015,
            'trainable': True,
            'batchSize': 64,
        })

    @staticmethod
    def setMlpFtbOpenConf():
        configuration['sampling'].update({
            'importantSentences': True,
            'overSampling': True,
            'sampleWeight': False,
            'favorisationCoeff': 2,
            'focused': False})
        configuration['embedding'].update({
            'useB1': 1,
            'useB-1': 0,
            'manual': False,
            'keras': False,
            'pretrained': True,
            'average': True,
            'compactVocab': False,
            'lemma': True,
            'dynamicVocab': False
        })
        configuration['mlp'].update({
            'posEmb': 125,
            'tokenEmb': 300,
            'dense1UnitNumber': 105,
            'dense1Dropout': 0.1,
            'lr': 0.067,
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

    @staticmethod
    def setRnnConf():
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

    @staticmethod
    def setBestMTConfForPOS():
        configuration['multitasking'].update({
            'tokenDim': 190,
            'affixeDim': 20,
            'capitalDim': 4,
            'symbolDim': 11,
            'taggingDenseUnits': 36,
            'IdenDenseUnitNumber': 197,
            'useCapitalization': False,
            'useSymbols': True,
            'testOnToken': True,
            'useB1': True,
            'useBx': True,
            'taggingBatchSize': 120,
            'lr': 0.01
        })
        configuration['embedding']['lemma'] = True
        configuration['sampling']['importantSentences'] = True
        configuration['sampling']['overSampling'] = True

    @staticmethod
    def setBestMTConfForIden():
        configuration['multitasking'].update({
            'tokenDim': 77,
            'affixeDim': 18,
            'capitalDim': 5,
            'symbolDim': 8,
            'taggingDenseUnits': 166,
            'IdenDenseUnitNumber': 74,
            'useCapitalization': False,
            'useSymbols': True,
            'testOnToken': True,
            'useB1': False,
            'useBx': True,
            'identBatchSize': 32,  # 51,
            'lr': .02  # 0.05
        })
        configuration['embedding']['lemma'] = True
        configuration['sampling']['importantSentences'] = True
        configuration['sampling']['overSampling'] = True


class LinearConf:
    @staticmethod
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

    @staticmethod
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

    @staticmethod
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

    @staticmethod
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

    @staticmethod
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

    @staticmethod
    def setSVMConf():
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

    @staticmethod
    def setSvmDiMSUMConf():
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

    @staticmethod
    def setSvmFtbConf():
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


class Generator:

    @staticmethod
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

    @staticmethod
    def generateCompoRnnConf():
        configuration['sampling'].update({
            'overSampling': True,
            'importantSentences': True,
            'importantTransitions': False,
            'sampleWeight':
                Generator.generateValue([True, False], continousPlage=False, uniform=True),
            'favorisationCoeff': int(Generator.generateValue([1, 40], continousPlage=True, uniform=False)),
            'focused': Generator.generateValue([True, False], continousPlage=False, uniform=True),
            'mweRepeition': Generator.generateValue([5, 10, 15, 20, 30], continousPlage=False, uniform=True)
        })
        configuration['embedding'].update({
            'pretrained': Generator.generateValue([True, False], continousPlage=False, uniform=True),
            'manual': True,
            'average': Generator.generateValue([True, False], continousPlage=False, uniform=False),
            'compactVocab': Generator.generateValue([True, False], uniform=True),
            'lemma': Generator.generateValue([True, False], continousPlage=False, uniform=False),
            'dynamicVocab': Generator.generateValue([False, True], continousPlage=False, uniform=False),
            'useB1': Generator.generateValue([1, 0], continousPlage=False, uniform=False),
            'useB-1': Generator.generateValue([1, 0], continousPlage=False, uniform=False)
        })

        if configuration['embedding']['pretrained']:
            configuration['embedding']['manual'] = False
        configuration['compoRnn'].update({
            'wordRnnUnitNum': int(Generator.generateValue([25, 200], uniform=False, continousPlage=True)),
            'posRnnUnitNum': int(Generator.generateValue([25, 200], uniform=False, continousPlage=True)),
            'rnnDropout': float(Generator.generateValue([.1, .2, .3, .4, .5, .6], continousPlage=False, uniform=True)),
            'gru': Generator.generateValue([True, False], continousPlage=False, uniform=False),
            'posEmb': int(Generator.generateValue([15, 150], uniform=False, continousPlage=True)),
            'tokenEmb': 300 if configuration['embedding']['pretrained'] else
            int(Generator.generateValue([100, 600], uniform=False, continousPlage=True)),
            'denseUnitNumber': int(Generator.generateValue([25, 600], uniform=False, continousPlage=True)),
            'denseDropout': float(
                Generator.generateValue([.1, .2, .3, .4, .5, .6], continousPlage=False, uniform=True)),
            'batchSize': Generator.generateValue([16, 32, 48, 64, 128], continousPlage=False, uniform=True),
            'lr': round(Generator.generateValue([.01, .2], continousPlage=True, uniform=False), 3),
            'shuffle': Generator.generateValue([True, False], continousPlage=False, uniform=False),
        })

    @staticmethod
    def generateMLPConf():
        configuration['sampling'].update({
            'overSampling': True,
            'importantSentences': True,
            'importantTransitions': False,
            'sampleWeight': Generator.generateValue([True, False], continousPlage=False, uniform=True),
            'favorisationCoeff': int(Generator.generateValue([1, 40], continousPlage=True, uniform=False)),
            'focused': Generator.generateValue([True, False], continousPlage=False, uniform=True),
            'mweRepeition': Generator.generateValue([5, 10, 15, 20, 30], continousPlage=False, uniform=True)
        })
        configuration['embedding'].update({
            'pretrained': Generator.generateValue([True, False], continousPlage=False, uniform=True),
            'manual': True,
            'average': Generator.generateValue([True, False], continousPlage=False, uniform=False),
            'compactVocab': Generator.generateValue([True, False], uniform=True),
            'lemma': Generator.generateValue([True, False], continousPlage=False, uniform=False),
            'dynamicVocab': Generator.generateValue([False, True], continousPlage=False, uniform=False),
            'useB1': Generator.generateValue([1, 0], continousPlage=False, uniform=False),
            'useB-1': Generator.generateValue([1, 0], continousPlage=False, uniform=False)
        })
        if configuration['embedding']['pretrained']:
            configuration['embedding']['manual'] = False
        configuration['mlp'].update({
            'posEmb': int(Generator.generateValue([15, 150], uniform=False, continousPlage=True)),
            'tokenEmb': 300 if configuration['embedding']['pretrained'] else
            int(Generator.generateValue([100, 600], uniform=False, continousPlage=True)),
            'dense1UnitNumber': int(Generator.generateValue([25, 600], uniform=False, continousPlage=True)),
            'dense1Dropout': float(
                Generator.generateValue([.1, .2, .3, .4, .5, .6], continousPlage=False, uniform=True)),
            'batchSize': Generator.generateValue([16, 32, 48, 64, 128], continousPlage=False, uniform=True),
            'lr': round(Generator.generateValue([.01, .1], continousPlage=True, uniform=False), 3),
            'posWindow': Generator.generateValue([1, 2, 3, 4], continousPlage=False, uniform=True)
        })

    @staticmethod
    def generateMLPConfForPretrained():
        configuration['sampling'].update({
            'overSampling': True,
            'importantSentences': True,
            'importantTransitions': False,
            'sampleWeight': Generator.generateValue([True, False], continousPlage=False, uniform=True),
            'favorisationCoeff': int(Generator.generateValue([1, 40], continousPlage=True, uniform=False)),
            'focused': Generator.generateValue([True, False], continousPlage=False, uniform=True),
            'mweRepeition': Generator.generateValue([5, 10, 15, 20, 30], continousPlage=False, uniform=True)
        })
        configuration['embedding'].update({
            'pretrained': True,
            'manual': False,
            'average': True,
            'compactVocab': False,
            'lemma': Generator.generateValue([True, False], continousPlage=False, uniform=True),
            'dynamicVocab': False,
            'useB1': True,
            'useB-1': True,
        })
        if configuration['embedding']['pretrained']:
            configuration['embedding']['manual'] = False

        configuration['mlp'].update({
            'posEmb': int(Generator.generateValue([15, 100], uniform=False, continousPlage=True)),
            'tokenEmb': 300 if configuration['embedding']['pretrained'] else
            int(Generator.generateValue([100, 400], uniform=False, continousPlage=True)),
            'dense1UnitNumber': int(Generator.generateValue([25, 600], uniform=False, continousPlage=True)),
            'dense1Dropout': float(Generator.generateValue([.1, .2, .3, .4], continousPlage=False, uniform=True)),
            'batchSize': Generator.generateValue([16, 32, 48, 64, 128], continousPlage=False, uniform=True),
            'lr': round(Generator.generateValue([.01, .07], continousPlage=True, uniform=False), 3),
        })

    @staticmethod
    def generateRNNConf():
        configuration['rnn']['wordDim'] = int(Generator.generateValue([250, 600], True, True))
        configuration['rnn']['posDim'] = int(Generator.generateValue([25, 100], True, True))

        configuration['rnn']['gru'] = True  # Generator.generateValue([True, False], False, False)
        configuration['rnn']['wordRnnUnitNum'] = int(Generator.generateValue([25, 200], True, True))
        configuration['rnn']['posRnnUnitNum'] = int(Generator.generateValue([25, 200], True, True))
        configuration['rnn']['rnnDropout'] = round(Generator.generateValue([0, .3], True, True), 1)

        configuration['rnn']['useDense'] = True  # Generator.generateValue([True, False], False, False)
        configuration['rnn']['denseDropout'] = 0  # round(Generator.generateValue([0, .5], True, True), 1)
        configuration['rnn']['denseUnitNum'] = int(Generator.generateValue([5, 200], True, True))
        configuration['rnn']['batchSize'] = 64  # Generator.generateValue([16, 32, 64, 128], False, True)
        configuration['nn']['compactVocab'] = Generator.generateValue([True, False], False, False)

    @staticmethod
    def generateLinearConf():
        configuration['features'].update({
            'lemma': True,
            'token': Generator.generateValue([True, False], favorisationTaux=.3),
            'pos': True,
            'suffix': False,
            'b1': Generator.generateValue([True, False], favorisationTaux=.5),
            'bigram': True,
            's0b2': Generator.generateValue([True, False], favorisationTaux=.5),
            'trigram': Generator.generateValue([True, False], favorisationTaux=.5),
            'syntax': False,
            'syntaxAbstract': False,
            'dictionary': Generator.generateValue([True, False], favorisationTaux=.5),
            's0TokenIsMWEToken': Generator.generateValue([True, False], favorisationTaux=.5),
            's0TokensAreMWE': False,
            'history1': Generator.generateValue([True, False], favorisationTaux=.5),
            'history2': Generator.generateValue([True, False], favorisationTaux=.5),
            'history3': Generator.generateValue([True, False], favorisationTaux=.5),
            'stackLength': Generator.generateValue([True, False], favorisationTaux=.5),
            'distanceS0s1': Generator.generateValue([True, False], favorisationTaux=.5),
            'distanceS0b0': Generator.generateValue([True, False], favorisationTaux=.5)
        })

    @staticmethod
    def generateKiperwasserConf():
        kiperConf = configuration['kiperwasser']
        kiperConf['wordDim'] = int(Generator.generateValue([50, 500], True))
        kiperConf['posDim'] = int(Generator.generateValue([15, 150], True))
        kiperConf['denseActivation'] = 'tanh'  # str(Generator.generateValue(['tanh', 'relu'], False))
        configuration['nn']['optimizer'] = 'adagrad'  # str(Generator.generateValue(['adam', 'adagrad'], False))
        kiperConf['lr'] = 0.07
        kiperConf['dense1'] = int(Generator.generateValue([10, 350], True))
        kiperConf['rnnDropout'] = round(Generator.generateValue([.1, .4], True), 2)
        kiperConf['rnnUnitNum'] = int(Generator.generateValue([20, 250], True))
        kiperConf['rnnLayerNum'] = 1  # Generator.generateValue([1, 2], False)

        configuration['embedding']['compactVocab'] = Generator.generateValue([True, False], False)
        configuration['embedding']['lemma'] = True  # Generator.generateValue([True, False], False)

    @staticmethod
    def generateMultTaskingConf():
        configuration['multitasking'].update({
            'windowSize': 3,
            'tokenDim': int(Generator.generateValue([25, 200], True)),
            'affixeDim': int(Generator.generateValue([5, 25], True)),
            'capitalDim': int(Generator.generateValue([1, 10], True)),
            'symbolDim': int(Generator.generateValue([5, 15], True)),
            'taggingDenseUnits': int(Generator.generateValue([25, 200], True)),
            'IdenDenseUnitNumber': int(Generator.generateValue([25, 200], True)),
            'useCapitalization': Generator.generateValue([True, False], False),
            'useSymbols': Generator.generateValue([True, False], False),
            'testOnToken': True,
            'useB1': Generator.generateValue([True, False], False),
            'useBx': Generator.generateValue([True, False], False),
            'taggingBatchSize': int(Generator.generateValue([8, 128], True)),
            'identBatchSize': int(Generator.generateValue([8, 128], True)),
            'initialEpochs': int(Generator.generateValue([1, 5], True)),
            'jointLearningEpochs': int(Generator.generateValue([8, 20], True)),
            'lr': round(Generator.generateValue([0.01, 0.2], True), 3)
        })
        configuration['embedding']['lemma'] = Generator.generateValue([True, False], False)
        configuration['sampling']['importantSentences'] = True
        configuration['sampling']['overSampling'] = True

    @staticmethod
    def generateMlpPhrase():
        configuration['mlpPhrase'].update({
            'phraseMaxLength': 50,
            'phraseTokenEmb': int(Generator.generateValue([25, 200], True)),
            'phrasePosEmb': int(Generator.generateValue([5, 50], True)),
            'gru': Generator.generateValue([True, False], False, True),
            'wordRnnUnitNum': int(Generator.generateValue([25, 500], True)),
            'useB1': Generator.generateValue([True, False], False),
            'useB-1': Generator.generateValue([True, False], False),
            'transPosEmb': int(Generator.generateValue([5, 50], True)),
            'transTokenEmb': int(Generator.generateValue([25, 200], True)),
            'denseUnitNumber': int(Generator.generateValue([25, 500], True)),
            'lr': round(Generator.generateValue([0.01, 0.2], True), 3)
        })
        configuration['embedding']['lemma'] = Generator.generateValue([True, False], False)
        configuration['sampling']['importantSentences'] = True
        configuration['sampling']['overSampling'] = True

    @staticmethod
    def generateChenManning():
        Standard.setChenManningParameters()
        configuration['chenParams'].update({
            'monitor': Generator.generateValue(['val_loss', 'val_acc'], False, True),
            'earlyStopping': Generator.generateValue([True, False], False, True)
        })
        if configuration['chenParams']['earlyStopping']:
            configuration['chenParams']['epochs'] = 100
            configuration['chenParams']['minDelta'] = round(Generator.generateValue([.0001, 0.1], True), 5)
            configuration['chenParams']['patience'] = int(Generator.generateValue([2, 10], True))
        else:
            configuration['chenParams']['epochs'] = int(Generator.generateValue([5, 50], True))

        configuration['chenParams']['lr'] = round(Generator.generateValue([0.01, 0.2], True), 3)
        configuration['embedding']['lemma'] = Generator.generateValue([True, False], False, True)
        configuration['sampling']['importantSentences'] = False
