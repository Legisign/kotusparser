#!/usr/bin/env python3
'''kotus2json.py -- convert Kotus XML to JSON

  Usage:
      kotus2json.py xmlfile [> jsonfile]

  2014-01-05  0.1    First working version. (TN)
  2014-01-05  0.2    Corrections. (TN)
  2016-03-05  0.3    Style changes. (TN)
  2017-10-06  0.4.0  Upload to GitHub. (TN)

'''

import sys
import os.path
import json
import kotusparser

version = '0.4.0'

def die(msg):
    print('{}: {}'.format(os.path.basename(sys.argv[0]), msg), \
          file=sys.stderr)
    sys.exit(1)

if not sys.argv[1:]:
    die('Usage: kotus2json XMLFILE...')

for arg in sys.argv[1:]:
    jsonfile = os.path.splitext(arg)[0] + '.json'
    try:
        vocab = []
        for w, p in kotusparser.KotusParser(arg):
            if w:
                d = {'s': w, 'tn': p if p else 0}
                vocab.append(d)
    except kotusparser.ParseError:
        die('Cannot read or parse error: {}'.format(arg))
    try:
        with open(jsonfile, 'w') as f:
            json.dump(vocab, f, ensure_ascii=False, indent=1)
    except IOError:
        die('Cannot write: {}'.format(jsonfile))
