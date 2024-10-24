from django.shortcuts import render
from django.db import connection
from django.views.decorators.csrf import csrf_exempt,csrf_protect
import m3u8
import glob
import re
import os
import urllib.parse
from datetime import datetime, timezone
from configparser import ConfigParser

# app based library includes
from .models import Genre, Artist, Song, Playlist, Show, Video, Image

###

def config(filename, section):
        filename = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + '/' + section + '/' + filename
        parser = ConfigParser()
        parser.read(filename)

        conf = {}
        if parser.has_section(section):
                params = parser.items(section)
                for param in params:
                        conf[param[0]] = param[1]
        else:
                raise Exception('Section {0} not found in the {1} file'.format(section, filename))
        return conf

###

# globals - should refactor this
params = config('music.ini', 'music')
musicDir = params['dir']
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

    returnList = list()

    try:
        # Attempt to load using m3u8 library
        m3u8_obj = m3u8.load(read_file)
        returnList = m3u8_obj.files
    except Exception as e:
        # Log the exception for debugging
        print(f"Error loading playlist with m3u8: {e}")
        
        # Fallback to manual file reading with encoding handling
        try:
            with open(read_file, encoding='utf-8', errors='replace') as f:
                plText = f.readlines()

            for line in plText:
                line = line.strip()  # Remove extra whitespace/newlines
                if line and not line.startswith("#"):  # Ignore comments and empty lines
                    returnList.append(line)

        except UnicodeDecodeError as ude:
            print(f"Unicode error reading file {filename}: {ude}")
        except Exception as e:
            print(f"General error reading file {filename}: {e}")

    return returnList


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

    sList = list()
    cover_url = None

    album_name = re.sub('_', ' ', album)

    if album_name == 'NO ALBUM':
        sList = a.getAlbumlessSongs(artist_id)
    else:
        album_lookup = urllib.parse.unquote(album_name)
        sList = a.getAlbumSongs(artist_id, album_lookup)
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

def playlistPage(request, playlist_slug):

    playlist_file = playlist_title = file_path = None

    # allow for lookup of playlists by ID or filename
    try:
        p = Playlist.objects.get(id=playlist_slug)
        playlist_title = p.title
        file_path = p.file_path
        playlist_file = re.sub(' ', '_', playlist_title)
    except:
        playlist_title = re.sub('_', ' ', playlist_slug)
        file_path = playlist_slug + ".m3u"
        playlist_file = playlist_slug

    playlist_files = getPlaylistSongs(playlist_file)

    playlist_songs = list()
    hourlySongs = [0] * (len(playlist_files) + 20)
    hourlyList = list()
    genreDict = dict()
    totalSongs = totalSecs = minCnt = 0
    hrsCnt = 1
    totalTime = ''
    genreBreakdown = list()


    for file_path in playlist_files:
        file_path = re.sub('\\\\', '/', file_path)
        cur = connection.cursor()
        sql = "select s.id as song_id, full_name, song_name, file_path, duration, genre_name "
        sql += " from song s, artist a, genre g"
        sql += " where file_path = %s and s.artist_id = a.id and s.genre_id = g.id"
        cur.execute(sql, [file_path])
        desc = cur.description
        column_names = [col[0] for col in desc]
        sList = [dict(zip(column_names, row)) for row in cur.fetchall()]
        for sl in sList:
            sl['song_name'] = re.sub('\]', '', sl['song_name'])
            sl['song_name'] = re.sub('\[', '', sl['song_name'])
            sl['full_name'] = re.sub('\]', '', sl['full_name'])
            sl['full_name'] = re.sub('\[', '', sl['full_name'])
            sl['cover_url'] = returnCoverUrl(sl['song_id'], useDefault=True)

            totalSongs += 1
            totalSecs += sl['duration']

            if sl['genre_name'] in genreDict:
                genreDict[sl['genre_name']] += sl['duration']
            else:
                genreDict[sl['genre_name']] = sl['duration']

            minCnt +=  sl['duration']/60
            if minCnt >= 60:
                minCnt = 0
                hrsCnt += 1
                hourlySongs[hrsCnt] = hourlyList
                hourlyList = list()
            else:
                hourlyList.append(sl)
            
            playlist_songs.append(sl)

    # add final hour
    hrsCnt += 1
    hourlySongs[hrsCnt] = hourlyList
    


    totalTime = 0
    hrsCnt = totalSecs // 3600  # Get total hours
    calc_mins = (totalSecs % 3600) // 60  # Get remaining minutes after hours
    totalTime = f"{hrsCnt} hours {calc_mins} minutes"

    for g in genreDict:
        gpct = round((genreDict[g]/totalSecs) * 100, 1)
        genreBreakdown.append(str(g) + ' : ' + str(gpct) + '%')

            

    templateData = {
        'raw_data': sList,
        'playlist_title': playlist_title,
        'playlist_songs': playlist_songs,
        'hourly_songs': hourlySongs,
        'genre_breakdown': genreBreakdown,
        'total_time': totalTime
    }

    return render(request, 'music/playlist.html', templateData)

###

def playlistIndex(request):
    
    plList = glob.glob(musicDir + "/*.m3u")
    plList.sort(key=os.path.getmtime, reverse=True)

    playlists = list()

    for p in plList:
        d = dict()
        # get file attributes
        stat = os.stat(p)
        d['date'] = datetime.fromtimestamp(stat.st_mtime)
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

def videoIndex(request):

    vList = glob.glob(musicDir + "/videos/*.mp4")
    vList.sort(key=os.path.getmtime, reverse=True)

    videoList = list()

    for v in vList:
        d = dict()
        # get filename - everything after the trailing slash
        d['url'] = v.rsplit('/', 1)[-1]
        d['url'] = re.sub('.mp4', '', d['url'])
        d['url'] = re.sub(' ', '_', d['url'])
        d['name'] = d['url']
        d['name'] = re.sub('_', ' ', d['name'])
        d['name'] = d['name'].title()
        videoList.append(d)

    templateData = {
        'contentList': videoList,
        'sectionName': 'Videos',
        'slug': 'videos'
    }

    return render(request, 'music/section.html', templateData)      

###


def videoPage(request, video_slug):

    v = None

    # allow for lookup of videos by ID or filename
    try:
        v = Video.objects.get(id=video_slug)
    except:
        v = dict()
        v['title'] =  re.sub('_', ' ', video_slug)
        v['file_path'] = "/videos/" + video_slug + ".mp4"

    templateData = {
        'content' : v
    }

    return render(request, 'music/video.html', templateData)

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

def showIndex(request):

    showList = Show.objects.all().order_by('-show_date')
    sList = list()
    for s in showList:
        d = dict()
        d['name'] = s.title
        d['url'] = s.id
        d['date'] = s.show_date
        d['location'] = s.location
        sList.append(d)

    templateData = {
        'contentList': sList,
        'sectionName': 'Shows',
        'slug': 'shows' 
    }

    return render(request, 'music/section.html', templateData)

###

def showPage(request, show_id):

    s = Show.objects.get(id=show_id)

    vList = s.getShowVideos(show_id)
    iList = s.getShowImages(show_id)

    pl = Playlist.objects.get(id=s.playlist_id)
    p_url = pl.title
    p_url = pl.file_path.rsplit('/', 1)[-1]
    p_url = re.sub('.m3u', '', p_url)



    templateData = {
        'content' : s,
        'videos' : vList,
        'images' : iList,
        'playlist_url' : p_url,
        'playlist_title' : pl.title
    }

    return render(request, 'music/show.html', templateData)

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

    return render(request, 'music/livesets.html', templateData)

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
