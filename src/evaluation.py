from __future__ import division

import sys
from collections import Counter

import reports
from config import configuration


def evaluate(sents, categorization=False, loggingg=True):
    tp, p, t, tpCat, pCat, tCat = getStatistics(sents)
    scores = calculateScores(tp, p, t, 'Identification', loggingg=loggingg)
    if categorization:
        scores += calculateScores(tpCat, pCat, tCat, 'Categorization', loggingg=loggingg)
        catList = ['lvc', 'ireflv', 'vpc', 'id', 'oth']
        for cat in catList:
            tp, p, t = getCategoryStatistics(sents, cat)
            scores += calculateScores(tp, p, t, cat, loggingg=loggingg)
    if configuration['others']['tokenBased']:
        tp, p, t = getTokenBasedStatistics(sents)
        calculateScores(tp, p, t, 'Token-based', loggingg=loggingg)
    if configuration['dataset']['dimsum']:
        tp, p, t = getDiMSUMStatistics(sents)
        calculateScores(tp, p, t, 'DiMSUM', loggingg=loggingg)
    if loggingg:
        sys.stdout.write(reports.doubleSep)
    # reports.saveSettings()
    # reports.saveScores(scores)
    # corpus.analyzeTestSet()
    return scores


def getDiMSUMStatistics(sents):
    ig, gold, identified = 0, 0, 0
    for sent in sents:
        gList, iList = [], []
        for w in sent.vMWEs:
            positions = sorted([t.position for t in w.tokens])
            for i in range(len(positions) - 1):
                if i < len(positions):
                    gList.append(str(positions[i]) + '.' + str(positions[i + 1]))
        for w in sent.identifiedVMWEs:
            positions = sorted([t.position for t in w.tokens])
            for j in range(len(positions) - 1):
                if j < len(positions):
                    iList.append(str(positions[j]) + '.' + str(positions[j + 1]))
        identified += len(iList)
        gold += len(gList)
        for l in set(iList + gList):
            if l in iList and l in gList:
                ig += 1
        for l in iList:
            if int(l.split('.')[1]) - int(l.split('.')[0]) != 1 and l not in gList:
                for w in sent.vMWEs:
                    positions = sorted([t.position for t in w.tokens])
                    ggList = []
                    for i in range(len(positions) - 1):
                        if i < len(positions):
                            ggList.append(str(positions[i]) + '.' + str(positions[i + 1]))
                    start, end = False, False
                    for g in ggList:
                        if g.startswith(l.split('.')[0]):
                            start = True
                        if g.endswith(l.split('.')[1]):
                            end = True
                    ig += 1 if start and end else 0
    return ig, gold, identified


def analyzePerformance(corpus):
    if not configuration['others']['analyzePerformance']:
        return
    # reportTokenFrequency(corpus.testingSents, corpus.lemmaText)
    for c in ['vid', 'lvc.full', 'lvc.cause', 'irv', 'vpc.full', 'vpc.semi', 'iav', 'mvc', 'lc']:
       reportCategory(corpus.testingSents, c)

    reportSeen(corpus.testingSents, corpus.mweDictionary)
    reportSeen(corpus.testingSents, corpus.mweDictionary, frequently=True)
    reportSeen(corpus.testingSents, corpus.mweDictionary, barely=True)
    reportPartiallySeen(corpus.testingSents, corpus.mweDictionary, corpus.mweTokenDictionary)
    reportPartiallySeenWithoutNoise(corpus.testingSents, corpus.mweDictionary, corpus.mweTokenDictionary,
                                    corpus.lemmaText)
    reportNonSeen(corpus.testingSents, corpus.mweDictionary)
    reportContinity(corpus.testingSents)
    reportDisContinity(corpus.testingSents)
    reportIdentic(corpus.testingSents, corpus.mweContextDictionary, corpus.mweDictionary)
    reportVariant(corpus.testingSents, corpus.mweContextDictionary, corpus.mweDictionary)
    reportEmbedded(corpus.testingSents)
    reportLength(corpus.testingSents)
    reportMultiTokens(corpus.testingSents)
    reportLength(corpus.testingSents, minLength=2, maxLength=2)
    reportLength(corpus.testingSents, minLength=3, maxLength=3)
    reportLength(corpus.testingSents, minLength=4, maxLength=100)

    reportMisIdentified(corpus.testingSents, corpus.mweDictionary, corpus.mweTokenDictionary, corpus.lemmaText)
    reportNonIdentified(corpus.testingSents, corpus.mweDictionary, corpus.mweTokenDictionary, corpus.lemmaText)


def reportTokenFrequency(sents, corpusLemmaText):
    wordcount = Counter(corpusLemmaText.split())
    tokenVisScoreMax, tokenVisScoreMin, tokenVisScores = 0, 0, []
    for s in sents:
        for w in s.vMWEs:
            tFrequencies = []
            for t in w.tokens:
                if t.getLemma() in wordcount:
                    tFrequencies.append(wordcount[t.getLemma()])
                else:
                    tFrequencies.append(0)
            w.tokenVisScore = round(reports.getMeanAbsoluteDeviation(tFrequencies), 1)
            tokenVisScores.append(w.tokenVisScore)
            if w.tokenVisScore > tokenVisScoreMax:
                tokenVisScoreMax = w.tokenVisScore
            if w.tokenVisScore < tokenVisScoreMin:
                tokenVisScoreMin = w.tokenVisScore
    # plt.plot(range(len(tokenVisScores)), tokenVisScores, 'ro')
    # plt.show()


def reportMisIdentified(sents, mweDic, mweTokenDic, corpusLemmaText, threshold=100):
    wordcount = Counter(corpusLemmaText.split())
    misIdentifiedNum, allIdentifiedNum = 0, 0
    for s in sents:
        mweIdxs = set([mwe.getTokenPositionString() for mwe in s.vMWEs])
        for w in s.identifiedVMWEs:
            w.toDelete = False if w.getTokenPositionString() not in mweIdxs else True
            if not w.toDelete:
                misIdentifiedNum += 1
            allIdentifiedNum += len(s.identifiedVMWEs)
    manipuleSents(sents, None)
    allMwes, mWTs, twoTokens, threeTokens, seens, nonSeens, partiallySeen, frequentlySeen, barelySeen, \
    partiallySeenWithoutNoise = 0, 0, 0, 0, 0, 0, 0, 0, 0, 0
    seensSet, mwtSet, twoTokensSet, threeTokensSet = set(), set(), set(), set()
    frequentlySeensSet, barelySeenSet, nonSeensSet, partiallySeenSet, partiallySeenWithoutNoiseSet = \
        set(), set(), set(), set(), set()

    for s in sents:
        for w in s.identifiedVMWEs:
            if len(w.tokens) == 1:
                mWTs += 1
                mwtSet.add(w)
            if len(w.tokens) == 2:
                twoTokens += 1
                twoTokensSet.add(w)
            if len(w.tokens) == 3:
                threeTokens += 1
                threeTokensSet.add(w)
            if isSeen(w, mweDic):
                seens += 1
                seensSet.add(w)
            if isSeen(w, mweDic, frequently=True):
                frequentlySeen += 1
                frequentlySeensSet.add(w)
            if isSeen(w, mweDic, barely=True):
                barelySeen += 1
                barelySeenSet.add(w)
            if not isSeen(w, mweDic):
                nonSeens += 1
                nonSeensSet.add(w)
            isPartiallySeen = False
            isPartiallySeenWithoutNoise = False
            if not isSeen(w, mweDic):
                for t in w.tokens:
                    if t.getLemma() in mweTokenDic.keys():
                        isPartiallySeen = True
                        if t.getLemma() in wordcount and wordcount[t.getLemma()] < threshold:
                            isPartiallySeenWithoutNoise = True
            if isPartiallySeen:
                partiallySeen += 1
                partiallySeenSet.add(w)
            if isPartiallySeenWithoutNoise:
                partiallySeenWithoutNoise += 1
                partiallySeenWithoutNoiseSet.add(w)
            allMwes += 1
    if not allMwes:
        return
    sys.stdout.write(reports.doubleSep)
    sys.stdout.write('Misidentified:')
    sys.stdout.write(reports.doubleSep)

    sys.stdout.write(reports.tabs + 'Misidentified / identified: {0}\n'.format(round(float(misIdentifiedNum) * 100 /
                                                                                     allIdentifiedNum, 1)))
    sys.stdout.write(reports.tabs + 'Seens: {0}\n'.format(round(float(seens) * 100 / allMwes, 1)))
    sys.stdout.write(
        reports.tabs + 'Non Seens: {0}\n'.format(round(float(nonSeens) * 100 / allMwes, 1)))
    sys.stdout.write(reports.tabs + 'Frequently Seen: {0}\n'.format(
        round(float(frequentlySeen) * 100 / allMwes, 1)))
    sys.stdout.write(reports.tabs + 'Barely Seen: {0}\n'.format(
        round(float(barelySeen) * 100 / allMwes, 1)))
    sys.stdout.write(reports.tabs + 'Partially Seen: {0}\n'.format(
        round(float(partiallySeen) * 100 / allMwes, 1)))
    sys.stdout.write(reports.tabs + 'Partially Seen (Without stop words): {0}\n'.format(
        round(float(partiallySeenWithoutNoise) * 100 / allMwes, 1)))
    sys.stdout.write(reports.tabs + 'Three Token MWEs: {0}\n'.format(
        round(float(threeTokens) * 100 / allMwes, 1)))
    sys.stdout.write(reports.tabs + 'Two Token MWEs: {0}\n'.format(
        round(float(twoTokens) * 100 / allMwes, 1)))
    sys.stdout.write(reports.tabs + 'MWTs: {0}\n'.format(round(float(mWTs) * 100 / allMwes, 1)))
    restoreTestSents(sents)


def reportCategory(sents, catName):
    g, i, catG,  catIG = 0, 0, 0, 0
    for s in sents:
        mweIdxs = set([mwe.getTokenPositionString() for mwe in s.identifiedVMWEs])
        g += len(s.vMWEs)
        #i += len(s.identifiedVMWEs)
        for w in s.vMWEs:
            if w.getTokenPositionString() in mweIdxs:
                i += 1
            if w.type2.lower().startswith(catName):
                catG += 1
                if w.getTokenPositionString() in mweIdxs:
                    catIG += 1
    gProportionStr= '{0} : {1}\n'.format(catName.upper(),
                    round(float(catG) * 100 / g, 1) if g else '-')
    iProportionStr = '{0}: {1}\n'.format(catName.upper(),
                                        round(float(catIG) * 100 / i, 1) if i else '-')
    presicionStr = '{0}: {1}\n'.format(catName.upper(),
                    round(float(catIG) * 100 / catG, 1) if catG else '-')
    sys.stdout.write(reports.tabs + gProportionStr)
    sys.stdout.write(reports.tabs + iProportionStr)
    sys.stdout.write(reports.tabs + presicionStr)


def reportNonIdentified(sents, mweDic, mweTokenDic, corpusLemmaText, threshold=100):
    wordcount = Counter(corpusLemmaText.split())
    nonIdentifiedNum, allGold = 0, 0
    for s in sents:
        mweIdxs = set([mwe.getTokenPositionString() for mwe in s.identifiedVMWEs])
        for w in s.vMWEs:
            w.toDelete = False if w.getTokenPositionString() not in mweIdxs else True
            if not w.toDelete:
                nonIdentifiedNum += 1
            allGold += len(s.vMWEs)
    manipuleSents(sents, None)
    allMwes, mWTs, twoTokens, threeTokens, seens, nonSeens, partiallySeen, partiallySeenWithoutNoise, frequentlySeen, \
    barelySeen = 0, 0, 0, 0, 0, 0, 0, 0, 0, 0
    lvcFull, vid, irv, vpcFull = 0, 0, 0, 0
    for s in sents:
        for w in s.vMWEs:
            mWTs += 1 if len(w.tokens) == 1 else 0
            twoTokens += 1 if len(w.tokens) == 2 else 0
            threeTokens += 1 if len(w.tokens) == 3 else 0
            seens += 1 if isSeen(w, mweDic) else 0
            frequentlySeen += 1 if isSeen(w, mweDic, frequently=True) else 0
            barelySeen += 1 if isSeen(w, mweDic, barely=True) else 0
            nonSeens += 1 if not isSeen(w, mweDic) else 0

            lvcFull += 1 if w.type2.lower() == 'lvc.full' else 0
            vid += 1 if w.type2.lower() == 'vid' else 0
            irv += 1 if w.type2.lower() == 'irv' else 0
            vpcFull += 1 if w.type2.lower() == 'vpc.full' else 0

            isPartiallySeen, isPartiallySeenWithoutNoise = False, False
            if not isSeen(w, mweDic):
                for t in w.tokens:
                    if t.getLemma() in mweTokenDic.keys():
                        isPartiallySeen = True
                        if t.getLemma() in wordcount and wordcount[t.getLemma()] < threshold:
                            isPartiallySeenWithoutNoise = True
            partiallySeen += 1 if isPartiallySeen else 0
            partiallySeenWithoutNoise += 1 if isPartiallySeenWithoutNoise else 0
            allMwes += 1
    if not allMwes:
        return
    sys.stdout.write(reports.doubleSep)
    sys.stdout.write('Non-identified:')
    sys.stdout.write(reports.doubleSep)
    sys.stdout.write(
        reports.tabs + 'Non-identified / Gold: {0}\n'.format(round(float(nonIdentifiedNum) * 100 / allGold, 1)))
    sys.stdout.write(reports.tabs + 'Seens: {0}\n'.format(round(float(seens) * 100 / allMwes, 1)))
    sys.stdout.write(reports.tabs + 'Non Seens: {0}\n'.format(round(float(nonSeens) * 100 / allMwes, 1)))
    sys.stdout.write(reports.tabs + 'Frequently Seen: {0}\n'.format(
        round(float(frequentlySeen) * 100 / allMwes, 1)))
    sys.stdout.write(reports.tabs + 'Barely Seen: {0}\n'.format(
        round(float(barelySeen) * 100 / allMwes, 1)))
    sys.stdout.write(reports.tabs + 'Partially Seen: {0}\n'.format(
        round(float(partiallySeen) * 100 / allMwes, 1)))
    sys.stdout.write(reports.tabs + 'Partially Seen (Without stop words): {0}\n'.format(
        round(float(partiallySeenWithoutNoise) * 100 / allMwes, 1)))
    sys.stdout.write(reports.tabs + 'Three Token MWEs: {0}\n'.format(
        round(float(threeTokens) * 100 / allMwes, 1)))
    sys.stdout.write(reports.tabs + 'Two Token MWEs: {0}\n'.format(
        round(float(twoTokens) * 100 / allMwes, 1)))
    sys.stdout.write(reports.tabs + 'MWTs: {0}\n'.format(round(float(mWTs) * 100 / allMwes, 1)))

    if configuration['dataset']['sharedtask2']:
        sys.stdout.write(reports.tabs + 'LVC Full: {0}\n'.format(
            round(float(lvcFull) * 100 / allMwes, 1)))
        sys.stdout.write(reports.tabs + 'VID: {0}\n'.format(
            round(float(vid) * 100 / allMwes, 1)))
        sys.stdout.write(reports.tabs + 'IRV: {0}\n'.format(
            round(float(irv) * 100 / allMwes, 1)))
        sys.stdout.write(reports.tabs + 'VPC Full: {0}\n'.format(
            round(float(vpcFull) * 100 / allMwes, 1)))
    sys.stdout.write(reports.doubleSep)
    restoreTestSents(sents)


# def reportPartiallySeen(sents, mweDic, mweTokenDic):
#     for s in sents:
#         for w in s.identifiedVMWEs:
#             isPartiallySeen = False
#             if not isSeen(w, mweDic):
#                 for t in w.tokens:
#                     if t.getLemma() in mweTokenDic.keys():
#                         isPartiallySeen = True
#             w.toDelete = False if isPartiallySeen else True
#     getProportion(sents, 'PartiallySeen')

def reportLength(sents, minLength=1, maxLength=1):
    for s in sents:
        for w in s.vMWEs + s.identifiedVMWEs:
            w.toDelete = False if maxLength >= len(w.tokens) >= minLength else True
    if minLength == 1:
        label = 'MWTs'
    elif minLength == maxLength:
        label = 'Length({0})'.format(minLength)
    else:
        label = '{0} < Length < {1}'.format(minLength, maxLength)
    getScores(sents, label)


def reportMultiTokens(sents):
    for s in sents:
        for w in s.vMWEs + s.identifiedVMWEs:
            w.toDelete = False if len(w.tokens) > 1 else True
    getScores(sents, 'Multitokens')


def reportIdentic(sents, mweOccurrenceDic, mweDic):
    for s in sents:
        for w in s.vMWEs + s.identifiedVMWEs:
            w.toDelete = False if isSeen(w, mweDic) and w.getContext(s) in mweOccurrenceDic.keys() else True
    getScores(sents, 'Identic', ' / (all:seen + non seen)')


def reportVariant(sents, mweOccurrenceDic, mweDic):
    for s in sents:
        for w in s.vMWEs + s.identifiedVMWEs:
            w.toDelete = False if isSeen(w, mweDic) and w.getContext(s) not in mweOccurrenceDic.keys() else True
    getScores(sents, 'Variant', ' / (all:seen + non seen)')


def reportEmbedded(sents):
    for s in sents:
        for w in s.vMWEs + s.identifiedVMWEs:
            w.toDelete = False if w.isEmbedded else True
    getScores(sents, 'Embeddeds')


def reportSeen(sents, mweDic, frequently=False, barely=False):
    for s in sents:
        for w in s.vMWEs + s.identifiedVMWEs:
            w.toDelete = False if isSeen(w, mweDic, frequently=frequently, barely=barely) else True
    label = 'Seen MWEs'
    label += '(Barely)' if barely else ''
    label += '(Frequently)' if frequently else ''
    getScores(sents, label)


def reportPartiallySeen(sents, mweDic, mweTokenDic):
    for s in sents:
        for w in s.vMWEs + s.identifiedVMWEs:
            isPartiallySeen = False
            if not isSeen(w, mweDic):
                for t in w.tokens:
                    if t.getLemma() in mweTokenDic.keys():
                        isPartiallySeen = True
            w.toDelete = False if isPartiallySeen else True
    getScores(sents, 'Partially-seen MWEs')


def reportPartiallySeenWithoutNoise(sents, mweDic, mweTokenDic, corpusLemmaText, threshold=100):
    wordcount = Counter(corpusLemmaText.split())
    for s in sents:
        for w in s.vMWEs + s.identifiedVMWEs:
            isPartiallySeen = False
            if not isSeen(w, mweDic):
                for t in w.tokens:
                    if t.getLemma() in mweTokenDic.keys() and \
                            wordcount[t.getLemma()] < threshold:
                        isPartiallySeen = True
            w.toDelete = False if isPartiallySeen else True
    getScores(sents, 'Partially-seen MWEs (Without Noise)')


def reportNonSeen(sents, mweDic):
    for s in sents:
        for w in s.vMWEs + s.identifiedVMWEs:
            w.toDelete = True if isSeen(w, mweDic) else False
    getScores(sents, 'Non-seen MWEs')


def isSeen(w, mweDic, frequently=False, barely=False, threshold=5):
    """
        A MWE is seen in the train corpus if all its lemmas (without respect of order)
        form one entry of train MWE dictionary
    """
    for mwe in mweDic.keys():
        if len(w.tokens) == len(mwe.split(' ')):
            allLemmasBelong = True
            for t in w.tokens:
                if t.getLemma() not in mwe:
                    allLemmasBelong = False
                    break
            for t in mwe.split(' '):
                if t not in w.getLemmaString():
                    allLemmasBelong = False
                    break
            if allLemmasBelong:
                if frequently:
                    if mweDic[mwe] > threshold:
                        return True
                    else:
                        return False
                elif barely:
                    if mweDic[mwe] <= threshold:
                        return True
                    else:
                        return False
                return True
    return False


def reportDisContinity(sents):
    """
        Continuous MWE could be a MWT or any MWE with no gap betweedn ts tokens
    """
    for s in sents:
        for w in s.vMWEs + s.identifiedVMWEs:
            w.toDelete = True if w.isContinuousMWE() else False
    getScores(sents, 'Discontinuous MWEs')


def reportContinity(sents):
    """
        Continuous MWE could be a MWT or any MWE with no gap betweedn ts tokens
    """
    for s in sents:
        for w in s.vMWEs + s.identifiedVMWEs:
            w.toDelete = False if w.isContinuousMWE() else True
    getScores(sents, 'Continuous MWEs')


def getScores(sents, label, label2=''):
    sys.stdout.write(reports.doubleSep + label + reports.doubleSep)
    manipuleSents(sents, label, label2=label2)
    tp, p, t = getStats(sents)
    scores = calculateScores(tp, p, t, label)
    restoreTestSents(sents)
    return scores


def getProportion(sents, label):
    allPredicted, nonDeletedPredicted, = 0, 0
    for s in sents:
        allPredicted += len(s.deletedIdentifiedVMWEs) + len(s.identifiedVMWEs)
        nonDeletedPredicted += len(s.identifiedVMWEs)
    sys.stdout.write('{0} proportion in Predicted: {1}{2}'.
                     format(label, round((float(nonDeletedPredicted) / allPredicted) * 100, 1), reports.doubleSep))


def manipuleSents(sents, label=None, label2=''):
    allGold, nonDeletedGold, allPredicted, nonDeletedPredicted, = 0, 0, 0, 0
    for s in sents:
        s.deletedVMWEs = [w for w in s.vMWEs if w.toDelete]
        s.vMWEs = [w for w in s.vMWEs if not w.toDelete]
        allGold += len(s.deletedVMWEs) + len(s.vMWEs)
        nonDeletedGold += len(s.vMWEs)
        s.deletedIdentifiedVMWEs = [w for w in s.identifiedVMWEs if w.toDelete]
        s.identifiedVMWEs = [w for w in s.identifiedVMWEs if not w.toDelete]
        allPredicted += len(s.deletedIdentifiedVMWEs) + len(s.identifiedVMWEs)
        nonDeletedPredicted += len(s.identifiedVMWEs)
    if label:
        sys.stdout.write(reports.tabs + 'Gold: {0}{1}\n'.
                         format(round((float(nonDeletedGold) / allGold) * 100 if allGold else 0, 1), label2))
        sys.stdout.write(reports.tabs + 'Predicted: {0}{1}\n'.
                         format(round((float(nonDeletedPredicted) / allPredicted) * 100 if allPredicted else 0, 1),
                                label2))


def restoreTestSents(sents):
    for s in sents:
        s.vMWEs += s.deletedVMWEs
        s.deletedVMWEs = []
        s.identifiedVMWEs += s.deletedIdentifiedVMWEs
        s.deletedIdentifiedVMWEs = []
        for w in s.vMWEs + s.identifiedVMWEs:
            w.toDelete = False


def getStats(sents):
    tp, p, t = 0, 0, 0
    for sent in sents:
        p += len(sent.vMWEs)
        t += len(sent.identifiedVMWEs)
        if sent.identifiedVMWEs:
            processedVmwe = []
            for m in sent.identifiedVMWEs:
                for vMWE in sent.vMWEs:
                    if m == vMWE and vMWE not in processedVmwe:
                        processedVmwe.append(vMWE)
                        tp += 1
    return tp, p, t


def getStatistics(sents):
    tp, p, t, tpCat, pCat, tCat = 0, 0, 0, 0, 0, 0
    for sent in sents:
        p += len(sent.vMWEs)
        t += len(sent.identifiedVMWEs)
        for vmw in sent.vMWEs:
            if len(vmw.tokens) > 1:
                pCat += 1
        for vmw in sent.identifiedVMWEs:
            if len(vmw.tokens) > 1:
                tCat += 1
        if sent.identifiedVMWEs:
            processedVmwe = []
            for m in sent.identifiedVMWEs:
                for vMWE in sent.vMWEs:
                    if m == vMWE and vMWE not in processedVmwe:
                        processedVmwe.append(vMWE)
                        tp += 1
                        if m.type == vMWE.type and len(vMWE.tokens) > 1:
                            tpCat += 1
    return tp, p, t, tpCat, pCat, tCat


def getTokenBasedStatistics(sents):
    ig, g, i, tpCat, pCat, tCat = 0, 0, 0, 0, 0, 0
    for sent in sents:
        glabels = ['-'] * len(sent.tokens)
        ilabels = ['-'] * len(sent.tokens)
        idx = 1
        for w in sent.vMWEs:
            for t in w.tokens:
                if glabels[t.position - 1] == '-':
                    glabels[t.position - 1] = str(idx)
            if not glabels[w.tokens[0].position - 1].endswith(':oth'):
                glabels[w.tokens[0].position - 1] += ':oth'
            idx += 1
        idx = 1
        for w in sent.identifiedVMWEs:
            for t in w.tokens:
                if ilabels[t.position - 1] == '-':
                    ilabels[t.position - 1] = str(idx)
            if not ilabels[w.tokens[0].position - 1].endswith(':oth'):
                ilabels[w.tokens[0].position - 1] += ':oth'
            idx += 1
        for j in range(len(glabels)):
            if glabels[j] != '-':
                g += 1
            if ilabels[j] != '-':
                i += 1
            if ilabels[j] != '-' and glabels[j] != '-':
                ig += 1
    return ig, g, i


def getCategoryStatistics(sents, cat):
    tp, p, t = 0, 0, 0
    cat = cat.lower()
    for sent in sents:
        for vmw in sent.vMWEs:
            if vmw.type.lower() == cat:
                p += 1
        for vmw in sent.identifiedVMWEs:
            if vmw.type.lower() == cat:
                t += 1
        if not sent.identifiedVMWEs:
            continue
        processedVmwe = []
        for m in sent.identifiedVMWEs:
            for vMWE in sent.vMWEs:
                if m == vMWE and vMWE not in processedVmwe and m.type.lower() == vMWE.type.lower() \
                        and m.type.lower() == cat:
                    processedVmwe.append(vMWE)
                    tp += 1
    return tp, p, t


def getMWTStatistics(corpus):
    tp, p, t, tpCat, pCat, tCat = 0, 0, 0, 0, 0, 0

    for sent in corpus.testingSents:
        for vmw in sent.vMWEs:
            if len(vmw.tokens) == 1:
                p += 1
        for vmw in sent.identifiedVMWEs:
            if len(vmw.tokens) == 1:
                t += 1
        processedVmwe = []
        for m in sent.identifiedVMWEs:
            for vMWE in sent.vMWEs:
                if len(m.tokens) == 1 and m == vMWE and vMWE not in processedVmwe:
                    processedVmwe.append(vMWE)
                    tp += 1
                    if m.type.lower() == vMWE.type.lower():
                        tpCat += 1
    return tp, p, t, tpCat, p, t


def calculateScores(ig, g, i, title, loggingg=True):
    """
    :param ig: golden identified
    :param g: golden
    :param i: identified
    :param title: logging indicator
    :param loggingg:
    :return: Fscore, recall, precision
    """
    title = 'F' if title != 'Identification' and title != 'Token-based' and title != 'DiMSUM' else title
    r = round(float(ig / g) if g != 0 else 0, 3)
    p = round(float(ig / i) if i != 0 else 0, 3)
    f = round(2 * (r * p) / (r + p), 3) if r + p != 0 else 0
    if loggingg:
        sys.stdout.write(reports.tabs + '{0} : {1}\n'.format(title, f))
        sys.stdout.write(reports.tabs + 'P, R  : {0}, {1}\n'.format(p, r))
    return title, f, r, p
