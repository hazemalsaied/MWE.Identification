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
        'idenDenseUnits': 64,
        'useCapitalization': True,
        'useSymbols': True,
        'testOnToken': True,
        'useB1': True,
        'useBx': True,
        'sytacticLabelDim': 25,
        'depParsingDenseUnits': 200
    },
    'xp': {
        'linear': False,
        'compo': False,
        'kiperwasser': False,
        'kiperComp': False,
        'mlpPhrase': False,
        'rnn': False,
        'rnnNonCompo': False,
        'rmlpTree': False,
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
    'rmlpTree': {
        'posEmb': 42,
        'tokenEmb': 480,
        'trainable': True,
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
        'createDepGraphs': False,
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
        'group': 'tweebank',
        'nltk': False,
        'trainTaggerAndIdentifier': False,
        'trainInTransfert': False,
        'shuffleOrRedistribute': True

    },
    'others': {
        'tuneCoop': False,
        'cvFolds': 5,
        'currentIter': -1,
        'shuffleTrain': False,
        'debugTrainNum': 10,
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
        'wordDim': 50,
        'posDim': 5,
        'optimizer': 'adagrad',
        'lr': 0.07,
        'dropout': .3,
        'batch': 1,
        'dense1': 25,
        'denseActivation': 'tanh',
        'denseDropout': 0,
        'rnnUnitNum': 5,
        'rnnDropout': 0.3,
        'rnnLayerNum': 2,
        'focusedElemNum': 8,
        'file': 'kiper.p',
        'earlyStop': False,
        'verbose': True,
        'eager': True,
        'pretrained': False,
        'gru': True,
        'trainValidationSet': True,
        'sampling': True,
        'samplingTaux': 15
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
        'useB-1': 0,
        'shuffle': False,
        'rnnSequence': False
    },
    'nn': {
        'validationSplit': .2,
        'monitor': 'val_loss',
        'loss': 'categorical_crossentropy',
        'optimizer': 'adagrad',
        'epochs': 10,
        'earlyStop': True,
        'checkPoint': False,
        'minDelta': .2,
        'patience': 4,
        'dense1Activation': 'relu',
        'predictVerbose': False,
        'depParserBatchSize': 32,
        'identBatchSize': 32,
        'idenLR': .01,
        'taggingLR': .02,
        'depParsingLR': .03,
        'taggingBatchSize': 32,
        'jointLearningEpochs': 20,
        'initialEpochs': 1,
        'batchSize': 32,
        'optim': 'adagrad'
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


class TrendConfig:
    @staticmethod
    def identAvgJoint():
        configuration['multitasking'].update({
            'affixeDim': 12,
            'capitalDim': 4,
            'depParsingDenseUnits': 101,
            'idenDenseUnits': 79,
            'symbolDim': 9,
            'sytacticLabelDim': 19,
            'taggingDenseUnits': 82,
            'tokenDim': 86,
            'useB1': True,
            'useBx': True,
            'useCapitalization': True,
            'useSymbols': True
        })

        configuration['embedding']['lemma'] = True

        configuration['nn'].update({
            'depParserBatchSize': 134,
            'depParsingLR': .017,
            'earlyStop': True,
            'idenLR': .015,
            'identBatchSize': 137,
            'initialEpochs': 1,
            'minDelta': 0.033,
            'monitor': 'val_loss',
            'taggingBatchSize': 141,
            'taggingLR': .029
        })

    @staticmethod
    def jointAvgJoint():
        configuration['multitasking'].update({
            'affixeDim': 12,
            'capitalDim': 4,
            'depParsingDenseUnits': 106,
            'idenDenseUnits': 78,
            'symbolDim': 9,
            'sytacticLabelDim': 20,
            'taggingDenseUnits': 79,
            'tokenDim': 84,
            'useB1': True,
            'useBx': True,
            'useCapitalization': True,
            'useSymbols': True})

        configuration['embedding']['lemma'] = True
        configuration['nn'].update({
            'depParserBatchSize': 128,
            'depParsingLR': 0.012,
            'earlyStop': True,
            'idenLR': 0.015,
            'identBatchSize': 140,
            'initialEpochs': 1,
            'minDelta': 0.036,
            'monitor': 'val_loss',
            'taggingBatchSize': 138,
            'taggingLR': 0.03
        })

    @staticmethod
    def rmlp():
        configuration['embedding'].update({
            'compactVocab': False,
            'dynamicVocab': False,
            'lemma': True,
            'pretrained': True
        })
        configuration['rnn'].update({
            'bTokenNum': 3,
            'batchSize': 160,
            'denseDropout': 0.3,
            'denseUnitNum': 80,
            'gru': True,
            'lr': .044,
            'posDim': 55,
            'posRnnUnitNum': 70,
            'rnnDropout': 0.2,
            'rnnSequence': False,
            'shuffle': False,
            'useB-1': 1,
            'wordDim': 300,
            'wordRnnUnitNum': 100,
            'EarlyStop': True,
        })
        configuration['nn'].update({
            'EarlyStop': True,
            'minDelta': 0.022,
            'monitor': 'val_loss'
        })

    @staticmethod
    def mlpTree():
        configuration['sampling'].update({
            'overSampling': True,
            'importantSentences': True,
            'importantTransitions': False,
            'favorisationCoeff': 11,
            'focused': False,
            'mweRepeition': 16,
            'sampleWeight': False
        })

        configuration['embedding'].update({
            'average': True,
            'compactVocab': True,
            'dynamicVocab': False,
            'lemma': True,
            'manual': False,
            'pretrained': True,
            'useB-1': 1,
            'useB1': 1
        })

        configuration['rmlpTree'].update({
            'denseDropout': 0.3,
            'denseUnitNumber': 90,
            'gru': True,
            'lr': 0.038,
            'posEmb': 40,
            'posRnnUnitNum': 80,
            'rnnDropout': 0.3,
            'rnnSequence': False,
            'shuffle': False,
            'tokenEmb': 300,
            'wordRnnUnitNum': 75
        })
        configuration['nn'].update({
            'monitor': 'val_loss',
            'earlyStop': True,
            'minDelta': 0.05,
            'batchSize': 256
        })

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
            'pretrained': True,
            'average': True,
            'compactVocab': True,
            'lemma': True,
            'dynamicVocab': False
        })
        configuration['mlp'].update({
            'posEmb': 60,
            'tokenEmb': 300,
            'dense1UnitNumber': 215,
            'dense1Dropout': 0.3,
            'lr': 0.034,
            'trainable': True,
            'batchSize': 64,
            'posWindow': 3
        })

    @staticmethod
    def mlpPhrase():
        configuration['mlpPhrase'].update({
            'phraseMaxLength': 50,
            'phraseTokenEmb': 80,
            'phrasePosEmb': 18,
            'gru': True,
            'wordRnnUnitNum': 110,
            'useB1': True,
            'useB-1': True,
            'transPosEmb': 15,
            'transTokenEmb': 95,
            'denseUnitNumber': 115,
            'lr': .057
        })
        configuration['embedding']['lemma'] = True
        configuration['sampling']['importantSentences'] = True
        configuration['sampling']['overSampling'] = True

    @staticmethod
    def mtPos():
        configuration['multitasking'].update({
            'tokenDim': 69,
            'affixeDim': 13,
            'capitalDim': 3,
            'symbolDim': 9,
            'taggingDenseUnits': 89,
            'idenDenseUnits': 88,
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
    def mtIden():
        configuration['multitasking'].update({
            'tokenDim': 89,
            'affixeDim': 13,
            'capitalDim': 3,
            'symbolDim': 9,
            'taggingDenseUnits': 87,
            'idenDenseUnits': 81,
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
    def mtDepParsing():
        configuration['embedding']['lemma'] = True

        configuration['multitasking'].update({
            'idenDenseUnits': 84,
            'affixeDim': 12,
            'capitalDim': 3,
            'depParsingDenseUnits': 108,
            'symbolDim': 9,
            'sytacticLabelDim': 19,
            'taggingDenseUnits': 80,
            'tokenDim': 80,
            'useB1': True,
            'useBx': True,
            'useCapitalization': True,
            'useSymbols': True
        })

        configuration['nn'].update({
            'depParserBatchSize': 83,
            'depParsingLR': .022,
            'earlyStop': True,
            'minDelta': .02,
            'monitor': 'val_loss'
        })

    @staticmethod
    def mtJoint():
        configuration['multitasking'].update({
            'tokenDim': 83,
            'affixeDim': 13,
            'capitalDim': 3,
            'symbolDim': 8,
            'taggingDenseUnits': 90,
            'idenDenseUnits': 64,
            'useCapitalization': True,
            'useSymbols': True,
            'testOnToken': True,
            'useB1': True,
            'useBx': True,
            'identBatchSize': 41,
            'taggingBatchSize': 39,
            'lr': 0.04
        })
        configuration['nn']['initialEpochs'] = 2
        configuration['embedding']['lemma'] = True
        configuration['sampling']['importantSentences'] = True
        configuration['sampling']['overSampling'] = True

    @staticmethod
    def mlp():
        configuration['sampling'].update({
            'importantSentences': True,
            'overSampling': True,
            'sampleWeight': False,
            'favorisationCoeff': 15,
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

    @staticmethod
    def mlpFtb():
        configuration['sampling'].update({
            'importantSentences': True,
            'overSampling': True,
            'sampleWeight': False,
            'favorisationCoeff': 8,
            'focused': True,
            'mweRepeition': 16})
        configuration['embedding'].update({
            'useB1': 1,
            'useB-1': 0,
            'manual': False,
            'keras': False,
            'pretrained': True,
            'average': True,
            'compactVocab': True,
            'lemma': True,
            'dynamicVocab': False
        })
        configuration['mlp'].update({
            'posEmb': 60,
            'tokenEmb': 300,
            'dense1UnitNumber': 200,
            'dense1Dropout': 0.3,
            'lr': 0.04,
            'trainable': True,
            'batchSize': 64,
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
    def mlpDimsum():
        configuration['sampling'].update({
            'importantSentences': True,
            'overSampling': True,
            'sampleWeight': True,
            'favorisationCoeff': 8,
            'focused': False,
            'mweRepeition': 16})
        configuration['embedding'].update({
            'useB1': 1,
            'useB-1': 1,
            'manual': False,
            'keras': False,
            'pretrained': True,
            'average': True,
            'compactVocab': True,
            'lemma': True,
            'dynamicVocab': True
        })
        configuration['mlp'].update({
            'posEmb': 60,
            'tokenEmb': 300,
            'dense1UnitNumber': 200,
            'dense1Dropout': 0.3,
            'lr': 0.035,
            'trainable': True,
            'batchSize': 64,
        })

    @staticmethod
    def mlpOpen():
        configuration['sampling'].update({
            'importantSentences': True,
            'overSampling': True,
            'sampleWeight': False,
            'favorisationCoeff': 16,
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
            'posEmb': 57,
            'tokenEmb': 300,
            'dense1UnitNumber': 157,
            'dense1Dropout': 0.4,
            'lr': 0.04,
            'trainable': True,
            'batchSize': 56,
        })

    @staticmethod
    def mtPOSIden():
        configuration['multitasking'].update({
            'affixeDim': 12,
            'capitalDim': 3,
            'depParsingDenseUnits': 102,
            'idenDenseUnits': 89,
            'symbolDim': 9,
            'sytacticLabelDim': 20,
            'taggingDenseUnits': 82,
            'tokenDim': 83,
            'useB1': 1,
            'useBx': 1,
            'useCapitalization': 1,
            'useSymbols': 1,
        })
        configuration['embedding']['lemma'] = True
        configuration['embedding']['average'] = True

        configuration['nn'].update({
            'depParserBatchSize': 134,
            'depParsingLR': 0.02,
            'earlyStop': 1,
            'idenLR': 0.027,
            'identBatchSize': 126,
            'initialEpochs': 1,
            'minDelta': 0.034,
            'monitor': -1,
            'taggingBatchSize': 138,
            'taggingLR': 0.028
        })
        
        




class Standard:
    @staticmethod
    def chenManningParameters():
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
    def rmlpClosed():
        configuration['embedding'].update({
            'compactVocab': False,
            'dynamicVocab': False,
            'lemma': True,
            'pretrained': False
        })
        configuration['rnn'].update({
            'bTokenNum': 2,
            'batchSize': 256,
            'denseDropout': 0.4,
            'denseUnitNum': 20,
            'gru': False,
            'lr': .027,
            'posDim': 55,
            'posRnnUnitNum': 50,
            'rnnDropout': 0.2,
            'rnnSequence': False,
            'shuffle': False,
            'useB-1': 0,
            'wordDim': 175,
            'wordRnnUnitNum': 100,
            'EarlyStop': True,
        })
        configuration['nn'].update({
            'EarlyStop': True,
            'minDelta': .006,
            'monitor': 'val_loss'
        })

    @staticmethod
    def rmlpOpen():
        configuration['embedding'].update({
            'compactVocab': False,
            'dynamicVocab': True,
            'lemma': True,
            'pretrained': True
        })
        configuration['rnn'].update({
            'bTokenNum': 2,
            'batchSize': 128,
            'denseDropout': 0.1,
            'denseUnitNum': 150,
            'gru': False,
            'lr': .031,
            'posDim': 70,
            'posRnnUnitNum': 40,
            'rnnDropout': 0.2,
            'rnnSequence': False,
            'shuffle': False,
            'useB-1': 0,
            'wordDim': 300,
            'wordRnnUnitNum': 100,
            'EarlyStop': True,
        })
        configuration['nn'].update({
            'EarlyStop': True,
            'minDelta': .007,
            'monitor': 'val_loss'
        })

    @staticmethod
    def mlpTreeClosed():
        configuration['sampling'].update({
            'overSampling': True,
            'importantSentences': True,
            'importantTransitions': False,
            'favorisationCoeff': 17,
            'focused': True,
            'mweRepeition': 20,
            'sampleWeight': True
        })
        configuration['embedding'].update({
            'average': False,
            'compactVocab': False,
            'dynamicVocab': False,
            'lemma': True,
            'manual': True,
            'pretrained': False,
            'useB-1': 0,
            'useB1': 1
        })

        configuration['rmlpTree'].update({
            'denseDropout': 0.6,
            'denseUnitNumber': 140,
            'gru': True,
            'lr': 0.058,
            'posEmb': 20,
            'posRnnUnitNum': 100,
            'rnnDropout': 0.4,
            'rnnSequence': False,
            'shuffle': False,
            'tokenEmb': 110,
            'wordRnnUnitNum': 50
        })
        configuration['nn'].update({
            'monitor': 'val_loss',
            'earlyStop': True,
            'minDelta': 0.05,
            'batchSize': 256
        })

    @staticmethod
    def mlpTreeOpen():
        configuration['sampling'].update({
            'overSampling': True,
            'importantSentences': True,
            'importantTransitions': False,
            'favorisationCoeff': 5,
            'focused': False,
            'mweRepeition': 15,
            'sampleWeight': True
        })
        configuration['embedding'].update({
            'average': True,
            'compactVocab': True,
            'dynamicVocab': False,
            'lemma': True,
            'manual': False,
            'pretrained': True,
            'useB-1': 1,
            'useB1': 1
        })

        configuration['rmlpTree'].update({
            'denseDropout': 0.5,
            'denseUnitNumber': 45,
            'gru': True,
            'lr': 0.053,
            'posEmb': 50,
            'posRnnUnitNum': 100,
            'rnnDropout': 0.3,
            'rnnSequence': False,
            'shuffle': False,
            'tokenEmb': 300,
            'wordRnnUnitNum': 115
        })

        configuration['nn'].update({
            'monitor': 'val_loss',
            'earlyStop': True,
            'minDelta': 0.05,
            'batchSize': 256
        })

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
            'pretrained': True,
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
            'posWindow': 2
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



    # @staticmethod
    # def mlpFtb():
    #     samling = configuration['sampling']
    #     samling['importantSentences'] = True
    #     samling['overSampling'] = True
    #     samling['sampleWeight'] = True
    #     samling['favorisationCoeff'] = 3
    #     samling['focused'] = True
    #
    #     configuration['nn']['optimizer'] = 'adagrad'
    #     configuration['mlp']['lr'] = 0.059
    #
    #     configuration['embedding']['lemma'] = True
    #     configuration['mlp']['posEmb'] = 103
    #     configuration['mlp']['tokenEmb'] = 410
    #     configuration['embedding']['compactVocab'] = True
    #
    #     configuration['mlp']['dense1UnitNumber'] = 167
    #     configuration['mlp']['dense1Dropout'] = 0.16

    @staticmethod
    def mlpDimsumClosed():
        configuration['sampling'].update({
            'importantSentences': True,
            'overSampling': True,
            'sampleWeight': False,
            'favorisationCoeff': 1,
            'focused': False,
            'mweRepeition': 15})
        configuration['embedding'].update({
            'useB1': 1,
            'useB-1': 0,
            'manual': True,
            'keras': False,
            'pretrained': False,
            'average': True,
            'compactVocab': False,
            'lemma': False,
            'dynamicVocab': True
        })
        configuration['mlp'].update({
            'posEmb': 90,
            'tokenEmb': 470,
            'dense1UnitNumber': 140,
            'dense1Dropout': 0.1,
            'lr': 0.016,
            'trainable': True,
            'batchSize': 16,
        })

    @staticmethod
    def mlpDimsumOpen():
        configuration['sampling'].update({
            'importantSentences': True,
            'overSampling': True,
            'sampleWeight': False,
            'favorisationCoeff': 1,
            'focused': False,
            'mweRepeition': 15})
        configuration['embedding'].update({
            'useB1': 1,
            'useB-1': 0,
            'manual': False,
            'keras': False,
            'pretrained': True,
            'average': True,
            'compactVocab': True,
            'lemma': True,
            'dynamicVocab': True
        })
        configuration['mlp'].update({
            'posEmb': 72,
            'tokenEmb': 300,
            'dense1UnitNumber': 580,
            'dense1Dropout': 0.1,
            'lr': 0.031,
            'trainable': True,
            'batchSize': 48,
        })

    @staticmethod
    def mlp():
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
    def mlpOpen():
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
    def mlpFtbClosed():
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
    def mlpFtbOpen():
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

    @staticmethod
    def mtPOSIdenOld():
        configuration['multitasking'].update({
            'tokenDim': 140,
            'affixeDim': 14,
            'capitalDim': 1,
            'symbolDim': 5,
            'taggingDenseUnits': 78,
            'idenDenseUnits': 30,
            'useCapitalization': False,
            'useSymbols': True,
            'testOnToken': True,
            'useB1': True,
            'useBx': True,
            'identBatchSize': 37,
            'taggingBatchSize': 21,
            'lr': 0.05
        })
        configuration['nn']['initialEpochs'] = 3
        configuration['embedding']['lemma'] = True
        configuration['sampling']['importantSentences'] = True
        configuration['sampling']['overSampling'] = True

    @staticmethod
    def mtPos():
        configuration['multitasking'].update({
            'tokenDim': 190,
            'affixeDim': 20,
            'capitalDim': 4,
            'symbolDim': 11,
            'taggingDenseUnits': 36,
            'idenDenseUnits': 197,
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
    def mtIdent():
        configuration['multitasking'].update({
            'tokenDim': 77,
            'affixeDim': 18,
            'capitalDim': 5,
            'symbolDim': 8,
            'taggingDenseUnits': 166,
            'idenDenseUnits': 74,
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

    @staticmethod
    def mtDepParsing():
        configuration['embedding']['lemma'] = True
        configuration['multitasking'].update({
            'idenDenseUnits': 44,
            'affixeDim': 10,
            'capitalDim': 1,
            'depParsingDenseUnits': 92,
            'symbolDim': 11,
            'sytacticLabelDim': 17,
            'taggingDenseUnits': 74,
            'tokenDim': 142,
            'useB1': False,
            'useBx': True,
            'useCapitalization': True,
            'useSymbols': True
        })
        configuration['nn'].update({
            'depParserBatchSize': 32,
            'depParsingLR': .033,
            'earlyStop': True,
            'minDelta': .008,
            'monitor': 'val_loss'
        })

    @staticmethod
    def identAvgJoint():
        configuration['multitasking'].update({
            'affixeDim': 20,
            'capitalDim': 1,
            'depParsingDenseUnits': 255,
            'idenDenseUnits': 120,
            'symbolDim': 10,
            'sytacticLabelDim': 34,
            'taggingDenseUnits': 108,
            'tokenDim': 39,
            'useB1': False,
            'useBx': True,
            'useCapitalization': True,
            'useSymbols': True})

        configuration['embedding']['lemma'] = True

        configuration['nn'].update({
            'depParserBatchSize': 128,
            'depParsingLR': 0.01,
            'earlyStop': True,
            'idenLR': 0.029,
            'identBatchSize': 256,
            'initialEpochs': 1,
            'minDelta': 0.016,
            'monitor': 'val_loss',
            'taggingBatchSize': 96,
            'taggingLR': 0.043})

    @staticmethod
    def jointAvgJoint():
        configuration['multitasking'].update({
            'affixeDim': 11,
            'capitalDim': 3,
            'depParsingDenseUnits': 127,
            'idenDenseUnits': 40,
            'symbolDim': 9,
            'sytacticLabelDim': 12,
            'taggingDenseUnits': 133,
            'tokenDim': 64,
            'useB1': True,
            'useBx': False,
            'useCapitalization': True,
            'useSymbols': True
        })

        configuration['embedding']['lemma'] = True

        configuration['nn'].update({
            'depParserBatchSize': 128,
            'depParsingLR': 0.012,
            'earlyStop': True,
            'idenLR': 0.01,
            'identBatchSize': 256,
            'initialEpochs': 2,
            'minDelta': 0.085,
            'monitor': 'val_loss',
            'taggingBatchSize': 96,
            'taggingLR': 0.013
        })

    @staticmethod
    def mtPOSIden():
        configuration['multitasking'].update({
            'affixeDim': 6,
            'capitalDim': 3,
            'depParsingDenseUnits': 41,
            'idenDenseUnits': 76,
            'symbolDim': 13,
            'sytacticLabelDim': 42,
            'taggingDenseUnits': 27,
            'tokenDim': 132,
            'useB1': True,
            'useBx': True,
            'useCapitalization': False,
            'useSymbols': True,
            'average': True,
        })
        configuration['embedding']['lemma'] = True

        configuration['nn'].update({
            'depParserBatchSize': 128,
            'depParsingLR': 0.015,
            'earlyStop': True,
            'idenLR': 0.037,
            'identBatchSize': 96,
            'initialEpochs': 1,
            'minDelta': 0.009,
            'monitor': 'loss',
            'taggingBatchSize': 256,
            'taggingLR': 0.037
        })

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
    def svm():
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
    def svmDiMSUM():
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
    def svmFtb():
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
    def rmlpTree():
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

        configuration['rmlpTree'].update({
            'wordRnnUnitNum': int(Generator.generateValue([25, 200], uniform=False, continousPlage=True)),
            'posRnnUnitNum': int(Generator.generateValue([25, 200], uniform=False, continousPlage=True)),
            'rnnDropout': float(Generator.generateValue([.1, .2, .3, .4, .5, .6], continousPlage=False, uniform=True)),
            'gru': Generator.generateValue([True, False], continousPlage=False, uniform=False),
            'posEmb': int(Generator.generateValue([15, 75], uniform=False, continousPlage=True)),
            'tokenEmb': 300 if configuration['embedding']['pretrained'] else
            int(Generator.generateValue([100, 300], uniform=False, continousPlage=True)),
            'denseUnitNumber': int(Generator.generateValue([25, 200], uniform=False, continousPlage=True)),
            'denseDropout': float(
                Generator.generateValue([.1, .2, .3, .4, .5, .6], continousPlage=False, uniform=True)),
            'lr': round(Generator.generateValue([.01, .2], continousPlage=True, uniform=False), 3),
            'shuffle': Generator.generateValue([True, False], continousPlage=False, uniform=False),
        })
        configuration['nn'].update({
            'monitor': Generator.generateValue(['val_loss', 'val_acc'], False, False),
            'earlyStop': True,  # Generator.generateValue([True, False], False, False),
            'minDelta': round(Generator.generateValue([0.001, 0.1], True), 3),
            'batchSize': int(Generator.generateValue([96, 128, 256], False))
        })

    @staticmethod
    def mlp():
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
        configuration['nn'].update({
            'monitor': Generator.generateValue(['val_loss', 'val_acc'], False, False),
            'earlyStop': Generator.generateValue([True, False], False, False),
            'minDelta': round(Generator.generateValue([0.001, 0.1], True), 3),
        })

    @staticmethod
    def mlpOpen():
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
    def rmlp():
        configuration['rnn'].update({
            'wordDim': int(Generator.generateValue([50, 300], True, True)),
            'posDim': int(Generator.generateValue([25, 75], True, True)),
            'gru': Generator.generateValue([True, False], False, False),
            'wordRnnUnitNum': int(Generator.generateValue([25, 150], True, True)),
            'posRnnUnitNum': int(Generator.generateValue([25, 100], True, True)),
            'rnnDropout': round(Generator.generateValue([0, .3], True, True), 1),
            'denseDropout': round(Generator.generateValue([0, .5], True, True), 1),
            'denseUnitNum': int(Generator.generateValue([5, 150], True, True)),
            'lr': round(Generator.generateValue([0.01, 0.2], True), 3),
            'earlyStop': True,
            's0TokenNum': 4,
            's1TokenNum': 2,
            'bTokenNum': int(Generator.generateValue([1, 5], True, True)),
            'useB-1': int(Generator.generateValue([0, 1], False, False)),
            'shuffle': Generator.generateValue([False, True], False),
            'rnnSequence': Generator.generateValue([False, True], False)
        })
        configuration['nn'].update({
            'monitor': Generator.generateValue(['val_loss', 'val_acc'], False, False),
            'earlyStop': Generator.generateValue([True, False], False, False),
            'minDelta': round(Generator.generateValue([0.001, 0.1], True), 3),
            'batchSize': int(Generator.generateValue([96, 128, 256], False)),
        })
        configuration['sampling']['importantSentences'] = True
        configuration['sampling']['overSampling'] = True
        configuration['embedding']['lemma'] = Generator.generateValue([True, False], False)
        configuration['embedding']['pretrained'] = Generator.generateValue([True, False], False)
        if configuration['embedding']['pretrained']:
            configuration['rnn']['wordDim'] = 300
        configuration['embedding']['compactVocab'] = Generator.generateValue([False, True], False)
        configuration['embedding']['dynamicVocab'] = Generator.generateValue([False, True], False)

    @staticmethod
    def svm():
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
    def kiper():

        # configuration['kiperwasser'].update({
        #     'wordDim': int(Generator.generateValue([50, 350], True)),
        #     'posDim': int(Generator.generateValue([5, 75], True)),
        #     'optimizer': 'adagrad',
        #     'lr': round(Generator.generateValue([0.01, 0.2], True), 3),
        #     'dropout': float(Generator.generateValue([.1, .2, .3, .4, .5, .6, .7], False)),
        #     'batch': int(Generator.generateValue([96, 128, 256], False)),
        #     'dense1': int(Generator.generateValue([50, 250], True)),
        #     'denseActivation': 'tanh', #str(Generator.generateValue(['tanh', 'relu'], False)),
        #     'denseDropout': float(Generator.generateValue([.1, .2, .3, .4, .5, .6, .7], False)),
        #     'rnnUnitNum': int(Generator.generateValue([50, 150], True)),
        #     'rnnDropout': float(Generator.generateValue([.1, .2, .3, .4, .5, .6, .7], False)),
        #     'rnnLayerNum': 1, #int(Generator.generateValue([1, 2], False)),
        #     'focusedElemNum': 8,
        #     'file': 'kiper.p',
        #     'earlyStop': True,
        #     'verbose': True,
        #     'eager': Generator.generateValue([True, False], False),
        #     'gru': False#Generator.generateValue([True, False], False)
        #     # 'trainValidationSet': Generator.generateValue([True, False], False),
        #     # 'sampling': Generator.generateValue([True, False], False),
        #     # 'samplingTaux':  int(Generator.generateValue([5, 50], True)),
        #     # 'pretrained': Generator.generateValue([True, False], False)
        # })
        # if configuration['kiperwasser']['pretrained']:
        #     configuration['kiperwasser']['wordDim'] = 300
        # # configuration['sampling']['importantSentences'] = Generator.generateValue([True, False], False)
        # # configuration['embedding']['compactVocab'] = Generator.generateValue([True, False], False)
        # configuration['embedding']['lemma'] = Generator.generateValue([True, False], False)
        # configuration['nn'].update({
        #     'epochs': 15,
        #     'minDelta': round(Generator.generateValue([0.001, 0.1], True), 3),
        #     'patience': 4,
        # })
        # # kiperConf = configuration['kiperwasser']
        # # kiperConf['wordDim'] = int(Generator.generateValue([50, 500], True))
        # # kiperConf['posDim'] = int(Generator.generateValue([15, 150], True))
        # # kiperConf['denseActivation'] = 'tanh'  # str(Generator.generateValue(['tanh', 'relu'], False))
        # # configuration['nn']['optimizer'] = 'adagrad'  # str(Generator.generateValue(['adam', 'adagrad'], False))
        # # kiperConf['lr'] = 0.07
        # # kiperConf['dense1'] = int(Generator.generateValue([10, 350], True))
        # # kiperConf['rnnDropout'] = round(Generator.generateValue([.1, .4], True), 2)
        # # kiperConf['rnnUnitNum'] = int(Generator.generateValue([20, 250], True))
        # # kiperConf['rnnLayerNum'] =int(Generator.generateValue([1, 2], False))

        configuration['kiperwasser'].update({
            'wordDim': 50,  # int(Generator.generateValue([50, 200], True)),
            'posDim': int(Generator.generateValue([5, 75], True)),
            'optimizer': 'adagrad',
            'lr': round(Generator.generateValue([0.01, 0.2], True), 3),
            'dropout': .1,  # float(Generator.generateValue([.1, .2, .3, .4, .5, .6, .7], False)),
            'batch': int(Generator.generateValue([96, 128, 256], False)),
            'dense1': 50,  # int(Generator.generateValue([50, 250], True)),
            'denseActivation': 'tanh',  # str(Generator.generateValue(['tanh', 'relu'], False)),
            'denseDropout': .1,  # float(Generator.generateValue([0, .1, .2, .3, .4], False)),
            'rnnUnitNum': 50,  # int(Generator.generateValue([50, 150], True)),
            'rnnDropout': .1,  # float(Generator.generateValue([.1, .2, .3, .4, .5], False)),
            'rnnLayerNum': 1,  # int(Generator.generateValue([1, 2], False)),
            'focusedElemNum': 8,
            'file': 'kiper.p',
            'earlyStop': True,
            'verbose': True,
            'eager': False,  # Generator.generateValue([True, False], False),
            'gru': False  # Generator.generateValue([True, False], False)
            # 'trainValidationSet': Generator.generateValue([True, False], False),
            # 'sampling': Generator.generateValue([True, False], False),
            # 'samplingTaux':  int(Generator.generateValue([5, 50], True)),
            # 'pretrained': Generator.generateValue([True, False], False)
        })
        if configuration['kiperwasser']['pretrained']:
            configuration['kiperwasser']['wordDim'] = 300
        # configuration['sampling']['importantSentences'] = Generator.generateValue([True, False], False)
        # configuration['embedding']['compactVocab'] = Generator.generateValue([True, False], False)
        configuration['embedding']['lemma'] = True  # Generator.generateValue([True, False], False)
        configuration['nn'].update({
            'epochs': 15,
            'minDelta': round(Generator.generateValue([0.001, 0.1], True), 3),
            'patience': 4,
        })

    @staticmethod
    def mlpPhrase():
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
    def chenManning():
        Standard.chenManningParameters()
        configuration['chenParams'].update({
            'tokenEmb': int(Generator.generateValue([25, 400], True)),
            'posEmb': int(Generator.generateValue([5, 100], True)),
            'synLabelEmb': int(Generator.generateValue([5, 100], True)),
            'dense1UnitNumber': int(Generator.generateValue([25, 400], True)),
            'dense1Activation': 'relu',
            'dense1Dropout': float(Generator.generateValue([.1, .2, .3, .4, .5, .6, .7], False)),
            'lr': round(Generator.generateValue([0.01, 0.2], True), 3),
            'batchSize': int(Generator.generateValue([16, 32, 48, 64, 96, 128, 256], False)),
            'unlabeled': False,
            'l2': Generator.generateValue([10e-2, 10e-3, 10e-4, 10e-5, 10e-6, 10e-7], False, True),
            'regularizer': Generator.generateValue([True, False], False, True),
            'cubeActivation': Generator.generateValue([True, False], False, True),
            'pretrained': Generator.generateValue([False, True], False, False),
            'earlyStopping': Generator.generateValue([True, False], False, False),
            'epochs': 20,
            'minDelta': round(Generator.generateValue([0.001, 0.1], True), 3),
            'patience': 4,
            'monitor': Generator.generateValue(['val_loss', 'val_acc'], False, False),
            'validationSplit': .2
        })
        if configuration['chenParams']['pretrained']:
            configuration['chenParams']['tokenEmb'] = 300
        configuration['embedding']['lemma'] = Generator.generateValue([True, False], False, True)
        configuration['sampling']['importantSentences'] = False

    @staticmethod
    def mt():
        configuration['multitasking'].update({
            'windowSize': 3,
            # Embedding dimensions
            'tokenDim': int(Generator.generateValue([25, 200], True)),
            'affixeDim': int(Generator.generateValue([5, 25], True)),
            'capitalDim': int(Generator.generateValue([1, 10], True)),
            'symbolDim': int(Generator.generateValue([5, 15], True)),
            'useB1': Generator.generateValue([True, False], False),
            'useBx': Generator.generateValue([True, False], False),
            # Dense layers
            'taggingDenseUnits': int(Generator.generateValue([25, 200], True)),
            'idenDenseUnits': int(Generator.generateValue([25, 200], True)),
            'depParsingDenseUnits': int(Generator.generateValue([25, 300], True)),
            'sytacticLabelDim': int(Generator.generateValue([5, 50], True)),
            # Tagging module
            'useCapitalization': Generator.generateValue([True, False], False),
            'useSymbols': Generator.generateValue([True, False], False),
            'testOnToken': True
        })
        configuration['nn'].update({
            'validationSplit': .2,
            'monitor': Generator.generateValue(['val_loss', 'val_acc'], False, False),
            'optim': Generator.generateValue(['adam', 'adagrad'], False, False),
            'loss': 'categorical_crossentropy',
            'optimizer': 'adagrad',
            'epochs': 20,
            'earlyStop': Generator.generateValue([True, False], False, False),
            'checkPoint': False,
            'minDelta': round(Generator.generateValue([0.005, 0.1], True), 3),
            'patience': 4,
            'predictVerbose': False,
            'depParserBatchSize': int(Generator.generateValue([64, 96, 128, 256], False)),
            'taggingBatchSize': int(Generator.generateValue([64, 96, 128, 256], False)),
            'identBatchSize': int(Generator.generateValue([64, 96, 128, 256], False)),
            'idenLR': round(Generator.generateValue([0.005, 0.09], True), 3),
            'taggingLR': round(Generator.generateValue([0.005, 0.09], True), 3),
            'depParsingLR': round(Generator.generateValue([0.005, 0.05], True), 3),
            'initialEpochs': int(Generator.generateValue([1, 3], True)),
        })
        configuration['embedding']['lemma'] = Generator.generateValue([True, False], False)
        configuration['sampling']['importantSentences'] = True
        configuration['sampling']['overSampling'] = True
