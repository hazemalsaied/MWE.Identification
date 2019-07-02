import keras
import numpy as np
from keras import optimizers
from keras import regularizers
from keras.callbacks import EarlyStopping
from keras.layers import Activation
from keras.layers import Input, Dense, Flatten, Embedding, Dropout
from keras.models import Model
from keras.utils import to_categorical
from keras.utils.generic_utils import get_custom_objects
from nltk.parse.transitionparser import TransitionParser, Transition, Configuration
from numpy import zeros
import reports
from reports import *
from wordEmbLoader import empty
from wordEmbLoader import unk
import facebookEmb
params = configuration['chenParams']
consts = configuration['chenConstant']


class Network:
    def __init__(self, corpus):
        self.depLabelDic = dict()
        self.vocabulary = Vocabulary(corpus)
        self.data, self.labels, self.depLabelDic = DataFactory.getData(corpus, self.vocabulary)
        self.model = Network.build(self.vocabulary, self.depLabelDic, corpus.langName)

    def train(self):
        num_classes = 3 if params['unlabeled'] else len(self.depLabelDic)
        self.labels = to_categorical(self.labels, num_classes=num_classes)
        self.model.fit(self.data, self.labels,
                       validation_split=params['validationSplit'],
                       epochs=params['epochs'],
                       batch_size=params['batchSize'],
                       verbose=2,
                       callbacks=Network.getCallBacks())

    def test(self, corpus):
        depParserData, depParserLabels, depLabelDic = DataFactory.getData(corpus, self.vocabulary, train=False)
        classNum = 3 if params['unlabeled'] else len(self.depLabelDic)
        depParserLabels = to_categorical(depParserLabels, num_classes=classNum)
        results = self.model.evaluate(depParserData, depParserLabels, batch_size=32, verbose=0)
        sys.stdout.write('Dep Parsing accuracy = {0}\nLoss = {1}, \n'.format(
            round(results[1] * 100, 1), round(results[0], 3)))

    @staticmethod
    def build(vocabulary, depLabelDic, langName):
        def cube(x):
            return pow(x, 3)

        get_custom_objects().update({'cube': Activation(cube)})

        inputLayers, interLayers = [], []
        inputToken = Input((consts['confElements'],))
        inputLayers.append(inputToken)
        tokenEmb = Embedding(len(vocabulary.tokenIndices), params['tokenEmb'],
                             weights=Network.getWeightMatrix(langName, vocabulary.tokenIndices))(inputToken)
        tokenFlatten = Flatten()(tokenEmb)
        interLayers.append(tokenFlatten)
        inputPos = Input((consts['confElements'],))
        inputLayers.append(inputPos)
        posEmb = Embedding(len(vocabulary.posIndices), params['posEmb'])(inputPos)
        posFlatten = Flatten()(posEmb)
        interLayers.append(posFlatten)

        inputSynLabels = Input((consts['synLabelNum'],))
        inputLayers.append(inputSynLabels)
        posEmb = Embedding(len(vocabulary.syntacticLabelIndices), params['synLabelEmb'])(inputSynLabels)
        posFlatten = Flatten()(posEmb)
        interLayers.append(posFlatten)

        interLayers = keras.layers.concatenate(interLayers)
        denseLayer = Dense(params['dense1UnitNumber'],
                           kernel_regularizer=Network.getRegularizer())(interLayers)
        denseLayer = Activation(Network.getActivation())(denseLayer)
        denseLayer = Dropout(params['dense1Dropout'])(denseLayer)
        classeNum = 3 if params['unlabeled'] else len(depLabelDic)
        softmaxLayer = Dense(classeNum, activation='softmax')(denseLayer)
        model = Model(inputs=inputLayers, outputs=softmaxLayer)
        model.compile(loss=configuration['nn']['loss'],
                      optimizer=Network.getOptimizer(),
                      metrics=['accuracy'])
        sys.stdout.write(str(model.summary()) + doubleSep)
        return model

    @staticmethod
    def getActivation():
        if params['cubeActivation']:
            return 'cube'
        return params['dense1Activation']

    @staticmethod
    def getRegularizer():
        if params['regularizer']:
            return regularizers.l2(params['l2'])
        return None

    @staticmethod
    def getOptimizer():
        if configuration['others']['verbose']:
            sys.stdout.write(reports.seperator + reports.tabs +
                             'Optimizer : Adagrad,  learning rate = {0}'.format(params['lr'])
                             + reports.seperator)
        return optimizers.Adagrad(lr=params['lr'], epsilon=None, decay=0.0)

    @staticmethod
    def getCallBacks():
        if params['earlyStopping']:
            es = EarlyStopping(monitor=params['monitor'],
                               min_delta=params['minDelta'],
                               patience=params['patience'],
                               verbose=configuration['others']['verbose'])
            return [es]
        return None


    @staticmethod
    def getWeightMatrix(lang, tokenIndices):
        if params['pretrained']:
            embeddingMatrix = Network.getEmbMatrix(lang, tokenIndices)
            return [embeddingMatrix]
        return None

    @staticmethod
    def getEmbMatrix(lang, vocab):
        """
        create a pretrained embedding matrix by loading the pretrained embeddings of simple words
        of the vocabulary that exist in FastText, initializing random embeddings for new words,
        and averaging or summing embedding of attached words that could occupy the head of the stack
        :param lang:
        :param vocab: index:word vocabulary
        :return:
        """
        wordEmbDic = facebookEmb.loadFastTextEmbeddings(lang)
        #idxs = range(0, len(vocab))
        embeddingMatrix = zeros((len(vocab), params['tokenEmb']))
        indexWordVocab = dict()
        for k, v in vocab.items():
            indexWordVocab[v] = k
        for i in range(0, len(vocab)):
            if indexWordVocab[i] in wordEmbDic:
                embeddingMatrix[i] = np.asarray(wordEmbDic[indexWordVocab[i]], dtype=float)
            else:
                embeddingMatrix[i] = np.random.uniform(low=-.5, high=.5, size=(1, params['tokenEmb']))
        return embeddingMatrix


class Vocabulary:
    def __init__(self, corpus):
        tokenFreqs, posFreqs, sytacticLabels = Vocabulary.getFrequencyDics(corpus)
        self.tokenIndices = Vocabulary.indexateDic(tokenFreqs)
        self.posIndices = Vocabulary.indexateDic(posFreqs)
        self.syntacticLabelIndices = Vocabulary.indexateDic(sytacticLabels)

    def __str__(self):
        res = seperator + tabs + 'Vocabulary' + doubleSep
        res += tabs + 'Tokens := {0} * POS : {1}'.format(len(self.tokenIndices), len(self.posIndices)) \
            if not configuration['xp']['compo'] else ''
        res += seperator
        return res

    @staticmethod
    def getFrequencyDics(corpus):
        syntacticLabels = Vocabulary.getSynLabels(corpus)
        tokenVocab = {unk: 5, empty: 5, 'root': 5}
        posVocab = {unk: 5, empty: 5, 'root': 5}
        for sent in corpus.trainingSents:
            for t in sent.tokens:
                if t.getTokenOrLemma() not in tokenVocab:
                    tokenVocab[t.getTokenOrLemma()] = 1
                else:
                    tokenVocab[t.getTokenOrLemma()] += 1
                posVocab[t.posTag.lower()] = 1
        return tokenVocab, posVocab, syntacticLabels

    @staticmethod
    def getSynLabels(corpus):
        syntacticLabelVocab = {unk: 5, empty: 5, 'root':5}
        for depGraph in corpus.trainDepGraphs:
            for n in depGraph.nodes:
                if depGraph.nodes[n]['rel'] is not None:
                    k = depGraph.nodes[n]['rel'].lower()
                    if k not in syntacticLabelVocab:
                        syntacticLabelVocab[k] = 1
                    else:
                        syntacticLabelVocab[k] += 1
        return syntacticLabelVocab

    @staticmethod
    def indexateDic(dic):
        res = dict()
        r = range(len(dic))
        for i, k in enumerate(dic):
            res[k] = r[i]
        return res


class DataFactory(object):

    @staticmethod
    def getData(corpus, vocabulary, train=True):
        """
        Create the training example in the libsvm format and write it to the input_file.
        Reference : Page 32, Chapter 3. Dependency Parsing by Sandra Kubler, Ryan McDonal and Joakim Nivre (2009)
        """
        transParser = TransitionParser(TransitionParser.ARC_STANDARD)
        transition = Transition(transParser.ARC_STANDARD)
        count_proj = 0
        data, labels, labelDic = [[] for _ in range(3)], [], dict()
        sents = corpus.trainingSents if train else corpus.testingSents
        depGraphs = corpus.trainDepGraphs if train else corpus.testDepGraphs
        for i in range(len(sents)):
            depgraph = depGraphs[i]
            sent = sents[i]
            if not transParser._is_projective(depgraph):
                continue
            count_proj += 1
            conf = Configuration(depgraph)
            while len(conf.buffer) > 0:
                dataEntry = DataFactory.getDataEntry(conf, sent, vocabulary)
                for i in range(3):
                    data[i].append(dataEntry[i])
                b0 = conf.buffer[0]
                if len(conf.stack) > 0:
                    s0 = conf.stack[len(conf.stack) - 1]
                    # Left-arc operation
                    rel = transParser._get_dep_relation(b0, s0, depgraph)
                    if rel is not None:
                        if conf.stack[-1] - 1 >= 0 and conf.buffer[0] - 1 >= 0:
                            sent.tokens[conf.stack[-1] - 1].dependencyParent = sent.tokens[conf.buffer[0] - 1]
                        sent.tokens[conf.stack[-1] - 1].dependencyLabel = rel
                        key = Transition.LEFT_ARC + ':' + rel
                        if key not in labelDic:
                            labelDic[key] = len(labelDic)
                        transition.left_arc(conf, rel)
                        labels.append(labelDic[key])
                        continue
                    # Right-arc operation
                    rel = transParser._get_dep_relation(s0, b0, depgraph)
                    if rel is not None:
                        precondition = True
                        # Get the max-index of buffer
                        maxID = conf._max_address
                        for w in range(maxID + 1):
                            if w != b0:
                                relw = transParser._get_dep_relation(b0, w, depgraph)
                                if relw is not None:
                                    if (b0, relw, w) not in conf.arcs:
                                        precondition = False
                        if precondition:
                            key = Transition.RIGHT_ARC + ':' + rel
                            if conf.stack[-1] - 1 >= 0 and conf.buffer[0] - 1 >= 0:
                                sent.tokens[conf.buffer[0] - 1].dependencyParent = sent.tokens[conf.stack[-1] - 1]
                            else:
                                sent.tokens[conf.buffer[0] - 1].dependencyParent = None
                            sent.tokens[conf.buffer[0] - 1].dependencyLabel = rel
                            transition.right_arc(conf, rel)
                            if key not in labelDic:
                                labelDic[key] = len(labelDic)
                            labels.append(labelDic[key])
                            continue
                # Shift operation as the default
                key = Transition.SHIFT
                if key not in labelDic:
                    labelDic[key] = len(labelDic)
                transition.shift(conf)
                labels.append(labelDic[key])
        print(" Number of training examples : " + str(len(corpus.trainDepGraphs)))
        print(" Number of valid (projective) examples : " + str(count_proj))
        if params['unlabeled']:
            labels = DataFactory.toUnlabeled(labels, labelDic)
        return [np.asarray(data[i]) for i in range(3)], labels, labelDic

    @staticmethod
    def toUnlabeled(labels, labelDic):
        newLabels, inversedLabelDic = [], dict()
        for k, v in labelDic.items():
            inversedLabelDic[v] = k
        for l in labels:
            if str(inversedLabelDic[l].lower()).startswith('left'):
                newLabels.append(1)
            elif str(inversedLabelDic[l].lower()).startswith('right'):
                newLabels.append(2)
            else:
                newLabels.append(0)
        return newLabels

    @staticmethod
    def getDataEntry(conf, sent, vocabulary):
        dataEntry = [[] for _ in range(3)]
        DataFactory.getBufferTokens(conf, sent, vocabulary, dataEntry)
        DataFactory.getStackTokens(conf, sent, vocabulary, dataEntry)
        DataFactory.getStackLeftMosts(conf, sent, vocabulary, dataEntry)
        DataFactory.getStackRightMosts(conf, sent, vocabulary, dataEntry)
        DataFactory.getStackLeftAndRightMostOfLeftAndRightMosts(conf, sent, vocabulary, dataEntry)
        return dataEntry

    @staticmethod
    def getStackLeftMosts(conf, sent, vocab, dataEntry):
        syntacticLabels = []
        for i in range(2):
            if len(conf.stack) >= 2 - i:
                if conf.stack[i - 2] > 0:
                    si = sent.tokens[conf.stack[i - 2] - 1]
                    leftMostChildren = DataFactory.getLeftMostChildren(si, sent)
                    for t in leftMostChildren[:2]:
                        DataFactory.addAllIdxs(t, vocab, dataEntry)
                    for _ in range(2 - len(leftMostChildren)):
                        DataFactory.addAllIdxs(None, vocab, dataEntry)
                else:
                    DataFactory.addAllIdxs(None, vocab, dataEntry)
                    DataFactory.addAllIdxs(None, vocab, dataEntry)
            else:
                DataFactory.addAllIdxs(None, vocab, dataEntry)
                DataFactory.addAllIdxs(None, vocab, dataEntry)
        return syntacticLabels

    @staticmethod
    def getStackRightMosts(conf, sent, vocab, dataEntry):
        for i in range(2):
            if len(conf.stack) >= 2 - i:
                if conf.stack[i - 2] > 0:
                    si = sent.tokens[conf.stack[i - 2] - 1]
                    rightMostChildren = DataFactory.getRightMostChildren(si, sent)
                    for t in rightMostChildren[:2]:
                        DataFactory.addAllIdxs(t, vocab, dataEntry)
                    for _ in range(2 - len(rightMostChildren)):
                        DataFactory.addAllIdxs(None, vocab, dataEntry)
                else:
                    DataFactory.addAllIdxs(None, vocab, dataEntry)
                    DataFactory.addAllIdxs(None, vocab, dataEntry)
            else:
                DataFactory.addAllIdxs(None, vocab, dataEntry)
                DataFactory.addAllIdxs(None, vocab, dataEntry)

    @staticmethod
    def getStackLeftAndRightMostOfLeftAndRightMosts(conf, sent, vocab, dataEntry):
        for i in range(2):
            if len(conf.stack) >= 2 - i and conf.stack[i - 2] > 0:
                si = sent.tokens[conf.stack[i - 2] - 1]
                leftMostOfLeftMostChild = DataFactory.getLeftMostOfLeftMostChildren(si, sent)
                DataFactory.addAllIdxs(leftMostOfLeftMostChild, vocab, dataEntry)
                rightMostOfRightMostChild = DataFactory.getRightMostOfRightMostChildren(si, sent)
                DataFactory.addAllIdxs(rightMostOfRightMostChild, vocab, dataEntry)
            else:
                DataFactory.addAllIdxs(None, vocab, dataEntry)
                DataFactory.addAllIdxs(None, vocab, dataEntry)

    @staticmethod
    def getLeftMostChildren(token, sent):
        leftMostChildren = []
        for t in sent.tokens[:token.position - 1]:
            if t.dependencyParent == token.position:
                leftMostChildren.append(t)
        return leftMostChildren

    @staticmethod
    def getLeftMostOfLeftMostChildren(token, sent):
        leftMostChildren = []
        for t in sent.tokens[:token.position - 1]:
            if t.dependencyParent == token.position:
                leftMostChildren.append(t)
                break
        if leftMostChildren:
            return DataFactory.getLeftMostChildren(leftMostChildren[0], sent)[0]
        return None

    @staticmethod
    def getRightMostOfRightMostChildren(token, sent):
        rightMostChildren = []
        for t in sent.tokens[:token.position - 1]:
            if t.dependencyParent == token.position:
                rightMostChildren.append(t)
                break
        if rightMostChildren:
            return DataFactory.getRightMostChildren(rightMostChildren[0], sent)[0]
        return None

    @staticmethod
    def getRightMostChildren(token, sent):
        rightMostChildren = []
        for t in reversed(sent.tokens[token.position:]):
            if t.dependencyParent == token.position:
                rightMostChildren.append(t)
        return rightMostChildren

    @staticmethod
    def addAllIdxs(t, vocab, dataEntry):
        DataFactory.addTokenIdx(t, vocab, dataEntry)
        DataFactory.addPosTagIdx(t, vocab, dataEntry)
        DataFactory.addSynLabelIdx(t, vocab, dataEntry)

    @staticmethod
    def addTokenIdx(t, vocab, dataEntry):
        if t is not None:
            if t == 'root':
                dataEntry[0].append(vocab.tokenIndices['root'])
            else:
                if t.getTokenOrLemma() in vocab.tokenIndices:
                    dataEntry[0].append(vocab.tokenIndices[t.getTokenOrLemma()])
                else:
                    dataEntry[0].append(vocab.tokenIndices[unk])
        else:
            dataEntry[0].append(vocab.tokenIndices[empty])

    @staticmethod
    def addPosTagIdx(t, vocab, dataEntry):
        if t is not None:
            if t == 'root':
                dataEntry[1].append(vocab.posIndices['root'])
            else:
                if t.posTag.lower() in vocab.posIndices:
                    dataEntry[1].append(vocab.posIndices[t.posTag.lower()])
                else:
                    dataEntry[1].append(vocab.posIndices[unk])
        else:
            dataEntry[1].append(vocab.posIndices[empty])

    @staticmethod
    def addSynLabelIdx(t, vocab, dataEntry):
        if t is not None:
            if t == 'root':
                dataEntry[2].append(vocab.syntacticLabelIndices['root'])
            elif t.dependencyLabel.lower() in vocab.syntacticLabelIndices:
                dataEntry[2].append(vocab.syntacticLabelIndices[t.dependencyLabel.lower()])
            else:
                dataEntry[2].append(vocab.syntacticLabelIndices[unk])
        else:
            dataEntry[2].append(vocab.syntacticLabelIndices[empty])

    @staticmethod
    def getBufferTokens(conf, sent, vocab, dataEntry):
        for i in range(3):
            if i < len(conf.buffer):
                bi = conf.buffer[i] - 1
                biToken = sent.tokens[bi]
                DataFactory.addTokenIdx(biToken, vocab, dataEntry)
                DataFactory.addPosTagIdx(biToken, vocab, dataEntry)
            else:
                DataFactory.addTokenIdx(None, vocab, dataEntry)
                DataFactory.addPosTagIdx(None, vocab, dataEntry)

    @staticmethod
    def getStackTokens(conf, sent, vocab, dataEntry):
        for i in range(1, 4):
            if conf.stack and i <= len(conf.stack):
                si = conf.stack[-i] - 1
                if si == -1:
                    DataFactory.addTokenIdx('root', vocab, dataEntry)
                    DataFactory.addPosTagIdx('root', vocab, dataEntry)
                else:
                    siToken = sent.tokens[si]
                    DataFactory.addTokenIdx(siToken, vocab, dataEntry)
                    DataFactory.addPosTagIdx(siToken, vocab, dataEntry)
            else:
                DataFactory.addTokenIdx(None, vocab, dataEntry)
                DataFactory.addPosTagIdx(None, vocab, dataEntry)

    @staticmethod
    def getSyntacticLabelIndice(t, vocab):
        if t:
            k = t.dependencyLabel.lower()
            if k in vocab:
                return vocab[k]
            return vocab[unk]
        return vocab[empty]
