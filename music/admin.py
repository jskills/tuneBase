from django.contrib import admin
from .models import Artist, Genre, Song, Playlist

# Register your models here.

class GenreAdmin(admin.ModelAdmin):
	 readonly_fields = ('created_date', 'last_updated_date',)

admin.site.register(Genre, GenreAdmin)

###

class ArtistAdmin(admin.ModelAdmin):
	readonly_fields = ('created_date', 'last_updated_date',)

admin.site.register(Artist, ArtistAdmin)

###

class SongAdmin(admin.ModelAdmin):
	readonly_fields = ('created_date', 'last_updated_date',)

admin.site.register(Song, SongAdmin)

###

class PlaylistAdmin(admin.ModelAdmin):
	readonly_fields = ('created_date', 'last_updated_date',)

admin.site.register(Playlist, PlaylistAdmin)
