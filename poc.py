import base64
import ConfigParser
from gmusicapi import Mobileclient


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
recommended = dict()
song_list = api.get_all_songs()
artists = dict()
for song in song_list:
    add_rate = int(song.get('rating', 0)) * int(song.get('playCount', 0))
    for aid in song['artistId']:
        artists[aid] = artists.get(aid, 0) + 1 + add_rate
for artist in artists:
    rate = artists[artist]
    info = api.get_artist_info(artist,
                               include_albums=False)
    for related in info['related_artists']:
        aid = related['artistId']
        recommended[aid] = recommended.get(aid, 0) + rate

max_score = float(sum(recommended.values())) or 1.0

for artist in recommended:
    recommended[artist] = (recommended[artist] * max_musics) / max_score

print recommended, sum(recommended.values())
