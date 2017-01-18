#!/usr/bin/env python3

import jargparse
import os
import owlready
import sys

sys.path.insert(1, os.path.dirname(os.path.abspath(__file__)) + '/../../../modules/python')
import synbio.data as sbd

############
### MAIN ###
############
parser = jargparse.ArgParser('Convert OWL to InterMine model XML')
parser.add_argument('colPath', help='path to the data collection.')
parser.add_argument('-d', '--dummy', action='store_true', help='dummy run, do not store anything')
parser.add_argument('-v', '--verbose', action='store_true', help='be verbose')
args = parser.parse_args()

dc = sbd.Collection(args.colPath)
ds = dc.getSet('parts/synbis')
ds.startLogging(__file__)

owlready.onto_path.append(ds.getLoadPath())
synbisOnto = owlready.get_ontology('http://intermine.org/synbiomine/synbis.owl').load()

print(owlready.to_owl(synbisOnto))
