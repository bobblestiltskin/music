from django.shortcuts import get_object_or_404, get_list_or_404, render, HttpResponse
#from django.http import HttpResponse
from django.template import loader

from .models import Artist, Label, Format, Item

# Create your views here.
def index(request):
    item_list = Item.objects.order_by('-release_id')[:5]
#    template = loader.get_template('discogs/index.html')
    context = {'item_list': item_list}
#    return HttpResponse(template.render(context, request))
    return render(request, 'discogs/index.html', context)

#    output = ', '.join([q.catalogue_number for q in item_list])
#    return HttpResponse(output)

#    return HttpResponse("Hello, world. You're at the discogs index.")

#    catalogue_number = models.CharField(max_length=200)
#    artist = models.ForeignKey(Artist, on_delete=models.CASCADE)
#    title = models.CharField(max_length=200)
#    label = models.ForeignKey(Label, on_delete=models.CASCADE)
#    format = models.ForeignKey(Format, on_delete=models.CASCADE)
#    released = models.DateTimeField('date released')
#    release_id = models.IntegerField(default=0)

def artist_info(request, artist_id):
    artist = get_object_or_404(Artist, pk=artist_id)
#    try:
#        artist = Artist.objects.get(pk=artist_id)
#    except Artist.DoesNotExist:
#        raise Http404("Artist does not exist")
    return render(request, 'discogs/artist_info.html', {'artist': artist})

def artist_list(request):
#    return HttpResponse("You're looking at all of the artists")
#    artist_list = get_list_or_404(Artist, pk=artist_id)
    artist_list = get_list_or_404(Artist)
    return render(request, 'discogs/artist_list.html', {'artist_list': artist_list})

def items_for_artist(request, artist_id):
    response = "You're looking at the items for artist %s."
    return HttpResponse(response % artist_id)

def label_info(request, label_id):
    label = get_object_or_404(Label, pk=label_id)
#    try:
#        label = Label.objects.get(pk=label_id)
#    except Label.DoesNotExist:
#        raise Http404("Label does not exist")
    return render(request, 'discogs/label_info.html', {'label': label})

def label_list(request):
#    return HttpResponse("You're looking at all of the labels")
    label_list = get_list_or_404(Label)
    return render(request, 'discogs/label_list.html', {'label_list': label_list})

def items_for_label(request, label_id):
    response = "You're looking at the items for label %s."
    return HttpResponse(response % label_id)

def format_info(request, format_id):
    format = get_object_or_404(Format, pk=format_id)
#    try:
#        format = Format.objects.get(pk=format_id)
#    except Format.DoesNotExist:
#        raise Http404("Format does not exist")
    return render(request, 'discogs/format_info.html', {'format': format})

def format_list(request):
#    return HttpResponse("You're looking at all of the formats")
    format_list = get_list_or_404(Format)
    return render(request, 'discogs/format_list.html', {'format_list': format_list})

def items_for_format(request, format_id):
    response = "You're looking at the items for format %s."
    return HttpResponse(response % format_id)

def item_details(request, release_id):
    response = "You're looking at the details for item - id %s."
    return HttpResponse(response % release_id)
