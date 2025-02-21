from enum import Enum

from config import configuration
from corpus import VMWE, getTokens


class TransitionType(Enum):
    SHIFT = 0
    REDUCE = 1
    MERGE = 2
    MARK_AS_OTH = 3
    MARK_AS_IREFLV = 4
    MARK_AS_ID = 5
    MARK_AS_LVC = 6
    MARK_AS_VPC = 7


class Transition(object):
    def __init__(self, type=None, config=None, previous=None, next=None, isInitial=False, sent=None,
                 isClassified=False):

        self.sent = sent
        self.isClassified = isClassified
        if isInitial:
            self.configuration = Configuration([], sent.tokens, [], sent, self, isInitial=True, reduced=None)
            self.type = None
            sent.initialTransition = self
            self.isLegal = True
        else:
            self.configuration = config
        if type:
            self.type = type
        self.previous = previous
        if previous:
            previous.next = self
        self.next = next
        if not self.previous:
            self.id = 0
        else:
            self.id = self.previous.id + 1

    def apply(self, parent, sent, parse=False, secondParse=False):
        pass

    def getLegalTransDic(self, categorisation=False):
        """
        returns a list of legal transitions, that can be applied on the current configuration
        :param categorisation:
        :return:
        """
        config = self.configuration
        if config and config.legalTrans:
            return config.legalTrans
        transitions = {}
        if configuration['others']['minimal']:
            if len(config.stack) >= 1:
                transitions[TransitionType.MARK_AS_ID] = MarkAs(type=TransitionType.MARK_AS_ID,
                                                                sent=self.sent)
                transitions[TransitionType.MARK_AS_VPC] = MarkAs(type=TransitionType.MARK_AS_VPC,
                                                                 sent=self.sent)
                transitions[TransitionType.MARK_AS_LVC] = MarkAs(type=TransitionType.MARK_AS_LVC,
                                                                 sent=self.sent)
                transitions[TransitionType.MARK_AS_IREFLV] = MarkAs(type=TransitionType.MARK_AS_IREFLV,
                                                                    sent=self.sent)
                transitions[TransitionType.MARK_AS_OTH] = MarkAs(type=TransitionType.MARK_AS_OTH,
                                                                 sent=self.sent)
            if len(config.stack) > 1:
                transitions[TransitionType.MERGE] = Merge(sent=self.sent)
            transitions[TransitionType.REDUCE] = Reduce(sent=self.sent)
        else:
            if config.stack:
                if isinstance(config.stack[-1], list) and len(config.stack[-1]) == 2 or \
                        (len(config.stack) == 1 and str(config.stack[-1].__class__).endswith('corpus.Token')):
                    if categorisation:
                        transitions[TransitionType.MARK_AS_ID] = MarkAs(type=TransitionType.MARK_AS_ID,
                                                                        sent=self.sent)
                        transitions[TransitionType.MARK_AS_VPC] = MarkAs(type=TransitionType.MARK_AS_VPC,
                                                                         sent=self.sent)
                        transitions[TransitionType.MARK_AS_LVC] = MarkAs(type=TransitionType.MARK_AS_LVC,
                                                                         sent=self.sent)
                        transitions[TransitionType.MARK_AS_IREFLV] = MarkAs(type=TransitionType.MARK_AS_IREFLV,
                                                                            sent=self.sent)
                    transitions[TransitionType.MARK_AS_OTH] = MarkAs(type=TransitionType.MARK_AS_OTH,
                                                                     sent=self.sent)
                if len(config.stack) > 1:
                    transitions[TransitionType.MERGE] = Merge(sent=self.sent)
                transitions[TransitionType.REDUCE] = Reduce(sent=self.sent)

        # if config.stack:
        #     transitions[TransitionType.REDUCE] = Reduce(sent=self.sent)
        #     if (len(config.stack) == 1 and str(config.stack[-1].__class__) == 'corpus.Token') or \
        #     len(config.stack)> 1:
        #         #if isinstance(config.stack[-1], list) and len(config.stack[-1]) == 2:
        #         transitions[TransitionType.MARK_AS_ID] = MarkAs(type=TransitionType.MARK_AS_ID,
        #                                                         sent=self.sent)
        #         transitions[TransitionType.MARK_AS_VPC] = MarkAs(type=TransitionType.MARK_AS_VPC,
        #                                                          sent=self.sent)
        #         transitions[TransitionType.MARK_AS_LVC] = MarkAs(type=TransitionType.MARK_AS_LVC,
        #                                                          sent=self.sent)
        #         transitions[TransitionType.MARK_AS_IREFLV] = MarkAs(type=TransitionType.MARK_AS_IREFLV,
        #                                                             sent=self.sent)
        #         transitions[TransitionType.MARK_AS_OTH] = MarkAs(type=TransitionType.MARK_AS_OTH,
        #                                                              sent=self.sent)
        #     if len(config.stack) > 1:
        #         whiteMerge = Merge(sent=self.sent)
        #         transitions[TransitionType.MERGE] = whiteMerge

        if config.buffer:
            transitions[TransitionType.SHIFT] = Shift(sent=self.sent)
        config.legalTrans = transitions
        return transitions

    def isTerminal(self):
        """
        determines wheteher the transition (its configuration) is terminal or not
        :return:
        """
        if self.configuration.stack or self.configuration.buffer:
            return False
        return True

    def isImportantTrans(self):
        """
        Determine whether the transition is possibly involved in the process of identifiening a MWE
        :return:
        """
        if self.next:
            if self.next.type == TransitionType.SHIFT and self.configuration.stack:
                return True
            if self.next.type != TransitionType.SHIFT and self.next.type != TransitionType.REDUCE:
                return True
        return False

    def isImportant(self, window=4):
        idx = 0
        nexTrans = self
        while nexTrans and idx < window:
            if nexTrans.type and nexTrans.type != TransitionType.SHIFT and nexTrans.type != TransitionType.REDUCE:
                return True
            nexTrans = nexTrans.next
            idx += 1
        idx = 0
        prevTrans = self
        while prevTrans and idx < window:
            if prevTrans.type and prevTrans.type != TransitionType.SHIFT and prevTrans.type != TransitionType.REDUCE:
                return True
            prevTrans = prevTrans.previous
            idx += 1
        return False

    def isMarkOrMerge(self):
        """
        determine whethter it's a mark or a merge or not
        :return:
        """
        if self is not None and self.type is not None and self.type.value is not None and self.type.value >= 2:
            return True
        return False

    def __str__(self):
        typeStr = '{0}'.format(self.type.name) if self.type else ''
        transSelectionType = 'C' if self.isClassified else 'L'
        typeStr += ': ' + transSelectionType + ' ' * (15 - len(typeStr))
        return '\n{0} \n{1}'.format(typeStr, str(self.configuration))


class Shift(Transition):
    def __init__(self, type=TransitionType.SHIFT, config=None, previous=None, next=None, isInitial=False, sent=None):
        super(Shift, self).__init__(type, config, previous, next, isInitial, sent)
        self.type = TransitionType.SHIFT

    def apply(self, parent, sent, parse=False, isClassified=False, secondParse=False):
        config = parent.configuration
        lastToken = config.buffer[0]
        newStack = list(config.stack)
        newStack.append(lastToken)
        reduced = parent.configuration.reduced if parent and parent.configuration else None
        newConfig = Configuration(newStack, config.buffer[1:], list(config.tokens), sent, self, reduced=reduced)
        super(Shift, self).__init__(config=newConfig, previous=parent, sent=sent, isClassified=isClassified)

    def isLegal(self):
        """
        Determine whether the shift transition is applicable on the current configuration
        :return:
        """
        if self.configuration.buffer:
            return True
        return False


class Reduce(Transition):
    def __init__(self, type=TransitionType.REDUCE, config=None, previous=None, next=None, isInitial=False, sent=None):
        super(Reduce, self).__init__(type, config, previous, next, isInitial, sent)

    def apply(self, parent, sent, parse=False, isClassified=False, secondParse=False):
        config = parent.configuration
        newBuffer = list(config.buffer)
        newStack = list(config.stack)
        newStack = newStack[:-1]
        newTokens = list(config.tokens)
        if str(config.stack[-1].__class__).endswith('corpus.Token'):
            reduced = config.stack[-1]
        else:
            if config.stack[-1] and isinstance(config.stack[-1], list):
                tokens = getTokens(config.stack[-1])
                reduced = tokens[-1]
            else:
                reduced = parent.configuration.reduced
        newConfig = Configuration(newStack, newBuffer, newTokens, sent, self, reduced=reduced)
        super(Reduce, self).__init__(config=newConfig, previous=parent, sent=sent, isClassified=isClassified)

    def isLegal(self):
        """
        Determine whether the Reduce transition is applicable on the current configuration
        :return:
        """
        if self.configuration.stack:
            return True
        return False


class Merge(Transition):
    def __init__(self, config=None, previous=None, next=None, isInitial=False, sent=None):
        super(Merge, self).__init__(TransitionType.MERGE, config, previous, next, isInitial, sent)

    def apply(self, parent, sent, parse=False, isClassified=False, secondParse=False):
        config = parent.configuration
        newBuffer = list(config.buffer)
        newStack = list(config.stack)[:-2]
        newStack.append([config.stack[-2], config.stack[-1]])
        newTokens = list(config.tokens)
        reduced = parent.configuration.reduced
        newConfig = Configuration(newStack, newBuffer, newTokens, sent, self, reduced=reduced)

        super(Merge, self).__init__(config=newConfig, previous=parent, sent=sent, isClassified=isClassified)

    def isLegal(self):
        """
        Determine whether the Merge transition is applicable on the current configuration
        :return:
        """
        if self.configuration.stack and len(self.configuration.stack) > 1:
            return True
        return False


class MarkAs(Transition):
    def __init__(self, type, config=None, previous=None, next=None, isInitial=False, sent=None):
        super(MarkAs, self).__init__(type, config, previous, next, isInitial, sent)

    def apply(self, parent, sent, parse=False, isClassified=False, secondParse=False):
        """
        modify the current configuration, by applying the transition
        :param parent:
        :param sent:
        :param parse:
        :param isClassified:
        :param secondParse: used with complementary training (SVM + MLP)
        :return:
        """
        if configuration['others']['minimal']:
            self.applyMinimal(parent, sent, parse, isClassified, secondParse)
        else:
            config = parent.configuration
            newBuffer = list(config.buffer)
            newStack = list(config.stack)[:-1]
            newStack.append([config.stack[-1]])
            newTokens = list(config.tokens)
            vMWETokens = getTokens(newStack[-1][0])
            if parse:
                vMWEIdx = len(sent.identifiedVMWEs) + 1
                vMWE = VMWE(vMWEIdx, tokens=vMWETokens, type=getStrFromTransType(self.type))
                if secondParse:
                    # used with complementary training (SVM + MLP)
                    poss = [v.getTokenPositionString() for v in sent.identifiedVMWEs]
                    if vMWE.getTokenPositionString() not in poss:
                        sent.identifiedVMWEs.append(vMWE)
                        vMWE.predictingModel = 'linear' if configuration['xp']['linear'] else 'mlp'
                    else:
                        for v in sent.identifiedVMWEs:
                            if v.getTokenPositionString() == vMWE.getTokenPositionString():
                                v.predictingModel += 'linear' if configuration['xp']['linear'] else 'mlp'
                                break
                else:
                    vMWE.predictingModel = 'linear' if configuration['xp']['linear'] else 'mlp'
                    sent.identifiedVMWEs.append(vMWE)
            newTokens.append(vMWETokens)
            reduced = parent.configuration.reduced
            newConfig = Configuration(newStack, newBuffer, newTokens, sent, self, reduced=reduced)
            super(MarkAs, self).__init__(config=newConfig, previous=parent, sent=sent, isClassified=isClassified)

    def applyMinimal(self, parent, sent, parse=False, isClassified=False, secondParse=False):
        config = parent.configuration
        newBuffer = list(config.buffer)
        newStack = list(config.stack)[:-2] if len(config.stack) > 1 else list(config.stack)[:-1]
        newStack.append([config.stack[-2], config.stack[-1]] if len(config.stack) > 1 else [config.stack[-1]])
        newTokens = list(config.tokens)
        vMWETokens = getTokens(newStack[-1])
        if parse:
            vMWEIdx = len(sent.identifiedVMWEs) + 1
            vMWE = VMWE(vMWEIdx, tokens=vMWETokens, type=getStrFromTransType(self.type))
            if secondParse:
                # used with complementary training (SVM + MLP)
                poss = [v.getTokenPositionString() for v in sent.identifiedVMWEs]
                if vMWE.getTokenPositionString() not in poss:
                    sent.identifiedVMWEs.append(vMWE)
                    vMWE.predictingModel = 'linear' if configuration['xp']['linear'] else 'mlp'
                else:
                    for v in sent.identifiedVMWEs:
                        if v.getTokenPositionString() == vMWE.getTokenPositionString():
                            v.predictingModel += 'linear' if configuration['xp']['linear'] else 'mlp'
                            break
            else:
                vMWE.predictingModel = 'linear' if configuration['xp']['linear'] else 'mlp'
                sent.identifiedVMWEs.append(vMWE)
        # else:
        #     vmwe = getVMWEByTokens(vMWETokens)
        #     if vmwe:
        #         vmwe.parsedByOracle = True
        #     else:
        #         raise
        newTokens += vMWETokens
        reduced = parent.configuration.reduced
        newConfig = Configuration(newStack, newBuffer, newTokens, sent, self, reduced=reduced)
        super(MarkAs, self).__init__(config=newConfig, previous=parent, sent=sent, isClassified=isClassified)

    def isLegal(self):
        """
        Determine whether the MarkAs transition is applicable on the current configuration
        :return:
        """
        if self.configuration.stack:
            return True
        return False


class Configuration:
    def __init__(self, stack, buffer, tokens, sent, transition, reduced=None, isInitial=False, ):

        self.buffer = buffer
        self.stack = stack
        self.tokens = tokens
        self.isInitial = isInitial
        self.isTerminal = self.isTerminal()
        self.sent = sent
        self.transition = transition
        self.legalTrans = {}
        self.reduced = reduced

    def isTerminal(self):
        """
        Determine whether the configuration is terminal or not
        :return:
        """

        if not self.buffer and not self.stack:
            return True
        return False

    def __str__(self):
        stackStr = printStack(self.stack)
        buffStr = '[ '
        if self.buffer:
            for elem in self.buffer[:2]:
                buffStr += elem.text + ','
            buffStr += ' ..' if len(self.buffer) > 2 else ''
        buffStr += ']'
        return 'S=' + stackStr + ' B=' + buffStr + ' Bx=' + self.reduced.getLemma() if self.reduced else ''


def initialize(transType, sent):
    """
    Returns an instance of the given transition type
    :param transType:
    :param sent:
    :return:
    """
    if isinstance(transType, int):
        transType = getType(transType)
    if transType == TransitionType.SHIFT:
        return Shift(sent=sent)
    if transType == TransitionType.MERGE:
        return Merge(sent=sent)
    if transType in [TransitionType.MARK_AS_OTH, TransitionType.MARK_AS_IREFLV,
                     TransitionType.MARK_AS_LVC, TransitionType.MARK_AS_VPC,
                     TransitionType.MARK_AS_ID]:
        return MarkAs(type=transType, sent=sent)
    return Reduce(sent=sent)


def getType(idx):
    """
    Returns the transition type using its index (value)
    :param idx:
    :return:
    """
    for type in TransitionType:
        if type.value == idx:
            return type
    return None


def getMWTTypeFromStr(type):
    """
    Returns the TransitionTypz given the acronym of MWE category
    :param type:
    :return:
    """
    if type:
        if type.lower() == 'vpc':
            return TransitionType.MARK_AS_VPC
        if type.lower() == 'ireflv':
            return TransitionType.MARK_AS_IREFLV
        if type.lower() == 'lvc':
            return TransitionType.MARK_AS_LVC
        if type.lower() == 'id':
            return TransitionType.MARK_AS_ID
    return TransitionType.MARK_AS_OTH


def getStrFromTransType(transType):
    """
    Return the category of a MWE given its Mark transition
    :param transType:
    :return:
    """
    if transType is TransitionType.MARK_AS_VPC:
        return 'vpc'
    if transType is TransitionType.MARK_AS_IREFLV:
        return 'ireflv'
    if transType is TransitionType.MARK_AS_LVC:
        return 'lvc'
    if transType is TransitionType.MARK_AS_ID:
        return 'id'
    return 'oth'


def printStack(elemlist):
    """
    Produce a string representing the stack
    :param elemlist:
    :return:
    """
    stackStr = ''
    elemlistStrs = getStackElems(elemlist)
    for r in elemlistStrs:
        if r == '[' or r == ']':
            if stackStr.endswith(', '):
                stackStr = stackStr[:-2]
            stackStr += r
        else:
            stackStr += r + ', '
    return stackStr + ' ' * (25 - len(stackStr))


def getStackElems(elemlist):
    """
    return a list representing the textual elements of the stack
    :param elemlist:
    :return:
    """
    elemlistStrs = ['[']
    for elem in elemlist:
        if str(elem.__class__).endswith('corpus.Token'):
            elemlistStrs.append(elem.text)
        elif isinstance(elem, list) and len(elem) == 1 and isinstance(elem[0], list):
            elemlistStrs.extend(getStackElems(elem[0]))
        elif isinstance(elem, list) and len(elem):
            elemlistStrs.extend(getStackElems(elem))
    elemlistStrs.append(']')
    return elemlistStrs
