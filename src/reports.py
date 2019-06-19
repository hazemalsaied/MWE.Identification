import cPickle as pickle
import errno
import os
import sys
from collections import Counter

import numpy

from config import configuration

tabs, seperator, doubleSep, finalLine = '\t', '\n' + '_' * 98 + '\n', '\n' + '=' * 98 + '\n', '\n' + '*|' * 49 + '\n'
PATH_ROOT_REPORTS_DIR = os.path.join(configuration['path']['projectPath'], 'Reports')

try:
    reportPath = os.path.join(configuration['path']['projectPath'], PATH_ROOT_REPORTS_DIR)
    if not os.path.isdir(reportPath):
        os.makedirs(reportPath)
        # schemaFolder = os.path.join(reportPath, 'schemas')
        # if not os.path.isdir(schemaFolder):
        #    os.makedirs(schemaFolder)
except OSError as e:
    if e.errno != errno.EEXIST:
        raise

XP_CURRENT_DIR_PATH = ''
configuration['evaluation'] = configuration['evaluation']
repFiles = configuration['files']['reports']


# def getXPDirectory(langName, xpNum):
#
#     if configuration['evaluation']['load']:
#         return
#     cvTxt = '-CV' if configuration['evaluation']['cv'] else ''
#     prefix = langName + cvTxt + '-' + str(xpNum)
#     global XP_CURRENT_DIR_PATH
#     XP_CURRENT_DIR_PATH = os.path.join(reportPath, prefix)


# def createXPDirectory():
#     if configuration['evaluation']['load'] :
#         return
#     try:
#         if not os.path.isdir(XP_CURRENT_DIR_PATH):
#             os.makedirs(XP_CURRENT_DIR_PATH)
#     except OSError as err:
#         if err.errno != errno.EEXIST:
#             raise


def parsedSentsOut(corpus, sentNum):
    sentIdx, sentNum = 0, sentNum
    for s in corpus.testingSents:
        if len(s.tokens) < 15 and len(s.vMWEs) == 1 and sentIdx < sentNum:
            sys.stdout.write(str(s) + '\n')
            sentIdx += 1


def createReportFolder(lang):
    xpNum = getXPNum()
    cvTxt = '-CV' if configuration['evaluation']['cv'] else ''
    prefix = lang + cvTxt + '-' + str(xpNum)
    global XP_CURRENT_DIR_PATH
    XP_CURRENT_DIR_PATH = os.path.join(reportPath, prefix)
    if not configuration['evaluation']['load']:
        sys.stdout.write('Result folder: {0}\n'.format(XP_CURRENT_DIR_PATH.split('/')[-1]))
        if not os.path.isdir(XP_CURRENT_DIR_PATH):
            os.makedirs(XP_CURRENT_DIR_PATH)


def getXPNum():
    configPath = os.path.join(configuration['path']['projectPath'], 'config.txt')
    with open(configPath, 'r+') as xpfile:
        content = xpfile.read()
        xpNum = int(content)
    with open(configPath, 'w') as xpfile:
        newXpNum = xpNum + 1
        if newXpNum < 10:
            newXpNum = '000' + str(newXpNum)
        elif newXpNum < 100:
            newXpNum = '00' + str(newXpNum)
        elif newXpNum < 1000:
            newXpNum = '0' + str(newXpNum)
        else:
            newXpNum = str(newXpNum)
        xpfile.write(newXpNum)
    return xpNum


# def saveModelSummary(model):
#     if not mustSave():
#         return
#     json_string = model.to_json()
#     summaryFile = os.path.join(XP_CURRENT_DIR_PATH, repFiles['summary'])
#     if configuration['evaluation']['cv']:
#         summaryFile = os.path.join(XP_CURRENT_DIR_PATH, str(configuration['others']['currentIter']),
#                                    repFiles['summary'])
#     with open(summaryFile, 'a') as f:
#         f.write(json_string)


# def saveNormalizer(normalizer):
#     if not mustSave():
#         return
#     vectFile = os.path.join(XP_CURRENT_DIR_PATH, repFiles['normaliser'])
#     if configuration['evaluation']['cv']:
#         vectFile = os.path.join(XP_CURRENT_DIR_PATH, str(configuration['others']['currentIter']),
#                                 repFiles['normaliser'])
#     filehandler = open(vectFile, 'w')
#     pickle.dump(normalizer, filehandler, pickle.HIGHEST_PROTOCOL)


# def saveSettings():
#     if configuration['evaluation']['load']:
#         return
#     if configuration['evaluation']['cv']:
#         settFile = os.path.join(XP_CURRENT_DIR_PATH, str(configuration['others']['currentIter']), SETTINGS_FILE)
#     else:
#         settFile = os.path.join(XP_CURRENT_DIR_PATH, SETTINGS_FILE)
#     settStr = settings.toString()
#     with open(settFile, 'w') as f:
#         f.write(settStr)


# def saveScores(scores):
#     if not mustSave():
#         return
#     results, line = '', ''
#     for i in range(1, len(scores) + 1):
#         line += str(scores[i - 1]) + ','
#         if i % 4 == 0:
#             results += line[:-1] + '\n'
#             line = ''
#     scoresFile = os.path.join(XP_CURRENT_DIR_PATH, repFiles['scores'])
#     if configuration['evaluation']['cv']:
#         scoresFile = os.path.join(XP_CURRENT_DIR_PATH, str(configuration['others']['currentIter']),
#  repFiles['scores'])
#     with open(scoresFile, 'w') as f:
#         f.write(results)


LOADED_MODEL_PATH = ''


# def getLoadedModelPath(num, lang):
#     prefix = lang + '-MLP-' if settings.MLP else '-LSTM-'
#     loadedFolder = prefix + (
#         ('0' + str(num)) if num < 10 else str(num))
#     rPath = os.path.join(configuration['path']['projectPath'], PATH_ROOT_REPORTS_DIR)
#     return os.path.join(rPath, loadedFolder)


def loadNormalizer(loadFolderPath):
    normalizerPath = os.path.join(loadFolderPath, repFiles['normaliser'])
    return pickle.load(open(normalizerPath, 'rb'))


# def saveNetwork(model):
# if not mustSave():
# rI = random.randint(100, 500)
# shemaFile = os.path.join(configuration['path']['projectPath'], 'tmp/schemas/shema{0}.png'.format(rI))
# sys.stdout.write('# Schema file: {0}\n'.format(rI))
# plot_model(model, to_file=shemaFile)
# return
# schemaPath = os.path.join(XP_CURRENT_DIR_PATH, repFiles['schema'])
# if configuration['evaluation']['cv']:
#     schemaPath = os.path.join(XP_CURRENT_DIR_PATH, str(configuration['others']['currentIter']),
#                               repFiles['schema'])
# plot_model(model, to_file=schemaPath)
# sys.stdout.write('# Parameters = {0}\n'.format(model.count_params()))
# saveModelSummary(model)
# saveModel(model)


# def saveModel(model):
#     if not mustSave():
#         return
#     if configuration['evaluation']['cv']:
#         modelFile = os.path.join(XP_CURRENT_DIR_PATH, str(configuration['others']['currentIter']),
#                                  repFiles['model'])
#     else:
#         modelFile = os.path.join(XP_CURRENT_DIR_PATH, repFiles['model'])
#     if not os.path.isfile(modelFile) and configuration['evaluation']['save']:
#         model.save(modelFile)


# def loadModel(loadFolderPath):
#     modelPath = os.path.join(loadFolderPath, repFiles['model'])
#     loaded_model = load_model(modelPath)
#     sys.stdout.write('# Load path = {0}\n'.format(modelPath))
#
#     loaded_model.load_weights(os.path.join(loadFolderPath, 'weigth.hdf5'))
#     # weightFie = os.path.join(LOADED_MODEL_PATH, MODEL_WEIGHT_FILE)
#     # loaded_model.load_weights(weightFie)
#     # loaded_model.compile(loss='categorical_crossentropy', optimizer='rmsprop', metrics=['accuracy'])
#     return loaded_model


# def saveCVScores(scores):
#     if not mustSave() or not configuration['evaluation']['cv']:
#         return
#     results = ''
#     for i in range(len(scores)):
#         if i == 0 or i % 4 == 0:
#             tmpScores = '{0} : F-score: {1}, Rappel: {2}, Precsion: {3}\n'.format(
#                 scores[i], scores[i + 1] / configuration['others']['currentIter'],
#                            scores[i + 2] / configuration['others']['currentIter'],
#                            scores[i + 3] / configuration['others']['currentIter'])
#             if not tmpScores.startswith('0.0'):
#                 sys.stdout.write(tmpScores)
#                 results += tmpScores + '\n'
#     scoresFile = os.path.join(XP_CURRENT_DIR_PATH, repFiles['scores'])
#     with open(scoresFile, 'w') as f:
#         f.write(results)


def settingsToDic():
    settFilePath = os.path.join(LOADED_MODEL_PATH, repFiles['config'])
    results = {}
    with open(settFilePath, 'r') as settFile:
        for line in settFile:
            parts = line.strip().split('=')
            if parts and len(parts) == 2:
                key = parts[0].strip().replace(' ', '_').upper()
                results[key] = parts[1]
    return results


# def saveHistory(history):
#     if not mustSave():
#         return
#     historyFile = os.path.join(XP_CURRENT_DIR_PATH, repFiles['history'])
#     if configuration['evaluation']['cv']:
#         historyFile = os.path.join(XP_CURRENT_DIR_PATH, str(configuration['others']['currentIter']),
#                                    repFiles['history'])
#     with open(historyFile, 'wb') as f:
#         pickle.dump(history, f, pickle.HIGHEST_PROTOCOL)


def createHeader(value):
    if value:
        sys.stdout.write(doubleSep + doubleSep + tabs + '{0}\n'.format(value) + doubleSep)


def getBestWeightFilePath():
    if not configuration['nn']['checkPoint']:
        return None
    bestWeightPath = os.path.join(XP_CURRENT_DIR_PATH, configuration['files']['bestWeights'])
    if configuration['evaluation']['cv']:
        bestWeightPath = os.path.join(XP_CURRENT_DIR_PATH,
                                      str(configuration['others']['currentIter']),
                                      configuration['files']['bestWeights'])
    return bestWeightPath


featureNumLine = 'Trainable params: '
linearParamLine = '# Feature number = '
paramLine = 'Trainable params: '
scoreLine = '	Identification : 0'  # tabs + 'Identification : 0'
linearTitleLine = '# Language = '
titleLine = '# XP = '


def mineLinearFile(newFile):
    path = '../tmp/tmp/{0}'.format(newFile)
    titles, params, scores = [], [], []
    with open(path, 'r') as log:
        for line in log.readlines():
            if line.startswith(linearParamLine):
                paramsValue = toNum(line[len(linearParamLine):len(linearParamLine) + 8].strip())
                params.append(round(int(paramsValue) / 1000000., 2))
            if line.startswith(scoreLine):
                fScore = toNum(line[len(scoreLine):len(scoreLine) + 5].strip())
                while len(fScore) < 4:
                    fScore = fScore + '0'
                scores.append(round(int(fScore) / 10000., 4) * 100)
            if line.startswith(linearTitleLine):
                titles.append(line[len(linearTitleLine):].strip())
    for i in range(len(scores)):
        if i < len(titles):
            sys.stdout.write(str(scores[i]))  # titles[i]#, scores[i]
    return titles, scores, params


def mineFile(newFile):
    path = '../tmp/tmp/{0}'.format(newFile)
    titles, params, scores = [], [], []
    with open(path, 'r') as log:
        for line in log.readlines():
            if line.startswith(paramLine):
                paramsValue = toNum(line[len(paramLine):len(paramLine) + 8].strip())
                params.append(round(int(paramsValue) / 1000000., 2))
            if line.startswith(scoreLine):
                fScore = toNum(line[len(scoreLine):len(scoreLine) + 5].strip())
                while len(fScore) < 4:
                    fScore = fScore + '0'
                scores.append(round(int(fScore) / 10000., 4) * 100)
            if line.startswith(titleLine) and not line.startswith('WARNING:root:Title: Language : FR'):
                titles.append(line[len(titleLine):].strip())
    return titles, scores, params


def clean(titles, scores, params, xpNum):
    addedItems, newScores, newTitles, newParams = 0, [], [], []
    for i in range(1, len(scores)):
        if addedItems == xpNum:
            addedItems = 0
            continue
        newScores.append(scores[i])
        if i < len(params):
            newParams.append(params[i])
        if i < len(titles):
            newTitles.append(titles[i])
        addedItems += 1
    return newTitles, newScores, newParams


def divide(prilist, subListLength):
    stepNum, newList = len(prilist) / subListLength, []
    if stepNum:
        for i in range(stepNum):
            newList.append(prilist[i * subListLength: (i + 1) * subListLength])
        return newList
    return None


def getLinearScores(newFile):
    titles, scores, params = mineLinearFile(newFile)
    getDetailedScores(newFile, scores, titles, params)


def getScores(newFile, xpNum=10, shouldClean=False, showTitle=True):
    titles, scores, params = mineFile(newFile)
    if shouldClean:
        titles, scores, params = clean(titles, scores, params, xpNum)
    # getDetailedScores(newFile, scores, titles, params)
    getBrefScores(newFile, scores, titles, params, xpNum, showTitle=showTitle)


def getDetailedScores(newFile, scores, titles, params):
    text = '\\textbf{title}\t\t&\t\t\\textbf{F}\t\t\\textbf{P}\t\t\\\\\\hline\n'
    for i in range(len(scores)):
        titleText = titles[i] if i < len(titles) else ''
        paramsText = '\t\t&\t\t{0}\t'.format(params[i] if i < len(params) else '')
        paramsText = paramsText if paramsText != '\t\t&\t\t' else ''
        text += '{0}\t\t&\t\t{1}{2}\\\\\\hline\n'.format(titleText, scores[i], paramsText)
    with open('../tmp/{0}.detailed.csv'.format(newFile), 'w') as res:
        res.write(text)


def getBrefScores(newFile, scores, titles, params, xpNum, showTitle=True):
    scores = divide(scores, xpNum)
    params = divide(params, xpNum)
    titles = divide(titles, xpNum)
    # text = '\\textbf{title}\t&\t\\textbf{F$_{mean}$}\t&\t\\textbf{F$_{max}$}\t&' \
    #       '\t\t\\textbf{MAD}\t\t&\t\t\\textbf{P}\t\t\\\\\\hline\n'
    text = ''
    for i in range(len(scores)):
        # if i < 12:
        #     header = '{0}\t\t&\t\t{1}\t\t'.format(dom[i], '')
        # else:
        #     header= '{0}\t\t&\t\t{1}\t\t'.format('', dom[i])
        if showTitle:
            titleText = titles[i][0] if titles else ''
            if titleText:
                titleText += '\t\t\t\t&'
        else:
            titleText = ''
        population = scores[i]
        meanValue = round(numpy.mean(population), 1)
        maxValue = round(max(population), 1)
        mad = getMeanAbsoluteDeviation(population)
        paramsText = '\t\t&{0}\t\t'.format(round(numpy.mean(params[i]), 1) if params else '')
        paramsText = paramsText if paramsText != '\t\t&\t\t' else ''
        text += '{0}{1}\t\t&\t\t{2}\t\t&\t\t{3}{4}\t\t\\\\\n'.format(
            titleText, meanValue, maxValue, mad, paramsText)
        sys.stdout.write(str(meanValue))
    with open('../tmp/tmp/{0}.tex'.format(newFile), 'w') as res:
        res.write(text)


def toNum(text, addPoint=False):
    textBuf = ''
    for c in text:
        if c.isdigit():
            textBuf += c
    if addPoint and textBuf.strip() != '0':
        return float(textBuf) / (pow(10, len(textBuf)))
    return textBuf


def getMeanAbsoluteDeviation(domain):
    avg = numpy.mean(domain)
    distances = []
    for v in domain:
        dis = v - avg
        if dis < 0:
            dis *= -1
        distances.append(dis)
    return round(sum(distances) / len(distances), 1)


def attaachTwoFiles(f1, f2):
    res = ''
    with open(f1, 'r') as f1:
        with open(f2, 'r') as f2:
            idx = 0
            content = f2.readlines()
            for line1 in f1:
                res += line1[:-1] + content[idx]
                idx += 1


def getStats(newFile):
    path = '../tmp/tmp/{0}'.format(newFile)
    langs, mweLEngth, oldMWEs, newMWEs, params, dataSize, scores, correctlyIdentifiedList, nonIdentifiedList \
        = [], [], [], [], [], [], [], [], []
    langLine = tabs + 'Language : '
    mweLengthLine = tabs + 'MWE length mean : '
    oldMWEsLine = tabs + 'Seen MWEs : '
    newMWEsLine = tabs + 'New MWEs : '
    paramLine = 'Total params: '
    dataSizeLine = tabs + 'data size after sampling = '
    scoreLine = tabs + 'Identification : '
    correctlyIdentifiedLine = tabs + 'Correctly identified MWEs'
    nonIdentifiedLine = 'Non Identified MWEs'
    correctlyIdentified, nonIdentified = False, False
    nonIdentifiedDic, nonIdentifiedDic = dict(), dict()
    with open(path, 'r') as log:
        for line in log:
            line = line[:-1]
            if line.startswith(langLine):
                langs.append(line[len(langLine):].strip())
            elif line.startswith(mweLengthLine):
                mweLEngth.append(line[len(mweLengthLine):].strip())
            elif line.startswith(oldMWEsLine):
                oldMWEs.append(line[len(oldMWEsLine) + 5:-3].strip())
            elif line.startswith(newMWEsLine):
                newMWEs.append(line[len(newMWEsLine) + 5:-3].strip())
            elif line.startswith(paramLine):
                params.append(line[len(paramLine):].strip())
            elif line.startswith(dataSizeLine):
                dataSize.append(line[len(dataSizeLine):].strip())
            elif line.startswith(scoreLine):
                scores.append(round(float(line[len(scoreLine):].strip()) * 100, 2))

            if line.startswith(correctlyIdentifiedLine):
                correctlyIdentified = True
                correctlyIdentifiedDic = {}
            if correctlyIdentified and line.strip() and not line.startswith('-') and not line.startswith('='):
                line = line.strip()
                parts = line.split(' : ')
                if len(parts) == 2:
                    correctlyIdentifiedDic[parts[0]] = parts[1]

            if nonIdentifiedLine in line:  # line.startswith(nonIdentifiedLine):
                correctlyIdentified = False
                correctlyIdentifiedList.append(correctlyIdentifiedDic)
                correctlyIdentifiedDic = dict()
                nonIdentified = True
                nonIdentifiedDic = dict()

            if nonIdentified and line.strip() and not line.startswith('-') and not line.startswith('='):
                line = line.strip()
                parts = line.split(' : ')
                if len(parts) == 2:
                    nonIdentifiedDic[parts[0]] = parts[1]

            if line.startswith('*|'):
                nonIdentified = False
                nonIdentifiedList.append(nonIdentifiedDic)
    for i in range(len(correctlyIdentifiedList)):
        for k in correctlyIdentifiedList[i].keys():
            if int(correctlyIdentifiedList[i][k]) < 5:
                del correctlyIdentifiedList[i][k]
        for k in nonIdentifiedList[i].keys():
            if int(nonIdentifiedList[i][k]) < 3:
                del nonIdentifiedList[i][k]
    for i in range(len(correctlyIdentifiedList)):
        nonIdentifiedList[i] = str(nonIdentifiedList[i]).replace(',', '-')
        correctlyIdentifiedList[i] = str(correctlyIdentifiedList[i]).replace(',', '-')
        params[i] = params[i].replace(',', ' ')
        scores[i] = str(scores[i]).replace(',', '.')
    res = ''

    for i in range(len(scores)):
        res += '{0},{1},{2},{3},{4},{5},{6},{7},{8}\n'.format(langs[i], scores[i], mweLEngth[i], oldMWEs[i], newMWEs[i],
                                                              params[i], dataSize[i], correctlyIdentifiedList[i],
                                                              nonIdentifiedList[i])
    with open(path + '.csv', 'w') as f:
        f.write(res)


langLine1 = '	Language : '
langLine = '	GPU Enabled	Language : '


def getAvgScores(scores, langNum=3, trialNum=3):
    result, xpScores, langSum = [], [], 0
    for i, v in enumerate(scores):
        if i != 0 and i % trialNum == 0:
            xpScores.append(round(float(langSum) / trialNum, 1))
            langSum = 0
        if i != 0 and i % (trialNum * langNum) == 0:
            result.append(xpScores)
            xpScores = []
        langSum += float(v)
    xpScores.append(round(float(langSum) / trialNum, 1))
    result.append(xpScores)
    return result


def getSeedScores(files, folder=None, pilot=False, withTitles=True, withTitle2=False):
    for ff in files:
        titles, scores, params, langs, titles2, seeds, precisions, recalls = mineNewFile(str(ff), folder)
        scores = [round(s * 100, 2) for s in scores]
        xpNums = int(len(scores) / 30.)
        for i in range(xpNums):
            bgVar = round(getMeanAbsoluteDeviation(scores[i * 30:(i * 30) + 10]), 2)
            bgScores = ','.join(str(s) for s in scores[i * 30:(i * 30) + 10]) if i * 30 < len(scores) else ''
            ptVar = round(getMeanAbsoluteDeviation(scores[(i * 30) + 10:(i * 30) + 20]), 2)
            ptScores = ','.join(str(s) for s in scores[i * 30 + 10:(i * 30) + 20]) if (i * 30) + 10 < len(
                scores) else ''
            trVar = round(getMeanAbsoluteDeviation(scores[(i * 30) + 20: (i * 30) + 30]), 2)
            trScores = ','.join(str(s) for s in scores[i * 30 + 20:(i * 30) + 30]) if (i * 30) + 20 < len(
                scores) else ''
            avg = round((bgVar + ptVar + trVar) / 3., 2)
            sys.stdout.write(
                ','.join([str(avg), str(bgVar), str(ptVar), str(trVar), bgScores, ptScores, trScores]) + ',' + titles[
                                                                                                                   i][
                                                                                                               :-1])


def getNewScores(files, folder=None, pilot=False, pos=False, withTitles=True, onCorpus=False, onFixed=False, ftb=False):
    for f in files:
        print str(f)
        titles, scores, params, langs, titles2, seeds, stats, precisions, recalls, misidentified, nonidentified, mwePosTags, posTags = \
            mineNewFile(str(f), folder, ftb=ftb)
        # scores, params = mineCoopFile(str(f))
        if pilot:
            x = 3
            for i in range(len(titles)):
                # if withTitle2:
                # withTitle2 = False
                #    sys.stdout.write('BG, BG,BG, PT, PT,PT, TR,TR, TR, BG_AVG, PT_AVG, TR_AVG ' + titles2[i][:-1])
                sys.stdout.write('{0},{1},{2},{3},{4}\n'.format(
                    scores[i * x] if pos and i * x < len(scores) else 0,
                    scores[i * x + 1] if pos and i * x + 1 < len(scores) else 0,
                    scores[i * x + 2] if pos and i * x + 2 < len(scores) else 0,
                    titles[i][:-1], str(f)
                ))
        # POS tagging
        # if pilot:
        #     x = 3
        #     for i in range(len(titles)):
        #         # if withTitle2:
        #         # withTitle2 = False
        #         #    sys.stdout.write('BG, BG,BG, PT, PT,PT, TR,TR, TR, BG_AVG, PT_AVG, TR_AVG ' + titles2[i][:-1])
        #         sys.stdout.write('{0},{1},{2},{3},{4},{5},{6},{7}\n'.format(
        #             poss[i*x ] if pos and i*x < len(poss) else 0,
        #             poss[i * x + 1] if pos and i * x + 1 < len(poss) else 0,
        #             poss[i * x + 2] if pos and i * x + 2 < len(poss) else 0,
        #             poss2[i*x] if pos and i * x  < len(poss2) else 0,
        #             poss2[i * x + 1] if pos and i * x + 1 < len(poss2) else 0,
        #             poss2[i * x + 2] if pos and i * x + 2 < len(poss2) else 0,
        #             # scores[i * x] if i * x < len(scores) else -1,
        #             # scores[i * x + 1] if i * x + 1 < len(scores) else -1,
        #             # scores[i * x + 2] if i * x + 2 < len(scores) else -1,
        #             titles[i][:-1], str(f)
        # POS + Identification
        # if pilot:
        #     x = 3
        #     for i in range(len(titles)):
        #         # if withTitle2:
        #         # withTitle2 = False
        #         #    sys.stdout.write('BG, BG,BG, PT, PT,PT, TR,TR, TR, BG_AVG, PT_AVG, TR_AVG ' + titles2[i][:-1])
        #         avg1 = round(scores[i * x],1) if i * x < len(scores) else -1
        #         avg2 = round(scores[i * x + 1],1) if i * x + 1 < len(scores) else -1
        #         avg3 = round(scores[i * x + 2], 3) if i * x + 2 < len(scores) else -1
        #         avgPos = poss[i] if pos and i < len(poss) else 0
        #         avgPos2 = poss2[i] if pos and i < len(poss2) else 0
        #         avgg = round((avg1 + avg2 + avg3) / 3., 1)
        #         sys.stdout.write('{0},{1},{2},{3},{4},{5},{6},{7},{8}{9},{10}\n'.format(
        #             poss[i*x ] if pos and i*x < len(poss) else 0,
        #             poss[i * x + 1] if pos and i * x + 1 < len(poss) else 0,
        #             poss[i * x + 2] if pos and i * x + 2 < len(poss) else 0,
        #             poss2[i*x] if pos and i * x  < len(poss2) else 0,
        #             poss2[i * x+1] if pos and i * x + 1 < len(poss2) else 0,
        #             poss2[i * x+2] if pos and i * x + 2 < len(poss2) else 0,
        #             scores[i * x] if i * x < len(scores) else -1,
        #             scores[i * x + 1] if i * x + 1 < len(scores) else -1,
        #             scores[i * x + 2] if i * x + 2 < len(scores) else -1,
        #             ',' + titles[i][:-1] ,
        #             str(f)
        #         ))
        elif onCorpus:
            for i, v in enumerate(scores):
                line = ','.join(str(x) for x in [langs[i], v, precisions[i], recalls[i]])
                print line
        elif onFixed:
            for i in range(len(posTags)):
                print posTags[i], ',', mwePosTags[i] if i < len(mwePosTags) else 0
            newStats = []
            for i in range(int(len(stats) / 5.)):
                newStats.append(stats[i*5]) # g
                newStats.append(stats[i*5 + 1]) # pred
                newStats.append(stats[i*5 + 2]) # F
                newStats.append(round(stats[i*5 + 3] * 100,1)) # P
                newStats.append(round(stats[i*5 + 4] * 100,1)) # R
                if newStats[-1] + newStats[-2] != 0:
                    newStats.append(round(2 * newStats[-1] * newStats[-2] / (newStats[-1] + newStats[-2]), 1))
                else:
                    newStats.append(0)
            stats = newStats
            for i, v in enumerate(scores):
                line = ','.join(str(x) for x in [langs[i], v, precisions[i], recalls[i]] +
                                stats[i * 96:(i + 1) * 96] +
                                misidentified[i * 9: (i + 1) * 9] +
                                nonidentified[i * 13: (i + 1) * 13]
                                ) + \
                       (',' + titles[i][:-1] + '\n' if withTitles else '') + '\n'
                sys.stdout.write(line)

        # elif onFixed:
        #     newStats = []
        #     for i in range(int(len(stats) / 5.)):
        #         newStats.append(stats[i*5]) # g
        #         newStats.append(stats[i*5 + 1]) # pred
        #         newStats.append(stats[i*5 + 2]) # F
        #         newStats.append(round(stats[i*5 + 3] * 100,1)) # P
        #         newStats.append(round(stats[i*5 + 4] * 100,1)) # R
        #         if newStats[-1] + newStats[-2] != 0:
        #             newStats.append(round(2 * newStats[-1] * newStats[-2] / (newStats[-1] + newStats[-2]), 1))
        #         else:
        #             newStats.append(0)
        #     stats = newStats
        #     for i, v in enumerate(scores):
        #         line = ','.join(str(x) for x in [langs[i], v, precisions[i], recalls[i]] +
        #                         stats[i * 96:(i + 1) * 96] +
        #                         misidentified[i * 9: (i + 1) * 9] +
        #                         nonidentified[i * 13: (i + 1) * 13]
        #                         ) + \
        #                (',' + titles[i][:-1] + '\n' if withTitles else '') + '\n'
        #         sys.stdout.write(line)
        #         # if i % 2 == 1 and v > scores[i - 1]:
        #         #     sys.stdout.write(line)
        #         # if i % 2 == 0 and v >= scores[i + 1] :
        #         #     sys.stdout.write(line)
        else:
            for i in range(len(scores)):
                print ','.join(str(x) for x in [langs[i], scores[i], precisions[i], recalls[i]]) + ',' + titles[i][
                                                                                                         :-1] if withTitles else ''
            # for i in range(len(titles)):
            #     if i*2 + 1 < len(scores):
            #         print str(scores[i*2]) +','+ str(scores[i*2 + 1]) + ',' + titles[i][:-1]


goldLine = '	Gold:'
predictedLine = '	Predicted:'
fLine = '	F :'


def mineNewFile(newFile, folder=None, ftb=False):
    x = ('MLP.New/' + folder) if folder else ''
    path = os.path.join('../Reports/Reports/', x, newFile)
    titles, params, scores, precisions, recalls, langs, titles2, seeds, stats, misidentified, nonIdentified, mwePosTags, posTags = \
        [], [], [], [], [], [], [], [], [], [], [], [], []
    previousLine = ''
    seedLine = '# Seed:'
    with open(path, 'r') as log:
        # shouldContinue = True
        isMisidentified, isNonidentified = False, False
        for line in log.readlines():
            # if shouldContinue:
            #     if line.startswith('XP Starts: 14/1') or line.startswith('XP Starts: 15/1') or \
            #             line.startswith('XP Starts: 16/1') or line.startswith('XP Starts: 17/1'):
            #         shouldContinue = False
            #     continue
            if line.startswith('POS tagging accuracy (MWEs)'):
                mwePosTags.append(line[:-1].split('=')[1])
            if line.startswith('POS tagging accuracy = '):
                posTags.append(line[:-1].split('=')[1])
            if line.startswith('Misidentified:'):
                isMisidentified = True  # False
                continue
            if isMisidentified and not line.startswith('='):
                misidentified.append(line[:-1].split(':')[1])
            if isMisidentified and line.startswith('	MWTs:'):
                isMisidentified = False

            if line.startswith('Non-identified:'):
                isNonidentified = True  # False
                continue
            if isNonidentified and not line.startswith('='):
                nonIdentified.append(line[:-1].split(':')[1])
            if isNonidentified and line.startswith('	VPC Full:'):
                isNonidentified = False
                if len(nonIdentified) / 13 != len(misidentified) / 9:
                    for i in range(9 * (len(nonIdentified) / 13 - len(misidentified) / 9)):
                        misidentified.append(0)
            if ftb and line.startswith('	MWTs:'):
                isNonidentified = False
            if line.startswith('	P, R  :') and previousLine.startswith('	Identification :'):
                precisions.append(float(line[:-1].split(':')[1].split(',')[0]) * 100)
                recalls.append(float(line[:-1].split(':')[1].split(',')[1]) * 100)
            if line.startswith(seedLine):
                seeds.append(int(line[len(seedLine):-1]))
            if line.startswith('# Configs:'):
                titles.append(line)
            if line.startswith('# CTitles:'):
                titles2.append(line)
            if line.__contains__(' Train ('):
                langs.append(line.strip()[:2])
            if line.startswith(langLine) or line.startswith(langLine1):
                if line.startswith(langLine):
                    langs.append(line[len(langLine):len(langLine) + 2])
                else:
                    langs.append(line[len(langLine1):len(langLine1) + 2])
            if line.startswith(paramLine):
                paramsValue = toNum(line[len(paramLine):len(paramLine) + 8].strip())
                params.append(round(int(paramsValue) / 1000000., 2))
            if line.startswith(scoreLine) and previousLine.startswith('='):
                fScore = toNum(line[len(scoreLine):len(scoreLine) + 5].strip())
                while len(fScore) < 4:
                    fScore = fScore + '0'
                scores.append(round(int(fScore) / 10000., 3) * 100)
            if line.startswith(goldLine) or line.startswith(predictedLine):
                stats.append(float(line[:-1].split(':')[1].split()[0]))
            if line.startswith(fLine):
                stats.append(float(line[:-1].split(':')[1].split()[0]) * 100)
            if line.startswith('	P, R  : ') and not previousLine.startswith('	Identification : '):
                stats.append(float(line.split(':')[1].split(',')[0]))
                stats.append(float(line.split(':')[1].split(',')[1]))

            if line.startswith(titleLine) and not line.startswith('WARNING:root:Title: Language : FR'):
                titles.append(line[len(titleLine):].strip())
            previousLine = line
    return titles, scores, params, langs, titles2, seeds, stats, precisions, recalls, misidentified, nonIdentified, mwePosTags, posTags


def mineCoopFile(newFile):
    path = '../Reports/Reports/{0}'.format(newFile)
    params, scores = [], []
    previousLine = ''
    with open(path, 'r') as log:
        for line in log.readlines():
            if line.startswith('# Configs:'):
                params.append(line)
            if line.startswith(scoreLine):
                fScore = toNum(line[len(scoreLine):len(scoreLine) + 5].strip())
                while len(fScore) < 4:
                    fScore = fScore + '0'
                scores.append(round(int(fScore) / 10000., 4) * 100)
    return scores, params


def orderResults(titles, values):
    results = dict()
    for i in range(len(titles)):
        xpTitles = titles[i].split(',')
        xpValues = values[i].split(',')
        if len(xpTitles) != len(xpValues):
            pass
        results[i] = dict()
        for j in range(len(xpTitles)):
            results[i][xpTitles[j]] = xpValues[j]
    for i in range(len(titles)):
        sys.stdout.write(str(sorted(results[i].items())) + '\n')


def readAndOrderResults():
    titles, values, idx = [], [], 0

    with open('tmp - tmp.csv.csv', 'r') as f:
        for line in f:
            if idx % 2 == 0:
                titles.append(line[:-1])
            else:
                values.append(line[:-1])
            idx += 1
    orderResults(titles, values)


def mineSTScriptRes(newFile):
    path = '../Reports/Reports/{0}'.format(newFile)
    results, res = [], []
    with open(path, 'r') as log:
        for line in log.readlines():
            if line.startswith('* MWE-based:'):
                res.append(round(float(line[-5:-1]) / 100., 1))
                res.append(round(float(line.split('=')[2][:-2]) * 100., 1))
                res.append(round(float(line.split('=')[4][:-2]) * 100., 1))
            #if line.startswith('* MWE-based:'):

            if line.startswith('* Tok-based:'):
                res.append(round(float(line[-5:-1]) / 100., 1))
                res.append(round(float(line.split('=')[2][:-2]) * 100., 1))
                res.append(round(float(line.split('=')[4][:-2]) * 100., 1))
            if line.startswith('* Continuous: MWE-based:'):
                res.append(round(float(line[-5:-1]) / 100., 1))
                res.append(round(float(line.split('=')[2][:-2]) * 100., 1))
                res.append(round(float(line.split('=')[4][:-2]) * 100., 1))
            if line.startswith('* Continuous: MWE-proportion:'):
                res.append(line.split('%')[0].split('=')[-1] + ' , ' + line.split('%')[1].split('=')[-1])
            if line.startswith('* Discontinuous: MWE-based:'):
                res.append(round(float(line[-5:-1]) / 100., 1))
                res.append(round(float(line.split('=')[2][:-2]) * 100., 1))
                res.append(round(float(line.split('=')[4][:-2]) * 100., 1))
            if line.startswith('* Discontinuous: MWE-proportion:'):
                res.append(line.split('%')[0].split('=')[-1] + ' , ' + line.split('%')[1].split('=')[-1])
            if line.startswith('* Multi-token: MWE-based: '):
                res.append(round(float(line[-5:-1]) / 100., 1))
                res.append(round(float(line.split('=')[2][:-2]) * 100., 1))
                res.append(round(float(line.split('=')[4][:-2]) * 100., 1))
            if line.startswith('* Multi-token: MWE-proportion:'):
                res.append(line.split('%')[0].split('=')[-1] + ' , ' + line.split('%')[1].split('=')[-1])
            if line.startswith('* Single-token: MWE-based:'):
                res.append(round(float(line[-5:-1]) / 100., 1))
                res.append(round(float(line.split('=')[2][:-2]) * 100., 1))
                res.append(round(float(line.split('=')[4][:-2]) * 100., 1))
            if line.startswith('* Single-token: MWE-proportion:'):
                res.append(line.split('%')[0].split('=')[-1] + ' , ' + line.split('%')[1].split('=')[-1])
            if line.startswith('* Seen-in-train: MWE-based:'):
                res.append(round(float(line[-5:-1]) / 100., 1))
                res.append(round(float(line.split('=')[2][:-2]) * 100., 1))
                res.append(round(float(line.split('=')[4][:-2]) * 100., 1))
            if line.startswith('* Seen-in-train: MWE-proportion:'):
                res.append(line.split('%')[0].split('=')[-1] + ' , ' + line.split('%')[1].split('=')[
                    -1])  # line.split('%')[0].split('=')[-1] + ' / ' + line.split('%')[1].split('=')[-1])
            if line.startswith('* Unseen-in-train: MWE-based:'):
                res.append(round(float(line[-5:-1]) / 100., 1))
                res.append(round(float(line.split('=')[2][:-2]) * 100., 1))
                res.append(round(float(line.split('=')[4][:-2]) * 100., 1))
            if line.startswith('* Unseen-in-train: MWE-proportion:'):
                res.append(line.split('%')[0].split('=')[-1] + ' , ' + line.split('%')[1].split('=')[-1])
            if line.startswith('* Variant-of-train: MWE-based: '):
                res.append(round(float(line[-5:-1]) / 100., 1))
                res.append(round(float(line.split('=')[2][:-2]) * 100., 1))
                res.append(round(float(line.split('=')[4][:-2]) * 100., 1))
            if line.startswith('* Variant-of-train: MWE-proportion:'):
                res.append(line.split('%')[0].split('=')[-1] + ' , ' + line.split('%')[1].split('=')[-1])
            if line.startswith('* Identical-to-train: MWE-proportion:'):
                res.append(line.split('%')[0].split('=')[-1] + ' , ' + line.split('%')[1].split('=')[-1])
            if line.startswith('* Identical-to-train: MWE-based:'):
                res.append(round(float(line[-5:-1]) / 100., 1))
                res.append(round(float(line.split('=')[2][:-2]) * 100., 1))
                res.append(round(float(line.split('=')[4][:-2]) * 100., 1))
                results.append(res)
                print res
                res = []
    #print results
    return results


def DivideXPFile():
    for subdir, dirs, files in os.walk('../Reports/Reports/MLP.New'):
        for d in dirs:
            for ff in os.listdir('../Reports/Reports/MLP.New/' + d):
                with open(os.path.join('../Reports/Reports/MLP.New', d, ff), 'r') as ff:
                    wordcount = Counter(ff.read().split())
                    if "Killed" in wordcount and wordcount["Killed"] > 1:
                        f1Text, f2Text = '', ''
                        file1 = True
                        with open(os.path.join('../Reports/Reports/MLP.New', d, ff), 'r') as fileToRead:
                            for l in fileToRead:
                                if file1:
                                    f1Text += l
                                else:
                                    f2Text += l
                                if ' Killed ' in l:
                                    file1 = False
                            with open(os.path.join('../Reports/Reports/MLP.New', d, str(ff) + '.f1Text'),
                                      'w+') as fff:
                                fff.write(f1Text)
                            with open(os.path.join('../Reports/Reports/MLP.New', d, str(ff) + '.f2Text'),
                                      'w+') as ffff:
                                ffff.write(f2Text)

                        sys.stdout.write(str(wordcount["Killed"]) + ' : ' + str(d) + '/' + str(ff))


def getSeenandNonSeenStats():
    path = os.path.join(configuration['path']['projectPath'], '/Results/Evaluation/Script/linear.fixedSize')
    with open(path, 'r') as ff:
        res = ''
        for l in ff:
            if l.startswith('* MWE-based:'):
                parts = l.split('=')
                ig = parts[1].split('/')[0]
                i = parts[1].split('/')[1]
                g = parts[3].split('/')[1]
                p = round(float(parts[2].split(' ')[0]), 2)
                r = round(float(parts[4].split(' ')[0]), 2)
                f = round(float(parts[5].split(' ')[0][:-1]), 2)
                res += '{0},{1},{2},{3},{4},{5},'.format(ig, i, g, p, r, f)
            if l.startswith('* Seen-in-train: MWE-based:'):
                parts = l.split('=')
                ig = parts[1].split('/')[0]
                i = parts[1].split('/')[1]
                g = parts[3].split('/')[1]
                p = round(float(parts[2].split(' ')[0]), 2)
                r = round(float(parts[4].split(' ')[0]), 2)
                f = round(float(parts[5].split(' ')[0][:-1]), 2)
                res += '{0},{1},{2},{3},{4},{5},'.format(ig, i, g, p, r, f)
            if l.startswith('* Unseen-in-train: MWE-based:'):
                parts = l.split('=')
                ig = parts[1].split('/')[0]
                i = parts[1].split('/')[1]
                g = parts[3].split('/')[1]
                p = round(float(parts[2].split(' ')[0]), 2)
                r = round(float(parts[4].split(' ')[0]), 2)
                f = round(float(parts[5].split(' ')[0][:-1]), 2)
                res += '{0},{1},{2},{3},{4},{5}\n'.format(ig, i, g, p, r, f)
        sys.stdout.write(res)

def analyzeCatReport():
    path = '/Users/halsaied/PycharmProjects/MWE.Identification/Results/Evaluation/Reports/TrainVsDev/catAnalysis.svm'
    with open(path, 'r') as ff:
        res = ''
        for l in ff:
            if l.startswith('	HE Train '):
                pass
            if l[1:4] in ['VID', 'LVC', 'IRV', 'VPC', 'IAV', 'MVC', 'LC:' ]:
                res += l[-5:-1] if not l.endswith('-\n') else '-'
                res += ','

            if l.startswith('	Mode'):
                res+= '\n'
    print res
if __name__ == '__main__':
    # getSeenandNonSeenStats()
    # mineSTScriptRes('scriptRes.tendy.txt')
    # analyzeCatReport()
    # getSeedScores(
    # for f in os.listdir('../Reports/MLP'):
    #     #if f.split('.')[1] != '02':
    #     if not f.startswith('06.02'):
    #         os.remove('../Reports/MLP/' + f)

    getNewScores(
        [f for f in os.listdir('../Reports/Reports/') if f.startswith('multi.j')], None
        , pilot=False, withTitles=False, pos=True, onFixed=True, onCorpus=False, ftb=False)

    # for subdir, dirs, files in os.walk('../Reports/Reports/MLP.New'):
    #    for dir in dirs:
    #         getNewScores(
    #             [f for f in os.listdir('../Reports/Reports/MLP.New/' + dir) if f.startswith('mlp')], dir
    #             , pilot=True, withTitles=True, withTitle2=False)
