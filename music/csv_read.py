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
#    upd = "ALTER SEQUENCE %s_id RESTART WITH 1;" % db
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
 
def format_csv_to_db(format):
  csv_to_db_format = {
    '10"' : '10"',
    '10", Album, Cle' : '10"',
    '10", EP' : '10"',
    '10", RE' : '10"',
    '12"' : '12"',
    '12", Gre' : '12"',
    '12", Ltd' : '12"',
    '12", Ltd, Promo' : '12"',
    '12", Maxi' : '12"',
    '12", Promo, TP' : '12"',
    '12", RE' : '12"',
    '12", Sin' : '12"',
    '12", Single' : '12"',
    '12", Single, Pic' : '12"',
    '2x12", Promo' : '12"',
    '2x7", Single' : '7"',
    '2x7", Single, Gat' : '7"',
    '2xCD, Album, RE, RM' : 'CD',
    '2xCD, Album, Sli' : 'CD',
    '2xCD, Comp' : 'CD',
    '2xCD, Comp + CD, Mixed' : 'CD',
    '2xCD, Comp + DVD' : 'CD',
    '2xCD, Comp + DVD-V' : 'CD',
    '2xCD, Comp, Enh' : 'CD',
    '2xCD, Comp, Promo' : 'CD',
    '2xLP, Comp' : 'LP',
    '3xCD, Comp + Box' : 'CD',
    '3xCD, Comp + Box + Ltd' : 'CD',
    '3xLP, Comp + Box, Ltd' : 'LP',
    '4xCD, Album, RE + Box, Comp' : 'CD',
    '7"' : '7"',
    '7", EP' : '7"',
    '7", EP, RE' : '7"',
    '7", EP, Single, S/Edition, Sol' : '7"',
    '7", EP, ora' : '7"',
    '7", Gre' : '7"',
    '7", Maxi, Sol' : '7"',
    '7", Mono' : '7"',
    '7", RE' : '7"',
    '7", RE, Fol' : '7"',
    '7", Rou' : '7"',
    '7", Single' : '7"',
    '7", Single + 7", Single' : '7"',
    '7", Single, 2nd' : '7"',
    '7", Single, Air' : '7"',
    '7", Single, Bla' : '7"',
    '7", Single, CBS' : '7"',
    '7", Single, Cle' : '7"',
    '7", Single, Col' : '7"',
    '7", Single, Com' : '7"',
    '7", Single, Cop' : '7"',
    '7", Single, Fir' : '7"',
    '7", Single, Gat' : '7"',
    '7", Single, Gre' : '7"',
    '7", Single, Inj' : '7"',
    '7", Single, Kno' : '7"',
    '7", Single, M/Print, Bro' : '7"',
    '7", Single, MP' : '7"',
    '7", Single, Mono' : '7"',
    '7", Single, Mono, RE, Pus' : '7"',
    '7", Single, Mono, Sol' : '7"',
    '7", Single, Mus' : '7"',
    '7", Single, No ' : '7"',
    '7", Single, Ori' : '7"',
    '7", Single, Pap' : '7"',
    '7", Single, Pho' : '7"',
    '7", Single, Pin' : '7"',
    '7", Single, Pos' : '7"',
    '7", Single, Pus' : '7"',
    '7", Single, RE' : '7"',
    '7", Single, RE, Sol' : '7"',
    '7", Single, RP' : '7"',
    '7", Single, RP, 2nd' : '7"',
    '7", Single, RP, Sol' : '7"',
    '7", Single, Sil' : '7"',
    '7", Single, Sol' : '7"',
    '7", Single, Sta' : '7"',
    '7", Single, T\'a' : '7"',
    '7", Single, Tex' : '7"',
    '7", Single, WEA' : '7"',
    'Box + 3xCD, Comp' : 'Box',
    'Box, Ltd + CD, Album + CD, Comp + DVD-V, Copy Prot' : 'Box',
    'CD' : 'CD',
    'CD, Album' : 'CD',
    'CD, Album, Comp' : 'CD',
    'CD, Album, Enh' : 'CD',
    'CD, Album, Mixed' : 'CD',
    'CD, Album, RE' : 'CD',
    'CD, Album, RE, RM' : 'CD',
    'CD, Album, RE, RM, Bon' : 'CD',
    'CD, Album, RE, RM, Gre' : 'CD',
    'CD, Album, RE, RM, Sli' : 'CD',
    'CD, Album, RM' : 'CD',
    'CD, Album, RP' : 'CD',
    'CD, Comp' : 'CD',
    'CD, Comp, Promo' : 'CD',
    'CD, Comp, Promo, Gat' : 'CD',
    'CD, Comp, RE' : 'CD',
    'CD, Comp, Rei' : 'CD',
    'CD, Comp, Sli' : 'CD',
    'Cass, Album' : 'Cass',
    'Cass, Single' : 'Cass',
    'Cass, Single, Yel' : 'Cass',
    'Flexi, 7", S/Sided' : 'Flexi',
    'Flexi, 7", Shape, S/Sided, Sil' : 'Flexi',
    'LP' : 'LP',
    'LP, Album' : 'LP',
    'LP, Album + 7", EP' : 'LP',
    'LP, Album, Ltd, RE, 180' : 'LP',
    'LP, Album, RE' : 'LP',
    'LP, Album, RE + 7", Single' : 'LP',
    'LP, Album, RE, Gat' : 'LP',
    'LP, Album, RE, RM + LP, Comp, RM' : 'LP',
    'LP, Album, RE, RM, 180' : 'LP',
    'LP, Comp' : 'LP',
    'LP, Comp, RE' : 'LP',
    'LP, MiniAlbum' : 'LP',
    'LP, RE' : 'LP',
    'LP, RE, RM + LP, Comp, RM' : 'LP',
  }
  return csv_to_db_format[format]

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
      formats.add(format_csv_to_db(d[k]))
    elif k == "Label":
      labels.add(d[k])
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
      for_id = get_id(cur, "discogs_format", "format", format_csv_to_db(d[k]))
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
