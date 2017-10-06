#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
'''kotusparser.py -- Kotus XML vocabulary list parser

  Tommi Nieminen <software@legisign.org> 2013-17.
  Distributed under the terms of the GNU General Public License (GPL)
  version 3 or later. See “copyleft.txt”.

  2014-03-24  1.0.5  Moved to GitHub. Changed version numbering to PyPi 
                     style.

'''

import xml.parsers.expat
from xml.parsers.expat import ExpatError as ParseError

version = '1.0.5'

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
        self.word = None
        self.paradigm = None

        # Implementation details
        self._element_stack = []
        self._xmlparser = xml.parsers.expat.ParserCreate()
        self._xmlparser.StartElementHandler = self._start_element
        self._xmlparser.EndElementHandler = self._end_element
        self._xmlparser.CharacterDataHandler = self._char_data

    def __iter__(self):
        return self

    def __next__(self):
        # May raise xml.parsers.expat.ExpatError exception, handle in caller
        self._xmlparser.Parse(next(self.stream))
        while not self.word:
            self._xmlparser.Parse(next(self.stream))
        return (self.word, self.paradigm)

    def next(self):
        # This function is for compatibility with Python 2.
        return self.__next__()

    def _start_element(self, element, attribs):
        self._element_stack.append(element)
        # This is to ensure correct output after end-of-data
        if element == 'st':
           self.word = self.paradigm = None

    def _end_element(self, element):
        self._element_stack.pop()

    def _char_data(self, data):
        if self._element_stack[-1] == 's':
            self.word = data
        elif self._element_stack[-1] == 'tn' and data.isnumeric():
            self.paradigm = int(data)

# Simple test if run as a script
if __name__ == '__main__':
    import sys
    for arg in sys.argv[1:]:
        with open(arg, 'r') as f:
            for word, paradigm in KotusParser(f):
                print('{0}:{1}'.format(word, paradigm))
