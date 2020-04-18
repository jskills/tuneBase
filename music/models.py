import datetime

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


