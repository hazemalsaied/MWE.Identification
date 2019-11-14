import oracle
from corpus import *
from transitions import TransitionType


def getTransDistribution(corpus):
    """
    return the distribution of transitions in training set
    :param corpus:
    :return:
    """
    shNum, rdNum, mgNum, mkNum = 0, 0, 0, 0
    importantSents = 0
    for s in corpus.trainingSents:
        if s.vMWEs:
            importantSents += 1
        t = s.initialTransition
        while t.next:
            if t.type == TransitionType.SHIFT:
                shNum += 1
            elif t.type == TransitionType.REDUCE:
                rdNum += 1
            elif t.type == TransitionType.MERGE:
                mgNum += 1
            else:
                mkNum += 1
            t = t.next
    sys.stdout.write(len(corpus.trainingSents), importantSents)
    sys.stdout.write(shNum, rdNum, mgNum, mkNum, (shNum + rdNum + mgNum + mkNum))
    return shNum, rdNum, mgNum, mkNum, (shNum + rdNum + mgNum + mkNum)


def getDimsumStats(corpus):
    """
    print the MWEs of train, seen and non seen tokens of test
    :param corpus:
    :return:
    """
    if not configuration['tmp']['dimsulStats']:
        return
    sys.stdout.write('# MWEs\n')
    for k in corpus.mweDictionary:
        sys.stdout.write('{0} : {1}\n'.format(k, corpus.mweDictionary[k]))
    seenToks, nonSeenToks = set(), set()
    for s in corpus.testingSents:
        for w in s.vMWEs:
            for t in w.tokens:
                if t.getLemma() in corpus.mweTokenDictionary:
                    seenToks.add(t.getLemma())
                else:
                    nonSeenToks.add(t.getLemma())
    sys.stdout.write('# seen tokens\n')
    for t in seenToks:
        sys.stdout.write('{0}\n' % t)
    sys.stdout.write('# non seen tokens\n')
    for t in nonSeenToks:
        sys.stdout.write('{0}\n' % t)


def analyzeCorporaAndOracle(langs):
    """
    test of oracle functioning
    :param langs:
    :return:
    """
    header = 'Non recognizable,Interleaving,Embedded,Distributed Embedded,Left Embedded,Right Embedded,Middle Embedded'
    analysisReport = header + '\n'
    for lang in langs:
        sys.stdout.write('Language = {0}\n'.format(lang))
        corpus = Corpus(lang)
        analysisReport += corpus.getVMWEReport() + '\n'
        oracle.parse(corpus)
        oracle.validate(corpus)
    with open('../Results/VMWE.Analysis.csv', 'w') as ff:
        ff.write(analysisReport)
