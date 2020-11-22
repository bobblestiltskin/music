#!/usr/bin/python3

'''
this program takes as input a csv file which is generated from discogs.com collection at https://www.discogs.com/users/export?w=collection
and populates an SQLite database comprising 4 tables : "discogs_artist", "discogs_format", "discogs_label", "discogs_item"

the tables are cleaned prior to insertion - the items table uses the other 3 tables as foreign keys

django was used to create the tables - see https://github.com/bobblestiltskin/music/blob/main/music/discogs/models.py

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

import argparse
import csv
import re
import sqlite3
import sys

def display(istring, collection):
#  for a in sorted(collection):
#    print("%s : %s" % (istring, a))
  print("Number of %ss is %d" % (istring, len(collection)))

def clean_tables(dbtype, cur, db):
  dlt = "delete from %s" % db
  cur.execute(dlt)
  if dbtype == "sqlite":
    upd = "UPDATE `sqlite_sequence` SET `seq` = 0 WHERE `name` = '%s'" % db
  elif dbtype == "postgresql":
    upd = "ALTER SEQUENCE %ss_id_seq RESTART;" % db
  cur.execute(upd)

def clean_db(dbtype, cur):
  clean_tables(dbtype, cur, "discogs_artist")
  clean_tables(dbtype, cur, "discogs_format")
  clean_tables(dbtype, cur, "discogs_label")
  clean_tables(dbtype, cur, "discogs_item")

def insert(dbtype, cur, db, field, collection):
  if dbtype == "sqlite":
    for a in sorted(collection):
      ins = "insert into %s(%s) values(?);" % (db, field)
      cur.execute(ins, (a,))
  elif dbtype == "postgresql":
    for a in sorted(collection):
      a=re.sub("'", "''", a)
      ins = "insert into %s(%s) values('%s');" % (db, field, a)
      cur.execute(ins)

def get_id(cur, db, field, value):
  if dbtype == "sqlite":
    get = "select id from %s where %s=?" % (db, field)
    cur.execute(get, (value,))
  elif dbtype == "postgresql":
    value=re.sub("'", "''", value)
    get = "select id from %s where %s='%s'" % (db, field, value)
    cur.execute(get)
  row = cur.fetchone()
  return row[0]
 
def clean_label(input):
  if args.clean_label_numbers:
    output = re.sub("\(\d+\)\s*$", "", input)
    output = re.sub("\(\d+\),", ",", output)
  else:
    output = input

  return output

def clean_artist(input):
  if args.clean_artist_numbers:
    output = re.sub("\(\d+\)\s*$", "", input)
    output = re.sub("\s+\(\d+\)\s+", " ", output)
  else:
    output = input

  return output

def clean_format(input):
  if args.clean_formats:
    output=re.sub(",.*", "", input)
    output=re.sub("^\d+x", "", output)
    output=re.sub(" \+.*", "", output)
  else:
    output = input

  return output

parser = argparse.ArgumentParser(description='Convert discogs.com collection CSV file to SQL tables.')
parser.add_argument('csv_file', metavar='CSV_filename', nargs='?', help='collections CSV file from discogs.com')
parser.add_argument('--dbtype', default='sqlite', nargs='?', choices=['sqlite', 'postgresql', 'mysql'], help='type of database')
parser.add_argument('--dbpasswd', nargs='?', help='database password')
parser.add_argument('--clean_artist_numbers', action='store_true', help='Clean bracketed numbers in artists')
parser.add_argument('--clean_label_numbers', action='store_true', help='Clean bracketed numbers in labels')
parser.add_argument('--clean_formats', action='store_true', help='Consolidate formats')

args = parser.parse_args()
print(args)

dbtype = args.dbtype
csvfile=open(args.csv_file,'r', newline='')
obj=csv.DictReader(csvfile)

# define some sets we push our fields containing duplicates into

id = set()
artists = set()
formats = set()
labels = set()
items = []
for row in obj:
  add = True
  d=dict(row)
  for k in d.keys():
#    print ("%s => %s" % (k,d[k]))
    if k == "Artist":
      artists.add(clean_artist(d[k]))
    elif k == "Format":
      formats.add(clean_format(d[k]))
    elif k == "Label":
      labels.add(clean_label(d[k]))
    elif k == "release_id":
      if d[k] in id: # filter out any duplicates
        add = False
      else:
        id.add(d[k])
  if (add):
    items.append(row)

display("label", labels)
display("artist", artists)
display("format", formats)

if dbtype == "sqlite":
  conn = sqlite3.connect('./db.sqlite3')
elif dbtype == "postgresql":
  import psycopg2
  conn = psycopg2.connect(
    host="localhost",
    database="discogs",
    user="discogs",
    password=args.dbpasswd)

print('Connected to %s database successfully.' % dbtype)
cur = conn.cursor()

clean_db(dbtype, cur)

insert(dbtype, cur, "discogs_artist", "artist", artists)
insert(dbtype, cur, "discogs_format", "format", formats)
insert(dbtype, cur, "discogs_label", "label", labels)
#
# now we insert the normalised data into the item table
#
for row in items:
  d=dict(row)
  for k in d.keys():
    if k == "Artist":
      art_id = get_id(cur, "discogs_artist", "artist", clean_artist(d[k]))
    elif k == "Format":
      for_id = get_id(cur, "discogs_format", "format", clean_format(d[k]))
    elif k == "Label":
      lab_id = get_id(cur, "discogs_label", "label", clean_label(d[k]))
  if dbtype == "sqlite":
    ins = "insert into discogs_item(catalogue_number, title, released, release_id, artist_id, format_id, label_id) values(?, ?, ?, ?, ?, ?, ?)"
    vals = (d["Catalog#"], d["Title"], d["Released"], d["release_id"], art_id, for_id, lab_id)
    cur.execute(ins, vals)
  elif dbtype == "postgresql":
    title=re.sub("'", "''", d["Title"])
    ins = "insert into discogs_item(catalogue_number, title, released, release_id, artist_id, format_id, label_id) values('%s', '%s', '%s', '%s', '%s', '%s', '%s')" % (d["Catalog#"], title, d["Released"], d["release_id"], art_id, for_id, lab_id)
    cur.execute(ins)

print('inserted to database successfully.')
conn.commit()
conn.close()
