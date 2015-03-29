from gmusicapi import Mobileclient

email = raw_input("Your email:")
password = raw_input("Your password:")

api = Mobileclient()
logged_in = api.login(email, password)
print api.get_all_songs()
