from spotify_connection import sp_get
from abc import ABCMeta, abstractmethod

#%%
class Music(object):
        """ Published music.
        
        Attributes:
            name: Name of the music
            sp_id: This music's ID on Spotify
            sp_artists_ids: List of IDs of music's artists on Spotify
            sp_tracks_ids: List of Spotify IDs of tracks associated with the music
        """
        
        __metaclass__ = ABCMeta
        
        def __init__(self, name=None, sp_id=None, sp_artists_ids=None, 
                     sp_tracks_ids=None, sp_releases_ids=None, sp_dict=None):
            self.name = name
            self.sp_id = sp_id
            self.sp_artists_ids = sp_artists_ids
            self.sp_tracks_ids = sp_tracks_ids
            self.sp_releases_ids = sp_releases_ids
            self.sp_dict = sp_dict
        
        @abstractmethod
        def music_type(self):
            pass
#%%
class Track(Music):
    def music_type():
        return 'track'

    def get_sp_track_dict(self, access_token):
        url_suffix = "/tracks/{sp_id}".format(sp_id=self.sp_id)
        self.sp_dict = sp_get(url_suffix, access_token)
        return self.sp_dict

    def get_sp_artists_ids(self, access_token):
        url_suffix = "/tracks/{sp_id}".format(sp_id=self.sp_id)
        self.sp_dict = sp_get(url_suffix, access_token)
        self.sp_artists_ids= [item['id'] for item in self.sp_dict['artists']]
        return self.sp_artists_ids

#%%
class Release(Music):
    """ Published recording.
    """
    def music_type():
        return 'release'

    def get_sp_release_dict(self, access_token):
        """Returns track ids for release ids"""
        url_suffix = "/albums/{sp_id}".format(sp_id=self.sp_id)
        self.sp_dict = sp_get(url_suffix, access_token)
        return self.sp_dict    

    def get_sp_tracks_ids(self, access_token):
        """Returns track ids for release ids"""
        url_suffix = "/albums/{sp_id}".format(sp_id=self.sp_id)
        self.sp_dict = sp_get(url_suffix, access_token)
        self.sp_tracks_ids = [tr['id'] for tr in self.sp_dict['tracks']['items']]
        return self.sp_tracks_ids


class Artist(Music):
    """
    """

    def music_type():
        return 'artist'

    def get_sp_artist_dict(self, access_token):
        url_suffix = "/artists/{sp_id}/albums".format(sp_id=self.sp_id)
        self.sp_dict = sp_get(url_suffix, access_token)
        return self.sp_dict

    def get_sp_releases_ids(self, access_token):
        url_suffix = "/artists/{sp_id}/albums".format(sp_id=self.sp_id)
        self.sp_dict = sp_get(url_suffix, access_token)
        self.sp_releases_ids= [item['id'] for item in self.sp_dict['items']]
        return self.sp_releases_ids
