#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys

from reports import OSTools

"""
    A script with multiple functions for processing latex files
    Used for cleaning latex files and for preparing latex files 
    to be correctly transformed in text format (rtf) using Pandoc 
"""

texOutFile = '/Users/halsaied/PycharmProjects/MWE.Identification/Reports/out.tex'


def mergeFiles(folderPath, excluded=['S_Store', 'ann.tex']):
    """
    Used to merge latex files of o given folder
    :param folderPath:
    :param excluded: files to exclude
    :return:
    """
    files = OSTools.getListOfFiles(folderPath)
    with open(texOutFile, 'w') as outfile:
        for fname in files:
            if str(fname[-7:]) not in excluded:
                with open(fname) as infile:
                    for line in infile:
                        outfile.write(line)


def removeTextComments():
    """
    Remove comments (starting with % sign) from latex files
    :return:
    """
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
                        if (idx > 0 and line[idx - 1] != '\\') or \
                                (idx > 1 and line[idx - 1] == '\\' and line[idx - 2] == '\\'):
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
    """
    Remive lines starting with given prefixes from tex files
    :param prefixes:
    :return:
    """
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
    """
    Remove given words from latex files
    :param words:
    :return:
    """
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
    """
    Remove an entire block from text file
    :param startStr: block start tag
    :param endStr: block end tag
    :return:
    """
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
    """
    Given a list of tuples (string1,string2), the function replace the first string be the second
    :param replaceCouples:
    :return:
    """
    outText = ''
    with open(texOutFile, 'r') as ff:
        for line in ff:
            for couple in replaceCouples:
                line = line.replace(couple[0], couple[1])
            outText += line
    with open(texOutFile, 'w') as ff:
        ff.write(outText)


def replaceCitations(replaceStr='\\cite'):
    """
    Replace citations by a constant string
    used to clean latex files of citations that the automatic corrector Antidote has problem with
    :param replaceStr:
    :return:
    """
    outText = ''
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


def extractCitations(replaceStr='\\cite'):
    """
    Extract all the citations of latex file
    :param replaceStr:
    :return:
    """
    outText = ''
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
                    outText += tmpLine[idx:endIdx] + '\n'
                    tmpLine = tmpLine[:idx] + tmpLine[endIdx:]
                else:
                    break
    with open(texOutFile, 'w') as ff:
        ff.write(outText)


if __name__ == '__main__':
    reload(sys)
    sys.setdefaultencoding('utf8')
    folderPath = '/Users/halsaied/PycharmProjects/MWE.Identification/Reports/T'
    extractCitations()
    # mergeFiles(folderPath)
    # removeTextComments()
    # removeBloc('\\begin{comment}', '\\end{comment}')

    # removeBloc('\\begin{table}', '\\end{table}')
    # removeGivenLines(['\\label', '\\FrameThisInToc', '\\DontFrameThisInToc'])
    # removeGivenWords(['\\quad', '\\\\','\\noindent', '\\hazemm', '\marie',
    # '\\mathieu', '\\draftnote', '\\draftreplace', '\\draftremove', '\\hazem'])
    #
    # replaceCitations()
    # replace([('\\ep', 'EP'),
    #          ('\\mlp', 'MLP'),
    #          ('\\rmlp', 'RMLP'),
    #          ('\\stt', 'Parseme'),
    #          ('\\st', 'Parseme'),
    #          ('\\lstm', 'lstm'),
    #          ('\\svm', 'SVM'),
    #          ('\\lvc', 'LVC'),
    #          ('\\irf', 'IRF'),
    #          ('\\id', 'ID'),
    #          ('\\vpc', 'VPC'),
    #          ('\\ftb', 'FTB'),
    #          ('\\dimsum', 'DiMSUM'),
    #          ('\\gru', 'GRU'),
    #          ('\\evaleps', 'evalEPs'),
    #          ('\\evalcmpts', 'evalTokens'),
    #           ('\\parsm', 'Parseme'),
    #          ('\\ff', 'F')
    #          ])
