from django import forms
from django.shortcuts import get_object_or_404, get_list_or_404
from .models import Artist, Label, Format, Item

# Create your forms here.

class SearchForm(forms.Form):
    artist_choice = forms.ModelChoiceField(queryset = Artist.objects.all(), required=False)
    label_choice = forms.ModelChoiceField(queryset = Label.objects.all(), required=False)
    format_choice = forms.ModelChoiceField(queryset = Format.objects.all(), required=False)
#    text_choice = forms.CharField(required=False)
