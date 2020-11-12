from django.db import models

# Create your models here.

from django.db import models

class Artist(models.Model):
    artist = models.CharField(max_length=200)
    def __str__(self):
        return self.artist

class Format(models.Model):
    format = models.CharField(max_length=200)
    def __str__(self):
        return self.format

class Label(models.Model):
    label = models.CharField(max_length=200)
    def __str__(self):
        return self.label

class Item(models.Model):
    catalogue_number = models.CharField(max_length=200)
    artist = models.ForeignKey(Artist, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    label = models.ForeignKey(Label, on_delete=models.CASCADE)
    format = models.ForeignKey(Format, on_delete=models.CASCADE)
    released = models.CharField(max_length=6)
    release_id = models.IntegerField(default=0)
    def __str__(self):
        item_tuple = (self.catalogue_number, self.label.label, self.artist.artist, self.title, self.format.format, self.released)
        return "<tr><td>" + "</td><td>".join(item_tuple) + "</td></tr>"
