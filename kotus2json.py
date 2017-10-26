#!/usr/bin/env python3
'''

  kotus2json.py -- convert Kotus XML to JSON

  Usage:
      kotus2json.py xmlfile [> jsonfile]

  2014-01-05  0.1    First working version. (TN)
  2014-01-05  0.2    Corrections. (TN)
  2016-03-05  0.3    Style changes. (TN)
  2017-10-06  0.4.0  Upload to GitHub. (TN)
  2017-10-09  0.4.1  Bug fix. I had changed KotusParser to handle a stream,
                     not a file. File has to opened here. (TN)
  2017-10-26  0.5.0  Simplified structure. A list will suffice for each
                     lexeme instead of a dict.
  2017-10-26  0.6.0  Taking that back! Of course one needs a dict.

'''

import sys
import os.path
import json
import kotusparser

version = '0.6.0'

def die(msg):
    prg = os.path.basename(sys.argv[0])
    print('{}: {}'.format(prg, msg), file=sys.stderr)
    sys.exit(1)

if not sys.argv[1:]:
    die('Usage: kotus2json XMLFILE...')
for arg in sys.argv[1:]:
    if not os.path.exists(arg):
        die('Not found: {}'.format(arg))
    jsonfile = os.path.splitext(arg)[0] + '.json'
    vocab = {}
    try:
        with open(arg, 'r') as xml:
            try:
                vocab = {w: [p, g] for w, p, g in kotusparser.KotusParser(xml)}
            except kotusparser.ParseError:
                die('Cannot read or parse error: {}'.format(arg))
    except (PermissionError, IOError):
        die("Cannot read: {]".format(arg))
    try:
        with open(jsonfile, 'w') as f:
            json.dump(vocab, f, ensure_ascii=False, indent=1)
    except (PermissionError, IOError):
        die('Cannot write: {}'.format(jsonfile))
