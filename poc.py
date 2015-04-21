import base64
import ConfigParser
from gmusicapi import Mobileclient


config = ConfigParser.ConfigParser()
config.read('config.ini')
api = Mobileclient()

email = config.get('login', 'email')
password = base64.b64decode(config.get('login', 'password'))

while not api.login(email, password):
    print "Please check your credentials"
    email = raw_input("Your email:")
    password = raw_input("Your password:")

password = base64.b64encode(password)
config.set('login', 'email', email)
config.set('login', 'password', password)
config.write(open('config.ini', 'w'))


recommended = dict()
song_list = api.get_all_songs()
for artists in song_list:
    for artist in artists['artistId']:
        info = api.get_artist_info(artist,
                                   include_albums=False)
        for related in info['related_artists']:
            recommended[related['artistId']] = related['name']
print recommended.values()
