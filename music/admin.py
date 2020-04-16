from django.contrib import admin

# Register your models here.

from .models import Genre

class GenreAdmin(admin.ModelAdmin):
	 readonly_fields = ('created_date', 'last_updated_date',)
admin.site.register(Genre, GenreAdmin)


from .models import Artist

class ArtistAdmin(admin.ModelAdmin):
	readonly_fields = ('created_date', 'last_updated_date',)

admin.site.register(Artist, ArtistAdmin)


from .models import Song

class SongAdmin(admin.ModelAdmin):
	readonly_fields = ('created_date', 'last_updated_date',)

admin.site.register(Song, SongAdmin)
