#!/usr/bin/python3
#
'''
discogs csv file contains the following fields

Catalog# => WR007, ONUDP16, ON UDP16
Artist => Gary Clail And Tackhead
Title => Hard Left
Label => World Records, On-U Sound, On-U Sound
Format => 12"
Rating => 
Released => 1986
release_id => 176778
CollectionFolder => Uncategorized
Date Added => 2020-02-18 10:53:08
Collection Media Condition => Very Good Plus (VG+)
Collection Sleeve Condition => Very Good Plus (VG+)
Collection Notes => 

'''

import csv
import sys

def display(istring, collection):
  for a in sorted(collection):
    print("%s : %s" % (istring, a))
  print("Number of %ss is %d" % (istring, len(collection)))

# read the csv file passed as the first argument

csv_file = sys.argv[1]
csvfile=open(csv_file,'r', newline='')
obj=csv.DictReader(csvfile)

# define some sets we push our fields containing duplicates into

artists = set()
formats = set()
labels = set()
for row in obj:
  d=dict(row)
  for k in d.keys():
#    print ("%s => %s" % (k,d[k]))
    if k == "Artist":
      artists.add(d[k])
    elif k == "Format":
      formats.add(d[k])
    elif k == "Label":
      labels.add(d[k])
#    elif k == "release_id":
#      print ("%s => %s" % (k,d[k]))
#
#display("label", labels)
#display("artist", artists)
#display("format", formats)
