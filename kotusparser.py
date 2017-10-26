#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
'''kotusparser.py -- Kotus XML vocabulary list parser

  Tommi Nieminen <software@legisign.org> 2013-17.
  Distributed under the terms of the GNU General Public License (GPL)
  version 3 or later.

  Exceptions are expected to be handled by the caller. Possible exceptions
  include:
  * xml.parsers.expat.ExpatError -- for all XML parsing errors

  2017-10-26  1.1.1  Bug fix: once the gradation field was set, its value was
                     used for subsequent words unless it was explicitly set
                     again.

'''

import xml.parsers.expat

version = '1.1.1'

class KotusParser(object):
    '''Iterates through a Kotus-format XML word list.

    Takes one obligatory parameter which is the name of the XML file. Returns
    an iterator which generates (word, paradigm) tuples one at a time. "word"
    is the base form of the word, paradigm is the paradigm number as stated
    in the XML file, or None if none given.
    '''
    def __init__(self, stream):
        # Public
        self.stream = stream
        self.word = None            # word type
        self.paradigm = None        # numeric paradigm
        self.gradation = None       # consonant gradation type

        # Implementation details
        self._element_stack = []
        self._xmlparser = xml.parsers.expat.ParserCreate()
        self._xmlparser.StartElementHandler = self._start_element
        self._xmlparser.EndElementHandler = self._end_element
        self._xmlparser.CharacterDataHandler = self._char_data

    def __iter__(self):
        '''Return an iterator.'''
        return self

    def __next__(self):
        '''Return next item.'''
        self._xmlparser.Parse(next(self.stream))
        while not self.word:
            self._xmlparser.Parse(next(self.stream))
        return (self.word, self.paradigm, self.gradation)

    def next(self):
        '''Python 2 compatibility function; for Python 3, use __next__.'''
        return self.__next__()

    def _start_element(self, element, attribs):
        '''Handle start elements'''
        self._element_stack.append(element)
        # This is to ensure correct output after end-of-data
        if element == 'st':
           self.word = self.paradigm = self.gradation = None

    def _end_element(self, element):
        '''Handle end elements'''
        self._element_stack.pop()

    def _char_data(self, data):
        '''Handle character data (text outside tags)'''
        if self._element_stack[-1] == 's':
            self.word = data.strip()
        elif self._element_stack[-1] == 'tn' and data.isnumeric():
            self.paradigm = int(data)
        elif self._element_stack[-1] == 'av':
            self.gradation = data

# Simple test if run as a script
if __name__ == '__main__':
    import sys
    for arg in sys.argv[1:]:
        with open(arg, 'r') as f:
            for word, paradigm, gradation in KotusParser(f):
                if not paradigm:
                    paradigm = '(tuntematon)'
                print('{} - {} - {}'.format(word, paradigm, gradation))
