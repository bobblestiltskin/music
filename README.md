This repository is for managing music collections.

It takes as input a csv file which is generated from discogs.com collection
at https://www.discogs.com/users/export?w=collection

The fields of this discogs CSV file file contains the following fields

```
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
```

The csv file is read by the file, csv_read.py, and those fields relevant to me at home are
extracted. The program then normalises the data (artist, label and format) and stores
this normalised data to SQLite tables. The database is used as input to django which is
used to publish the data. It is currently functional and demonstrates my poor graphic
design capabilities, but it does return the data as intended with links back to discogs
and the search facility works, too.


```

$ cd src
$ git clone https://github.com/bobblestiltskin/music
$ cd music/music
$ pip3 install Django

$ python3 -m django --version # check the Django version
$ python3 manage.py migrate # this creates the db.sqlite file
$ sqlite3 db.sqlite3  # but it is empty when we select on the interesting table
$ python3 csv_read.py <path-to-my-csv-file>
$ sqlite3 db.sqlite3 # now the tables have the csv data
$ vi music/settings.py # set ALLOWED_HOSTS = ['*']
$ python3 manage.py runserver 0.0.0.0:8000 # make visible externally
```
