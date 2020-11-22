from django.shortcuts import get_object_or_404, get_list_or_404, render, HttpResponse, HttpResponseRedirect
from django.template import loader, Context, Template

#from admin.models import Choice
from .models import Artist, Label, Format, Item

from .forms import SearchForm

#    catalogue_number = models.CharField(max_length=200)
#    artist = models.ForeignKey(Artist, on_delete=models.CASCADE)
#    title = models.CharField(max_length=200)
#    label = models.ForeignKey(Label, on_delete=models.CASCADE)
#    format = models.ForeignKey(Format, on_delete=models.CASCADE)
#    released = models.DateTimeField('date released')
#    release_id = models.IntegerField(default=0)

import re

def index(request):
    form = SearchForm()
    context = {'form' : form}
    return render(request, 'discogs/index.html', context)

def collate_item_list(item_list):
    output_list = []
    for item in item_list:
      output_list.append({'catalogue_number' : item.catalogue_number, 'artist' : item.artist, 'label' : item.label, 'title' : item.title, 'format' : item.format, 'released' : item.released, 'release_id' : item.release_id})
    return output_list

def index_search(request):
    artist_id = request.POST['artist_choice']
    label_id = request.POST['label_choice']
    format_id = request.POST['format_choice']
#    text = request.POST['text_choice']

    item_list = Item.objects.order_by('artist')

    if artist_id:
      item_list = item_list.filter(artist=artist_id)

    if label_id:
      item_list = item_list.filter(label=label_id)

    if format_id:
      item_list = get_list_or_404(item_list, format=format_id)
    else:
      item_list = get_list_or_404(item_list)

    output_list = collate_item_list(item_list)
    return render(request, 'discogs/search_results.html', {'output_list' : output_list})

def type_list(request, object, file, hash_name):
    type_list = get_list_or_404(object)
    type_hash_list=[]
    for type in type_list:
      stype = str(type)
      ptype=re.sub("\s+", "+", stype)
      ptype1=re.sub("/", "%2F", ptype)
      type_hash={'name' : stype, 'regexp' : ptype1, 'id' : type.id}
      type_hash_list.append(type_hash)
    return render(request, 'discogs/' + file + '.html', {hash_name : type_hash_list})

def artist_for_regexp(request, artist_regexp):
    response = "https://www.discogs.com/search/?type=artist&title=%s"
    return HttpResponseRedirect(response % artist_regexp)

def artist_info(request, artist_id):
    artist_list = get_list_or_404(Item, artist=artist_id)
    item_list = []
    for artist in artist_list:
      item_list.append({'catalogue_number' : artist.catalogue_number, 'label' : artist.label, 'title' : artist.title, 'format' : artist.format, 'released' : artist.released, 'release_id' : artist.release_id})
    artist = get_object_or_404(Artist, pk=artist_id)
    sartist = str(artist)
    partist=re.sub("\s+", "+", sartist)
    partist1=re.sub("/", "%2F", partist)
    artist_hash={'name' : sartist, 'regexp' : partist1, 'item_list' : item_list}
    return render(request, 'discogs/artist_info.html', artist_hash)

def artist_list(request):
    return type_list(request, Artist, "artist_list", "artist_hash_list")

def items_for_artist(request, artist_id):
    item_list = get_list_or_404(Item, artist=artist_id)
    output_list = collate_item_list(item_list)
    return render(request, 'discogs/search_results.html', {'output_list' : output_list})

def label_for_regexp(request, label_regexp):
    response = "https://www.discogs.com/search/?type=label&title=%s"
    return HttpResponseRedirect(response % label_regexp)

def label_info(request, label_id):
    label_list = get_list_or_404(Item, label=label_id)
    item_list = []
    for label in label_list:
      item_list.append({'catalogue_number' : label.catalogue_number, 'artist' : label.artist, 'title' : label.title, 'format' : label.format, 'released' : label.released, 'release_id' : label.release_id})
    label = get_object_or_404(Label, pk=label_id)
    slabel = str(label)
    plabel=re.sub("\s+", "+", slabel)
    plabel1=re.sub("/", "%2F", plabel)
    label_hash={'name' : slabel, 'regexp' : plabel1, 'item_list' : item_list}
    return render(request, 'discogs/label_info.html', label_hash)

def label_list(request):
    return type_list(request, Label, "label_list", "label_hash_list")

def items_for_label(request, label_id):
    item_list = get_list_or_404(Item, label=label_id)
    output_list = collate_item_list(item_list)
    return render(request, 'discogs/search_results.html', {'output_list' : output_list})

def format_info(request, format_id):
    format = get_object_or_404(Format, pk=format_id)
    return render(request, 'discogs/format_info.html', {'format': format})

def format_list(request):
    format_list = get_list_or_404(Format)
    return render(request, 'discogs/format_list.html', {'format_list': format_list})

def items_for_format(request, format_id):
    item_list = get_list_or_404(Item, label=label_id)
    output_list = collate_item_list(item_list)
    return render(request, 'discogs/search_results.html', {'output_list' : output_list})

def item_details(request, release_id):
    response = "https://www.discogs.com/release/%s"
    return HttpResponseRedirect(response % release_id)
