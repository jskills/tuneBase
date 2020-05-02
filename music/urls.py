from django.contrib import admin
from django.urls import path
from . import views

admin.site.site_header = 'Music Database Administration'

app_name = 'music'

urlpatterns = [
	# Site Index
	path('', views.index, name='index'),
	# /music/

	# Bio Page
	path('bio/', views.bioPage, name='bioPage'),
	# /music/bio/

	# Artist Page
	path('artist/<int:artist_id>/', views.artistPage, name='artistPage'),
	# /music/artist/1

	# Album Page
	path('album/<int:artist_id>/<slug:album>/', views.albumPage, name='albumPage'),
	# /music/album/1/Dirt/

	# Song Page
	path('song/<int:song_id>/', views.songPage, name='songPage'),
	# /music/song/1/

	# PlayList Index Page
	path('mixtape/', views.playlistIndex, name='playlistIndex'),
	# /music/mixtape/

	# Video Index Page
	path('videos/', views.videoIndex, name='videoIndex'),
	# /music/videos/

	# Past Gigs Index Page
	path('shows/', views.liveSetIndex, name='liveSetIndex'),
	# /music/shows/

	# Playlist Page
	path('mixtape/<slug:playlist_file>/', views.playlistPage, name='playlistPage'),
	# /music/mixtape/Kind_Jim/

	# Video Page
	path('videos/<slug:video_file>/', views.videoPage,  name='videoPage'),
	# /music/videos/2020-05-01_20-29-53.mp4

	# Genre Index Page
	path('genre/', views.genreIndex, name='genreIndex'),
	# /music/genre/

	# Genre Page
	path('genre/<int:genre_id>/', views.genrePage, name='genrePage'),
	# /music/genre/29/

	# Live Stream Page
	path('live/', views.livePage, name='livePage'),
	# /music/live

	# Search Page
	path('search/', views.searchPage, name='searchPage')
	# /music/search/ (with POSTED value for "searchTerm"
]

