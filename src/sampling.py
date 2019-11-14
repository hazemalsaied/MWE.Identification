import random
import sys

import numpy as np
import sklearn.utils
from imblearn.over_sampling import RandomOverSampler

import reports
from config import configuration


def overSample(labels, data, linearInMlp=False):
    """
    A function used for applying random oversampling
    :param labels:
    :param data:
    :param linearInMlp: used for oversampling stacking models (MLP fed with SVM predictions)
    :return:
    """
    tokenData, posData, linearPred = [], [], []
    elementNumber = 3 + configuration['embedding']['useB1'] + configuration['embedding']['useB-1']
    if not configuration['sampling']['overSampling']:
        for item in data:
            tokenData.append(np.asarray(item[:elementNumber]))
            posData.append(np.asarray(item[elementNumber:elementNumber * 2]))
            if linearInMlp:
                linearPred.append(np.asarray(item[elementNumber * 2:]))
        return np.asarray(labels), [np.asarray(tokenData), np.asarray(posData), np.asarray(linearPred)]
    if configuration['others']['verbose']:
        sys.stdout.write(reports.doubleSep + reports.tabs + 'Resampling:' + reports.doubleSep)
        sys.stdout.write(reports.tabs + 'data size before sampling = {0}\n'.format(len(labels)))
    ros = RandomOverSampler(random_state=0)
    data, labels = ros.fit_sample(data, labels)
    for item in data:
        tokenData.append(np.asarray(item[:elementNumber]))
        posData.append(np.asarray(item[elementNumber:elementNumber * 2]))
        linearPred.append(np.asarray(item[elementNumber * 2:]))
    if configuration['others']['verbose']:
        sys.stdout.write(reports.tabs + 'data size after sampling = {0}\n'.format(len(labels)))
    if linearInMlp:
        return np.asarray(labels), [np.asarray(tokenData), np.asarray(posData), np.asarray(linearPred)]
    return np.asarray(labels), [np.asarray(tokenData), np.asarray(posData)]


def focusedSampling(data, labels, corpus, vocabulary):
    """
    used  for applying the focused sampling of rarely seen MWEs
    :param data:
    :param labels:
    :param corpus:
    :param vocabulary:
    :return:
    """
    newData, newLabels = [], []
    traitedMWEs = set()
    oversamplingTaux = configuration['sampling']['mweRepeition']
    mWEDicAsIdxs = getMWEDicAsIdxs(corpus, vocabulary)
    for i in range(len(labels)):
        if labels[i] > 2:
            mweIdx = data[i][0]
            if mweIdx in mWEDicAsIdxs and mweIdx not in traitedMWEs:
                traitedMWEs.add(mweIdx)
                mwe = mWEDicAsIdxs[mweIdx]
                mweLength = len(mwe.split(' '))
                mweOccurrence = corpus.mweDictionary[mwe]
                if mweOccurrence < oversamplingTaux:
                    for underProcessingTransIdx in range(i - (2 * mweLength - 1) + 1, i + 1):
                        for j in range(oversamplingTaux - mweOccurrence):
                            newData.append(data[underProcessingTransIdx])
                            newLabels.append(labels[underProcessingTransIdx])
    if data and newData:
        if configuration['others']['verbose']:
            sys.stdout.write(reports.tabs + 'data size before focused sampling = {0}\n'.format(len(labels)))
        labels = np.concatenate((labels, newLabels))
        data = np.concatenate((data, newData))
        if configuration['others']['verbose']:
            sys.stdout.write(reports.tabs + 'data size after focused sampling = {0}\n'.format(len(labels)))
    return np.asarray(data), np.asarray(labels)


def getClassWeights(labels):
    """
    Estimate the desired class weights for unbalanced datasets
    :param labels:
    :return:
    """
    if not configuration['sampling']['sampleWeight']:
        return {}
    classes = np.unique(labels)
    class_weight = sklearn.utils.class_weight.compute_class_weight('balanced', classes, labels)
    res = dict()
    for c in classes:
        cIdx = classes.tolist().index(c)
        res[c] = float(class_weight[cIdx] * configuration['sampling']['favorisationCoeff']) if c > 1 else class_weight[
            cIdx]
    if configuration['others']['verbose']:
        sys.stdout.write(
            reports.tabs + 'Favorisation Coeff : {0}\n'.format(configuration['sampling']['favorisationCoeff']))

    return res


def shuffle(lists):
    """
    shuffle a list of lists (equal in length)
    :param lists:
    :return:
    """
    for l in lists:
        if len(l) != len(lists[0]):
            raise Exception('Suffling can not proceed on lists with different lengths')
    newLists = []
    for i in range(len(lists)):
        newLists.append([])
    r = range(lists[0].shape[0])
    random.shuffle(r)
    for i in r:
        for j in range(len(lists)):
            newLists[j].append(lists[j][i])
    return newLists


def getSampleWeightArray(labels, classWeightDic):
    """
    produce a list of coefficients corresponding to the desired weigh of given labels
    :param labels:
    :param classWeightDic:
    :return:
    """
    if not configuration['sampling']['sampleWeight']:
        return None
    sampleWeights = []
    for l in labels:
        sampleWeights.append(classWeightDic[l])
    return np.asarray(sampleWeights)


def getMWEDicAsIdxs(corpus, vocabulary):
    """
    give a dictionary: { index of the MWE in the token vocabulary: its lemmatized form}
    :param corpus:
    :param vocabulary:
    :return:
    """
    result = dict()
    for mwe in corpus.mweDictionary:
        idx = getIdxsStrForMWE(mwe, vocabulary)
        if idx:
            result[idx] = mwe
    return result


def getIdxsStrForMWE(mwe, vocabulary):
    """
    returns the index of the MWE in the token vocabulary
    :param mwe:
    :param vocabulary:
    :return:
    """
    tokenLemmas = mwe.replace(' ', '_')
    if tokenLemmas not in vocabulary.tokenIndices:
        return None
    return vocabulary.tokenIndices[tokenLemmas]


def shuffleArrayInParallel(arrays):
    """
    shuffle multiple array in the same way
    :param arrays:
    :return:
    """
    rangee = range(len(arrays[0]))
    random.shuffle(rangee)

    results = []
    for i in range(len(arrays)):
        results.append([])
    for i in rangee:
        for j in range(len(arrays)):
            results[j].append(arrays[j][i])
    newResult = []
    for i in range(len(arrays)):
        newResult.append(np.asarray(results[i]))
    return newResult
