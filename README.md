# tuneBase
This is a Django based website for a DJ.
There is some (very) basic design and navigation.

The Postgres DB is utilized holding all metadata for MP3s in a given song library.
It can be populated from scratch by using a utility that will traverse a file system, discover all mp3 files, extract mp3 tag info and populate appropriate database fields.

Additionally, other things like shows, videos and m3u playlists can also be discovered and added to the database.

The site should allow for the discovery or any genre, artist, song or playlist.

Standard HTML media tags or Jplayer is used to allow for playing songs or setlists.

Also included is a live stream page with the restream.io widget for DJs that live stream.


