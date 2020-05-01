from django.shortcuts import render
from django.db import connection
from django.views.decorators.csrf import csrf_exempt,csrf_protect
import m3u8
import glob
import re
import os




from .models import Genre, Artist, Song, Playlist

musicDir = "/media/jskills/Toshiba-2TB/"
coverImageDir = musicDir + "cover_art/"

###

def returnCoverUrl(song_id, useDefault=False):
	cover_url = None

	if useDefault:
		cover_url = "1.jpg"

	coverFile = coverImageDir + str(song_id) + ".jpg"
	if os.path.exists(coverFile):
		cover_url = str(song_id) + ".jpg"

	return cover_url

###

def getPlaylistSongs(filename):
	read_file = musicDir + filename + ".m3u"

	m3u8_obj = m3u8.load(read_file)

	return m3u8_obj.files

###

def index(request):
	return render(request, 'music/index.html')

###

def bioPage(request):
	return render(request, 'music/bio.html')

###

def livePage(request):
        return render(request, 'music/live.html')

###


def artistPage(request, artist_id):
	a = Artist.objects.get(id=artist_id)
	aList = a.getUniqueAlbums(artist_id)
	sList = Song.objects.filter(artist=artist_id)

	templateData = {
		'album_list': aList,
		'song_list' : sList,
		'artist_id': artist_id,
		'full_name': a.full_name,
		'total_songs' : sList.count() 
	}

	return render(request, 'music/artist.html', templateData)

###

def albumPage(request, artist_id, album):
	a = Artist.objects.get(id=artist_id)

	album_name = re.sub('_', ' ', album)

	sList = a.getAlbumSongs(artist_id, album_name)

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

###

def playlistPage(request, playlist_file):

	playlist_title = re.sub('_', ' ', playlist_file)

	file_path = playlist_file + ".m3u"
	playlist_files = getPlaylistSongs(playlist_file)

	playlist_songs = list()


	for file_path in playlist_files:
		file_path = re.sub('\\\\', '/', file_path)
		cur = connection.cursor()
		sql = "select s.id as song_id, full_name, song_name, file_path from song s, artist a"
		sql += " where file_path = %s and s.artist_id = a.id"
		cur.execute(sql, [file_path])
		desc = cur.description
		column_names = [col[0] for col in desc]
		sList = [dict(zip(column_names, row)) for row in cur.fetchall()]
		for sl in sList:
			#sl['song_name'] = re.sub('\]', '', sl['song_name'])
			#sl['song_name'] = re.sub('\[', '', sl['song_name'])
			#sl['full_name'] = re.sub('\]', '', sl['full_name'])
			#sl['full_name'] = re.sub('\[', '', sl['full_name'])
			sl['cover_url'] = returnCoverUrl(sl['song_id'], useDefault=True)
			playlist_songs.append(sl)

	templateData = {
		'playlist_title': playlist_title,
		'playlist_songs': playlist_songs
	}

	return render(request, 'music/playlist.html', templateData)

###

def playlistIndex(request):
	
	plList = glob.glob(musicDir + "/*.m3u")
	plList.sort(key=os.path.getmtime, reverse=True)

	playlists = list()

	for p in plList:
		d = dict()
		# get filename - everything after the trailing slash
		d['url'] = p.rsplit('/', 1)[-1]
		d['url'] = re.sub('.m3u', '', d['url'])
		d['name'] = d['url']
		d['name'] = re.sub('_', ' ', d['name'])
		d['name'] = d['name'].title()
		playlists.append(d)

	templateData = {
		'contentList': playlists,
		'sectionName': 'Play Lists',
		'slug': 'mixtape'	
	}

	return render(request, 'music/section.html', templateData)

###


def genreIndex(request):

	genreList = Genre.objects.all().order_by('genre_name')
	gList = list()
	for g in genreList:
		d = dict()
		d['name'] = g.genre_name
		d['url'] = g.id
		gList.append(d)

	templateData = {
		'contentList': gList,
		'sectionName': 'Genres',
		'slug': 'genre'	
	}

	return render(request, 'music/section.html', templateData)

###

def genrePage(request, genre_id):

	g = Genre.objects.get(id=genre_id)

	aList = g.getGenreArtists(genre_id)

	templateData = {
		'contentList': aList,
		'sectionName': 'Genre : ' + g.genre_name,
		'slug': 'artist'	
	}

	return render(request, 'music/section.html', templateData)

###

def liveSetIndex(request):

	liveSets = Playlist.objects.filter(live_ind=True).order_by('last_updated_date')

	playLists = list()

	for ls in liveSets:
		d = dict()
		d['name'] = ls.title
		d['url'] = ls.file_path.rsplit('/', 1)[-1]
		d['url'] = re.sub('.m3u', '', d['url'])
		d['live_ind'] = ls.live_ind
		playLists.append(d)	

	templateData = {
		'contentList' : playLists,
		'sectionName' : 'Past Gigs',
		'slug' : 'mixtape'
	}

	return render(request, 'music/shows.html', templateData)

###

@csrf_exempt
def searchPage(request):

	searchText = request.POST['search_text']

	searchDict = dict()

	s = Song()

	if searchText:
		searchDict = s.multiSearch(searchText)

	noneFound = False

	if not searchDict:
		noneFound = True

	templateData = {
		'song_list' : searchDict['songList'],
		'album_list' : searchDict['albumList'],
		'artist_list' : searchDict['artistList'],
		'pl_list' : searchDict['plList'],
		'search_text' : searchText
	}

	return render(request, 'music/search.html', templateData)

###
