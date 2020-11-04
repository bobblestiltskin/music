from django.contrib import admin

# Register your models here.

from django.contrib import admin

from .models import Artist, Format, Label, Item

admin.site.register(Artist)
admin.site.register(Format)
admin.site.register(Label)
admin.site.register(Item)
