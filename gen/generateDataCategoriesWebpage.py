#!/usr/bin/env python

import os
import sys

sys.path.insert(1, os.path.dirname(os.path.abspath(__file__)) + '/../modules/python')
import intermyne.utils as imu
import synbio.dataset as sbds

############
### MAIN ###
############
parser = imu.ArgParser('Generate organism entries for $INTERMINE/synbiomine/webapp/resources/webapp/dataCategories.jsp')
parser.add_argument('datasetPath', help='path to the dataset location.')
parser.add_argument('-v', '--verbose', action="store_true", help="verbose output")
args = parser.parse_args()

ds = sbds.Dataset(args.datasetPath)
orgs = ds.getOrganisms()

for taxonId, name in sorted(orgs.iteritems(), key=lambda item: item[1]):
    print '  <li>%s (<i>taxon %d</i>)</li>' % (orgs[taxonId], taxonId)