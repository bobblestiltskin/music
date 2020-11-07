from django.shortcuts import get_object_or_404, get_list_or_404, render, HttpResponse
from django.template import loader, Context, Template

from .models import Artist, Label, Format, Item

import re

def index(request):
    item_list = Item.objects.order_by('-release_id')[:5]
    context = {'item_list': item_list}
    return render(request, 'discogs/index.html', context)

#    catalogue_number = models.CharField(max_length=200)
#    artist = models.ForeignKey(Artist, on_delete=models.CASCADE)
#    title = models.CharField(max_length=200)
#    label = models.ForeignKey(Label, on_delete=models.CASCADE)
#    format = models.ForeignKey(Format, on_delete=models.CASCADE)
#    released = models.DateTimeField('date released')
#    release_id = models.IntegerField(default=0)

def artist_info(request, artist_id):
    artist_list = get_list_or_404(Item, artist=artist_id)
    item_list = []
    for artist in artist_list:
      item_list.append({'catalogue_number' : artist.catalogue_number, 'label' : artist.label, 'title' : artist.title, 'format' : artist.format, 'release_id' : artist.release_id})
    artist = get_object_or_404(Artist, pk=artist_id)
    sartist = str(artist)
    partist=re.sub("\s+", "+", sartist)
    artist_hash={'name' : sartist, 'regexp' : partist, 'item_list' : item_list}
    return render(request, 'discogs/artist_info.html', artist_hash)

def artist_list(request):
    artist_list = get_list_or_404(Artist)
    artist_hash_list=[]
    for artist in artist_list:
      sartist = str(artist)
      partist=re.sub("\s+", "+", sartist)
      artist_hash={'name' : sartist, 'regexp' : partist, 'id' : artist.id}
      artist_hash_list.append(artist_hash)
    return render(request, 'discogs/artist_list.html', {'artist_hash_list' : artist_hash_list})

def items_for_artist(request, artist_id):
    response = "You're looking at the items for artist %s."
    return HttpResponse(response % artist_id)

def label_info(request, label_id):
    label = get_object_or_404(Label, pk=label_id)
    return render(request, 'discogs/label_info.html', {'label': label})

def label_list(request):
    label_list = get_list_or_404(Label)
    return render(request, 'discogs/label_list.html', {'label_list': label_list})

def items_for_label(request, label_id):
    response = "You're looking at the items for label %s."
    return HttpResponse(response % label_id)

def format_info(request, format_id):
    format = get_object_or_404(Format, pk=format_id)
    return render(request, 'discogs/format_info.html', {'format': format})

def format_list(request):
    format_list = get_list_or_404(Format)
    return render(request, 'discogs/format_list.html', {'format_list': format_list})

def items_for_format(request, format_id):
    response = "You're looking at the items for format %s."
    return HttpResponse(response % format_id)

def item_details(request, release_id):
    response = "You're looking at the details for item - id %s."
    return HttpResponse(response % release_id)
