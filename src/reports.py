import datetime
import errno
import os
import sys

from config import configuration

tabs, seperator, doubleSep, finalLine = '\t', '\n' + '_' * 98 + '\n', '\n' + '=' * 98 + '\n', '\n' + '*|' * 49 + '\n'
PATH_ROOT_REPORTS_DIR = os.path.join(configuration['path']['projectPath'], 'Reports')

try:
    reportPath = os.path.join(configuration['path']['projectPath'], 'Reports')
    if not os.path.isdir(reportPath):
        os.makedirs(reportPath)
except OSError as e:
    if e.errno != errno.EEXIST:
        raise

repFiles = configuration['files']['reports']

LOADED_MODEL_PATH = ''

featureNumLine = 'Trainable params: '
linearParamLine = '# Feature number = '
paramLine = 'Trainable params: '
scoreLine = '\tIdentification : 0'
linearTitleLine = '# Language = '
titleLine = '# XP = '

langLine1 = '\tLanguage : '
langLine = '\tGPU Enabled,Language : '
goldLine = '\tGold:'
predictedLine = '\tPredicted:'
fLine = '\tF :'


class ReportMiner:
    @staticmethod
    def getNewScores(files, division):
        for ff in files:
            configs, scores, langs, stats, precisions, recalls, misidentified, nonidentified, trainTimes = \
                ReportMiner.mineNewFile(str(ff))
            if division == 'fixed':
                x = 3
                for i in range(len(configs)):
                    sys.stdout.write('{0},{1},{2},{3},{4}\n'.format(
                        scores[i * x] if i * x < len(scores) else 0,
                        scores[i * x + 1] if i * x + 1 < len(scores) else 0,
                        scores[i * x + 2] if i * x + 2 < len(scores) else 0,
                        configs[i][:-1],
                        str(ff)))
            elif division == 'corpus':
                for i, v in enumerate(scores):
                    line = ','.join(str(x) for x in [langs[i], v, precisions[i], recalls[i]])
                    print line
            elif division == 'dev':
                newStats = []
                for i in range(int(len(stats) / 5.)):
                    newStats.append(stats[i * 5])  # g
                    newStats.append(stats[i * 5 + 1])  # pred
                    newStats.append(stats[i * 5 + 2])  # F
                    newStats.append(round(stats[i * 5 + 3] * 100, 1))  # P
                    newStats.append(round(stats[i * 5 + 4] * 100, 1))  # R
                    if newStats[-1] + newStats[-2] != 0:
                        newStats.append(round(2 * newStats[-1] * newStats[-2] / (newStats[-1] + newStats[-2]), 1))
                    else:
                        newStats.append(0)
                stats = newStats
                for i, v in enumerate(scores):
                    line = ','.join(str(x) for x in [langs[i], v, precisions[i], recalls[i]] +
                                    stats[i * 96:(i + 1) * 96] +
                                    (misidentified[i * 10: (i + 1) * 10]  if (i + 1) * 10 < len(misidentified) else [])+
                                    (nonidentified[i * 14: (i + 1) * 14] if  (i + 1) * 14 <len(nonidentified) else []) )
                    sys.stdout.write(line + '\n')

    @staticmethod
    def getDimsumSCore(files, division):
        for ff in files:
            print ff
            configs, scores, langs, stats, precisions, recalls, misidentified, nonidentified, trainTimes = \
                ReportMiner.mineDimsumReport(str(ff))
            if division == 'dev':
                newStats = []
                for i in range(int(len(stats) / 5.)):
                    newStats.append(stats[i * 5])  # g
                    newStats.append(stats[i * 5 + 1])  # pred
                    newStats.append(stats[i * 5 + 2])  # F
                    newStats.append(round(stats[i * 5 + 3] * 100, 1))  # P
                    newStats.append(round(stats[i * 5 + 4] * 100, 1))  # R
                    if newStats[-1] + newStats[-2] != 0:
                        newStats.append(round(2 * newStats[-1] * newStats[-2] / (newStats[-1] + newStats[-2]), 1))
                    else:
                        newStats.append(0)
                stats = newStats
                for i, v in enumerate(scores):
                    t = 10
                    line = ','.join(str(x) for x in [langs[i], v, precisions[i], recalls[i]] +
                                    stats[i * 96:(i + 1) * 96] +
                                    (misidentified[i * t: (i + 1) * t] if (i + 1) * t <= len(misidentified) else []) +
                                    (nonidentified[i * t: (i + 1) * t] if (i + 1) * t <= len(nonidentified) else []))
                    sys.stdout.write(line + '\n')

    @staticmethod
    def getMisIdentified(files):
        # idx = 0
        for ff in files:
            #     path = os.path.join('../Reports/Reports/', ff)
            #     txt = ''
            #     with open(path, 'r') as log:
            #         for l in log.readlines():
            #             if l.startswith(',Mode: '):
            #                 if idx == 1:
            #                     break
            #                 else:
            #                     idx +=1
            #             # if idx ==1:
            #             txt += l
            #     with open(path+'1', 'w') as log:
            #         log.write(txt)
            langs, misidentified, nonIdentified, titles = ReportMiner.mineForMisiidentified(str(ff))
            print ff
            print str(titles)
            for i, v in enumerate(langs):
                line = ','.join(str(x) for x in [langs[i]] + misidentified[i * 10: (i + 1) * 10])
                sys.stdout.write(line + '\n')

    @staticmethod
    def mineForMisiidentified(newFile):
        path = os.path.join('../Reports/Reports/', newFile)
        langs, misidentified, nonIdentified, titles = [], [], [], []
        tit1Line = ',Mode: '
        tit2Line = ',Division: '
        with open(path, 'r') as log:
            isMisidentified, isNonidentified = False, False
            for line in log.readlines():
                if line.startswith(tit1Line):
                    titles.append(line[len(tit1Line):-1])
                if line.startswith(tit2Line):
                    titles.append(line[len(tit2Line):-1])
                if line.startswith('Misidentified:'):
                    isMisidentified = True
                    continue
                if isMisidentified and not line.startswith('=') and line != '\n':
                    misidentified.append(line[:-1].split(':')[1])
                if isMisidentified and line.startswith('\tMWTs:'):
                    isMisidentified = False
                if line.startswith('Non-identified:'):
                    isNonidentified = True  # False
                    continue
                if isNonidentified and not line.startswith('=') and line != '\n':
                    nonIdentified.append(line[:-1].split(':')[1])
                if isNonidentified and line.startswith('\tVPC Full:'):
                    isNonidentified = False
                    if len(nonIdentified) / 13 != len(misidentified) / 9:
                        for i in range(9 * (len(nonIdentified) / 13 - len(misidentified) / 9)):
                            misidentified.append(0)
                if line.__contains__(' Train ('):
                    langs.append(line.strip()[:2])
                if line.startswith(langLine) or line.startswith(langLine1):
                    if line.startswith(langLine):
                        langs.append(line[len(langLine):len(langLine) + 2])
                    else:
                        langs.append(line[len(langLine1):len(langLine1) + 2])
        return langs, misidentified, nonIdentified, titles

    @staticmethod
    def getLangs(path):
        results = []
        with open(path, 'r') as log:
            for l in log.readlines():
                if l.__contains__(' Train ('):
                    results.append(l.strip()[:2])
        return results

    @staticmethod
    def mineReport(path, line, usePreviousLine=False, previousLine='', cut=0):
        results, pl = [], ''
        with open(path, 'r') as log:
            for l in log.readlines():
                if l.startswith(line) and pl.startswith(previousLine):
                    pointer = -1
                    if cut and len(line) + cut < len(l):
                        pointer = len(line) + cut
                    results.append(l[len(line):pointer])
                if usePreviousLine:
                    pl = l
        return results

    @staticmethod
    def mineMTReports(files):
        for ff in files:
            print ff
            path = os.path.join('../Reports/Reports/', ff)
            configs = ReportMiner.mineReport(path, '# Configs:')
            lass = ReportMiner.mineReport(path, 'LAS = ', cut=4)
            uass = ReportMiner.mineReport(path, 'UAS = ', cut=4)
            ident = ReportMiner.mineReport(path, '\tIdentification : ', cut=5)
            pos = ReportMiner.mineReport(path, 'POS tagging accuracy = ', cut=4)
            mwePpos = ReportMiner.mineReport(path, 'POS tagging accuracy (MWEs) = ', cut=4)
            ident = [float(i) * 100 for i in ident]
            for i in range(len(configs)):
                print ','.join(str(x) for x in [
                    lass[i * 3] if i * 3 < len(lass) else '-', lass[i * 3 + 1] if i * 3 + 1 < len(lass) else '-',
                    lass[i * 3 + 2] if i * 3 + 2 < len(lass) else '-',
                    uass[i * 3] if i * 3 < len(uass) else '-', uass[i * 3 + 1] if i * 3 + 1 < len(uass) else '-',
                    uass[i * 3 + 2] if i * 3 + 2 < len(uass) else '-',
                    # pos[i * 3] if i * 3 < len(pos) else '-',
                    # pos[i * 3 + 1] if i * 3 + 1 < len(pos) else '-',
                    # pos[i * 3 + 2] if i * 3 + 2 < len(pos) else '-',
                    # mwePpos[i * 3] if i * 3 < len(mwePpos) else '-',
                    # mwePpos[i * 3 + 1] if i * 3 + 1 < len(mwePpos) else '-',
                    # mwePpos[i * 3 + 2] if i * 3 + 2 < len(mwePpos) else '-',
                    # (ident[i * 3]) if i * 3 < len(ident) else '-',
                    # (ident[i * 3 + 1]) if i * 3 + 1 < len(ident) else '-',
                    # (ident[i * 3 + 2]) if i * 3 + 2 < len(ident) else '-',
                    # params[i].split(',')[0] + '.' + params[i].split(',')[1][0],
                    configs[i],
                    str(ff)])

    @staticmethod
    def mineMTResult(files):
        for ff in files:
            print ff
            path = os.path.join('../Reports/Reports/', ff)
            lass = ReportMiner.mineReport(path, 'LAS = ', cut=4)
            uass = ReportMiner.mineReport(path, 'UAS = ', cut=4)
            ident = ReportMiner.mineReport(path, '\tIdentification : ', cut=5)
            pos = ReportMiner.mineReport(path, 'POS tagging accuracy = ', cut=4)
            mwePpos = ReportMiner.mineReport(path, 'POS tagging accuracy (MWEs) = ', cut=4)
            params = ReportMiner.mineReport(path, '# Configs:')
            ident = [float(i) * 100 for i in ident]
            langs = ReportMiner.getLangs(path)
            for i in range(len(ident)):
                print ','.join(str(x) for x in [
                    #lass[i ],
                    #uass[i],
                    pos[i ],
                    mwePpos[i],
                    ident[i],
                    # langs[i],
                    params[i].split(',')[0]]
                    )

    @staticmethod
    def parseChenManningReports(files):
        for ff in files:
            path = os.path.join('../Reports/Reports/', ff)
            # configs = ReportMiner.mineReport(path, '# Configs:')
            # params = ReportMiner.mineReport(path, 'Total params: ')
            lass = ReportMiner.mineReport(path, 'LAS = ')
            uass = ReportMiner.mineReport(path, 'UAS = ')
            langs = ReportMiner.getLangs(path)

            for i in range(len(lass)):
                print ','.join(str(x) for x in [langs[i],
                                                lass[i],
                                                uass[i]])  # ,
                # params[i].split(',')[0] + '.' + params[i].split(',')[1][0],
                # configs[i],
                # str(ff)])

    @staticmethod
    def parseUdPIPE(files):
        for ff in files:
            path = os.path.join('../Reports/Reports/', ff)
            langs = ReportMiner.mineReport(path, 'Evaluating dev:')
            devResults = ReportMiner.mineReport(path, 'Parsing from gold tokenization with gold tags - forms:',
                                                usePreviousLine=True,
                                                previousLine='Evaluating dev:')
            tstResults = ReportMiner.mineReport(path, 'Parsing from gold tokenization with gold tags - forms:',
                                                usePreviousLine=True,
                                                previousLine='Evaluating test:')
            for i in range(len(langs)):
                print ','.join(str(x) for x in [langs[i],
                                                devResults[i] if i < len(devResults) else '-',
                                                tstResults[i] if i < len(tstResults) else '-'])

    @staticmethod
    def parsePOSUdPIPE(files):
        for ff in files:
            path = os.path.join('../Reports/Reports/', ff)
            langs = ReportMiner.mineReport(path, 'Evaluating')
            results = ReportMiner.mineReport(path, 'Tagging from gold tokenization - forms: ')
            for i in range(len(langs)):
                print ','.join(str(x) for x in [langs[i],
                                                results[i] if i < len(results) else '-'])

    @staticmethod
    def analyzeCatReport():
        path = '/Users/halsaied/PycharmProjects/MWE.Identification/Results/Evaluation/Reports/TrainVsDev/catAnalysis.svm'
        with open(path, 'r') as ff:
            res = ''
            for l in ff:
                if l.startswith(',HE Train '):
                    pass
                if l[1:4] in ['VID', 'LVC', 'IRV', 'VPC', 'IAV', 'MVC', 'LC:']:
                    res += l[-5:-1] if not l.endswith('-\n') else '-'
                    res += ','

                if l.startswith(',Mode'):
                    res += '\n'
        print res

    @staticmethod
    def mineSTScriptRes(newFile):
        path = '../Reports/{0}'.format(newFile)
        results, res = [], []
        with open(path, 'r') as log:
            for line in log.readlines():
                if line.startswith('Evaluating:  '):
                    res.append(line[-4:-1])
                if line.startswith('* MWE-based:'):
                    res.append(round(float(line[-5:-1]) / 100., 1))
                    res.append(round(float(line.split('=')[2][:-2]) * 100., 1))
                    res.append(round(float(line.split('=')[4][:-2]) * 100., 1))
                # if line.startswith('* Tok-based:'):
                #     res.append(round(float(line[-5:-1]) / 100., 1))
                #     res.append(round(float(line.split('=')[2][:-2]) * 100., 1))
                #     res.append(round(float(line.split('=')[4][:-2]) * 100., 1))
                if line.startswith('* Continuous: MWE-based:'):
                    res.append(round(float(line[-5:-1]) / 100., 1))
                    res.append(round(float(line.split('=')[2][:-2]) * 100., 1))
                    res.append(round(float(line.split('=')[4][:-2]) * 100., 1))
                # if line.startswith('* Continuous: MWE-proportion:'):
                #     res.append(line.split('%')[0].split('=')[-1] + ' , ' + line.split('%')[1].split('=')[-1])
                if line.startswith('* Discontinuous: MWE-based:'):
                    res.append(round(float(line[-5:-1]) / 100., 1))
                    res.append(round(float(line.split('=')[2][:-2]) * 100., 1))
                    res.append(round(float(line.split('=')[4][:-2]) * 100., 1))
                # if line.startswith('* Discontinuous: MWE-proportion:'):
                #     res.append(line.split('%')[0].split('=')[-1] + ' , ' + line.split('%')[1].split('=')[-1])
                if line.startswith('* Multi-token: MWE-based: '):
                    res.append(round(float(line[-5:-1]) / 100., 1))
                    res.append(round(float(line.split('=')[2][:-2]) * 100., 1))
                    res.append(round(float(line.split('=')[4][:-2]) * 100., 1))
                # if line.startswith('* Multi-token: MWE-proportion:'):
                #     res.append(line.split('%')[0].split('=')[-1] + ' , ' + line.split('%')[1].split('=')[-1])
                if line.startswith('* Single-token: MWE-based:'):
                    res.append(round(float(line[-5:-1]) / 100., 1))
                    res.append(round(float(line.split('=')[2][:-2]) * 100., 1))
                    res.append(round(float(line.split('=')[4][:-2]) * 100., 1))
                # if line.startswith('* Single-token: MWE-proportion:'):
                #     res.append(line.split('%')[0].split('=')[-1] + ' , ' + line.split('%')[1].split('=')[-1])
                if line.startswith('* Seen-in-train: MWE-based:'):
                    res.append(round(float(line[-5:-1]) / 100., 1))
                    res.append(round(float(line.split('=')[2][:-2]) * 100., 1))
                    res.append(round(float(line.split('=')[4][:-2]) * 100., 1))
                # if line.startswith('* Seen-in-train: MWE-proportion:'):
                #     res.append(line.split('%')[0].split('=')[-1] + ' , ' + line.split('%')[1].split('=')[
                #         -1])  # line.split('%')[0].split('=')[-1] + ' / ' + line.split('%')[1].split('=')[-1])
                if line.startswith('* Unseen-in-train: MWE-based:'):
                    res.append(round(float(line[-5:-1]) / 100., 1))
                    res.append(round(float(line.split('=')[2][:-2]) * 100., 1))
                    res.append(round(float(line.split('=')[4][:-2]) * 100., 1))
                # if line.startswith('* Unseen-in-train: MWE-proportion:'):
                #     res.append(line.split('%')[0].split('=')[-1] + ' , ' + line.split('%')[1].split('=')[-1])
                if line.startswith('* Variant-of-train: MWE-based: '):
                    res.append(round(float(line[-5:-1]) / 100., 1))
                    res.append(round(float(line.split('=')[2][:-2]) * 100., 1))
                    res.append(round(float(line.split('=')[4][:-2]) * 100., 1))
                # if line.startswith('* Variant-of-train: MWE-proportion:'):
                #     res.append(line.split('%')[0].split('=')[-1] + ' , ' + line.split('%')[1].split('=')[-1])
                # if line.startswith('* Identical-to-train: MWE-proportion:'):
                #     res.append(line.split('%')[0].split('=')[-1] + ' , ' + line.split('%')[1].split('=')[-1])
                if line.startswith('* Identical-to-train: MWE-based:'):
                    res.append(round(float(line[-5:-1]) / 100., 1))
                    res.append(round(float(line.split('=')[2][:-2]) * 100., 1))
                    res.append(round(float(line.split('=')[4][:-2]) * 100., 1))
                    results.append(res)
                    print res
                    res = []
        newResults = []
        for i in range(int(len(results) / 5)):
            newRes = [0] * len(results[0])
            newRes[0] = results[i * 5][0]
            for j in range(1, len(results[0])):
                newRes[j] = round(
                    (results[i * 5][j] + results[i * 5 + 1][j] + results[i * 5 + 2][j] + results[i * 5 + 3][
                        j] + results[i * 5 + 4][j]) / 5, 1)
            print newRes
            newResults.append(newRes)
        return results

    @staticmethod
    def mineDimsumReport(newFile):
        path = os.path.join('../Reports/Reports/', newFile)
        configs, scores, precisions, recalls, langs, stats, misidentified, nonIdentified, trainTime = \
            [], [], [], [], [], [], [], [], []
        previousLine = ''
        trainTimeLine = ',TRAINING TIME:'
        with open(path, 'r') as log:
            isMisidentified, isNonidentified = False, False
            for line in log.readlines():
                if line.startswith(trainTimeLine):
                    trainTime.append(line[len(trainTimeLine):-9])
                if line.startswith('Misidentified:'):
                    isMisidentified = True  # False
                    continue
                if isMisidentified and line != '\n' and not line.startswith('='):
                    misidentified.append(line[:-1].split(':')[1])
                if isMisidentified and line.startswith('\tMWTs:'):
                    isMisidentified = False
                if line.startswith('Non-identified:'):
                    isNonidentified = True  # False
                    continue
                if isNonidentified and line != '\n' and not line.startswith('='):
                    nonIdentified.append(line[:-1].split(':')[1])
                if isNonidentified and (line.startswith('\tVPC Full:') or line.startswith('\tMWTs:')):
                    isNonidentified = False
                    if len(nonIdentified) / 13 != len(misidentified) / 9:
                        for i in range(9 * (len(nonIdentified) / 13 - len(misidentified) / 9)):
                            misidentified.append(0)
                # if ftb and line.startswith(',MWTs:'):
                #     isNonidentified = False
                if line.startswith('\tP, R  :') and previousLine.startswith('\tIdentification :'):
                    precisions.append(float(line[:-1].split(':')[1].split(',')[0]) * 100)
                    recalls.append(float(line[:-1].split(':')[1].split(',')[1]) * 100)
                if line.startswith('# Configs:'):
                    configs.append(line)
                if line.__contains__(' Train ('):
                    langs.append(line.strip()[:2])
                if line.startswith(langLine) or line.startswith(langLine1):
                    if line.startswith(langLine):
                        langs.append(line[len(langLine):len(langLine) + 2])
                    else:
                        langs.append(line[len(langLine1):len(langLine1) + 2])
                if line.startswith(scoreLine) and previousLine.startswith('='):
                    fScore = ReportMiner.toNum(line[len(scoreLine):len(scoreLine) + 5].strip())
                    while len(fScore) < 4:
                        fScore = fScore + '0'
                    scores.append(round(int(fScore) / 10000., 3) * 100)
                if line.startswith(goldLine) or line.startswith(predictedLine):
                    stats.append(float(line[:-1].split(':')[1].split()[0]))
                if line.startswith(fLine):
                    stats.append(float(line[:-1].split(':')[1].split()[0]) * 100)
                if line.startswith('\tP, R  : ') and (not previousLine.startswith('\tIdentification : ') and not previousLine.startswith('\tDiMSUM')) :
                    stats.append(float(line.split(':')[1].split(',')[0]))
                    stats.append(float(line.split(':')[1].split(',')[1]))

                if line.startswith(titleLine) and not line.startswith('WARNING:root:Title: Language : FR'):
                    configs.append(line[len(titleLine):].strip())
                previousLine = line
        return configs, scores, langs, stats, precisions, recalls, misidentified, nonIdentified, trainTime

    @staticmethod
    def mineNewFile(newFile):
        path = os.path.join('../Reports/Reports/', newFile)
        configs, scores, precisions, recalls, langs, stats, misidentified, nonIdentified, trainTime = \
            [], [], [], [], [], [], [], [], []
        previousLine = ''
        trainTimeLine = ',TRAINING TIME:'
        with open(path, 'r') as log:
            isMisidentified, isNonidentified = False, False
            for line in log.readlines():
                if line.startswith(trainTimeLine):
                    trainTime.append(line[len(trainTimeLine):-9])
                if line.startswith('Misidentified:'):
                    isMisidentified = True  # False
                    continue
                if isMisidentified and line!= '\n' and not line.startswith('='):
                    misidentified.append(line[:-1].split(':')[1])
                if isMisidentified and line.startswith('\tMWTs:'):
                    isMisidentified = False
                if line.startswith('Non-identified:'):
                    isNonidentified = True  # False
                    continue
                if isNonidentified and line!= '\n' and not line.startswith('='):
                    nonIdentified.append(line[:-1].split(':')[1])
                if isNonidentified and line.startswith('\tVPC Full:'):
                    isNonidentified = False
                    if len(nonIdentified) / 13 != len(misidentified) / 9:
                        for i in range(9 * (len(nonIdentified) / 13 - len(misidentified) / 9)):
                            misidentified.append(0)
                # if ftb and line.startswith(',MWTs:'):
                #     isNonidentified = False
                if line.startswith('\tP, R  :') and previousLine.startswith('\tIdentification :'):
                    precisions.append(float(line[:-1].split(':')[1].split(',')[0]) * 100)
                    recalls.append(float(line[:-1].split(':')[1].split(',')[1]) * 100)
                if line.startswith('# Configs:'):
                    configs.append(line)
                if line.__contains__(' Train ('):
                    langs.append(line.strip()[:2])
                if line.startswith(langLine) or line.startswith(langLine1):
                    if line.startswith(langLine):
                        langs.append(line[len(langLine):len(langLine) + 2])
                    else:
                        langs.append(line[len(langLine1):len(langLine1) + 2])
                if line.startswith(scoreLine) and previousLine.startswith('='):
                    fScore = ReportMiner.toNum(line[len(scoreLine):len(scoreLine) + 5].strip())
                    while len(fScore) < 4:
                        fScore = fScore + '0'
                    scores.append(round(int(fScore) / 10000., 3) * 100)
                if line.startswith(goldLine) or line.startswith(predictedLine):
                    stats.append(float(line[:-1].split(':')[1].split()[0]))
                if line.startswith(fLine):
                    stats.append(float(line[:-1].split(':')[1].split()[0]) * 100)
                if line.startswith('\tP, R  : ') and not previousLine.startswith('\tIdentification : '):
                    stats.append(float(line.split(':')[1].split(',')[0]))
                    stats.append(float(line.split(':')[1].split(',')[1]))

                if line.startswith(titleLine) and not line.startswith('WARNING:root:Title: Language : FR'):
                    configs.append(line[len(titleLine):].strip())
                previousLine = line
        return configs, scores, langs, stats, precisions, recalls, misidentified, nonIdentified, trainTime

    @staticmethod
    def toNum(text, addPoint=False):
        textBuf = ''
        for c in text:
            if c.isdigit():
                textBuf += c
        if addPoint and textBuf.strip() != '0':
            return float(textBuf) / (pow(10, len(textBuf)))
        return textBuf


class STDOutTools:
    @staticmethod
    def generateOarsub(xpNum=21, duration=100, tourNum=1, name='mlp'):
        for i in range(1, xpNum + 1):
            sys.stdout.write('oarsub -p "GPU_MODEL <> \'NO\'" -q production -l nodes=1,walltime={0} '
                             '"NNIdenSys/Scripts/nonCompo.sh" -n {4}{1}.{2} '
                             '-O Reports/{3}{1}.{2} -E Reports/{3}{1}.{2}\n'.
                             format(duration, tourNum, i, name, name[-10:]))

    @staticmethod
    def generateKiperOarsub(xpNum=21, duration=100, tourNum=1, name='mlp'):
        for i in range(1, xpNum + 1):
            sys.stdout.write('oarsub -p "cluster=\'grimani\'" -q production -l nodes=1,walltime={0} '
                             '"NNIdenSys/Scripts/nonCompo.sh" -n {4}{1}.{2} '
                             '-O Reports/{3}{1}.{2} -E Reports/{3}{1}.{2}\n'.
                             format(duration, tourNum, i, name, name[-10:]))

    @staticmethod
    def getExcutionTime(label, start):
        sys.stdout.write('{0}{1}: {2} minutes {3}'.format(tabs,
                                                          label.upper(),
                                                          round((datetime.datetime.now() - start).seconds / 60., 2),
                                                          doubleSep))


class OSTools:
    @staticmethod
    def getListOfFiles(dirName):
        # create a list of file and sub directories
        # names in the given directory
        listOfFile = os.listdir(dirName)
        allFiles = list()
        # Iterate over all the entries
        for entry in listOfFile:
            # Create full path
            fullPath = os.path.join(dirName, entry)
            # If entry is a directory then get the list of files in this directory
            if os.path.isdir(fullPath):
                allFiles = allFiles + OSTools.getListOfFiles(fullPath)
            else:
                allFiles.append(fullPath)

        return allFiles

    @staticmethod
    def deleteKiperFiles():
        res = 'rm '
        files = OSTools.getListOfFiles('/Users/halsaied/PycharmProjects/MWE.Identification/Reports/Reports')
        for ff in files:
            if 'kiper' in ff:
                res += 'Reports/' + ff.split('/')[-1] + ' '
        print res

    @staticmethod
    def cleanReports(path='Reports/Reports'):
        proPath = os.path.dirname(__file__)[:-len(os.path.basename(os.path.dirname(__file__)))]
        directory = os.path.join(proPath, path)
        labels = ['One legal', '1- ', '2- ', '3- ', '0- ', '4- ', '5- ', '4- ' '2- ' '+', '\n', 'WARNING', 'INFO',
                  'Obligatory', 'Selected by', '[', 'S=', 'SHIFT',
                  'MERGE', 'REDUCE', 'MARK', 'MWEs']

        files = OSTools.getListOfFiles(directory)
        for filename in files:
            # filePath = os.path.join(directory, filename)
            with open(filename, 'r') as ff:
                text = ''
                lines = ff.readlines()
                for l in lines:
                    startWithOneLabel = False
                    for x in labels:
                        if l.startswith(x):
                            startWithOneLabel = True
                            break
                    if not startWithOneLabel:
                        text += l
            if text:
                with open(filename, 'w') as ff:
                    ff.write(text)

    @staticmethod
    def deleteResultFiles():
        directory = '/Users/halsaied/PycharmProjects/MWE.Identification/Results/Evaluation/Data'
        files = OSTools.getListOfFiles(directory)
        for filename in files:
            if filename.endswith('.gold.cupt') or filename.endswith('.train.cupt'):
                os.remove(filename)

    @staticmethod
    def moveFiles():
        import shutil
        dest = '/Users/halsaied/PycharmProjects/MWE.Identification/Results/baseline-cv'
        files = OSTools.getListOfFiles(dest)
        for ff in files:
            filename = ff.split('/')[-1]
            shutil.move(ff, os.path.join(dest, filename))

    @staticmethod
    def copyTrainFiles():
        targetPath = '/Users/halsaied/PycharmProjects/MWE.Identification/Results/SVM0-CV'
        destPath = '/Users/halsaied/PycharmProjects/MWE.Identification/Results/baseline-cv'
        from shutil import copyfile
        files = OSTools.getListOfFiles(targetPath)
        for ff in files:
            if ff.endswith('train.cupt'):
                filename = ff.split('/')[-1]
                filenameNumber = int(filename[2]) + 1
                filename = filename[:2] + str(filenameNumber) + filename[3:]
                copyfile(ff, os.path.join(destPath, filename))

    @staticmethod
    def removeNonCuptFiles():
        targetPath = '/Users/halsaied/PycharmProjects/MWE.Identification/Results/SVM0-CV'
        files = OSTools.getListOfFiles(targetPath)
        for ff in files:
            if ff.endswith('train.txt.cupt'):
                os.remove(ff)

    @staticmethod
    def attaachTwoFiles(f1, f2):
        res = ''
        with open(f1, 'r') as f1:
            with open(f2, 'r') as f2:
                idx = 0
                content = f2.readlines()
                for line1 in f1:
                    res += line1[:-1] + content[idx]
                    idx += 1


def mad(numberList):
    m = float(sum(numberList)) / len(numberList)
    devs = []
    for n in numberList:
        devs.append(n - m if n > m else m - n)
    return round(float(sum(devs)) / len(devs), 1)


def readResamplingReport():
    with open('/Users/halsaied/PycharmProjects/MWE.Identification/Reports/tmp.csv', 'r') as ff:
        content = ff.readlines()
        results = []
        for line1 in content:
            lineParts = line1.split(',')
            results.append([lineParts[0], float(lineParts[1]), float(lineParts[2]), float(lineParts[3])])
        for i in range(len(results) / 5):
            f = round(float(
                float(results[i * 5][1]) + float(results[i * 5 + 1][1]) + float(results[i * 5 + 2][1]) + float(
                    results[i * 5 + 3][1]) + float(results[i * 5 + 4][1])) / 5, 1)
            p = round(float(results[i * 5][2] + results[i * 5 + 1][2] + results[i * 5 + 2][2] + results[i * 5 + 3][2] +
                            results[i * 5 + 4][2]) / 5, 1)
            r = round(float(results[i * 5][3] + results[i * 5 + 1][3] + results[i * 5 + 2][3] + results[i * 5 + 3][3] +
                            results[i * 5 + 4][3]) / 5, 1)
            m = mad([results[i * 5][1], results[i * 5 + 1][1], results[i * 5 + 2][1], results[i * 5 + 3][1],
                     +results[i * 5 + 4][1]])
            sys.stdout.write(results[i * 5][0], f, p, r, m)

def readStats(newFile):
    path = os.path.join('../Reports/Reports/', newFile)
    res = ''
    with open(path, 'r') as log:
        for line in log.readlines():
            if line.startswith('== '):
                res += line
    # print res
    return res
def deleteJobs(jobId):
    res = 'oardel '
    for i in range(12):
        res += ' ' + str(jobId+i)
    print res

if __name__ == '__main__':
    files = [f for f in os.listdir('../Reports/Reports/')if f.startswith('multi.joint.dev')]
    # OSTools.cleanReports()
    # readStats('r')
    # STDOutTools.generateOarsub(xpNum=6, duration=72, tourNum=1, name='kiper.minimized.gpu')
    # STDOutTools.generateKiperOarsub(xpNum=12, duration=20, tourNum=2, name='k.gpu')
    ReportMiner.getNewScores(files, ['corpus', 'fixed', 'dev'][0])
    # ReportMiner.getDimsumSCore(files, ['corpus', 'fixed', 'dev'][2])
    # ReportMiner.getMisIdentified(files)
    # ReportMiner.mineMTReports(files)
    # str = ''
    # str =str.replace(',', '.')
    # str = str.replace('	', ',')
    # numsAsStr = str.split(',')
    # nums = []
    # for n in numsAsStr:
    #     nums.append(float(n))
    # k = 3
    # for i in range(len(nums)/k):
    #     print nums[i*k], nums[i*k +1], nums[i*k +2]#, nums[i*k +3]
    # print deleteJobs(2131081)
