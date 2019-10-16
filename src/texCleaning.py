#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys
from reports import OSTools

texOutFile = '/Users/halsaied/PycharmProjects/MWE.Identification/Reports/out.tex'


def mergeFiles(folderPath, excluded=['S_Store','ann.tex']):
    files = OSTools.getListOfFiles(folderPath)
    with open(texOutFile, 'w') as outfile:
        for fname in files:
            if str(fname[-7:]) not in excluded:
                with open(fname) as infile:
                    for line in infile:
                        outfile.write(line)

def removeTextComments():
    outText = ''
    with open(texOutFile, 'r') as inFile:
        for line in inFile:
            if line.strip().startswith('%'):
                continue
            if '%' in line:
                idx = 0
                lineAdded = False
                for c in line:
                    if c == '%':
                        if (idx > 0 and line[idx-1] != '\\') or \
                                (idx > 1 and line[idx-1] == '\\' and line[idx-2] == '\\'):
                            outText += line[:idx] + '\n'
                            lineAdded = True
                            break
                    idx += 1
                if not lineAdded:
                    outText += line
            else:
                outText += line
    with open(texOutFile, 'w') as ff:
        ff.write(outText)

def removeGivenLines(prefixes):
    outText = ''
    with open(texOutFile, 'r') as inFile:
        for line in inFile:
            addLine = True
            for prefixe in prefixes:
                if line.strip().startswith(prefixe):
                    addLine = False
                    break
            if addLine:
                outText += line
    with open(texOutFile, 'w') as ff:
        ff.write(outText)

def removeGivenWords(words):
    outText = ''
    with open(texOutFile, 'r') as inFile:
        for line in inFile:
            tmpLine = line
            for word in words:
                tmpLine = tmpLine.replace(word, '')
            outText += tmpLine
    with open(texOutFile, 'w') as ff:
        ff.write(outText)

def removeBloc(startStr, endStr):
    outText, addLines, nestedBlocks = '', True, 0
    with open(texOutFile, 'r') as inFile:
        for line in inFile:
            if line.strip().startswith(startStr) or startStr in line:
                addLines = False
                nestedBlocks += 1
            if addLines:
                outText += line
            if line.strip().startswith(endStr) or endStr in line:
                nestedBlocks -= 1
                if nestedBlocks == 0:
                    addLines = True
    with open(texOutFile, 'w') as ff:
        ff.write(outText)

def replace(replaceCouples):
    outText = ''
    with open(texOutFile, 'r') as ff:
        for line in ff:
            for couple in replaceCouples:
                line = line.replace(couple[0], couple[1])
            outText += line
    with open(texOutFile, 'w') as ff:
        ff.write(outText)

def replaceCitations(replaceStr='\\cite'):
    outText= ''
    with open(texOutFile, 'r') as ff:
        for line in ff:
            tmpLine = line
            while True:
                if replaceStr in tmpLine:
                    idx = tmpLine.index(replaceStr)
                    endIdx = idx
                    for c in tmpLine[idx:]:
                        endIdx += 1
                        if c == '}':
                            break
                    tmpLine = tmpLine[:idx] + 'XXX' + tmpLine[endIdx:]
                else:
                    break
            outText += tmpLine
    with open(texOutFile, 'w') as ff:
        ff.write(outText)


if __name__ == '__main__':
    reload(sys)
    sys.setdefaultencoding('utf8')
    folderPath = '/Users/halsaied/PycharmProjects/MWE.Identification/Reports/La these'
    mergeFiles(folderPath)
    removeTextComments()
    removeBloc('\\begin{comment}', '\\end{comment}')
    removeBloc('\\begin{tabular}', '\\end{tabular}')
    removeGivenLines(['\\label', '\\FrameThisInToc', '\\DontFrameThisInToc'])
    removeGivenWords(['\\quad', '\\\\','\\noindent', '\\hazem', '\marie', '\\mathieu', '\\draftnote', '\\draftreplace', '\\draftremove'])

    replaceCitations()
    replace([('\\ep', 'EP'), 
             ('\\mlp', 'MLP'),
             ('\\stt', 'Parseme'),
             ('\\st', 'Parseme'),
             ('\\lstm', 'lstm'),
             ('\\svm', 'SVM'),
             ('\\lvc', 'LVC'),
             ('\\irf', 'IRF'),
             ('\\id', 'ID'),
             ('\\vpc', 'VPC'),
             ('\\ftb', 'FTB'),
             ('\\dimsum', 'DiMSUM'),
             ('\\gru', 'GRU'),
             ('\\evaleps', 'evalEPs'),
             ('\\evalcmpts', 'evalTokens'),
              ('\\parsm', 'Parseme'),
             ('\\ff', 'F')
             ])
