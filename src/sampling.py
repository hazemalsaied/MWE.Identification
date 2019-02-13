import random
import sys

import numpy as np
import sklearn.utils
from imblearn.over_sampling import RandomOverSampler

import reports
from config import configuration


def overSample(labels, data, linearInMlp=False):
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


def overSampleImporTrans(data, labels, corpus, vocabulary):
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
        print len(data[0]), len(newData[0])
        data = np.concatenate((data, newData))
        if configuration['others']['verbose']:
            sys.stdout.write(reports.tabs + 'data size after focused sampling = {0}\n'.format(len(labels)))
    return np.asarray(data), np.asarray(labels)


def getClassWeights(labels):
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
    if not configuration['sampling']['sampleWeight']:
        return None
    sampleWeights = []
    for l in labels:
        sampleWeights.append(classWeightDic[l])
    return np.asarray(sampleWeights)


def getMWEDicAsIdxs(corpus, vocabulary):
    result = dict()
    for mwe in corpus.mweDictionary:
        idx = getIdxsStrForMWE(mwe, vocabulary)
        if idx:
            result[idx] = mwe
    return result


def getIdxsStrForMWE(mwe, vocabulary):
    tokenLemmas = mwe.replace(' ', '_')
    if tokenLemmas not in vocabulary.tokenIndices:
        return None
    return vocabulary.tokenIndices[tokenLemmas]


def shuffleArrayInParallel(arrays):
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


def test():
    a = [1, 2, 3, 4, 5, 6]
    b = [[1, 2, 3, 4, 5, 6], [1, 2, 3, 4, 5, 6]]
    c = [np.asarray([1, 2, 3, 4, 5, 6]), np.asarray([1, 2, 3, 4, 5, 6]), np.asarray([1, 2, 3, 4, 5, 6])]
    sys.stdout.write(str(shuffleArrayInParallel(c)) + '\n')


if __name__ == '__main__':
    test()
