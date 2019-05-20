# Natural Language Toolkit: Arc-Standard and Arc-eager Transition Based Parsers
#
# Author: Long Duong <longdt219@gmail.com>
#
# Copyright (C) 2001-2019 NLTK Project
# URL: <http://nltk.org/>
# For license information, see LICENSE.TXT

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import src.config

unk = src.config.configuration['constants']['unk']
empty = src.config.configuration['constants']['empty']

from nltk.parse.transitionparser import TransitionParser, Transition, Configuration



