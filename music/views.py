from django.shortcuts import render
from django.db import connection
import re
import os




from .models import Genre, Artist, Song

musicDir = "/media/jskills/Toshiba-2TB/"
coverImageDir = musicDir + "cover_art/"

###

def returnCoverUrl(song_id):
	cover_url = None
	coverFile = coverImageDir + str(song_id) + ".jpg"
	if os.path.exists(coverFile):
		cover_url = str(song_id) + ".jpg"

	return cover_url

###

def index(request):
	return render(request, 'music/index.html')

###


def artistPage(request, artist_id):
	a = Artist.objects.get(id=artist_id)

	cur = connection.cursor()
	sql = "select distinct(INITCAP(album)) as album from song where artist_id = %s"
	cur.execute(sql, [artist_id])
	sList = cur.fetchall()
	# fetchall sends back a list of tuples
	aList = list()
	for s in sList:
		d = dict()
		d['album'] = str(s[0])
		if d['album']:
			d['album_url'] = re.sub(' ', '_', d['album'])
		aList.append(d)

	templateData = {
		'album_list': aList,
		'artist_id': artist_id,
		'full_name': a.full_name	
	}

	return render(request, 'music/artist.html', templateData)

###

def albumPage(request, artist_id, album):
	a = Artist.objects.get(id=artist_id)

	album_name = re.sub('_', ' ', album)

	cur = connection.cursor()
	sql = "select * from song where artist_id = %s and LOWER(album) = LOWER(%s) order by track_number"
	cur.execute(sql, [artist_id, album_name])
	desc = cur.description
	column_names = [col[0] for col in desc]
	sList = [dict(zip(column_names, row)) for row in cur.fetchall()]

	cover_url = None
	for s in sList:
		cover_url = returnCoverUrl(s['id'])
		if cover_url:
			break

	templateData = {
		'song_list': sList,
		'album_name': album_name,
		'artist_id': artist_id,
                'full_name': a.full_name,
		'cover_url': cover_url
	}

	return render(request, 'music/album.html', templateData)

###

def songPage(request, song_id):
	s = Song.objects.get(id=song_id)
	a = Artist.objects.get(id=s.artist_id)

	cover_url = returnCoverUrl(s.id)

	templateData = {
		'song_object' : s,
		'artist_object' : a,
		'cover_url': cover_url
	}

	return render(request, 'music/song.html', templateData)


