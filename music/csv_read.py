#!/usr/bin/python3
#
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
 
# read the csv file passed as the first argument

if len(sys.argv) < 2:
  print("Need to pass the full path of the discogs csv file or import")
  sys.exit(-1);
  
dbtype = "sqlite"
if len(sys.argv) == 3:
  dbtype = sys.argv[2];

valid_dbtypes = ('sqlite', 'postgresql', 'mysql')
if dbtype not in valid_dbtypes:
  print ("Valid DG types are ", valid_dbtypes)
  sys.exit(-1);

print("dbtype is %s" % dbtype)

csv_file = sys.argv[1]
csvfile=open(csv_file,'r', newline='')
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
      artists.add(d[k])
    elif k == "Format":
      formats.add(d[k])
    elif k == "Label":
      labels.add(d[k])
    elif k == "release_id":
      if d[k] in id:
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
    password="this is really really secret so you will never guess it!")

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
      art_id = get_id(cur, "discogs_artist", "artist", d[k])
    elif k == "Format":
      for_id = get_id(cur, "discogs_format", "format", d[k])
    elif k == "Label":
      lab_id = get_id(cur, "discogs_label", "label", d[k])
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
