#!/usr/bin/python
# -*- coding: utf-8 -*-
import copy
import itertools
import pickle
import random
import re
from collections import Counter
from random import uniform
from nltk.parse import DependencyGraph

from reports import *


class Corpus:
    """
        a class used to encapsulate all the information of the corpus
    """

    def __init__(self, langName):
        """
            an initializer of the corpus, responsible of creating a structure of objects encapsulating all the
            information of the corpus, its sentences, tokens and MWEs.

            This function iterate over the lines of corpus document to create the precedent ontology
        """
        self.langName = langName
        self.readDataSets(langName)
        # self.getVMWEReport()
        self.analyzeSents()
        self.orderParentVMWEs()
        self.getTrainAndTest()
        self.cleanSents()
        self.extractDictionaries()
        self.deleteNonRecognizableMWE()
        printStats(self.trainingSents, 'Train', mweDic=self.mweDictionary, langName=langName, test=False)
        printStats(self.testingSents, 'Test', mweDic=self.mweDictionary, test=True)

    def toVocabulary(self):
        unk = configuration['constants']['unk']
        empty = configuration['constants']['empty']
        number = configuration['constants']['number']
        tokenCounter, posCounter = Counter(), Counter()
        for s in self.trainingSents:
            for t in s.tokens:
                tokenCounter.update({t.getTokenOrLemma(): 1})
                posCounter.update({t.posTag.lower(): 1})
        if configuration['embedding']['compactVocab']:
            for t in tokenCounter.keys():
                if t not in self.mweTokenDictionary:
                    del tokenCounter[t]
        else:
            for t in tokenCounter.keys():
                if tokenCounter[t] == 1 and uniform(0, 1) < configuration['constants']['alpha']:
                    del tokenCounter[t]
        tokenCounter.update({unk: 1, number: 1, empty: 1})
        posCounter.update({unk: 1, empty: 1})
        Corpus.printVocabReport(tokenCounter, posCounter)
        return {w: i for i, w in enumerate(tokenCounter.keys())}, {w: i for i, w in enumerate(posCounter.keys())}

    @staticmethod
    def printVocabReport(tokenCounter, posCounter):
        res = seperator + tabs + 'Vocabulary' + doubleSep
        res += tabs + 'Tokens := {0} * POS : {1}'.format(len(tokenCounter), len(posCounter)) \
            if not configuration['xp']['compo'] else ''
        res += seperator
        return res

    def cleanSents(self):
        if not configuration['tmp']['cleanSents']:
            return
        for s in self.trainingSents + self.testingSents:
            for t in s.tokens:
                if t.text != ',' and t.text != '-':
                    t.text = re.sub(r'[^\w\s]', '', t.text)
                    t.lemma = re.sub(r'[^\w\s]', '', t.lemma)
                    if t.text == '' or t.getLemma() == '':
                        t.text = 'punc'
                        t.lemma = 'punc'

    def getImportantWordLexicon(self):
        importWordCorpus, processedMWEs = '', []
        for s in self.trainingSents:
            for w in s.vMWEs:
                if w.getLemmaString() not in processedMWEs:
                    importWordCorpus += w.getLemmaString() + '\n'
                    processedMWEs.append(w.getLemmaString())
        wordCount = Counter(importWordCorpus.split())
        res = dict()
        for k in sorted(wordCount):
            if wordCount[k] >= configuration['others']['importantWordThShold']:
                res[k] = wordCount[k]
        return res

    def readDataSets(self, langName):
        datasetConf, pathConf, self.devDataSet = configuration['dataset'], configuration['path'], []
        sharedtaskVersion = '.2' if datasetConf['sharedtask2'] else ''
        path = os.path.join(pathConf['projectPath'], pathConf['corpusFolder'] + sharedtaskVersion, langName)
        if sharedtaskVersion:
            configuration['others']['replaceNumbers'] = False
            self.trainDataSet = readCuptFile(os.path.join(path, 'train.cupt'))
            devFile = os.path.join(path, 'dev.cupt')
            if os.path.exists(devFile):
                self.devDataSet = readCuptFile(devFile)
            else:
                self.devDataSet = []
                self.devDepGraphs = []
            self.testDataSet = readCuptFile(os.path.join(path, 'test.cupt'))
        elif datasetConf['ftb']:
            configuration['others']['replaceNumbers'] = True
            path = os.path.join(pathConf['projectPath'], 'ressources/FTB')
            self.trainDataSet = readFTB(os.path.join(path, 'train.cupt'))
            self.devDataSet = readFTB(os.path.join(path, 'dev.cupt'))
            self.testDataSet = readFTB(os.path.join(path, 'test.cupt'))
            self.deleteNumericalExpressions()
            self.deleteFtbMWT()
        elif datasetConf['dimsum']:
            configuration['others']['replaceNumbers'] = True
            path = os.path.join(pathConf['projectPath'], 'ressources/dimsum')
            if configuration['others']['dimsumAsCupt']:
                self.trainDataSet = readCuptFile(os.path.join(path, 'dimsum16.train.cupt'))
                self.testDataSet = readCuptFile(os.path.join(path, 'dimsum16.test.cupt'))
            else:
                self.trainDataSet = readDiMSUM(os.path.join(path, 'dimsum16.train'))
                self.testDataSet = readDiMSUM(os.path.join(path, 'dimsum16.test'))
        else:
            mweFile, testMweFile = os.path.join(path, 'train.parsemetsv'), os.path.join(path, 'test.parsemetsv')
            conlluFile, testConllu = getTrainAndTestConlluPath(path)
            if conlluFile and testConllu:
                self.trainDataSet = readConlluFile(conlluFile)
                integrateMweFile(mweFile, self.trainDataSet)
                self.testDataSet = readConlluFile(testConllu)
                integrateMweFile(testMweFile, self.testDataSet)
            else:
                self.trainDataSet = readMWEFile(mweFile)
                self.testDataSet = readMWEFile(testMweFile)

        if configuration['tmp']['shuffleOrRedistribute']:
            if not configuration['evaluation']['corpus'] and \
                    not configuration['dataset']['ftb'] and not \
                    configuration['dataset']['dimsum']:
                self.shuffleSent(langName)
                self.distributeSent(langName)

    def printMWTstats(self):
        res = dict()
        for s in self.trainingSents:
            for v in s.vMWEs:
                if len(v.tokens) == 1:
                    if v.tokens[0].text in res:
                        res[v.tokens[0].text] += 1
                    else:
                        res[v.tokens[0].text] = 1
        for key in sorted(res.iterkeys()):
            sys.stdout.write("%s: %s\n" % (key, res[key]))

    def deleteNonRecognizableMWE(self):
        for s in self.trainingSents:
            newVmwes = [v for v in s.vMWEs if v.isRecognizable]
            if s.vMWEs != newVmwes:
                s.vMWEs = newVmwes
                for t in s.tokens:
                    newParentMWEs = []
                    for v in t.parentMWEs:
                        if v in s.vMWEs:
                            newParentMWEs.append(v)
                    if t.parentMWEs != newParentMWEs:
                        t.parentMWEs = newParentMWEs

    def deleteFtbMWT(self):
        if not configuration['dataset']['ftb'] or not configuration['others']['removeFtbMWT']:
            return
        for sent in self.trainDataSet + self.testDataSet + self.devDataSet:
            for v in sent.vMWEs:
                v.shouldBeDeleted = False
                if len(v.tokens) == 1:
                    v.shouldBeDeleted = True
            newVmwes = []
            for v in sent.vMWEs:
                if not v.shouldBeDeleted:
                    newVmwes.append(v)
                else:
                    for t in v.tokens:
                        t.parentMWEs.remove(v)
            sent.vMWEs = newVmwes
        sys.stdout.write('FTB MWTs are cleaned!\n')

    def deleteNumericalExpressions(self):
        if not configuration['dataset']['ftb'] or not configuration['tmp']['deleteNumericalExpressions']:
            return
        # percentage = self.getNumericalExpressionPercentage()
        # sys.stdout.write(doubleSep + tabs + 'Numerical expressions:\n' + tabs +
        #  'Train: {0} Test: {1}'.format(percentage[0], percentage[1]) + doubleSep)
        if configuration['others']['verbose']:
            sys.stdout.write('\tDeleting numeric expressions!\n')
        for sent in self.trainDataSet + self.testDataSet + self.devDataSet:
            for v in sent.vMWEs:
                v.shouldBeDeleted = False
                for c in v.getLemmaString():
                    if c.isdigit():
                        v.shouldBeDeleted = True
                        break
            newVmwes = []
            for v in sent.vMWEs:
                if not v.shouldBeDeleted:
                    newVmwes.append(v)
                else:
                    for t in v.tokens:
                        t.parentMWEs.remove(v)
            sent.vMWEs = newVmwes

    def getNumericalExpressionPercentage(self):
        trainDigitalExps, allTrainExpOcc, testDigiralExps, allTestExpOcc = 0, 0, 0, 0
        mweDictionary = self.getMWEDictionary()
        for mwe in mweDictionary.keys():
            allTrainExpOcc += mweDictionary[mwe]
            for c in mwe:
                if c.isdigit():
                    trainDigitalExps += mweDictionary[mwe]
                    break
        mweDictionary = self.getMWEDictionary(onTest=True)
        for mwe in mweDictionary.keys():
            allTestExpOcc += mweDictionary[mwe]
            for c in mwe:
                if c.isdigit():
                    testDigiralExps += mweDictionary[mwe]
                    break
        t = round(float(trainDigitalExps) / allTrainExpOcc, 2) if trainDigitalExps else 0
        tst = round(float(testDigiralExps) / allTestExpOcc, 2) if testDigiralExps else 0
        return t, tst

    def getNewMWEPercentage(self):
        newMWE, oldMWE, res = 0, 0, 0
        for s in self.testingSents:
            for v in s.vMWEs:
                if v.getLemmaString() not in self.mweDictionary:
                    newMWE += 1
                else:
                    oldMWE += 1
        if configuration['others']['verbose']:
            res = tabs + 'Seen MWEs : {0} ({1} %)\n'.format(oldMWE, str(int(100 * float(oldMWE) / (oldMWE + newMWE))))
            if newMWE:
                res += tabs + 'New MWEs : {0} ({1} %)'.format(newMWE, str(
                    int(100 * float(newMWE) / (oldMWE + newMWE)))) + doubleSep
        return res

    def filterImportatntSents(self):
        return [s for s in self.trainingSents if s.vMWEs]

    def analyzeTestSet(self):
        occurrenceDic, nonIdentifiedOccurrenceDic = dict(), dict()
        # testMWEDic = self.getMWEDictionary(onTest=True)
        for sent in self.testingSents:
            sentVMWEs, sentIdentifiedVMWEs = [], []
            for v in sent.vMWEs:
                sentVMWEs.append(v.getTokenPositionString())
            for v in sent.identifiedVMWEs:
                sentIdentifiedVMWEs.append(v.getTokenPositionString())
                if v.getTokenPositionString() in sentVMWEs:
                    if v.getLemmaString() in self.mweDictionary:
                        occurrence = getOccurrenceRang(self.mweDictionary[v.getLemmaString()])
                        if occurrence not in occurrenceDic:
                            occurrenceDic[occurrence] = set()
                        occurrenceDic[occurrence].add(v.getLemmaString())
                    else:
                        if 0 not in occurrenceDic:
                            occurrenceDic[0] = set()
                        occurrenceDic[0].add(v.getLemmaString())
            for v in sent.vMWEs:
                if v.getTokenPositionString() not in sentIdentifiedVMWEs:
                    if v.getLemmaString() in self.mweDictionary:
                        occurrence = getOccurrenceRang(self.mweDictionary[v.getLemmaString()])
                        if occurrence not in nonIdentifiedOccurrenceDic:
                            nonIdentifiedOccurrenceDic[occurrence] = set()
                        nonIdentifiedOccurrenceDic[occurrence].add(v.getLemmaString())
                    else:
                        if 0 not in nonIdentifiedOccurrenceDic:
                            nonIdentifiedOccurrenceDic[0] = set()
                        nonIdentifiedOccurrenceDic[0].add(v.getLemmaString())
        res = '## Correctly identified MWEs\n'
        for k in sorted(occurrenceDic.keys()):
            res += '### ' + str(k) + '\n'
            idx = 1
            for v in occurrenceDic[k]:
                res += '\t' + str(idx) + '. ' + v + '\n'
                idx += 1
        res += '\n## Non Identified MWEs\n'
        for k in nonIdentifiedOccurrenceDic:
            res += '### ' + str(k) + '\n'
            idx = 1
            for v in nonIdentifiedOccurrenceDic[k]:
                res += '\t' + str(idx) + '. ' + v + '\n'
                idx += 1
        # with open(os.path.join(configuration['path']['projectPath'], 'tmp/testAnalysis.md'), 'w') as f:
        #    f.write(res)
        res = tabs + 'Test analysis' + doubleSep
        res += tabs + 'Correctly identified MWEs' + doubleSep
        for k in occurrenceDic:
            res += tabs + str(k) + ' : ' + str(len(occurrenceDic[k])) + '\n'
        res += seperator + tabs + 'Non Identified MWEs' + doubleSep
        for k in nonIdentifiedOccurrenceDic:
            res += tabs + str(k) + ' : ' + str(len(nonIdentifiedOccurrenceDic[k])) + '\n'
        sys.stdout.write(res)

    def duplicateImportantSent(self, taux=25):
        sys.stdout.write(tabs + 'Duplication of important sentences' + doubleSep)
        sys.stdout.write(tabs + 'Important sentences before : {0}'.format(self.trainingSents) + doubleSep)
        newSents, idx = 0, []
        traitedMWEs = set()
        for sent in self.trainingSents:
            if idx != 0 and idx % 1000 == 0:
                self.mweDictionary = self.getMWEDictionary()
            for v in sent.vMWEs:
                if v.getLemmaString() in self.mweDictionary and v.getLemmaString() not in traitedMWEs \
                        and self.mweDictionary[v.getLemmaString()] < taux:
                    for v1 in sent.vMWEs:
                        traitedMWEs.add(v1.getLemmaString())
                    for i in range(0, taux - self.mweDictionary[v.getLemmaString()]):
                        newSents.append(copy.deepcopy(sent))
                    break
            idx += 1
        self.trainingSents += newSents
        sys.stdout.write(tabs + 'Important sentences after : {0}'.format(self.trainingSents) + doubleSep)
        self.mweDictionary = self.getMWEDictionary()

    def createMWEFiles(self, seed, title=''):
        if configuration['evaluation']['corpus'] or configuration['evaluation']['trainVsDev'] or configuration['tmp'][
            'outputCupt']:
            datasetConf, modelConf = configuration['dataset'], configuration['xp']
            dataset = 'ST2' if datasetConf['sharedtask2'] else \
                ('FTB' if datasetConf['ftb'] else ('DiMSUM' if datasetConf['dimsum'] else 'ST1'))

            model = 'MLP'
            for k in configuration['xp'].keys():
                if configuration['xp'][k] and type(True) == type(configuration['xp'][k]):
                    model = k.upper()
            folder = os.path.join(configuration['path']['projectPath'],
                                  configuration['path']['output'],
                                  dataset,
                                  model)
            if not os.path.exists(folder):
                os.makedirs(folder)
            import datetime
            today = datetime.date.today().strftime('%b.%d')
            division = 'debug'
            for k in configuration['evaluation']:
                if configuration['evaluation'][k]:
                    division = k.lower()
                    break
            fileHeader = (title + '.' if title else title) + (
                '.'.join(str(_) for _ in [division, model, dataset, seed, today, self.langName]))
            with open(os.path.join(folder, fileHeader + '.cupt'), 'w') as f:
                f.write(self.toConllU())
            # with open(os.path.join(folder, fileHeader + '.gold.cupt'), 'w') as f:
            #    f.write(self.toConllU(gold=True))
            # with open(os.path.join(folder, fileHeader + '.train.cupt'), 'w') as f:
            #    f.write(self.toConllU(gold=True, train=True))
            sys.stdout.write(tabs + 'Cupt files: {0}\n'.format(fileHeader) + doubleSep)

    def createMWEDict(self):
        res = ''
        for k in self.mweDictionary:
            res += k + ' :' + str(self.mweDictionary[k]) + '\n'
        with open(os.path.join(configuration['path']['projectPath'], 'tmp/dict.txt'), 'w') as f:
            f.write(res)

    def extractDictionaries(self):
        self.mweDictionary = self.getMWEDictionary()
        self.mwtDictionary = self.getMWEDictionary(mwtOnly=True)
        self.mweOccurrenceDictionary = self.getMWEDictionary(useOccurrence=True)
        self.mweContextDictionary = self.getMWEDictionary(useContext=True)
        self.mweTokenDictionary = self.getMWETokenDictionary()
        self.lemmaText = self.toLemmaText()
        self.importantFrequentWords = self.getImportantWordLexicon()

    def getDepLblsSet(self):
        depLbls = set()
        for s in self.trainingSents:
            for t in s.tokens:
                depLbls.add(t.dependencyLabel)
        return sorted(depLbls)

    def toText(self):
        res = ''
        for sent in self:
            res += sent.text + '\n'
        return res

    def toLemmaText(self):
        res = ''
        for sent in self:
            res += ' '.join([t.getLemma() for t in sent.tokens])
        return res

    def getMWEDictionary(self, mwtOnly=False, onTest=False, useOccurrence=False, useContext=False):
        mweDictionary = {}
        for sent in self.testingSents if onTest else self.trainingSents:
            for mwe in sent.vMWEs:
                if not mwe.isRecognizable:
                    continue
                if mwtOnly:
                    if len(mwe.tokens) != 1:
                        continue
                if useContext:
                    lemmaString = mwe.getContext(sent)
                elif useOccurrence:
                    lemmaString = ' '.join(t.text.lower() for t in mwe.tokens)
                else:
                    lemmaString = ' '.join(t.lemma if t.lemma else t.text for t in mwe.tokens).lower()
                if lemmaString in mweDictionary:
                    mweDictionary[lemmaString] += 1
                else:
                    mweDictionary[lemmaString] = 1
        return mweDictionary

    def getMWETokenDictionary(self):
        mweTokenDictionary = {}
        for sent in self:
            for mwe in sent.vMWEs:
                for t in mwe.tokens:
                    mweTokenDictionary[t.lemma.lower() if t.lemma else t.text.lower()] = True
        return mweTokenDictionary

    def divideCorpus(self, foldIdx, foldNum=5):
        testFoldSize = int(len(self.trainDataSet) * 0.2)
        self.testingSents = self.trainDataSet[foldIdx * testFoldSize: (foldIdx + 1) * testFoldSize]
        if foldIdx == 0:
            self.trainingSents = self.trainDataSet[(foldIdx + 1) * testFoldSize:]
        elif foldIdx == foldNum - 1:
            self.trainingSents = self.trainDataSet[:foldIdx * testFoldSize]
        else:
            self.trainingSents = itertools.chain(self.trainDataSet[0:foldIdx * testFoldSize],
                                                 self.trainDataSet[(foldIdx + 1) * testFoldSize:])

    def getGoldenMWEFile(self):
        res = ''
        for sent in self.testingSents:
            idx = 1
            for token in sent.tokens:
                tokenLbl = ''
                if token.parentMWEs:
                    for parent in token.parentMWEs:
                        if tokenLbl:
                            tokenLbl += ';' + str(parent.id)
                        else:
                            tokenLbl += str(parent.id)
                        if token.getLemma() == parent.tokens[0].getLemma() and parent.type:
                            tokenLbl += ':' + parent.type
                if tokenLbl == '':
                    tokenLbl = '_'
                res += '{0}\t{1}\t{2}\t{3}\n'.format(idx, token.text.strip(), '_', tokenLbl)
                idx += 1
            res += '\n'
        return res

    def getMWEDictionaryWithWindows(self):
        mweDictionary = {}
        for sent in self:
            for mwe in sent.vMWEs:
                windows = ''
                for i in range(len(mwe.tokens)):
                    if i > 0:
                        distance = str(sent.tokens.index(mwe.tokens[i]) - sent.tokens.index(mwe.tokens[i - 1]))
                        if windows:
                            windows += ';' + distance
                        else:
                            windows = distance
                lemmaString = mwe.getLemmaString()
                if lemmaString in mweDictionary and mweDictionary[lemmaString] != windows:
                    oldWindow = mweDictionary[lemmaString]
                    oldWindowDistances = oldWindow.split(';')
                    newWindowDistances = windows.split(';')
                    newWindows = ''
                    if len(oldWindowDistances) == len(newWindowDistances):
                        for i in range(len(oldWindowDistances)):
                            if oldWindowDistances[i] > newWindowDistances[i]:
                                newWindows += oldWindowDistances[i] + (';' if i < (len(oldWindowDistances) - 1) else '')
                            else:
                                newWindows += newWindowDistances[i] + (';' if i < (len(newWindowDistances) - 1) else '')
                    mweDictionary[lemmaString] = newWindows
                else:
                    mweDictionary[lemmaString] = windows
        return mweDictionary

    def getTrainAndTest(self):
        self.trainingSents, self.testingSents = [], []
        if configuration['evaluation']['fixedSize']:
            tokenNum = 0
            for sent in self.trainDataSet:
                self.trainingSents.append(sent)
                tokenNum += len(sent.tokens)
                if tokenNum >= configuration['others']['tokenAvg']:
                    break
            if self.devDataSet:
                self.testingSents = self.devDataSet
            else:
                tokenNum = 0
                for sent in reversed(self.trainDataSet):
                    self.testingSents.append(sent)
                    tokenNum += len(sent.tokens)
                    if tokenNum >= configuration['others']['testTokenAvg']:
                        break
        elif configuration['evaluation']['dev']:
            if (configuration['dataset']['sharedtask2'] or configuration['dataset']['ftb']) and self.devDataSet:
                self.trainingSents = self.trainDataSet
                self.testingSents = self.devDataSet
            else:
                pointer = int(len(self.trainDataSet) * (1 - configuration['others']['test']))
                self.trainingSents = self.trainDataSet[:pointer]
                self.testingSents = self.trainDataSet[pointer:]
        elif configuration['evaluation']['corpus']:
            self.trainingSents = self.trainDataSet + self.devDataSet
            self.testingSents = self.testDataSet
        elif configuration['evaluation']['trainVsTest']:
            self.trainingSents = self.trainDataSet
            self.testingSents = self.testDataSet
        elif configuration['evaluation']['trainVsDev']:
            if self.devDataSet:
                self.trainingSents = self.trainDataSet
                self.testingSents = self.devDataSet
            else:
                trainPointer = int(len(self.trainDataSet) * 0.8)
                self.trainingSents = self.trainDataSet[:trainPointer]
                self.testingSents = self.trainDataSet[trainPointer:]
        else:
            debugTrainNum, idx, self.trainingSents = configuration['others']['debugTrainNum'], 0, []
            for s in self.trainDataSet:
                if s.vMWEs and idx < debugTrainNum:
                    self.trainingSents.append(s)
                    idx += 1
                if idx == debugTrainNum:
                    break
            if configuration['others']['debugOnDev']:
                self.testingSents = self.devDataSet if self.devDataSet else self.trainDataSet[-100:]
            else:
                self.testingSents = self.trainingSents
        if configuration['dataset']['dimsum'] and configuration['evaluation']['corpus'] and \
                configuration['tmp']['onGroup']:
            self.testingSents = []
            for s in self.testDataSet:
                if s.group != '' and s.group.startswith(configuration['tmp']['group']):
                    self.testingSents.append(s)
                elif s.group == '':
                    pass
        self.allTrainingSents = self.trainingSents
        if configuration['sampling']['importantSentences'] or configuration['sampling']['importantTransitions']:
            self.trainingSents = self.filterImportatntSents()

        self.trainDepGraphs, self.testDepGraphs = [], []
        if configuration['dataset']['sharedtask2'] and configuration['tmp']['createDepGraphs']:
            for s in self.allTrainingSents:
                self.trainDepGraphs.append(createDepGraph(s))
            for s in self.testingSents:
                self.testDepGraphs.append(createDepGraph(s))
        self.trainDataSetDepGraphs, self.testDataSetDepGraphs = [], []
        if configuration['dataset']['sharedtask2'] and configuration['tmp']['createDepGraphs']:
            for s in self.trainDataSet:
                self.trainDataSetDepGraphs.append(createDepGraph(s))
            for s in self.testingSents:
                self.testDataSetDepGraphs.append(createDepGraph(s))

    def distributeSent(self, lang):
        if configuration['others']['shuffleTrain']:
            return
        idxDic = loadObj(lang + 'idxDic')
        newTrainingSentSet = []
        for key in idxDic.keys():
            newTrainingSentSet.append(self.trainDataSet[idxDic[key]])
        self.trainDataSet = newTrainingSentSet

    def shuffleSent(self, lang):
        datasetFolder = 'sharedtask.2' if configuration['dataset']['sharedtask2'] else 'sharedtask'
        if configuration['dataset']['ftb']:
            datasetFolder = 'FTB'
        idxPath = os.path.join(configuration['path']['projectPath'], 'ressources/LangDist/' + datasetFolder,
                               lang + 'idxDic.pkl')
        if configuration['others']['shuffleTrain'] or not os.path.lexists(idxPath):
            sys.stdout.write(tabs + 'train data set has been shuffled\n' + doubleSep)
            idxDic = dict()
            idxList = range(len(self.trainDataSet))
            random.shuffle(idxList)
            for i in range(len(self.trainDataSet)):
                idxDic[i] = idxList[i]
            newTrainingSentSet = []
            for key in idxDic.keys():
                newTrainingSentSet.append(self.trainDataSet[idxDic[key]])
            self.trainDataSet = newTrainingSentSet
            saveObj(idxDic, lang + 'idxDic')

    def analyzeSents(self):
        for sent in self.trainDataSet + self.devDataSet + self.testDataSet:
            sent.recognizeEmbedded()
            sent.recognizeInterleaving()
            sent.recognizeAlternating()
            sent.setTokenParent()
            sent.recognizeAttached()
            sent.recognizeNested()
            sent.recognizeContinuous()

    def orderParentVMWEs(self):
        """
            Sorting parents to get the direct parent on the top of parentVMWEs list
        """
        for sent in self.trainDataSet:
            if sent.vMWEs and sent.containsEmbedding:
                for token in sent.tokens:
                    if token.parentMWEs and len(token.parentMWEs) > 1:
                        token.parentMWEs = sorted(token.parentMWEs, key=lambda mwe: (len(mwe)))

    def getVMWEReport(self):
        embeddedNum, leftEmbeddedNum, rightEmbeddedNum, middleEmbeddedNum = 0, 0, 0, 0
        nonRecognizableNum, distributedEmbeddedNum, interleavingNum = 0, 0, 0
        # interleavingReport, embeddingReport = '', ''
        wNum, wLens, mwtNum = 0, 0, 0
        for sent in self.trainDataSet:
            if sent.vMWEs:
                wNum += len(sent.vMWEs)
                for w in sent.vMWEs:
                    if len(w.tokens) == 1:
                        mwtNum += 1
                    wLens += len(w.tokens)
        wlen = float(wLens) / wNum
        density = float(wNum) / len(self.trainDataSet)
        for sent in self.trainDataSet:
            if len(sent.vMWEs) > 1:
                for vmwe in sent.vMWEs:
                    nonRecognizableNum += 1 if not vmwe.isRecognizable else 0
                    # interleavingReport += str(sent) if vmwe.isInterleaving else ''
                    interleavingNum += 1 if vmwe.isInterleaving else 0
                    # embeddingReport += str(sent) if vmwe.isEmbedded else ''
                    embeddedNum += 1 if vmwe.isEmbedded else 0
                    distributedEmbeddedNum += 1 if vmwe.isEmbedded and not vmwe.isRecognizable else 0
                    leftEmbeddedNum += 1 if vmwe.isLeftEmbedded else 0
                    rightEmbeddedNum += 1 if vmwe.isRightEmbedded else 0
                    middleEmbeddedNum += 1 if vmwe.isMiddleEmbedded else 0
        res = '{0},{1},{2},{3},{4},{5},{6},{7},{8},{9},{10},{11},{12}'.format(self.langName, len(self.trainDataSet), wNum, density, mwtNum, wlen, nonRecognizableNum,
                                                               interleavingNum,
                                                               embeddedNum, distributedEmbeddedNum, leftEmbeddedNum,
                                                               rightEmbeddedNum, middleEmbeddedNum)
        print '==',  res
        return res

    def getRangs(self):
        ss = self.trainDataSet
        testNum = int(len(ss) * 0.2)
        testRanges = [[0, testNum], [testNum, 2 * testNum], [2 * testNum, 3 * testNum], [3 * testNum, 4 * testNum],
                      [4 * testNum, len(ss)]]

        trainRanges = [[testNum, len(ss)], [0, testNum, 2 * testNum, len(ss)],
                       [0, 2 * testNum, 3 * testNum, len(ss)], [0, 3 * testNum, 4 * testNum, len(ss)],
                       [0, 4 * testNum]]

        return testRanges, trainRanges

    def __str__(self):
        res = ''
        for sent in self.testingSents:
            tokenList = []
            for token in sent.tokens:
                tokenList.append(token.text.strip())
            labels = ['_'] * len(tokenList)
            for mwe in sent.identifiedVMWEs:
                for token in mwe.tokens:
                    if labels[token.position - 1] == '_':
                        labels[token.position - 1] = str(mwe.id)
                    else:
                        labels[token.position - 1] += ';' + str(mwe.id)
                    if mwe.tokens[0] == token and mwe.type:
                        labels[token.position - 1] += ':' + mwe.type

            for i in range(len(tokenList)):
                res += '{0}\t{1}\t{2}\t{3}\n'.format(i + 1, tokenList[i], '_', labels[i])
            res += '\n'
        return res

    def __iter__(self):
        for sent in self.trainingSents:
            yield sent

    def toConllU(self, useCupt=True, gold=False, train=False):
        header = '# global.columns = ID FORM LEMMA UPOS XPOS FEATS HEAD DEPREL DEPS MISC PARSEME:MWE\n'
        return header + ''.join(
            s.toConllU(useCupt=useCupt, gold=gold) for s in (self.trainingSents if train else self.testingSents))

    def toDiMSUM(self, train=False):
        return ''.join(
            s.toDiMSUM() for s in (self.trainingSents if train else self.testingSents))

    def getTransDistribution(self):
        transNum = {}
        for sent in self:
            if sent.vMWEs:
                transition = sent.initialTransition
                while not transition.isTerminal():
                    if transition.isImportant():
                        if transition.type not in transNum:
                            transNum[transition.type] = 1
                        else:
                            transNum[transition.type] += 1
                    transition = transition.next
            pass

        sys.stdout.write(str(transNum.values()) + '\n')
        for t in transNum:
            sys.stdout.write(str(t) + ' : ' + str(round((transNum[t] / float(sum(transNum.values()))) * 100, 2)) + '\n')


class Sentence:
    """
       Encapsulate all the information of a sentence
    """

    def __init__(self, idx, sentid=''):

        self.sentid = sentid
        self.id = idx
        self.text = ''
        self.group = ''
        self.tokens = []
        self.vMWEs = []
        self.identifiedVMWEs = []
        self.initialTransition = None
        self.containsEmbedding = False
        self.containsInterleaving = False
        self.containsDistributedEmbedding = False

    def getWMWEIds(self):
        result = []
        for vMWE in self.vMWEs:
            result.append(vMWE.getId())
        return result

    def getVMWE(self, idx):

        for vMWE in self.vMWEs:
            if vMWE.getId() == int(idx):
                return vMWE
        return None

    def setTextandPOS(self):

        tokensTextList = []
        for token in self.tokens:
            self.text += token.text + ' '
            tokensTextList.append(token.text)
        self.text = self.text.strip()

    def recognizeNested(self):
        for vMwe1 in self.vMWEs:
            for vMwe2 in self.vMWEs:
                if vMwe1 is not vMwe2 and vMwe1.isNestedExp(vMwe2):
                    vMwe1.isNested = True

    def recognizeAttached(self):
        for vMwe1 in self.vMWEs:
            for vMwe2 in self.vMWEs:
                if vMwe1 is not vMwe2 and vMwe1.isAttachedWith(vMwe2):
                    vMwe1.isAttached = True

    def recognizeContinuous(self):
        for mwe in self.vMWEs:
            mwe.isContinuousMWE()

    def recognizeEmbedded(self, annotated=True):
        mwes = self.vMWEs if annotated else self.identifiedVMWEs
        for vMwe1 in mwes:
            if vMwe1.isEmbedded:
                continue
            for vMwe2 in mwes:
                if vMwe1 is not vMwe2 and vMwe1.getTokenPositionString() == vMwe2.getTokenPositionString():
                    vMwe1.isRecognizable = False
                    vMwe1.isBadAnnotated = True
                if vMwe1 is not vMwe2 and len(vMwe1) < len(vMwe2):
                    isEmbedded = True
                    vMwe2Lemma = vMwe2.getTokenPositionString()
                    for token in vMwe1.tokens:
                        if token.getPositionString() not in vMwe2Lemma:
                            isEmbedded = False
                            break
                    if isEmbedded:
                        self.containsEmbedding = True
                        vMwe1.isEmbedded = True
                        vMwe2.isEmbedder = True
                        vMwe1.parent = vMwe2
                        vMwe2.child = vMwe1
                        if vMwe2.getTokenPositionString().startswith(vMwe1.getTokenPositionString()):
                            vMwe1.isLeftEmbedded = True
                            vMwe2.isLeftEmbedder = True
                        elif vMwe2.getTokenPositionString().endswith(vMwe1.getTokenPositionString()):
                            vMwe1.isRightEmbedded = True
                            vMwe2.isRightEmbedder = True
                        elif vMwe1.getTokenPositionString() in vMwe2.getTokenPositionString():
                            vMwe1.isMiddleEmbedded = True
                            vMwe2.isMiddleEmbedder = True
                        else:
                            vMwe1.isRecognizable = False

    def recognizeInterleaving(self):
        # @TODO: mainpulatr triple interleaving: Example CS
        # '25356- :: prakticky všechno 2:3:1 **se** 2 **zdá** na burze 3:1 **obracet** 1 **k** 1 **lepšímu** .'
        # 'MWEs:'
        # '1- ID: se obracet k dobrý (+):Embedder'
        # '2- IReflV: se zdát (-):Interleaving'
        # '3- IReflV: se obracet (+):Left Embedded'
        processedVMWEs = []
        for vmwe1 in self.vMWEs:
            if vmwe1 not in processedVMWEs:
                for vmwe2 in self.vMWEs:
                    if vmwe1 is not vmwe2:
                        firstCondition, secondCondition = False, False
                        master = vmwe1 if len(vmwe1) > len(vmwe2) else vmwe2
                        slave = vmwe1 if len(vmwe1) <= len(vmwe2) else vmwe2
                        for token in slave.tokens:
                            if master in token.parentMWEs:
                                firstCondition = True
                            else:
                                secondCondition = True
                        if firstCondition and secondCondition:
                            self.containsInterleaving = True
                            processedVMWEs.extend([slave, master])  # master,
                            master.isInterleaver = True
                            slave.isInterleaving = True
                            slave.isRecognizable = False

    def recognizeAlternating(self):
        processedVMWEs = []
        for vmwe1 in self.vMWEs:
            if vmwe1 not in processedVMWEs:
                for vmwe2 in self.vMWEs:
                    if vmwe1 is vmwe2:
                        continue
                    firstCondition = True
                    for token in vmwe1.tokens:
                        if token.getPositionString() in vmwe2.getTokenPositionString():
                            firstCondition = False
                    if firstCondition:
                        start = vmwe1.tokens[0].position
                        end = vmwe1.tokens[-1].position
                        secondCondition = False
                        for token in vmwe2.tokens:
                            if end > token.position > start:
                                secondCondition = True
                        if secondCondition:
                            orderedList = []
                            for token in vmwe1.tokens:
                                positionStr = '0' + str(token.position) if token.position < 10 else str(token.position)
                                orderedList.append(positionStr + '-1')
                            for token in vmwe2.tokens:
                                positionStr = '0' + str(token.position) if token.position < 10 else str(token.position)
                                orderedList.append(positionStr + '-2')
                            orderedList = sorted(orderedList)
                            condA, condB = False, False
                            for i in range(len(orderedList)):
                                if orderedList[i].endswith('-2') and 0 < i < len(orderedList) - 1:
                                    if orderedList[i - 1].endswith('-1') and orderedList[i + 1].endswith('-1'):
                                        condB = True
                            if condB:
                                vmwe2.isRecognizable = False
                                vmwe2.isAletrnating = True
                                processedVMWEs.extend([vmwe1, vmwe2])

    def getDirectParents(self):
        for token in self.tokens:
            token.getDirectParent()

    def getInterleavingVMWEs(self):
        res = []
        for mwe in self.vMWEs:
            if mwe.isInterleaving:
                res.append(mwe)
        return res

    def getEmbeddedVMWEs(self):
        res = []
        for mwe in self.vMWEs:
            if mwe.isEmbedded:
                res.append(mwe)
        return res

    def getLeftEmbeddedVMWEs(self):
        res = []
        for mwe in self.vMWEs:
            if mwe.isLeftEmbedded:
                res.append(mwe)
        return res

    def getRecognizableVMWEs(self):
        res = []
        for mwe in self.vMWEs:
            if mwe.isRecognizable:
                res.append(mwe)
        return res

    def setTokenParent(self):
        for token in self.tokens:
            if token.parentMWEs:
                parents = filterNonRecognizableVMWEs(list(token.parentMWEs))
                if parents:
                    parents = sorted(parents, key=lambda parent: (len(parent)))
                    token.parent = parents
                else:
                    token.parent = None
            else:
                token.parent = None

    def isProjective(self):
        # TODO
        pass

    def toConllU(self, useCupt=True, gold=False):
        labels = ['*'] * len(self.tokens)
        for mwe in self.vMWEs if gold else self.identifiedVMWEs:
            for token in mwe.tokens:
                if labels[token.position - 1] == '*':
                    labels[token.position - 1] = str(mwe.id)
                else:
                    labels[token.position - 1] += ';' + str(mwe.id)
                if mwe.tokens[0] == token and mwe.type:
                    labels[token.position - 1] += ':' + (mwe.type2.upper() if gold and mwe.type2 else 'VID')
        return ''.join(t.toConllU(labels[i], useCupt=useCupt) for i, t in enumerate(self.tokens)) + '\n'

    def toDiMSUM(self):
        labels = ['O'] * len(self.tokens)
        parents = [0] * len(self.tokens)
        for mwe in self.identifiedVMWEs:
            if not mwe.isContinuousMWE():
                idxs = []
                for token in mwe.tokens:
                    idxs.append(token.position)
                for i in xrange(min(idxs) - 1, max(idxs)):
                    if self.tokens[i] not in mwe.tokens:
                        labels[i] = 'o'
            for token in mwe.tokens:
                if labels[token.position - 1] == 'O' and token == mwe.tokens[0]:
                    labels[token.position - 1] = 'B'
                else:
                    labels[token.position - 1] = 'I'
                    parents[token.position - 1] = int(mwe.tokens[0].position)
        return ''.join(t.toDiMSUM(labels[i], parents[i]) for i, t in enumerate(self.tokens)) + '\n'

    def __str__(self):

        vMWEText, identifiedMWE = '', ''
        if self.vMWEs:
            vMWEText += 'MWEs:\n'
            for vMWE in self.vMWEs:
                vMWEText += str(vMWE) + '\n'
        if self.identifiedVMWEs:
            identifiedMWE = ' Identified MWEs: \n'
            for mwe in self.identifiedVMWEs:
                identifiedMWE += str(mwe) + '\n'

        transStr = ''
        trans = self.initialTransition
        while trans:
            transStr += str(trans)
            trans = trans.next
        if self.vMWEs:
            text = ''
            for token in self.tokens:
                if token.parentMWEs is not None and len(token.parentMWEs) > 0:
                    idxs = ''
                    for vmwe in token.parentMWEs:
                        idxs += ':' + str(vmwe.id) if idxs else str(vmwe.id)
                    text += idxs + ' **' + token.text + '**' + ' '
                else:
                    text += token.text + ' '
        else:
            text = self.text
        return '{0}- {1}:: {2}\n{3}{4}{5}'.format(self.id, self.sentid, text, vMWEText, identifiedMWE, transStr)

    def __iter__(self):
        for vmwe in self.vMWEs:
            yield vmwe


class VMWE:
    """
        A class used to encapsulate the information of a verbal multi-word expression
    """

    def __init__(self, idx, tokens=None, type='', isEmbedded=False, isEmbedder=False, isLeftEmbedded=False,
                 isLeftEmbedder=False, isRightEmbedded=False, isRightEmbedder=False, isInterleaving=False,
                 isContinous=False, isRecognizable=True, isMiddleEmbedded=False, isMiddleEmbedder=False, isNested=False,
                 isAttached=False, parent=None, type2=''):
        self.id = int(idx)
        self.tokens = tokens if tokens else []
        self.type = type
        self.type2 = type2
        self.isNested = isNested
        self.isAttached = isAttached
        self.isEmbedded = isEmbedded
        self.isEmbedder = isEmbedder
        self.isLeftEmbedded = isLeftEmbedded
        self.isRightEmbedded = isRightEmbedded
        self.isLeftEmbedder = isLeftEmbedder
        self.isRightEmbedder = isRightEmbedder
        self.isMiddleEmbedded = isMiddleEmbedded
        self.isMiddleEmbedder = isMiddleEmbedder
        self.isInterleaving = isInterleaving
        self.isContinous = isContinous
        self.directParent = None
        self.parent = parent
        self.parsedByOracle = False
        self.isInterleaver = False
        self.isBadAnnotated = False
        self.isAletrnating = False
        self.isRecognizable = isRecognizable
        self.predictingModel = None

    def getId(self):
        return self.id

    def getContext(self, sent):
        minTokPosition, maxTokPosition = len(sent.tokens), 0
        for t in self.tokens:
            if t.position < minTokPosition:
                minTokPosition = t.position
            if t.position > maxTokPosition:
                maxTokPosition = t.position
        lemmaString = ''
        for t in sent.tokens:
            if minTokPosition <= t.position <= maxTokPosition:
                lemmaString += t.text.lower() + ' '
        return lemmaString[:-1]

    def isContinuousMWE(self):
        if len(self.tokens) == 1:
            return True
        idxs = []
        for token in self.tokens:
            idxs.append(token.position)
        self.isContinous = True
        for i in xrange(min(idxs), max(idxs) + 1):
            if i not in idxs:
                self.isContinous = False
        return self.isContinous

    def __str__(self):
        return '{0}- {1}: {2} {3}'.format(self.id, self.type, self.getLemmaString(), self.getCaracter())

    def getString(self):
        result = ''
        for token in self.tokens:
            result += token.text + ' '
        return result[:-1].lower()

    def getLemmaString(self):
        return ' '.join(
            t.lemma.lower() if t.lemma.lower() and t.lemma.lower() != '_' else t.text for t in self.tokens).lower()

    def getTokenOrLemmaString(self):
        useLemma = configuration['embedding']['lemma']
        if not useLemma:
            return ' '.join(t.text.lower() for t in self.tokens)
            # for token in self.tokens:
            #    result += token.text.lower() + ' '
            # return result[:-1].lower()
        else:
            return ' '.join(t.lemma if t.lemma and t.lemma != '_' else t.text for t in self.tokens).lower()
            # result = ''
            # for token in self.tokens:
            #     if token.lemma.lower():
            #         result += token.lemma + ' '
            #     else:
            #         result += token.text + ' '
            # return result[:-1].lower()

    def getTokenPositionString(self):
        result = '.'
        for token in self.tokens:
            result += token.getPositionString()
        return result

    def In(self, vmwes):
        for vmwe in vmwes:
            if vmwe.getString() == self.getString():
                return True
        return False

    def getCaracter(self):
        res = '(+)' if self.isRecognizable else '(-)'
        if self.isInterleaving:
            res += ':Interleaving'
        if self.isEmbedder:
            res += ':Embedder'
        if self.isEmbedded:
            if self.isLeftEmbedded:
                res += ':Left Embedded'
            elif self.isRightEmbedded:
                res += ':Right Embedded'
            elif self.isMiddleEmbedded:
                res += ':Middle Embedded'
            elif self.isEmbedded:
                res += 'Dist Embedded'
        return res

    def isNestedExp(self, parentMWE):
        if int(parentMWE.tokens[0].position) < int(self.tokens[0].position) < int(parentMWE.tokens[-1].position):
            positions = []
            for t in self.tokens:
                positions.append(t.position)
            minPos = min(positions)
            maxPos = max(positions)
            for t in parentMWE.tokens:
                if minPos <= t.position <= maxPos:
                    return False
            return True
        return False

    def isAttachedWith(self, mwe2):
        if self.tokens[-1].position + 1 == mwe2.tokens[0].position or \
                self.tokens[-1].position + 2 == mwe2.tokens[0].position:
            return True
        return False

    def __iter__(self):
        for t in self.tokens:
            yield t

    def __eq__(self, other):
        if self.getTokenPositionString() == other.getTokenPositionString():
            return True
        return False

    def __hash__(self):
        return hash(self.getTokenPositionString())

    def __len__(self):
        return len(self.tokens)

    def __contains__(self, vmwe):
        if not isinstance(vmwe, VMWE):
            raise TypeError()
        if vmwe is self or vmwe.getTokenPositionString() == self.getTokenPositionString():
            return False
        if vmwe.getTokenPositionString() in self.getTokenPositionString():
            return True
        for token in vmwe.tokens:
            if token.getPositionString() not in self.getTokenPositionString():
                return False
        return True


class Token:
    """
        a class used to encapsulate all the information of a sentence tokens
    """

    def __init__(self, position, txt, lemma='', posTag='', abstractPosTag='', morphologicalInfo=None,
                 dependencyParent=-1,
                 dependencyLabel='', line=''):
        self.position = int(position)
        self.text = txt
        self.lemma = lemma
        self.abstractPosTag = abstractPosTag
        self.posTag = posTag
        self.line = line
        self.superSense = ''
        if not morphologicalInfo:
            self.morphologicalInfo = []
        else:
            self.morphologicalInfo = morphologicalInfo
        self.dependencyParent = dependencyParent
        self.dependencyLabel = dependencyLabel
        self.predictedDepParent = None
        self.predictedDepLabel = None
        self.parentMWEs = []
        self.directParent = None
        self.parent = None

    def setParent(self, vMWE):
        self.parentMWEs.append(vMWE)

    def getLemma(self):
        if self.lemma:
            return self.lemma.strip().lower()
        return self.text.strip().lower()

    def getPositionString(self):
        if self.position < 10:
            return '0' + str(self.position) + '.'
        else:
            return str(self.position) + '.'

    def getDirectParent(self):
        if not self.parentMWEs:
            return None
        self.directParent = None
        if self.parentMWEs:
            if len(self.parentMWEs) == 1:
                self.directParent = self.parentMWEs[0]
            else:
                parents = sorted(self.parentMWEs,
                                 key=lambda mwe: (mwe.isInterleaving, mwe.isEmbedded, len(mwe)),
                                 reverse=True)
                for parent in parents:
                    if not parent.isInterleaving:
                        self.directParent = parent
                        break
        return self.directParent

    def In(self, vmwe):
        for token in vmwe.tokens:
            if token.text.lower() == self.text.lower() and token.position == self.position:
                return True
        return False

    def isMWT(self):
        if self.parentMWEs:
            for vmw in self.parentMWEs:
                if len(vmw.tokens) == 1:
                    return vmw
        return None

    def isNumber(self):
        for l in self.getTokenOrLemma():
            if l.isdigit():
                return True
        return False

    def getTokenOrLemma(self):
        if configuration['embedding']['lemma']:
            return self.lemma.lower()
        return self.text.lower()

    def getStandardKey(self, getPos=False, getToken=False):
        if getPos:
            return self.posTag.lower()
        if getToken:
            return self.getTokenOrLemma()
        return self.getTokenOrLemma() + '_' + self.posTag.lower()

    def toConllU(self, mweInfo, useCupt=True):
        return '{0}\t{1}\t{2}\t{3}\t{4}\t{5}\t{6}\t{7}\t{8}\t{9}{10}\n'.format(
            self.position,
            self.text,
            self.lemma if self.lemma else '_',
            self.abstractPosTag if self.abstractPosTag else '_',
            self.posTag if self.posTag else '_',
            self.morphologicalInfo if self.morphologicalInfo else '_',
            self.dependencyParent if self.dependencyParent else '_',
            self.dependencyLabel if self.dependencyLabel else '_',
            '_', '_',
            '\t' + mweInfo if useCupt else ''
        )

    def toDiMSUM(self, mweInfo, tokenParent):
        return '{0}\t{1}\t{2}\t{3}\t{4}\t{5}\t{6}\t{7}\t{8}\n'.format(
            self.line.split('\t')[0],
            self.line.split('\t')[1],
            self.line.split('\t')[2],
            self.line.split('\t')[3],
            mweInfo,
            tokenParent,
            self.line.split('\t')[6],
            self.line.split('\t')[7],
            self.line.split('\t')[8]
        )

    def __str__(self):
        parentTxt = ' '
        if self.parentMWEs:
            for par in self.parentMWEs:
                if parentTxt:
                    parentTxt += '; ' + str(par.id)
                else:
                    parentTxt += str(par.id)
        return str(self.position) + ' : ' + self.text + ' : ' + self.posTag + parentTxt + '\n'


def dimsumToCupt(p):
    cuptTxt, mweNum, intermediateMWE = '', 0, False
    with open(p, 'r') as f:
        for l in f:
            if l == '\n':
                mweNum, intermediateMWE, = 0, False
            if not l.startswith('#') and l != '\n':
                lParts = l.split('\t')
                mweTag = '*'
                if lParts[4] == 'B':
                    mweNum += 1
                    if intermediateMWE:
                        intermediateMWE = False
                        mweNum += 1
                    mweTag = str(mweNum) + ':oth'
                elif lParts[4] == 'b':
                    mweTag = str(mweNum + 1) + ':oth'
                    intermediateMWE = True
                elif lParts[4] == 'I':
                    mweTag = str(mweNum)
                elif lParts[4] == 'i':
                    mweTag = str(mweNum + 1)
                cuptTxt += '\t'.join(lParts[0:4] + [lParts[3]] + ['_'] * 5 + [mweTag]) + '\n'
            else:
                cuptTxt += l
    with open(p + '.cupt', 'w') as f:
        f.write(cuptTxt)


class DepenecyLabelManager():
    def __init__(self, corpus):
        depLbls = set()
        for s in corpus.trainingSents:
            for t in s.tokens:
                depLbls.add(t.dependencyLabel)
        self.depLbls = sorted(depLbls)

    def getArcIdx(self, lbl, right=True):
        if lbl in self.depLbls:
            if right:
                return self.depLbls.index(lbl)
            return len(self.depLbls) + self.depLbls.index(lbl)
        return None


def printStats(sents, title, mweDic=None, langName='', test=False):
    if not configuration['others']['verbose']:
        return
    impSents, mweNum, tokenNum, emNum, interleavingNum, mwtNum, recognizableNum, continousMweNum = 0, 0, 0, 0, 0, 0, 0, 0
    frequentMwes = sum([int(v) for v in mweDic.values() if v > 5])
    mwes = set()
    for sent in sents:
        if sent.vMWEs:
            impSents += 1
        mweNum += len(sent.vMWEs)
        tokenNum += len(sent.tokens)
        for v in sent.vMWEs:
            mwes.add(v.getLemmaString())
            emNum += 1 if v.isEmbedded else 0
            interleavingNum += 1 if v.isInterleaving else 0
            mwtNum += 1 if len(v.tokens) == 1 else 0
            recognizableNum += 1 if v.isRecognizable else 0
            continousMweNum += 1 if v.isContinous else 0

    sys.stdout.write(doubleSep)
    sys.stdout.write(tabs + langName + ' ' + title + ' ({0})'.format(len(sents)))
    sys.stdout.write(doubleSep)
    sys.stdout.write(tabs + 'Important sentence: {0}\n'.format(impSents))
    sys.stdout.write(tabs + 'Token occurrences: {0}\n'.format(tokenNum))
    sys.stdout.write(tabs + 'MWE number: {0}\n'.format(len(mwes)))
    sys.stdout.write(tabs + 'MWE occurrences: {0}\n'.format(mweNum))
    sys.stdout.write(tabs + 'Continuous occurrences: {0} %\n'.format(
        round(float(continousMweNum) / mweNum * 100, 0) if mweNum > 0 else 0))
    sys.stdout.write(tabs + 'Frequent MWE occurences: {0} %\n'.format(
        round(float(frequentMwes) / mweNum * 100, 0)) if not test and mweNum > 0 else '')
    sys.stdout.write(tabs + 'MWE length: {0}\n'.format(getMWEMeanLength(sents)))
    sys.stdout.write(tabs + 'Seen occurrences : {0}% \n'.format(getNewMWEPercentage(sents, mweDic)) if test else '')
    sys.stdout.write(tabs + 'Recognizable MWEs: {0} %\n'.format(round(float(recognizableNum) / mweNum * 100, 0)))
    sys.stdout.write(tabs + 'MWT occurrences: {0}\n'.format(mwtNum) if mwtNum else '')
    sys.stdout.write(tabs + 'Embedded occurrences: {0}\n'.format(emNum) if emNum else '')
    sys.stdout.write(tabs + 'Interleaving occurrences: {0}\n'.format(interleavingNum) if interleavingNum else '')
    sys.stdout.write(doubleSep if test else '')


def getNewMWEPercentage(sents, mweDic):
    newMWE, oldMWE, res = 0, 0, 0
    for s in sents:
        for v in s.vMWEs:
            if v.getLemmaString() not in mweDic:
                newMWE += 1
            else:
                oldMWE += 1
    if configuration['others']['verbose']:
        res = tabs + 'Seen MWEs : {0} ({1} %)\n'.format(oldMWE, str(int(100 * float(oldMWE) / (oldMWE + newMWE))))
        if newMWE:
            res += tabs + 'New MWEs : {0} ({1} %)'.format(newMWE, str(
                int(100 * float(newMWE) / (oldMWE + newMWE)))) + doubleSep
    return int(100 * float(oldMWE) / (oldMWE + newMWE))


def getMWEMeanLength(sents):
    mweNum, tokenNum, res = 0, 0, ''
    for sent in sents:
        mweNum += len(sent.vMWEs)
        for v in sent.vMWEs:
            tokenNum += len(v.tokens)
    return round(float(tokenNum) / mweNum, 2)
    # if configuration['others']['verbose']:
    #     res = tabs + 'MWE length mean : {0}\n'.format(round(float(tokenNum) / mweNum, 2))
    # return res


def saveObj(obj, name):
    datasetFolder = 'sharedtask.2' if configuration['dataset']['sharedtask2'] else 'sharedtask'
    if configuration['dataset']['ftb']:
        datasetFolder = 'FTB'
    with open(os.path.join(configuration['path']['projectPath'],
                           'ressources/LangDist/' + datasetFolder, name + '.pkl'), 'wb') as f:
        pickle.dump(obj, f, pickle.HIGHEST_PROTOCOL)


def loadObj(name):
    datasetFolder = 'sharedtask.2' if configuration['dataset']['sharedtask2'] else 'sharedtask'
    if configuration['dataset']['ftb']:
        datasetFolder = 'FTB'
    with open(os.path.join(configuration['path']['projectPath'],
                           'ressources/LangDist/' + datasetFolder, name + '.pkl'), 'rb') as f:
        return pickle.load(f)


def readConlluFile(conlluFile):
    sentences = []
    with open(conlluFile, 'r') as corpusFile:
        sent, senIdx, sentId = None, 0, ''
        lineNum, missedUnTag, missedExTag = 0, 0, 0
        for line in corpusFile:
            if len(line) > 0 and line.endswith('\n'):
                line = line[:-1]
            if line.startswith('# sentid:'):
                sentId = line.split('# sentid:')[1].strip()
            elif line.startswith('# sentence-text:'):
                continue

            elif line.startswith('1\t'):
                if sentId.strip():
                    sent = Sentence(senIdx, sentid=sentId)
                else:
                    sent = Sentence(senIdx)
                senIdx += 1
                sentences.append(sent)

            if not line.startswith('#'):
                lineParts = line.split('\t')

                if len(lineParts) != 10 or '-' in lineParts[0]:
                    continue

                lineNum += 1
                if lineParts[3] == '_':
                    missedUnTag += 1
                if lineParts[4] == '_':
                    missedExTag += 1

                morpho = ''
                if lineParts[5] != '_':
                    morpho = lineParts[5].split('|')
                if lineParts[6] != '_':
                    token = Token(lineParts[0], lineParts[1], lemma=lineParts[2].lower(),
                                  abstractPosTag=lineParts[3], morphologicalInfo=morpho,
                                  dependencyParent=int(lineParts[6]),
                                  dependencyLabel=lineParts[7], line=line)
                else:
                    token = Token(lineParts[0], lineParts[1], lemma=lineParts[2].lower(),
                                  abstractPosTag=lineParts[3], morphologicalInfo=morpho,
                                  dependencyLabel=lineParts[7], line=line)
                getPosTag(token, lineParts[3], lineParts[4])
                # Associate the token with the sentence
                sent.tokens.append(token)
                sent.text += token.text + ' '
    return sentences


def getTrainAndTestConlluPath(path):
    testFiles = configuration['files']['test']
    trainFiles = configuration['files']['train']
    if os.path.isfile(
            os.path.join(path, trainFiles['depAuto'])) \
            and configuration['others']['autoData']:
        conlluFile = os.path.join(path, trainFiles['depAuto'])
        testConllu = os.path.join(path, testFiles['depAuto'])
    elif os.path.isfile(os.path.join(path, trainFiles['posAuto'])) \
            and configuration['others']['autoData']:
        conlluFile = os.path.join(path, trainFiles['posAuto'])
        testConllu = os.path.join(path, testFiles['posAuto'])
    elif os.path.isfile(os.path.join(path, trainFiles['conllu'])):
        conlluFile = os.path.join(path, trainFiles['conllu'])
        testConllu = os.path.join(path, testFiles['conllu'])
    else:
        conlluFile, testConllu = None, None
    return conlluFile, testConllu


def readMWEFile(mweFile):
    sentences = []
    with open(mweFile) as corpusFile:
        # Read the corpus file
        sent = None
        senIdx = 1
        for line in corpusFile:
            if len(line) > 0 and line.endswith('\n'):
                line = line[:-1]
            if line.startswith('1\t'):
                # sentId = line.split('# sentid:')[1]
                if sent:
                    sent.setTextandPOS()
                    sent.recognizeEmbedded()
                    sent.recognizeInterleaving()
                sent = Sentence(senIdx)
                senIdx += 1
                sentences.append(sent)

            elif line.startswith('# sentence-text:'):
                if len(line.split(':')) > 1:
                    sent.text = line.split('# sentence-text:')[1]

            lineParts = line.split('\t')

            # Empty line or lines of the form: '8-9	can't	_	_'
            if len(lineParts) != 4 or '-' in lineParts[0]:
                continue
            token = Token(lineParts[0], lineParts[1])
            # Trait the MWE
            # if not forTest and lineParts[3] != '_':
            if lineParts[3] != '_':
                vMWEids = lineParts[3].split(';')
                for vMWEid in vMWEids:
                    idx = int(vMWEid.split(':')[0])
                    # New MWE captured
                    if idx not in sent.getWMWEIds():
                        type = str(vMWEid.split(':')[1])
                        vMWE = VMWE(idx, [token], type)
                        sent.vMWEs.append(vMWE)
                    # Another token of an under-processing MWE
                    else:
                        vMWE = sent.getVMWE(idx)
                        if vMWE is not None:
                            vMWE.tokens.append(token)
                    # associate the token with the MWE
                    token.setParent(vMWE)
            # Associate the token with the sentence
            sent.tokens.append(token)
        return sentences


def integrateMweFile(mweFile, sentences):
    mweNum = 0
    with open(mweFile) as corpusFile:
        # Read the corpus file
        lines = corpusFile.readlines()
        noSentToAssign = False
        sentIdx = 0
        for line in lines:
            if line == '\n' or line.startswith('# sentence-text:') or (
                    line.startswith('# sentid:') and noSentToAssign):
                continue
            if len(line) > 0 and line.endswith('\n'):
                line = line[:-1]
            if line.startswith('1\t'):
                sent = sentences[sentIdx]
                sentIdx += 1
            lineParts = line.split('\t')
            if '-' in lineParts[0]:
                continue
            if lineParts and len(lineParts) == 4 and lineParts[3] != '_':

                token = sent.tokens[int(lineParts[0]) - 1]
                vMWEids = lineParts[3].split(';')
                for vMWEid in vMWEids:
                    idx = int(vMWEid.split(':')[0])
                    # New MWE captured
                    if idx not in sent.getWMWEIds():
                        if len(vMWEid.split(':')) > 1:
                            type = str(vMWEid.split(':')[1])
                            vMWE = VMWE(idx, [token], type)
                        else:
                            vMWE = VMWE(idx, [token])
                        mweNum += 1
                        sent.vMWEs.append(vMWE)
                    # Another token of an under-processing MWE
                    else:
                        vMWE = sent.getVMWE(idx)
                        if vMWE:
                            vMWE.tokens.append(token)
                    # associate the token with the MWE
                    token.setParent(vMWE)

    return mweNum


def getVMWESents(ss, num):
    result, idx = [], 0
    for s in ss:
        result.append(s)
        idx += 1
        if idx >= num:
            return result
    if len(result) < num:
        for s in ss:
            if s not in result:
                result.append(s)
            if len(result) >= num:
                return result
    return result[:num]


def getTokens(elemlist):
    while isinstance(elemlist, list) and len(elemlist) == 1:
        elemlist = elemlist[0]
    if not elemlist:
        return []
    if str(elemlist.__class__).endswith('Token'):
        return [elemlist]
    if isinstance(elemlist, list):
        result = []
        for elem in elemlist:
            if str(elem.__class__).endswith('Token'):
                result.append(elem)
                continue
            elif isinstance(elem, list):
                if len(elem) == 1:
                    result.extend(getTokens(elem[0]))
                else:
                    result.extend(getTokens(elem))
        return result
    return [elemlist]


def getTokenLemmas(tokens):
    text = ''
    tokens = getTokens(tokens)
    for token in tokens:
        if token.lemma != '':
            text += token.lemma + ' '
        else:
            text += token.text + ' '
    return text.strip()


def getParent(tokens):
    if hasOrphanToken(tokens):
        return None
    parent = tokens[0].parent
    for token in tokens:
        if token.parent != parent:
            return None
    return parent


def getParents(tokens, allChildren=True):
    if hasOrphanToken(tokens):
        return []
    parents = regroupParents(tokens)
    parents = filterNonRecognizableVMWEs(parents)
    if allChildren:
        parents = filterOnLength(parents, len(tokens))
    parents = filterPartialParents(parents, tokens)
    parents = sorted(parents, key=lambda parent: (len(parent)))
    return parents


def filterPartialParents(parents, childs):
    for parent in list(parents):
        for child in childs:
            if parent not in child.parentMWEs:
                if parent in parents:
                    parents.remove(parent)
    return parents


def filterOnLength(mwes, length):
    for mwe in list(mwes):
        if len(mwe) != length:
            mwes.remove(mwe)
    return mwes


def filterNonRecognizableVMWEs(mwes):
    for mwe in list(mwes):
        if not mwe.isRecognizable:
            mwes.remove(mwe)
    return mwes


def isOrphanToken(token):
    if token and token.parentMWEs:
        for vmwe in token.parentMWEs:
            if vmwe.isRecognizable:
                return False
        return True
    if token and (not token.parentMWEs):
        return True


def hasOrphanToken(tokens):
    # Do they have all a parent?
    for token in tokens:
        if isOrphanToken(token):
            return True
    return False


def regroupParents(tokens):
    parents = set()
    for token in tokens:
        for parent in token.parentMWEs:
            parents.add(parent)
    return list(parents)


def getVMWEByTokens(tokens):
    vmwes = regroupParents(tokens)
    vmwes = filterOnLength(vmwes, len(tokens))
    if vmwes:
        return vmwes[0]
    return None


def createDepGraph(sent):
    cuptData = '\n'.join(t.line for t in sent.tokens)
    conllData = cuptSentToConllU(cuptData)
    # print conllData
    return DependencyGraph(conllData)


def readDepGraphs(cuptFile):
    conlldata = cuptToConllU(cuptFile)
    graphs = [DependencyGraph(entry)
              for entry in conlldata.split('\n\n') if entry]
    return graphs


def readCuptFile(cuptFile, verbose=0):
    sentences = []
    deformedLemma, importantDeformedLemma, numericTokens = 0, 0, 0
    with open(cuptFile, 'r') as corpusFile:
        sent, senIdx = None, 0
        for line in corpusFile:
            if line and line.endswith('\n'):
                line = line[:-1]
            if line.startswith('#'):
                continue
            if line.startswith('1\t'):
                if sent:
                    sent.text = sent.text.strip()
                    sent.recognizeEmbedded()
                    sent.recognizeInterleaving()
                sent = Sentence(senIdx)
                sentences.append(sent)
                senIdx += 1
            lineParts = line.split('\t')
            if len(lineParts) != 11 or '-' in lineParts[0] or '.' in lineParts[0]:
                continue
            text = lineParts[1]
            importantDeformedLemma += 1 if (lineParts[2].strip() == '' or lineParts[2].lower() == '_') and lineParts[
                10] != '*' else 0
            deformedLemma += 1 if (lineParts[2].strip() == '' or lineParts[2].lower() == '_') and lineParts[
                10] == '*' else 0
            if configuration['others']['traitDeformedLemma'] \
                    and (lineParts[2].strip() == '' or lineParts[2].lower() == '_'):
                lemma = text.lower()
            else:
                lemma = lineParts[2].lower()
            if configuration['others']['replaceNumbers']:
                for c in lineParts[1]:
                    if c.isdigit():
                        text, lemma = 'number', 'number'
                        numericTokens += 1
                        break

            token = Token(lineParts[0], text, lemma=lemma,
                          # lineParts[2].lower()if lineParts[2] else lineParts[1].lower(),
                          abstractPosTag=lineParts[3] if lineParts[3] != '_' else lineParts[4],
                          dependencyParent=int(lineParts[6]) if (lineParts[6] != '_' and lineParts[6] != '-') else -1,
                          dependencyLabel=lineParts[7] if lineParts[7] != '_' else '', line=line)
            getPosTag(token, lineParts[3], lineParts[4])
            sent.tokens.append(token)
            sent.text += token.text + ' '
            if lineParts[10] != '*':
                vMWEids = lineParts[10].split(';')
                for vMWEid in vMWEids:
                    idx = int(vMWEid.split(':')[0])
                    if idx not in sent.getWMWEIds():
                        type = str(vMWEid.split(':')[1])
                        vMWE = VMWE(idx, [token], getType(type))
                        vMWE.type2 = type
                        sent.vMWEs.append(vMWE)
                    else:
                        vMWE = sent.getVMWE(idx)
                        if vMWE:
                            vMWE.tokens.append(token)
                    token.setParent(vMWE)
    if cuptFile.endswith('train.cupt') and verbose:
        sys.stdout.write(tabs + ' Annotation issues' + doubleSep)
        sys.stdout.write((tabs + 'Train deformed lemmas: %d \n' % (deformedLemma)) if deformedLemma else '')
        sys.stdout.write((tabs + 'Train numeric tokens: %d \n' % (numericTokens)) if numericTokens else '')
        sys.stdout.write((tabs + 'Train important deformed Lemmas: %d \n' % (
            importantDeformedLemma)) if importantDeformedLemma else '')
    return sentences


def getType(type):
    type = type.lower()
    if type.startswith('lvc') or type == 'mvc':
        return 'lvc'
    if type.startswith('vpc') or type == 'iav':
        return 'vpc'
    if type == 'vid':
        return 'id'
    if type == 'irv' or type == 'ls.icv':
        return 'ireflv'


def getStats(sentences, asCSV=False):
    res = 'Sent num = {0}\n'.format(len(sentences))
    tokNum, mweNum, mwtNum, irefNum, idNum, lvcNum, vpcNum = 0, 0, 0, 0, 0, 0, 0

    for s in sentences:
        mweNum += len(s.vMWEs)
        tokNum += len(s.tokens)
        for v in s.vMWEs:
            mwtNum += 1 if len(v.tokens) == 1 else 0
            if v.type:
                if v.type.lower() == 'lvc':
                    lvcNum += 1
                if v.type.lower() == 'ireflv':
                    irefNum += 1
                if v.type.lower() == 'id':
                    idNum += 1
                if v.type.lower() == 'vpc':
                    vpcNum += 1
    if asCSV:
        res = ''
        for stat in [len(sentences), tokNum, mweNum, mwtNum, irefNum, lvcNum, idNum, vpcNum]:
            res += str(stat) + ','
        res = res[:-1]
    else:
        res += 'Tokens: {0}\n'.format(tokNum)
        res += 'Total VMWEs: {0}\n'.format(mweNum)
        res += 'Total MWTs: {0}\n'.format(mwtNum)
        res += 'Ireflv: {0}\n'.format(irefNum)
        res += 'lvc: {0}\n'.format(lvcNum)
        res += 'id: {0}\n'.format(idNum)
        res += 'vpc: {0}\n'.format(vpcNum)
    return res


def readFTB(ftbFile, verbose=False, stats=False):
    configuration['others']['replaceNumbers'] = True
    sentences, nonValidLines, shouldPrint = [], 0, False
    with open(ftbFile, 'r') as corpusFile:
        sent, senIdx, mweIdx, lineNum = None, 0, 1, 0
        for line in corpusFile:
            lineNum += 1
            if line and line.endswith('\n'):
                line = line[:-1]
            if not line or line.startswith('#'):
                continue
            if line.startswith('1\t'):
                if sent:
                    sent.text = sent.text.strip()
                    if verbose:
                        if shouldPrint:
                            sys.stdout.write(str(sent) + '\n')
                            for t in sent.tokens:
                                sys.stdout.write(t.line)
                        for v in sent.vMWEs:
                            if len(v.tokens) == 1:
                                sys.stdout.write('FTB MWT {0}\n'.format(lineNum))
                                sys.stdout.write(str(sent))
                                break
                sent = Sentence(senIdx)
                sentences.append(sent)
                mweIdx = 1
                senIdx += 1
                shouldPrint = False
            lineParts = line.split('\t')
            if len(lineParts) != 10 or '-' in lineParts[0] or '.' in lineParts[0]:
                nonValidLines += 1
                print('FTB annotation error:%d %s' % (lineNum, line))
                continue
            text, lemma = lineParts[1], lineParts[2].lower()
            if configuration['others']['replaceNumbers']:
                for c in lineParts[1]:
                    if c.isdigit():
                        text, lemma = 'number', 'number'
            token = Token(lineParts[0], text, lemma=lemma,
                          abstractPosTag=lineParts[3] if lineParts[3] != '_' else lineParts[4],
                          dependencyParent=int(lineParts[6]) if (lineParts[6] != '_' and lineParts[6] != '-') else -1,
                          dependencyLabel=lineParts[7] if lineParts[7] != '_' else '',
                          line=line)
            getPosTag(token, lineParts[3], lineParts[4])
            sent.tokens.append(token)
            sent.text += token.text + ' '
            morpho = getMorphological(lineParts[5].lower())
            if 'mwehead' in morpho:
                vMWE = VMWE(mweIdx, [token], 'oth')
                vMWE.type2 = morpho['mwehead']
                sent.vMWEs.append(vMWE)
                token.setParent(vMWE)
                mweIdx += 1
            elif lineParts[7] == 'dep_cpd':
                if sent.vMWEs and token.dependencyParent == sent.vMWEs[-1].tokens[0].position:
                    sent.vMWEs[-1].tokens.append(token)
                    token.setParent(sent.vMWEs[-1])
                else:
                    if verbose:
                        sys.stdout.write('Annotation bug dep_cpd without dep parent: line: {0}, word:'
                                         ' {1} DependencyParent: {2}, head Position: {3} \n'.
                                         format(lineNum, lineParts[1], token.dependencyParent,
                                                sent.vMWEs[-1].tokens[0].position if sent.vMWEs else ''))
                        shouldPrint = True  # sent
                    if sent.vMWEs:
                        sent.vMWEs = sent.vMWEs[:-1]
                        # else:
                        #    if lineParts[7] == 'dep_cpd' and 'mwehead' in morpho:
                        #        bugNum += 1
                        # else:
                        #   sys.stdout.write(' Annotation error {0} : {1}'.format(lineNum, sent))
                        # assert not sent.vMWEs, ' Annotation error {0} : {1}'.format(lineNum, sent)
    tNum, mNum, mwtNum, biNum, triNum, otherNum = 0, 0, 0, 0, 0, 0
    for s in sentences:
        tNum += len(s.tokens)
        mNum += len(s.vMWEs)
        for v in s.vMWEs:
            if len(v.tokens) == 1:
                mwtNum += 1
            elif len(v.tokens) == 2:
                biNum += 1
            elif len(v.tokens) == 3:
                triNum += 1
            else:
                otherNum += 1
    return sentences


def getMorphological(morphoStr):
    if morphoStr == '_':
        return {}
    result = dict()
    morphAttribs = morphoStr.split('|')
    for attib in morphAttribs:
        attribComposants = attib.split('=')
        # sys.stdout.write('Morpho annotation error : {0}'.format(morphoStr))
        # assert len(attribComposants) <= 1, 'Morpho annotation error : {0}'.format(morphoStr)
        if len(attribComposants) > 1:
            result[attribComposants[0]] = attribComposants[1]
    return result


def getOccurrenceRang(occ):
    occurrenceRang = [5, 25, 50, 100, 200, 300, 500]
    for i in reversed(occurrenceRang):
        if occ >= i:
            return i
    return 0


# universalPosTags = set()
# xposTags = set()

def getPosTag(token, lineParts3, lineParts4):
    # universalPosTags.add(lineParts3.lower())
    # xposTags.add(lineParts4.lower())
    useUniversalPOS = configuration['others']['universalPOS']
    if useUniversalPOS:
        token.posTag = lineParts3
    else:
        if lineParts4 != '_':
            token.posTag = lineParts4
        else:
            token.posTag = lineParts3


def readDiMSUM(dimsumFile, verbose=True):
    configuration['others']['replaceNumbers'] = True
    sentences = []
    BMWEs, bMWEs = [], []
    with open(dimsumFile, 'r') as corpusFile:
        sent, senIdx, mweIdx, lineNum = None, 0, 1, 0
        for line in corpusFile:
            lineNum += 1
            if line and line.endswith('\n'):
                line = line[:-1]
            if not line or line.startswith('#'):
                continue
            if line.startswith('1\t'):
                if sent:
                    sent.text = ' '.join([t.text.lower() for t in sent.tokens])
                    sent.group = sent.tokens[0].line.split('\t')[-1].lower()
                    BMWEs, bMWEs = [], []
                sent = Sentence(senIdx)
                sentences.append(sent)
                mweIdx = 1
                senIdx += 1
            lineParts = line.split('\t')
            if len(lineParts) != 9 and verbose:
                print('DiMSUM annotation error:%d %s' % (lineNum, line))
                continue
            text, lemma = lineParts[1], lineParts[2].lower()
            if configuration['others']['replaceNumbers']:
                for c in lineParts[1]:
                    if c.isdigit():
                        text, lemma = 'number', 'number'
            token = Token(lineParts[0], text, lemma=lemma, abstractPosTag=lineParts[3], posTag=lineParts[3], line=line)
            token.superSense = lineParts[7].lower()
            sent.tokens.append(token)
            if lineParts[4].lower() == 'b':
                vMWE = VMWE(mweIdx, [token], 'oth')
                sent.vMWEs.append(vMWE)
                token.setParent(vMWE)
                if lineParts[4] == 'B':
                    BMWEs.append(vMWE)
                else:
                    bMWEs.append(vMWE)
                mweIdx += 1
            elif lineParts[4].lower() == 'i':
                parentMWE = BMWEs[-1] if BMWEs and lineParts[4] == 'I' else (bMWEs[-1] if bMWEs else None)
                if parentMWE:
                    parentMWE.tokens.append(token)
                    token.setParent(parentMWE)
                elif verbose:
                    sys.stdout.write('Annotation bug : line: {0}, word:'
                                     ' {1} DependencyParent: {2}, head Position: {3} \n'.
                                     format(lineNum, lineParts[1], token.dependencyParent,
                                            sent.vMWEs[-1].tokens[0].position))
    return sentences


def cuptSentToConllU(cuptTxt, withoutComments=True):
    conll = ''
    for line in cuptTxt.split('\n'):
        if line.startswith('#'):
            if withoutComments:
                continue
            else:
                conll += line
        elif line == '\n':
            conll += line
        elif not line.startswith('#') or line != '\n':
            if len(line.split('\t')[0].split('-')) == 1:
                parts = line.split('\t')[:-1]
                if ' ' in parts[1]:
                    parts[1] = parts[1].replace(' ', '-')
                if ' ' in parts[2]:
                    parts[2] = parts[2].replace(' ', '-')
                if parts[6] == '0':
                    parts[7] = 'ROOT'
                # for t in parts:
                #    conll += t + '\t'
                conll += '\t'.join(p for p in parts) + '\n'  # conll[:-1] + '\n'
                # conll += '\t'.join(t for t in line.split('\t')[:-1]) + '\n'
    return conll


def cuptToConllU(filePath, withoutComments=True):
    with open(filePath, 'r') as corpusFile:
        conll = ''
        for line in corpusFile:
            if line.startswith('#'):
                if withoutComments:
                    continue
                else:
                    conll += line
            elif line == '\n':
                conll += line
            elif not line.startswith('#') or line != '\n':
                if len(line.split('\t')[0].split('-')) == 1:
                    parts = line.split('\t')[:-1]
                    if ' ' in parts[1]:
                        parts[1] = parts[1].replace(' ', '-')
                    if ' ' in parts[2]:
                        parts[2] = parts[2].replace(' ', '-')
                    if parts[6] == '0':
                        parts[7] = 'root'
                    # for t in parts:
                    #    conll += t + '\t'
                    conll += '\t'.join(p for p in parts) + '\n'  # conll[:-1] + '\n'
                    # conll += '\t'.join(t for t in line.split('\t')[:-1]) + '\n'
    return conll


def getAllLangStats(langs):
    res = ''
    for lang in langs:
        corpus = Corpus(lang)
        res += corpus.langName + ',' + getStats(corpus.trainDataSet, asCSV=True) + ',' + \
               getStats(corpus.devDataSet, asCSV=True) + ',' + \
               getStats(corpus.testDataSet, asCSV=True) + '\n'
    return res


def getRelevantModelAndNormalizer(sent, trainingSent, models, normalizers, test=False):
    if test:
        return models[5], normalizers[5] if normalizers else None
    foldNum = int(str(float(trainingSent.index(sent) / (len(trainingSent) / 5)))[0])
    return models[foldNum], normalizers[foldNum] if normalizers else None


def getLemmaString(tokens):
    return ' '.join(
        t.lemma.lower() if t.lemma.lower() and t.lemma.lower() != '_' else t.text for t in tokens).lower()


def getFTBDictionary(corpus, path='ressources/FTB/dictionary.md'):
    dictionary = dict()
    for s in corpus.trainDataSet:
        for v in s.vMWEs:
            cat = v.type2.lower()
            lemma = v.getLemmaString()
            if cat not in dictionary:
                dictionary[cat] = {}
            if lemma not in dictionary[cat]:
                dictionary[cat][lemma] = 1
            else:
                dictionary[cat][lemma] = dictionary[cat][lemma] + 1
    dictionaryTxt = ''
    for k, v in dictionary.items():
        dictionaryTxt += '## {0} ({1}) \n\n'.format(k, sum(v.values()))
        idx = 1
        for kk, vv in v.items():
            dictionaryTxt += '\t {0}. {1} : {2}\n\n'.format(idx, kk, vv)
            idx += 1
    with open(os.path.join(configuration['path']['projectPath'], path), 'w') as ff:
        ff.write(dictionaryTxt)


if __name__ == '__main__':
    # sents = readFTB('/Users/halsaied/PycharmProjects/NNIdenSys/ressources/FTB/dev.expandedcpd.gold.conll')
    # Token(1,'1'), [[Token(2,'2'),Token(3,'3')], Token(4,'4')], [Token(5,'5')],
    dimsumToCupt(os.path.join(configuration['path']['projectPath'], '/ressources/dimsum/dimsum16.test'))
    dimsumToCupt(os.path.join(configuration['path']['projectPath'], '/ressources/dimsum/dimsum16.train'))
