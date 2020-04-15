from django.db import models

# Create your models here.

class Artist(models.Model):
	full_name = models.CharField(max_length=200, unique=True)
	created_date = models.DateTimeField(auto_now_add=True, db_index=True)
	last_updated_date = models.DateTimeField(auto_now_add=True, db_index=True)
	last_updated_by = models.CharField(max_length=20)

	class Meta:
		db_table = '"artist"'

class Genre(models.Model):
	genre_name = models.CharField(max_length=200, unique=True)
	created_date = models.DateTimeField(auto_now_add=True, db_index=True)
	last_updated_date = models.DateTimeField(auto_now_add=True, db_index=True)
	last_updated_by = models.CharField(max_length=20)

	class Meta:
		db_table = '"genre"'

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
	last_updated_date = models.DateTimeField(auto_now_add=True, db_index=True)
	last_updated_by = models.CharField(max_length=20)

	class Meta:
		db_table = '"song"'


	
