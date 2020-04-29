import datetime
import re
from django.db import connection
from django.db import models



# Create your models here.

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
		sql = "select distinct(INITCAP(album)) as album from song where artist_id = %s"
		cur.execute(sql, [id])
		sList = cur.fetchall()
		aList = list()
		for s in sList:
			if s[0] is None:
				continue
			print("found album: " + str(s[0]))
			d = dict()
			d['album'] = str(s[0])
			if d['album']:
				d['album_url'] = re.sub(' ', '_', d['album'])
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
	created_date = models.DateTimeField(auto_now_add=True, db_index=True)
	last_updated_date = models.DateTimeField(auto_now=True, db_index=True)
	last_updated_by = models.CharField(max_length=20)

	class Meta:
		db_table = '"song"'
		ordering = ['song_name']

	def __str__(self):
		return self.song_name

###

class Playlist(models.Model):
	title = models.CharField(max_length=250)
	file_path = models.CharField(max_length=300, unique=True)
	comment = models.CharField(max_length=200, blank=True, null=True)
	set_date = models.DateField(blank=True, null=True)
	location = models.CharField(max_length=200, blank=True, null=True)
	live_ind = models.BooleanField(default=False)
	created_date = models.DateTimeField(auto_now_add=True, db_index=True)
	last_updated_date = models.DateTimeField(auto_now=True, db_index=True)
	last_updated_by = models.CharField(max_length=20)

	class Meta:
		db_table = '"playlist"'
		ordering = ['set_date']

	def __str__(self):
		return self.title


