#!/usr/bin/env python

import jargparse
from lxml import etree
import os
import requests
import sys

sys.path.insert(1, os.path.dirname(os.path.abspath(__file__)) + '/../../modules/python')
import synbio.data as sbd

#################
### FUNCTIONS ###
#################
"""
Fetch details for the given part
"""
def fetchPartDetails(partName, partsPath):
    partPath = '%s/%s.xml' % (partsPath, partName)

    if os.path.exists(partPath):
        print 'Skipping fetch of part %s as we already have it' % partName
        return

    url = 'http://virtualparts.org/part/%s/xml' % partName
    r = requests.get(url)

    with open(partPath, 'w') as f:
        f.write(r.text)

"""
Fetch interactions for the given part
"""
def fetchInteractions(partName, interactionsPath):
    partPath = '%s/%s.xml' % (interactionsPath, partName)

    if os.path.exists(partPath):
        print 'Skipping fetch of interaction %s as we already have it' % partName
        return

    url = 'http://virtualparts.org/part/%s/interactions/xml' % partName
    r = requests.get(url)

    with open(partPath, 'w') as f:
        f.write(r.text)

############
### MAIN ###
############
parser = jargparse.ArgParser('Fetch Virtual Parts Repository parts directly')
parser.add_argument('colPath', help='path to the data collection')
args = parser.parse_args()

dc = sbd.Collection(args.colPath)
ds = dc.getSet('polen')
ds.startLogging(__file__)

partsPath = '%s/parts' % ds.getRawPath()
interactionsPath = '%s/interactions' % ds.getRawPath()

# Uses api from http://virtualparts.org/repositorydocumentation
pageNum = 1
partsCount = 0

while True:
    url = 'http://virtualparts.org/parts/page/%d/xml' % pageNum
    # print "Fetching page %s" % url
    r = requests.get(url)

    # We're doing this processing so that we get individual parts files that we can compare with what we get when
    # we do individual parts requests from POLEN
    tree = etree.fromstring(r.content)

    part_es = tree.findall('./Part')
    partsInPageCount = len(part_es)
    partsCount += partsInPageCount

    print 'Found %d parts in page %d' % (partsInPageCount, pageNum)

    for part_e in part_es:
        # Don't allow directory traversal by a part name
        partName = part_e.find('Name').text
        if partName != os.path.basename(partName):
            print 'WARNING: Part name %s contains directory traversal.  Dropping' % (partName)
            continue

        print 'Found part %s' % partName

        # Unfortunately the page xml only gives part summary information, not the detailed information that we want
        # So we need to request the xml for each part separately
        fetchPartDetails(partName, partsPath)
        fetchInteractions(partName, interactionsPath)

    if partsInPageCount <= 0:
        break
    else:
        pageNum += 1

print "Found %d parts in total" % partsCount
