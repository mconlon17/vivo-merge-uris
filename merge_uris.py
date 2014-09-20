"""
    merge_uris.py: Given pairs of uri ("from") and ("to") remove assertions
    for the "from" uri and add all those assertions to the "to" uri.
    This has the effect of removing the "from" entity and having all its
    facts attributed to the "to" uri.

    Use merge_uris when from and to refer to the same thing.  Typically the
    from is a duplicate and the to is the one you want to keep.

    An example:  Suppose you have an extensive profile for a faculty member
    at uri x.  A second profile is discovered at uri y which has a single
    publication.  You want to merge x and y so that the publication is assigned
    to the full profile at x and the redundant profile at y is removed.  In
    this case the from is "y" and the to is "x".  After the merge, all the
    things that were said about y (publication, anything else) are assigned to
    x.  y, and all facts about y, are removed.

    Note:  merge_uris is remarkably dangerous.  It will merge ANY two uris.
    merge_uri should be used carefully and as part of a comprehensive activity
    to maintain the data quality of a VIVO triple store.

    Version 0.0 MC 2013-11-30
    --  complete draft
    Version 0.1 MC 2014-01-03
    --  translate_predicate reverses a URI predicate to a tagged predicate
    --  Uses csv file to drive bulk merges.
    Version 0.2 MC 2014-06-21
    --  Use functions from vivotools
    Version 0.3 MC 2014-06-22
    --  Code style improvements
    Version 0.4 MC 2014-08-26
    --  Updated for new tools, add command line argument for filename
"""

__author__ = "Michael Conlon"
__copyright__ = "Copyright 2014, University of Florida"
__license__ = "BSD 3-Clause license"
__version__ = "0.4"

from vivofoundation import rdf_header
from vivofoundation import rdf_footer
from vivofoundation import read_csv
from vivofoundation import merge_uri
from datetime import datetime
import codecs
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("filename", help="File containing from and to URIs",
                    default="2014-09-20.txt")
args = parser.parse_args()

print datetime.now(), "Start"
ardf = rdf_header()
srdf = rdf_header()
rows = read_csv(args.filename)
for i in sorted(rows.keys()):
    row = rows[i]
    ardf = ardf + "\n<!-- Merge " + row["from"] + " to " + row["to"] + " -->\n"
    print i, "Merge", row["from"], "to", row["to"]
    [add, sub] = merge_uri(row["from"], row["to"])
    ardf = ardf + add
    srdf = srdf + sub
ardf = ardf + rdf_footer()
srdf = srdf + rdf_footer()
add_file = codecs.open("add.rdf", mode='w', encoding='ascii',
                       errors='xmlcharrefreplace')
sub_file = codecs.open("sub.rdf", mode='w', encoding='ascii',
                       errors='xmlcharrefreplace')
print >>add_file, ardf
print >>sub_file, srdf
add_file.close()
sub_file.close()
print datetime.now(), "Finished"
