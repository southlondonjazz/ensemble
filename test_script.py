from classes import Artist
import json

from spotify_connection import sp_get, sp_auth

with open('secrets.json', 'r') as infile:
    client_secret, client_id = json.loads(infile.read()).values()

access_token = sp_auth(client_id, client_secret)

test_artist = Artist('Joe Armon-Jones', sp_id='5mUcc8OOP4RuzrupeGYwW5')

print(test_artist.get_sp_releases(access_token))