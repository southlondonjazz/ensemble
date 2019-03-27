from classes import Artist, Release, Track
import json
from spotify_connection import sp_auth, get_sp_access_token
from pymongo import MongoClient

client = MongoClient()
db = client.ensemble
access_token = get_sp_access_token('secrets.json')

def crawl(start_artists_ids=['5mUcc8OOP4RuzrupeGYwW5'], count=0, max_depth=1):
    #TODO de-dupe. otherwise you get over 8K results at a depth of 2
    if count == max_depth:
        return print("Finished at depth {}.".format(count))

    else:
        for start_artist_id in start_artists_ids:
            # for every artist id
            start_artist_obj = Artist(sp_id=start_artist_id)
            # get the json response
            start_artist_dict = start_artist_obj.get_sp_artist_dict(access_token)
            # dump the json response in mongodb
            db.spotify.insert_one(start_artist_dict)
            # then get all the ids of their releases
            start_artist_releases = start_artist_obj.get_sp_releases_ids(access_token)

            for rel in start_artist_releases:
                # for every release id
                rel_obj = Release(sp_id=rel)
                # get the json response
                rel_dict = rel_obj.get_sp_release_dict(access_token)
                # dump the json response in mongodb
                db.spotify.insert_one(rel_dict)
                # then get all the ids of the release's tracks
                start_artist_tracks = rel_obj.get_sp_tracks_ids(access_token)

                for track in start_artist_tracks:
                    # for every track id
                    tr_obj = Track(sp_id=track)
                    # get the json response
                    tr_dict = tr_obj.get_sp_track_dict(access_token)
                    # dump the json response in mongodb
                    db.spotify.insert_one(tr_dict)
                    # then get all of the artists of that track
                    tr_artists_ids = tr_obj.get_sp_artists_ids(access_token)
            count += 1
        return crawl(start_artists_ids=tr_artists_ids, count=count)

if __name__ == "__main__":
    crawl()