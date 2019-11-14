import math

from corpus import *
from xpTools import xp, XpMode


def runRSGAsynch(langs, dataset, xpMode, division,
                 seeds=[0], xpNumByThread=50, xpNum=1,
                 mlpInLinear=False,
                 linearInMlp=False,
                 complentary=False,
                 dontParse=False):
    """
    A function used for running a tunning job, where each hyperparameter set is generated asynchronously
    :param langs:
    :param dataset: Parsme1.0, Parseme1.1, FTB, DiMSUM ?
    :param xpMode: SVM, MLP, MLP-RSent, MLP-RStack, MLP-RStack2, Kiperwasser?
    :param division: Fixedsize, trainVsDev, trainDevVsTest, ...
    :param seeds: 0, 1, [0,1]
    :param xpNumByThread: How many experiment by job? 100, 200, .. ?
    :param xpNum: How many run for each experiment?
    :param mlpInLinear: Stacking learning? MLP fed with SVM prediction
    :param linearInMlp: Stacking learning? SVM fed with MLP prediction
    :param complentary: Complementary learning? SVM + MLP
    :param dontParse: training a model without evaluating it?
    :return:
    """
    configs = []
    for i in range(xpNumByThread):
        generateConf(xpMode)
        configs.append(copy.deepcopy(configuration))
    for i in range(xpNumByThread):
        configuration.update(configs[i])
        if dontParse:
            configuration['tmp']['dontParse'] = True
        xp(langs, dataset, xpMode, division, xpNum=xpNum, seeds=seeds,
           mlpInLinear=mlpInLinear, linearInMlp=linearInMlp,
           complentary=complentary, outputCupt=False)


def runRSG(langs, dataset, xpMode, division, fileName,
           xpNumByThread=50, xpNum=1,
           mlpInLinear=False,
           linearInMlp=False,
           complentary=False):
    """
    A function used for running a tunning job, with respect of a given grill of hyperparameter sets
    :param langs:
    :param dataset:
    :param xpMode:
    :param division:
    :param fileName:
    :param xpNumByThread: How many experiment by job? 100, 200, .. ?
    :param xpNum: How many run for each experiment?
    :param mlpInLinear: Stacking learning? MLP fed with SVM prediction
    :param linearInMlp: Stacking learning? SVM fed with MLP prediction
    :param complentary: Complementary learning? SVM + MLP
    :return:
    """
    exps = getGrid(fileName)
    threadConf = []
    for i in range(len(exps)):
        exp = exps[i]
        if not exp[0]:
            for j in range(i, i + xpNumByThread):
                exps[j][0] = True
                threadConf.append(exps[j][1])
            break
    with open(os.path.join(configuration['path']['projectPath'], 'ressources/RSG', fileName), 'wb') as ff:
        pickle.dump(exps, ff)
    for i in range(len(threadConf)):
        configuration.update(threadConf[i])
        xp(langs, dataset, xpMode, division, xpNum=xpNum,
           mlpInLinear=mlpInLinear, linearInMlp=linearInMlp,
           complentary=complentary)


def getGrid(fileName):
    """
    provides the grid of hyperparameter sets, used for synchronuous tunnging
    :param fileName:
    :return:
    """
    randomSearchGridPath = os.path.join(configuration['path']['projectPath'], 'ressources/RSG', fileName)
    with open(randomSearchGridPath, 'rb') as ff:
        xps = pickle.load(ff)
        return xps


def generateConf(xpMode):
    """
    A function used for generating random hyperparameter sets
    :param xpMode:
    :return:
    """
    if xpMode == XpMode.rmlp:
        Generator.rmlp()
    elif xpMode == XpMode.linear:
        Generator.svm()
    elif xpMode == XpMode.kiperwasser:
        if configuration['tmp']['minimizedKiper']:
            Generator.minimizedKiper()
        else:
            Generator.kiper()
    elif xpMode == XpMode.rmlpTree:
        Generator.rmlpTree()
    elif xpMode == XpMode.multitasking:
        Generator.mt()
    elif xpMode == XpMode.mlpPhrase:
        Generator.mlpPhrase()
    elif xpMode == XpMode.chenManning:
        Generator.chenManning()
    else:
        Generator.mlp()


class Generator:
    """
    Each method of this class (except generateValue) is responsable of generating a random hyperparameter set
    for its corressponding model
    The content of these functions was the subject of numerous modifications and their contents is experimental
    """

    @staticmethod
    def generateValue(plage, continousPlage=False, uniform=False, favorisationTaux=0.7):
        """
        Reponsable of generating random values according to uniform or geometrically drawn distributions
        :param plage:
        :param continousPlage:
        :param uniform:
        :param favorisationTaux: used for generating a biased unifrom distribution
        :return:
        """
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
        """
        Responsable of generating random hyperparameter set for MLP-RStack2
        :return:
        """
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
        """
        Responsable of generating random hyperparameter set for MLP
        :return:
        """
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
    def rmlp():
        """
        Responsable of generating random hyperparameter set for MLP-RStack
        :return:
        """
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
        """
        Responsable of generating random hyperparameter set for SVM
        :return:
        """
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
        """
        Responsable of generating random hyperparameter set for Kiper
        :return:
        """
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
        configuration['sampling']['importantSentences'] = True
        configuration['kiperwasser'].update({
            'wordDim': int(Generator.generateValue([50, 200], True)),
            'posDim': int(Generator.generateValue([15, 75], True)),
            'optimizer': 'adagrad',
            'lr': round(Generator.generateValue([0.01, 0.1], True), 3),
            'dropout': float(Generator.generateValue([.1, .2, .3, .4, .5, .6, .7], False)),
            'batch': int(Generator.generateValue([128, 192, 256], False)),
            'dense1': int(Generator.generateValue([50, 250], True)),
            'denseActivation': str(Generator.generateValue(['tanh', 'relu'], False)),
            'denseDropout': float(Generator.generateValue([0, .1, .2, .3, .4], False)),
            'rnnUnitNum': int(Generator.generateValue([50, 150], True)),
            'rnnDropout': float(Generator.generateValue([.1, .2, .3, .4, .5], False)),
            'rnnLayerNum': int(Generator.generateValue([1, 2], False)),
            'focusedElemNum': 8,
            'file': 'kiper.p',
            'earlyStop': Generator.generateValue([True, False], False),
            'verbose': True,
            'eager': False,  # Generator.generateValue([True, False], False),
            'gru': Generator.generateValue([True, False], False),
            # 'trainValidationSet': Generator.generateValue([True, False], False),
            # 'sampling': Generator.generateValue([True, False], False),
            # 'samplingTaux':  int(Generator.generateValue([5, 50], True)),
            'pretrained': Generator.generateValue([True, False], False)
        })
        if configuration['kiperwasser']['pretrained']:
            configuration['kiperwasser']['wordDim'] = 300
        # configuration['sampling']['importantSentences'] = Generator.generateValue([True, False], False)
        configuration['embedding']['compactVocab'] = Generator.generateValue([True, False], False)
        configuration['embedding']['lemma'] = True  # Generator.generateValue([True, False], False)
        configuration['nn'].update({
            'epochs': 12,
            'minDelta': round(Generator.generateValue([0.001, 0.1], True), 3),
            'patience': 4,
        })

    @staticmethod
    def minimizedKiper():
        """
        Responsable of generating random hyperparameter set for Kiper
        :return:
        """
        configuration['sampling']['importantSentences'] = True
        configuration['kiperwasser'].update({
            'wordDim': int(Generator.generateValue([50, 150], True)),
            'posDim': int(Generator.generateValue([15, 65], True)),
            'optimizer': 'adagrad',
            'lr': round(Generator.generateValue([0.01, 0.2], True), 3),
            'dropout': float(Generator.generateValue([.1, .2, .3, .4, .5, .6, .7], False)),
            'batch': 16,
            'dense1': int(Generator.generateValue([50, 150], True)),
            'denseActivation': str(Generator.generateValue(['tanh', 'relu'], False)),
            'denseDropout': float(Generator.generateValue([0, .1, .2, .3, .4], False)),
            'rnnUnitNum': int(Generator.generateValue([50, 100], True)),
            'rnnDropout': float(Generator.generateValue([.1, .2, .3, .4, .5], False)),
            'rnnLayerNum': 1,  # int(Generator.generateValue([1, 2], False)),
            'file': 'kiper.p',
            'earlyStop': True,  # Generator.generateValue([True, False], False),
            'verbose': True,
            'gru': Generator.generateValue([True, False], False),
            # 'sampling': Generator.generateValue([True, False], False),
            # 'samplingTaux':  int(Generator.generateValue([5, 50], True)),
            'pretrained': False  # Generator.generateValue([True, False], False)
        })
        # if configuration['kiperwasser']['pretrained']:
        #     configuration['kiperwasser']['wordDim'] = 300
        # configuration['sampling']['importantSentences'] = Generator.generateValue([True, False], False)
        configuration['embedding']['compactVocab'] = Generator.generateValue([True, False], False)
        configuration['embedding']['lemma'] = True  # Generator.generateValue([True, False], False)
        configuration['nn'].update({
            'epochs': 7,
            'minDelta': round(Generator.generateValue([0.001, 0.5], True), 3)
        })

    @staticmethod
    def mlpPhrase():
        """
        Responsable of generating random hyperparameter set for MLP-RSent
        :return:
        """
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
        """
        Responsable of generating random hyperparameter set for syntactic parser ChenManning
        :return:
        """
        from config import Standard
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
        """
        Responsable of generating random hyperparameter set for Multtasking architecture
        :return:
        """
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
