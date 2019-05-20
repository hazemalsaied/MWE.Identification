from nltk.parse import DependencyEvaluator
from nltk.parse.transitionparser import TransitionParser

from xpTools import *


def parse(lang):
    corpus = Corpus(lang)
    parser_std = TransitionParser('arc-standard')
    parser_std.train(corpus.trainDepGraphs, 'temp.arcstd.model')
    result = parser_std.parse(corpus.testDepGraphs, 'temp.arcstd.model')
    de = DependencyEvaluator(result, corpus.testDepGraphs)
    print 'Labeled Attachment Score (LAS)  = {0}'.format(round(de.eval()[0] * 100, 1))
    print 'Unlabeled Attachment Score (UAS) = {0}'.format(round(de.eval()[1] * 100, 1))


if __name__ == '__main__':
    reload(sys)
    sys.setdefaultencoding('utf8')

    # configuration['tmp']['createDepGraphs'] = True
    # initXp(XpMode.linear, Dataset.sharedtask2, None, None, None)  # Evaluation.trainVsDev
    # for l in allSharedtask2Lang:
    #     parse(l)
