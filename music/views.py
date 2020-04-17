from django.http import Http404
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse

from .models import Genre, Artist, Song

def index(request):
	return render(request, 'music/index.html')

def artistPage(request, artist_id):
	alist = Song.objects.raw('select * from song where artist_id = %s', [artist_id])
	album_list = {
		'request': request,
		'album_list': alist
	}
	return render(request, 'music/artist.html', album_list)

	



