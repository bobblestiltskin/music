this repository is for managing music collections.

It takes as input a csv file which is generated from discogs.com collection
at https://www.discogs.com/users/export?w=collection

The fields of this discogs CSV file file contains the following fields

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

The csv file is read by the file, csv_read.py, and those fields relevant to me at home are
extracted. The program then normalises the data (artist, label and format) and stores
this normalised data to SQLite tables. The database is used as input to django which is
used to publish the data. It is currently functional and demonstrates my poor graphic
design capabilities, but it does return the data as intended with links back to discogs
and the search facility works, too.

I will next work on providing both PostgreSQL and MySQL interfaces both for csv_read.py
and the django front-end, so they can be used instead of SQLite.

I have a couple of hundred items in my CSV file, and I think that the easiest way of
cataloguing all of the music is by utilising the discogs collection facility, since
it will involve a lot less typing than any other method. I will go into data entry
phase after adding the two other database interfaces. I will tidy this code base after
deploying to my public facing webserver ...
