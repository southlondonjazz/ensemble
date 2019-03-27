import base64
import requests
import json

#%% Authorise Spotify

class SpotifyConnect(object):
    # TODO Move the stuff below in here probably
    # This way I won't have the 'access_token' duplication and can rely on
    # this to ask for new tokens when an error comes up
    pass

def get_sp_access_token(secrets_json):
    with open(secrets_json, 'r') as infile:
        client_secret, client_id = json.loads(infile.read()).values()
    access_token = sp_auth(client_id, client_secret)
    return access_token

def sp_auth(client_id, client_secret):
    """Returns an access token string"""
    headers = {
    'Content-Type': 'application/x-www-form-urlencoded',
    'Authorization': 'Basic {}'.format((base64.b64encode((client_id +':'+client_secret).encode())).decode())
    }
    auth_params = {'grant_type': 'client_credentials'}
    auth_response = requests.post("https://accounts.spotify.com/api/token", headers=headers, params=auth_params)
    auth_response.raise_for_status()
    access_token = auth_response.json()['access_token']
    return access_token

#%% Access Spotify

def sp_get(url_suffix, access_token, params=None):
    """ Returns a dict for a Spotify object"""
    url = "https://api.spotify.com/v1{}".format(url_suffix)
    headers_dict =  {'Authorization': 'Bearer {}'.format(access_token)}
    r = requests.get(url, headers=headers_dict, params=params)
    r.raise_for_status()
    return r.json()