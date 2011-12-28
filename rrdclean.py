#!/usr/bin/env python
#
# rrdclean.py - trivial tool to remove spikes from rrd files
#
#
# Why another tool? Dunno. It's probably as bad as others in most
# aspects, but this one is interactive which is a property I needed...
#
# Author: Magnus Hagander <magnus@hagander.net>, Redpill Linpro AB
#
#
#
# Note: error control is basically missing, expect ugly
# exceptions instead of nice error messages...

import os
import sys
from subprocess import Popen, PIPE
import xml.dom.minidom

rrdname = sys.argv[1]
if not os.path.exists(rrdname):
	print "File %s does not exist" % rrdname
	sys.exit(1)

alldata = Popen("rrdtool dump %s" % rrdname, shell=True, stdout=PIPE).communicate()[0]

# It's not that much data, so process everything in memory
dom = xml.dom.minidom.parseString(alldata)
rowvals = []
for n in dom.getElementsByTagName("row"):
	# First child is the <v> tag, then comes the value
	num = n.firstChild.firstChild.nodeValue
	if num != "NaN":
		rowvals.append(float(num))

print "Read %s values (rest is NaN)" % len(rowvals)
rowvals.sort(reverse=True)
cutoff = ''
for endpos in range(20,len(rowvals),20):
	print "\n".join(map(str, rowvals[endpos-20:endpos]))
	cutoff = raw_input("Enter cutoff value, or blank to see more values: ")
	if cutoff != "": break

cutoff = float(cutoff)
for n in dom.getElementsByTagName("row"):
	num = n.firstChild.firstChild.nodeValue
	if num != "NaN":
		if float(num) > cutoff:
			while True:
				if n.previousSibling.previousSibling.nodeType == n.COMMENT_NODE:
					x = raw_input("Replace value %s at %s [y/n]? " % (float(num), n.previousSibling.previousSibling.nodeValue))
				else:
					x = raw_input("Replace value %s [y/n]? " % (float(num),))

				if x == "y":
					print "Ok, replacing"
					n.firstChild.firstChild.nodeValue = "NaN"
					break
				elif x == "n":
					break

# Now dump the output
rrdbak = "%s.bak" % rrdname
os.rename(rrdname, rrdbak)
p = Popen("rrdtool restore -r - %s" % rrdname, shell=True, stdin=PIPE)
dom.writexml(p.stdin)
p.stdin.flush()
p.stdin.close()
p.wait()

# Reset the owner and permissions to what they were before
s = os.stat(rrdbak)
os.chown(rrdname, s.st_uid, s.st_gid)
os.chmod(rrdname, s.st_mode)
