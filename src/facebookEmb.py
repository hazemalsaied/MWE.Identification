import os

import numpy as np
from numpy import zeros

from config import configuration


def getEmbMatrix(lang, vocab, dimension=300, inverseVocab=False):
    """
    create a pretrained embedding matrix by loading the pretrained embeddings of simple words
    of the vocabulary that exist in FastText, initializing random embeddings for new words,
    and averaging or summing embedding of attached words that could occupy the head of the stack
    :param lang:
    :param vocab: index:word vocabulary
    :return:
    """
    # vocab = list(getCorpusTokens(lang))
    wordEmbDic = loadFastTextEmbeddings(lang)
    vocabSize = len(vocab)
    idxs = range(0, vocabSize)
    embeddingMatrix = zeros((vocabSize, dimension))
    if inverseVocab:
        newVocabDic = dict()

        for k, v in vocab.items():
            newVocabDic[v] = k
        vocab = newVocabDic
    for i in idxs:
        if vocab[i] in wordEmbDic:
            embeddingMatrix[i] = np.asarray(wordEmbDic[vocab[i]], dtype=float)
        elif '_' not in vocab[i]:
            embeddingMatrix[i] = np.random.uniform(low=-.5, high=.5, size=(1, dimension))
    for i in idxs:
        newWord = False
        if '_' in vocab[i]:
            words = vocab[i].split('_')
            avVec = np.zeros((1, 300))
            for w in words:
                if w in wordEmbDic:
                    avVec += np.asarray(wordEmbDic[w], dtype=float)
                else:
                    newWord = True
                    break
            if not newWord:
                if configuration['embedding']['average']:
                    embeddingMatrix[i] = np.array(avVec) / len(words)
                else:
                    embeddingMatrix[i] = avVec
        if '_' not in vocab[i] or newWord:
            embeddingMatrix[i] = np.random.uniform(low=-.5, high=.5, size=(1, dimension))

    # embeddingMatrix[-1] = np.random.rand(1, configuration['mlp']['tokenEmb'])
    # embeddingMatrix[-2] = np.random.rand(1, configuration['mlp']['tokenEmb'])
    # embeddingMatrix[-3] = np.random.rand(1, configuration['mlp']['tokenEmb'])
    vocabIdx = dict()
    for i in idxs:
        vocabIdx[vocab[i]] = i
    # vocabIdx[configuration['constants']['unk']] = len(vocab) + 1
    # vocabIdx[configuration['constants']['empty']] = len(vocab) + 1
    # vocabIdx[configuration['constants']['number']] = len(vocab) + 1
    return vocabIdx, embeddingMatrix


def getCorpusTokens(lang):
    """
    Returns a set of lexical form and lemma of corpus tokens
    :param lang:
    :return:
    """
    tokenDic = set()
    from corpus import Corpus
    corpus = Corpus(lang)
    for s in corpus.trainDataSet + corpus.testDataSet:
        for t in s.tokens:
            tokenDic.add(t.text)
            tokenDic.add(t.lemma)
    return tokenDic


def createLightEmbs(fbFolder, filePath, lang):
    """
    A function that produce a light version of pretrained dictionary
    by ignoring the keys that don't belong to training corpus
    :param fbFolder:
    :param filePath:
    :param lang:
    :return:
    """
    lightEmbstr = ''
    tokenDic = getCorpusTokens(lang)
    with open(os.path.join(fbFolder, filePath), 'r') as f:
        idx = 0
        for l in f:
            if idx == 0:
                idx += 1
            else:
                lineParts = l.split(' ')
                if lineParts[0] in tokenDic:
                    lightEmbstr += l
    with open(os.path.join(fbFolder + 'Light', filename), 'w') as ff:
        ff.write(lightEmbstr)


def loadFastTextEmbeddings(lang):
    """
    Load fasttext pretrained embeddings from embedding files
    :param lang:
    :return: a dictionary of pretrained embeddings
    """
    wordEmb = dict()
    embPath = os.path.join(configuration['path']['projectPath'],
                           'ressources/FacebookEmbsLight/wiki.{0}.vec'.format(lang.lower()))
    with open(embPath, 'r') as f:
        for l in f:
            parts = l.split(' ')
            wordEmb[parts[0].lower()] = parts[1:-1]
    return wordEmb


if __name__ == '__main__':
    # from corpus import *
    from xpTools import setXPMode, setDataSet, setTrainAndTest, Dataset, XpMode, Evaluation

    folder = os.path.join(configuration['path']['projectPath'], '/ressources/FacebookEmbs')
    setXPMode(XpMode.linear)
    setTrainAndTest(Evaluation.corpus)
    setDataSet(Dataset.sharedtask2)
    for filename in os.listdir(folder):
        if filename.startswith('wiki'):
            createLightEmbs(folder, filename, filename[5:7].upper())
