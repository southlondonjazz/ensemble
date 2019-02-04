from spotify_connection import sp_get
from abc import ABCMeta, abstractmethod

#%%
class Music(object):
        """ Published music.
        
        Attributes:
            name: Name of the music
            sp_id: This music's ID on Spotify
            sp_artists: List of IDs of music's the artists on Spotify
            sp_tracks: List of Spotify IDs of tracks associated with the music
        """
        
        __metaclass__ = ABCMeta
        
        def __init__(self, name, sp_id=None, sp_artists=None, sp_tracks=None,
                     sp_releases=None):
            self.name = name
            self.sp_id = sp_id
            self.sp_artists = sp_artists
            self.sp_tracks = sp_tracks
            self.sp_releases = sp_releases
            
        def get_artists(self):
            pass
        
        @abstractmethod
        def music_type(self):
            pass

class Track(Music):
    def music_type():
        return 'track'

    def get_sp_artists(self, access_token):
        url_suffix = "/tracks/{sp_id}".format(sp_id=self.sp_id)
        sp_obj = sp_get(url_suffix, access_token)
        self.sp_artists = [item['id'] for item in sp_obj['items']['artists']]
        return self.sp_artists

#%%
class Release(Music):
    """ Published recording.        
    """
    def music_type():
        return 'release'
    
    def get_sp_tracks(self, access_token):
        """Returns track ids for release ids"""
        url_suffix = "/albums/{sp_id}".format(sp_id=self.sp_id)
        sp_obj = sp_get(url_suffix, access_token)
        self.sp_tracks = [tr['id'] for tr in sp_obj['items']['tracks']]
        return self.sp_tracks


class Artist(Music):
    
    def get_sp_releases(self, access_token):
        url_suffix = "/artists/{sp_id}/albums".format(sp_id=self.sp_id)
        sp_obj = sp_get(url_suffix, access_token)
        self.sp_releases = [item['id'] for item in sp_obj['items']]
        return self.sp_releases
        
    
#list_output = {'recording_id1' : ['track_id1','track_id2','track_id3'],
#               'recording_id2' : ['track_id4', 'track_id5']}
#
#
#sum(list_output.values(), [])
