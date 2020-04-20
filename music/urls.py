from django.contrib import admin
from django.urls import path
from . import views

admin.site.site_header = 'Music Database Administration'

app_name = 'music'

urlpatterns = [
	# e.g. /music/
	path('', views.index, name='index'),
	#path('artist/', views.artist, name='artist'),
	# e.g. /music/artist/1/
	path('artist/<int:artist_id>/', views.artistPage, name='artistPage'),
	# e.g. /music/album/1/Dirt
	path('album/<int:artist_id>/<slug:album>/', views.albumPage, name='albumPage'),
	# e.g. /music/song/1/
	path('song/<int:song_id>/', views.songPage, name='songPage'),
]

