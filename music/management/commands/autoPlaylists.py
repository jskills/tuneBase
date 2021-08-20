import sys
import os
from django.core.management.base import BaseCommand, CommandError
from music.models import Playlist 

#######################

# set locally 
musicDir = "/media/jskills/Toshiba-2TB/"
coverImageDir = musicDir + "cover_art/"

class Command(BaseCommand):
    help = 'Automatically create playlists'

    def handle(self, *args, **options):
        Playlist.autolatest()
