import gensim

from config import configuration

unk = configuration['constants']['unk']
empty = configuration['constants']['empty']
number = configuration['constants']['number']


def trainPosEmbWithWordToVec(corpus):
    """
    Returns a Word2Vec representing POSs
    :param corpus:
    :return:
    """
    initConf = configuration['initialisation']
    normailsedSents = []
    for sent in corpus.trainingSents + corpus.testingSents:
        normailsedSent = []
        for token in sent.tokens:
            normailsedSent.append(token.posTag.lower())
        normailsedSents.append(normailsedSent)
    model = gensim.models.Word2Vec(normailsedSents, size=configuration['mlp']['posEmb'],
                                   window=initConf['Word2VecWindow'])
    return model


def getFreqDic(corpus, posTag=False):
    """
    return a dictionary of tokens (lemma, word, POS) with theirs frequencies in a given corpus
    :param corpus:
    :param posTag:
    :return:
    """
    freqDic = dict()
    for sent in corpus.trainingSents:
        for token in sent.tokens:
            key = token.posTag.lower() if posTag else token.getTokenOrLemma().lower()
            if key not in freqDic:
                freqDic[key] = 1
            else:
                freqDic[key] += 1
    return freqDic
