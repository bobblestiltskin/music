from django.urls import path

from . import views

app_name = 'discogs'
urlpatterns = [
    # ex: /discogs/
    path('', views.index, name='index'),
    # ex: /discogs/search
    path('search/', views.index_search, name='index_search'),
    #path('search/<int:artist_id>', views.index_search, name='index_search'),
    # ex: /discogs/artist/
    path('artist/', views.artist_list, name='artist_list'),
    # ex: /discogs/artist/search/regexp/
    path('artist/search/<str:artist_regexp>/', views.artist_for_regexp, name='artist_for_regexp'),
    # ex: /discogs/artist/5/
    path('artist/<int:artist_id>/', views.artist_info, name='artist_info'),
    # ex: /discogs/artist/list/5/
    path('artist/list/<int:artist_id>/', views.items_for_artist, name='items_for_artist'),
    # ex: /discogs/label/
    path('label/', views.label_list, name='label_list'),
    # ex: /discogs/label/5/
    path('label/<int:label_id>/', views.label_info, name='label_info'),
    # ex: /discogs/label/list/5/
    path('label/list/<int:label_id>/', views.items_for_label, name='items_for_label'),
    # ex: /discogs/format/
    path('format/', views.format_list, name='format_list'),
    # ex: /discogs/format/5/
    path('format/<int:format_id>/', views.format_info, name='format_info'),
    # ex: /discogs/format/list/5/
    path('format/list/<int:format_id>/', views.items_for_format, name='items_for_format'),
    # ex: /discogs/5/
    path('<int:release_id>/', views.item_details, name='item_details'),
]
