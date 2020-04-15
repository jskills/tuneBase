from django.contrib import admin

# Register your models here.

from .models import Genre
admin.site.register(Genre)

from .models import Artist
admin.site.register(Artist)

from .models import Song
admin.site.register(Song)
