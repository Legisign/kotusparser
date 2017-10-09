#!/usr/bin/env python3
'''kotus2csv.py -- convert Kotus XML to CSV

  Usage:
      kotus2csv.py xmlfile [> csvfile]

  2017-10-09  0.1    First working version. (TN)

'''

import sys
import os.path
import csv
import kotusparser

version = '0.1.0'

if not sys.argv[1:]:
    print('Usage: kotus2csv XMLFILE...', file=sys.stderr)
    sys.exit(1)

for arg in sys.argv[1:]:
    csvfile = os.path.splitext(arg)[0] + '.csv'
    with open(arg, 'r') as infile:
        with open(csvfile, 'w') as outfile:
            writer = csv.writer(outfile, quoting=csv.QUOTE_ALL)
            wordid = 0
            for word, para, grad in kotusparser.KotusParser(infile):
                wordid += 1
                writer.writerow([wordid, word, para, grad])
