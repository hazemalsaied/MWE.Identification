import sys

from corpus import getRelevantModelAndNormalizer
from modelLinear import getFeatures
from transitions import *

markNum = 0


def parse(sents, model, vectorizer=None, linearModels=None, linearVecs=None, mlpModels=None, initialize=True):
    global markNum
    for sent in sents:
        sys.stdout.write(str(sent) + '\n')
        if initialize:
            sent.identifiedVMWEs = []
        sent.initialTransition, sentEmbs, tokens = None, None, None
        if False and configuration['xp']['kiperwasser']:
            tokenIdxs, posIdxs = model.getIdxs(sent)
            sentEmbs = model.getContextualizedEmbs(tokenIdxs, posIdxs)
        elif configuration['xp']['kiperComp']:
            tokens = sent.tokens[:5]
            tokenIdxs, posIdxs = model.getIdxs(tokens)
            sentEmbs = model.getContextualizedEmbs(tokenIdxs, posIdxs)
        sent.initialTransition = Transition(None, isInitial=True, sent=sent)
        t = sent.initialTransition
        while not t.isTerminal():
            newT = nextTrans(t, sent, model, vectorizer, sentEmbs, tokens,
                             linearModels=linearModels,
                             linearVecs=linearVecs,
                             mlpModels=mlpModels)
            markNum = 1 + markNum if newT and newT.type and newT.type.value and newT.type.value > 2 else 0
            newT.apply(t, sent, parse=True, isClassified=newT.isClassified, secondParse=not initialize)
            t = newT
            if configuration['xp']['kiperComp']:
                sentEmbs, tokens = refreshSentEmb(t, tokens, model, sentEmbs)
            sys.stdout.write(str(t))
            sys.stdout.flush()
        sent.recognizeEmbedded(annotated=False)


serieWithoutReduceIdx = 0


def nextTrans(t, sent, model, vectorizer, sentEmbs=None, tokens=None, linearModels=None, linearVecs=None,
              mlpModels=None):
    global markNum
    legalTansDic, predictedTrans = t.getLegalTransDic(), []
    reduceNum, tTmp = 0, t
    while tTmp and tTmp.type and tTmp.type != TransitionType.REDUCE:
        sys.stdout.write('Obligatory reduce\n')
        reduceNum += 1
        tTmp = tTmp.previous
    if reduceNum >= 10 or markNum > 4:
        if TransitionType.REDUCE in legalTansDic:
            trans = legalTansDic[TransitionType.REDUCE]
            trans.isClassified = False
            return trans
        else:
            sys.stderr.write('Reduce application is not possible for a long loop!\n')
            sys.stderr.write(str(t.configuration))

    if len(legalTansDic) == 1:
        sys.stdout.write('One legal transition\n')
        return initialize(legalTansDic.keys()[0], sent)
    sys.stdout.write('Selected by classifier\n')
    if configuration['xp']['kiperwasser']:
        predictedTrans = model.predict(t, sentEmbs)
    elif configuration['xp']['kiperComp']:
        predictedTrans = model.predict(t, sentEmbs, tokens)
    elif configuration['xp']['rnn'] or configuration['xp']['rnnNonCompo']:
        probVector = model.predict(t)
        predictedTrans = sorted(range(len(probVector)), key=lambda k: probVector[k], reverse=True)
    elif configuration['xp']['linear']:
        featDic = getFeatures(t, sent)
        if mlpModels:
            mlpModel, mlpNormalizer = getRelevantModelAndNormalizer(sent, None, mlpModels, None, True)
            probVector = mlpModel.predict(t)
            predictedTrans = sorted(range(len(probVector)), key=lambda k: probVector[k], reverse=True)
            featDic['MLP_Prediction'] = predictedTrans[0]
        if configuration['others']['svmScikit']:
            predTransValue = model.predict(vectorizer.transform(featDic))[0]  # .toarray()
            predTrans = getType(predTransValue)
            if predTrans in legalTansDic:
                trans = legalTansDic[predTrans]
                trans.isClassified = True
                return trans
            for t in [TransitionType.SHIFT, TransitionType.MERGE, TransitionType.REDUCE, TransitionType.MARK_AS_OTH]:
                if t in legalTansDic:
                    trans = legalTansDic[t]
                    trans.isClassified = False
                    return trans
        elif configuration['others']['svm']:
            predictions = model.predict(featDic)
            for item in predictions:
                predTrans = getType(item[0])
                if predTrans in legalTansDic:
                    trans = legalTansDic[predTrans]
                    trans.isClassified = True
                    return trans
        else:
            probVector = model.decision_function(vectorizer.transform(featDic))[0]
            predictedTrans = sorted(range(len(probVector)), key=lambda k: probVector[k], reverse=True)
    elif configuration['xp']['rmlpTree']:
        probVector = model.predict(t)
        predictedTrans = sorted(range(len(probVector)), key=lambda k: probVector[k], reverse=True)
    elif configuration['xp']['multitasking']:
        probVector = model.predictIdent(t, sent)
        sys.stdout.write(str(probVector) + '\n')
        predictedTrans = sorted(range(len(probVector)), key=lambda k: probVector[k], reverse=True)
    elif configuration['xp']['mlpPhrase'] or configuration['xp']['mlpWide']:
        probVector = model.predict(t)
        predictedTrans = sorted(range(len(probVector)), key=lambda k: probVector[k], reverse=True)
    else:
        probVector = model.predict(t, linearModels=linearModels, linearVecs=linearVecs)
        predictedTrans = sorted(range(len(probVector)), key=lambda k: probVector[k], reverse=True)
    for t in predictedTrans:
        transType = getType(t)
        if transType in legalTansDic:
            trans = legalTansDic[transType]
            trans.isClassified = True
            return trans
    sys.stdout.write('The first legal transition\n')
    return initialize(legalTansDic.keys()[0], sent)


def refreshSentEmb(t, tokens, model, sentEmbs):
    if t.configuration.buffer and t.configuration.buffer[-1] not in tokens \
            and tokens[-1].position == t.configuration.buffer[0].position:
        existingTokens = []
        if t.configuration.stack:
            for sItem in t.configuration.stack:
                tokenBfr = getTokens(sItem)
                for tItem in tokenBfr:
                    existingTokens.append(tItem)
        for iItem in t.configuration.buffer[:1]:
            existingTokens.append(iItem)
        if len(existingTokens) == len(tokens):
            if len(t.configuration.buffer) > 1:
                tokens.append(t.configuration.buffer[1])
        else:
            for i in range(len(tokens) - len(existingTokens)):
                for tItem in tokens:
                    if tItem not in existingTokens:
                        tokens.remove(tItem)
                        break
                if t.configuration.buffer and len(t.configuration.buffer) > i + 1:
                    tokens.append(t.configuration.buffer[i + 1])
        tokenIdxs, posIdxs = model.getIdxs(tokens)
        sentEmbs = model.getContextualizedEmbs(tokenIdxs, posIdxs)
    return sentEmbs, tokens
# import sys
#
# from corpus import getRelevantModelAndNormalizer
# from modelLinear import getFeatures
# from transitions import *
#
# markNum = 0
#
#
# def parse(sents, model, vectorizer=None, linearModels=None, linearVecs=None, mlpModels=None, initialize=True):
#     global markNum
#     for sent in sents:
#         if initialize:
#             sent.identifiedVMWEs = []
#         sentEmbs, tokens = getSentEmb(sent, model)
#         sent.initialTransition = Transition(None, isInitial=True, sent=sent)
#         t = sent.initialTransition
#         while not t.isTerminal():
#             newT = nextTrans(t, sent, model, vectorizer, sentEmbs, tokens,
#                              linearModels=linearModels,
#                              linearVecs=linearVecs,
#                              mlpModels=mlpModels)
#             markNum = 1 + markNum if newT and newT.isMarkOrMerge() else 0
#             newT.apply(t, sent, parse=True, isClassified=newT.isClassified, secondParse=not initialize)
#             t = newT
#             sentEmbs, tokens = refreshSentEmb(t, tokens, model, sentEmbs)
#         sent.recognizeEmbedded(annotated=False)
#
#
# def nextTrans(t, sent, model, vectorizer,
#               sentEmbs=None, tokens=None,
#               linearModels=None,
#               linearVecs=None,
#               mlpModels=None):
#     obligReduce = shouldReduce(t)
#     if obligReduce:
#         return obligReduce
#     legalTansDic, predictedTrans = t.getLegalTransDic(), []
#
#     obligMark = shouldMark(t, sent)
#     if obligMark:
#         return obligMark
#
#     if len(legalTansDic) == 1:
#         return initialize(legalTansDic.keys()[0], sent)
#     predictedTrans = predict(t, sent, model, vectorizer, sentEmbs, tokens, linearModels, linearVecs, mlpModels)
#     for t in predictedTrans:
#         transType = getType(t)
#         if transType in legalTansDic:
#             trans = legalTansDic[transType]
#             trans.isClassified = True
#             return trans
#
#
# def predict(t, sent, model, vectorizer,
#             sentEmbs=None, tokens=None,
#             linearModels=None,
#             linearVecs=None,
#             mlpModels=None):
#     if configuration['xp']['kiperwasser']:
#         # predictedTrans = model.predict(t, sentEmbs)
#         return model.predict(t, sent)[0]
#     if configuration['xp']['kiperComp']:
#         return model.predict(t, sentEmbs, tokens)
#
#     if configuration['xp']['linear']:
#         featDic = getFeatures(t, sent)
#         if mlpModels:
#             mlpModel, mlpNormalizer = getRelevantModelAndNormalizer(sent, None, mlpModels, None, True)
#             probVector = mlpModel.predict(t)
#             predictedTrans = sorted(range(len(probVector)), key=lambda k: probVector[k], reverse=True)
#             featDic['MLP_Prediction'] = predictedTrans[0]
#         if configuration['others']['svmScikit']:
#             return model.predict(vectorizer.transform(featDic))
#             # predTransValue = model.predict(vectorizer.transform(featDic))[0]  # .toarray()
#             # predTrans = getType(predTransValue)
#             # if predTrans in legalTansDic:
#             #     trans = legalTansDic[predTrans]
#             #     trans.isClassified = True
#             #     return trans
#             # for t in [TransitionType.SHIFT, TransitionType.MERGE, TransitionType.REDUCE, TransitionType.MARK_AS_OTH]:
#             #     if t in legalTansDic:
#             #         trans = legalTansDic[t]
#             #         trans.isClassified = False
#             #         return trans
#         if configuration['others']['svm']:
#             return model.predict(featDic)
#             # for item in predictions:
#             #     predTrans = getType(item[0])
#             #     if predTrans in legalTansDic:
#             #         trans = legalTansDic[predTrans]
#             #         trans.isClassified = True
#             #         return trans
#         else:
#             probVector = model.decision_function(vectorizer.transform(featDic))[0]
#             return sorted(range(len(probVector)), key=lambda k: probVector[k], reverse=True)
#     # if configuration['xp']['multitasking']:
#     #     probVector = model.predictIdent(t)
#     #     return sorted(range(len(probVector)), key=lambda k: probVector[k], reverse=True)
#     # if configuration['xp']['rnn'] or configuration['xp']['rnnNonCompo']:
#     #     probVector = model.predict(t)
#     #     return sorted(range(len(probVector)), key=lambda k: probVector[k], reverse=True)
#     if configuration['xp']['mlpPhrase'] or configuration['xp']['mlpWide'] or configuration['xp']['rmlpTree'] or \
#             configuration['xp']['multitasking'] or configuration['xp']['rnn'] or configuration['xp']['rnnNonCompo']:
#         probVector = model.predict(t)
#         return sorted(range(len(probVector)), key=lambda k: probVector[k], reverse=True)
#
#     probVector = model.predict(t, linearModels=linearModels, linearVecs=linearVecs)
#     return sorted(range(len(probVector)), key=lambda k: probVector[k], reverse=True)
#
#
# def shouldReduce(t):
#     global markNum
#     noReduceNum = 0
#     tmpT = t
#     while tmpT and tmpT.type and tmpT.type != TransitionType.REDUCE:
#         noReduceNum += 1
#         tmpT = tmpT.previous
#     if noReduceNum >= 10 or markNum > 4:
#         if TransitionType.REDUCE in t.getLegalTransDic():
#             trans = t.getLegalTransDic()[TransitionType.REDUCE]
#             trans.isClassified = False
#             return trans
#         sys.stderr.write('Reduce application is not possible for a long loop!\n')
#
#     return None
#
#
# def shouldMark(t, sent):
#     if configuration['tmp']['markObligatory']:
#         legalTansDic = t.getLegalTransDic()
#         if len(t.configuration.buffer) == 0:
#             if t.configuration.stack[-1] and not str(t.configuration.stack[-1].__class__).endswith('corpus.Token'):
#                 if TransitionType.REDUCE in legalTansDic and \
#                         configuration['tmp']['addTokens'] and sent.identifiedVMWEs:
#                     if configuration['tmp']['transOut']:
#                         sys.stdout.write('Obligatory mark (token extension):\n')
#                     for t in getTokens(t.configuration.stack[-1])[:2]:
#                         sent.identifiedVMWEs[-1].tokens.append(t)
#                     trans = legalTansDic[TransitionType.REDUCE]
#                     trans.isClassified = False
#                     return trans
#                 if not configuration['tmp']['addTokens'] and TransitionType.MARK_AS_OTH in legalTansDic:
#                     if configuration['tmp']['transOut']:
#                         sys.stdout.write('Obligatory mark\n')
#                     trans = legalTansDic[TransitionType.MARK_AS_OTH]
#                     trans.isClassified = False
#                     return trans
#     return None
#
#
# def refreshSentEmb(t, tokens, model, sentEmbs):
#     if not configuration['xp']['kiperComp']:
#         return None, None
#     if t.configuration.buffer and t.configuration.buffer[-1] not in tokens \
#             and tokens[-1].position == t.configuration.buffer[0].position:
#         existingTokens = []
#         if t.configuration.stack:
#             for sItem in t.configuration.stack:
#                 tokenBfr = getTokens(sItem)
#                 for tItem in tokenBfr:
#                     existingTokens.append(tItem)
#         for iItem in t.configuration.buffer[:1]:
#             existingTokens.append(iItem)
#         if len(existingTokens) == len(tokens):
#             if len(t.configuration.buffer) > 1:
#                 tokens.append(t.configuration.buffer[1])
#         else:
#             for i in range(len(tokens) - len(existingTokens)):
#                 for tItem in tokens:
#                     if tItem not in existingTokens:
#                         tokens.remove(tItem)
#                         break
#                 if t.configuration.buffer and len(t.configuration.buffer) > i + 1:
#                     tokens.append(t.configuration.buffer[i + 1])
#         tokenIdxs, posIdxs = model.getIdxs(tokens)
#         sentEmbs = model.getContextualizedEmbs(tokenIdxs, posIdxs)
#     return sentEmbs, tokens
#
#
# def getSentEmb(sent, model):
#     if False and configuration['xp']['kiperwasser']:  # @TODO
#         tokenIdxs, posIdxs = model.getIdxs(sent)
#         return model.getContextualizedEmbs(tokenIdxs, posIdxs), None
#     elif configuration['xp']['kiperComp']:
#         tokens = sent.tokens[:5]
#         tokenIdxs, posIdxs = model.getIdxs(tokens)
#         return model.getContextualizedEmbs(tokenIdxs, posIdxs), tokens
#     return None, None
