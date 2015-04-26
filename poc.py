import base64
import ConfigParser
from gmusicapi import Mobileclient, exceptions
from math import ceil
from random import sample


config = ConfigParser.ConfigParser()
config.read('config.ini')
api = Mobileclient()

try:
    email = config.get('login', 'email')
    password = base64.b64decode(config.get('login', 'password'))

    max_musics = config.get('options', 'max_musics')

except ConfigParser.NoSectionError:
    email = password = max_musics = None

while not api.login(email, password):
    print "Please check your credentials"
    email = raw_input("Your email:")
    password = raw_input("Your password:")

while not max_musics:
    max_musics = raw_input("How many songs do you want?")

password = base64.b64encode(password)
config.set('login', 'email', email)
config.set('login', 'password', password)
config.set('options', 'max_musics', max_musics)
config.write(open('config.ini', 'w'))


max_musics = int(max_musics)
artists = dict()
recommended = dict()
liked_songs = api.get_promoted_songs()
song_list = api.get_all_songs()
for song in liked_songs:
    for aid in song['artistId']:
        add_rate = 5
        artists[aid] = artists.get(aid, 0) + 1 + add_rate

for song in song_list:
    if len(artists) >= max_musics:
        break
    rating = int(song.get('rating', 0))
    if rating == 0:
        add_rate = int(song.get('playCount', 0))
        for aid in song['artistId']:
            artists[aid] = artists.get(aid, 0) + 1 + add_rate
for artist in artists:
    rate = artists[artist]
    try:
        info = api.get_artist_info(artist,
                                   include_albums=False,
                                   max_top_tracks=0,
                                   max_rel_artist=5)
    except exceptions.CallFailure:
        pass
    for related in info.get('related_artists', []):
        aid = related['artistId']
        recommended[aid] = recommended.get(aid, 0) + rate

max_score = float(sum(recommended.values())) or 1.0

for artist in recommended:
    recommended[artist] = (recommended[artist] * max_musics) / max_score

playlist_id = api.create_playlist('Test me Again', 'lalala')
songs_id = list()
for artist in recommended:
    info = api.get_artist_info(artist, include_albums=False,
                               max_rel_artist=0,
                               max_top_tracks=ceil(recommended[artist]))
    for song in info.get('topTracks', []):
        print len(songs_id)
        songs_id.append(api.add_aa_track(song['storeId']))

api.add_songs_to_playlist(playlist_id, sample(songs_id, max_musics))
