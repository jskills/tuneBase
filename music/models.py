import datetime
import re
from django.db import connection
from django.db import models
from django.conf import settings
import urllib.parse


# Create models here


class Artist(models.Model):
    full_name = models.CharField(max_length=200, unique=True)
    created_date = models.DateTimeField(auto_now_add=True, db_index=True)
    last_updated_date = models.DateTimeField(auto_now=True, db_index=True)
    last_updated_by = models.CharField(max_length=20)

    class Meta:
        db_table = '"artist"'
        ordering = ['full_name']

    def __str__(self):
        return self.full_name

    def getUniqueAlbums(self, id):
        cur = connection.cursor()
        sql = "select distinct(album) as album from song where artist_id = %s"
        sql += " order by 1"
        cur.execute(sql, [id])
        sList = cur.fetchall()
        aList = list()
        for s in sList:
            d = dict()
            if s[0] is None or s[0] == '':
                d['album'] = 'NO ALBUM'
            else:
                d['album'] = str(s[0]).title()
            if d['album']:
                d['album_url'] = re.sub(' ', '_', d['album'])
                d['album_url'] = urllib.parse.quote(d['album_url'])
            aList.append(d)

        connection.close()

        return aList

    def getAlbumSongs(self, id, album_name):
        cur = connection.cursor()
        sql = "select * from song where artist_id = %s and LOWER(album) = LOWER(%s)"
        sql += " order by track_number"
        cur.execute(sql, [id, album_name])
        desc = cur.description
        column_names = [col[0] for col in desc]
        sList = [dict(zip(column_names, row)) for row in cur.fetchall()]
        connection.close()  

        return sList

    def getAlbumlessSongs(self, id,):
        cur = connection.cursor()
        sql = "select * from song where artist_id = %s and (album is NULL or album = '')"
        sql += " order by song_name"
        cur.execute(sql, [id])
        desc = cur.description
        column_names = [col[0] for col in desc]
        sList = [dict(zip(column_names, row)) for row in cur.fetchall()]
        connection.close()

        return sList 

###

class Genre(models.Model):
    genre_name = models.CharField(max_length=200, unique=True)
    created_date = models.DateTimeField(auto_now_add=True, db_index=True)
    last_updated_date = models.DateTimeField(auto_now=True, db_index=True)
    last_updated_by = models.CharField(max_length=20)

    class Meta:
        db_table = '"genre"'
        ordering = ['genre_name']

    def __str__(self):
        return self.genre_name

    def getGenreArtists(self, id):
        cur = connection.cursor()
        sql = "select distinct(artist_id) as url, full_name as name from song s, artist a"
        sql += " where genre_id = %s and s.artist_id = a.id order by full_name"
        cur.execute(sql, [id])
        desc = cur.description
        column_names = [col[0] for col in desc]
        aList = [dict(zip(column_names, row)) for row in cur.fetchall()]
        connection.close()
    
        return aList
    
###

class YTMSong(models.Model):
    video_id = models.CharField(max_length=200, unique=True)
    entity_id = models.CharField(max_length=200, unique=True)
    title = models.CharField(max_length=250)
    artist_name = models.CharField(max_length=250)
    artist_id = models.CharField(max_length=250, blank=True, null=True)
    album_name = models.CharField(max_length=250, blank=True, null=True)
    album_id = models.CharField(max_length=250, blank=True, null=True)
    duration = models.CharField(max_length=250, blank=True, null=True)
    created_date = models.DateTimeField(auto_now_add=True, db_index=True)
    last_updated_date = models.DateTimeField(auto_now=True, db_index=True)
    last_updated_by = models.CharField(max_length=20)

    class Meta:
        db_table = '"ytm_song"'
        ordering = ['title']

    def __str__(self):
        return self.title

###

class Song(models.Model):
    song_name = models.CharField(max_length=250)
    artist = models.ForeignKey(Artist, on_delete=models.PROTECT)
    album = models.CharField(max_length=200, blank=True, null=True)
    file_path = models.CharField(max_length=300, unique=True)
    genre = models.ForeignKey(Genre, on_delete=models.PROTECT)
    track_number =  models.IntegerField(blank=True, null=True)
    year = models.CharField(max_length=4, blank=True, null=True)
    comment = models.CharField(max_length=200, blank=True, null=True)
    duration =  models.IntegerField(blank=True, null=True)
    bit_rate = models.CharField(max_length=20, blank=True, null=True)   
    ytm = models.ForeignKey(YTMSong, on_delete=models.PROTECT, null=True)
    created_date = models.DateTimeField(auto_now_add=True, db_index=True)
    last_updated_date = models.DateTimeField(auto_now=True, db_index=True)
    last_updated_by = models.CharField(max_length=20)

    class Meta:
        db_table = '"song"'
        ordering = ['song_name']

    def __str__(self):
        return self.song_name

    @property
    def artist_name(self):
        return Artist.objects.get(id__exact=self.artist_id)

    def multiSearch(self, searchText):
        returnDict = dict()
        songList = albumList = artistList = plList = list()

        # get any song, artist, album or playlist with the search term present
        songList = Song.objects.filter(song_name__icontains=searchText)
        returnDict['songList'] = songList
        aList = list()
        albumList = Song.objects.filter(album__icontains=searchText).distinct()
        for al in albumList:
            d = dict()
            d['album'] = al.album
            d['artist_id'] = al.artist_id
            d['album_url'] = re.sub(' ', '_', d['album'])
            d['album_url'] = urllib.parse.quote(d['album_url'])
            if d not in aList:
                aList.append(d)
        returnDict['albumList'] = aList
        artistList = Artist.objects.filter(full_name__icontains=searchText)
        returnDict['artistList'] = artistList
        playlistList = Playlist.objects.filter(title__icontains=searchText)
        plList = list()
        for pl in playlistList:
            d = dict()
            d['title'] = pl.title
            d['url'] = d['title']
            d['url'] = pl.file_path.rsplit('/', 1)[-1]
            d['url'] = re.sub('.m3u', '', d['url'])
            d['live_ind'] = pl.live_ind
            plList.append(d)
        returnDict['plList'] = plList

        return returnDict

    def get_latest(limit_num=50):
        latest_songs = Song.objects.order_by('-created_date')[:limit_num:1]
        return latest_songs
    

###

class Playlist(models.Model):
    title = models.CharField(max_length=250)
    file_path = models.CharField(max_length=300, unique=True)
    comment = models.CharField(max_length=200, blank=True, null=True)
    set_date = models.DateField(blank=True, null=True)
    live_ind = models.BooleanField(default=False)
    created_date = models.DateTimeField(auto_now_add=True, db_index=True)
    last_updated_date = models.DateTimeField(auto_now=True, db_index=True)
    last_updated_by = models.CharField(max_length=20)

    class Meta:
        db_table = '"playlist"'
        ordering = ['last_updated_date']

    def __str__(self):
        return self.title

    def write_playlist_file(title, file_path, song_list):
        # check to see if playlists exists
        # it should always except the first time this runs
        # if it already exists:
        #    just update the file itself and the last_updated fields on the record

        file_path = settings.MUSIC_DIR + file_path
        print("file : ", file_path)
        f = open(file_path, 'w')
        f.write('#EXTM3U\n')
        for s in song_list:
            duration = s.duration if s.duration else '240'
            line = str('#EXTINF:'+ duration + ', ' + s.artist.full_name + ' - ' + s.song_name +'\n')
            f.write(line)
            f.write(s.file_path + '\n')
        f.close()

    def auto_latest():
        song_list = Song.get_latest()
        Playlist.write_playlist_file(title='Newest Added', file_path='Newest_Added.m3u', song_list=song_list)


###

class Show (models.Model):
    title = models.CharField(max_length=250)
    playlist = models.ForeignKey(Playlist, on_delete=models.PROTECT)
    location = models.CharField(max_length=200, blank=True, null=True)
    show_date = models.DateField(blank=True, null=True) 
    comment = models.CharField(max_length=200, blank=True, null=True)
    created_date = models.DateTimeField(auto_now_add=True, db_index=True)
    last_updated_date = models.DateTimeField(auto_now=True, db_index=True)
    last_updated_by = models.CharField(max_length=20)

    class Meta:
        db_table = '"show"'
        ordering = ['-show_date']

    def __str__(self):
        return self.title

    def getShowVideos(self, id):
        vList = list()
        vList = Show.objects.get(id=id).video_set.all()
        return vList

    def getShowImages(self, id):
        iList = list()
        iList = Show.objects.get(id=id).image_set.all()
        return iList


###

class Image(models.Model):
    title = models.CharField(max_length=250)
    file_path = models.CharField(max_length=300, unique=True)
    comment = models.CharField(max_length=200, blank=True, null=True)
    shows = models.ManyToManyField(Show)
    created_date = models.DateTimeField(auto_now_add=True, db_index=True)
    last_updated_date = models.DateTimeField(auto_now=True, db_index=True)
    last_updated_by = models.CharField(max_length=20)

    class Meta:
        db_table = '"image"'
        ordering = ['created_date']

    def __str__(self):
        return self.title
    
###

class Video(models.Model):
    title = models.CharField(max_length=250)
    file_path = models.CharField(max_length=300, unique=True)
    comment = models.CharField(max_length=200, blank=True, null=True)
    shows = models.ManyToManyField(Show)
    created_date = models.DateTimeField(auto_now_add=True, db_index=True)
    last_updated_date = models.DateTimeField(auto_now=True, db_index=True)
    last_updated_by = models.CharField(max_length=20)

    class Meta:
        db_table = '"video"'
        ordering = ['created_date']

    def __str__(self):
        return self.title

###
