import sys
import os
from django.core.management.base import BaseCommand, CommandError
from music.models import Playlist 

#######################

class Command(BaseCommand):
    help = 'Automatically create playlists'

    def handle(self, *args, **options):
        p = Playlist.auto_latest()
