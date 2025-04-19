from flask import Blueprint,request
from flask_restful import Resource,reqparse,abort,fields,marshal_with
from functools import wraps #RBAC
from flask_jwt_extended import jwt_required,get_jwt_identity,get_current_user
from . import models
from .models import Song
from .database import db
from datetime import datetime
from .worker import export_data
import time
from .cache import cache
from sqlalchemy import func


views=Blueprint('views',__name__)

def admin_required(f):
    @wraps(f)
    def decorated_function(*args,**kwargs):
        if not get_current_user().is_admin:
            abort(403,description="You are not authorized to perform this action")
        return f(*args,**kwargs)
    return decorated_function
search_parser=reqparse.RequestParser()

def creator_required(f):
    @wraps(f)
    def decorated_function(*args,**kwargs):
        album_id=kwargs.get('album_id')
        if album_id is None:
            return f(*args,**kwargs)
        album=models.Album.query.get(album_id)
        if album is None:
            abort(404,description="Album Not Found")
        current_user=get_current_user()
        if current_user.user_id != album.creator:
            abort(403,description="You are not allowed to perform this task")
        return f(*args,**kwargs)
    return decorated_function



home_fields={
    "user_id":fields.Integer,
    "name":fields.String,
    "email":fields.String,
    "is_admin":fields.Boolean,
    "is_creator":fields.Boolean,
    "albums":fields.List(fields.Nested({
        "album_id":fields.Integer,
        "album_name":fields.String,
        "album_artist":fields.String,
        "songs":fields.List(fields.Nested({
            "song_id":fields.Integer,
            "song_name":fields.String,
            "lyrics":fields.String,
            "genre":fields.String,
            "duration":fields.String,
            "date_created":fields.String,
            "playlist":fields.List(fields.Nested({
                "playlist_id":fields.Integer,
                "song":fields.String,
                "user_id":fields.Integer
            }))

        }))
    })),

}

class Home(Resource):
    @jwt_required()
    @marshal_with(home_fields)
    def get(self):
        current_user=get_current_user()
        if current_user.is_admin:
            return current_user,200
        elif current_user.is_creator:
            return current_user,200
        else:
            albums=db.session.query(models.Album).all()
            current_user.albums=albums
            return current_user,200
        
class Album(Resource):
    album_fields={
        "album_name":fields.String,
        "album_artist":fields.String
    }
    @jwt_required()
    #@admin_required
    @marshal_with(album_fields)
    def get(self):
        album_id=request.args.get('album_id')
        # album_id is None
        if album_id is None:
            return {"message":"Album ID is required"},400
        
        try:
            album_id=int(album_id)
        except ValueError:
            return {"message":"Invalid Album ID format"},400
        

        album=models.Album.query.get(int(album_id))
        if not album:
            return {"message":"Album not found"},404
        else:
            return {"album_id":album.album_id,"album_name":album.album_name,"album_artist":album.album_artist},200        
    
    album_post_parser=reqparse.RequestParser()
    album_post_parser.add_argument("album_name",type=str,help="Album name is required",required=True)
    album_post_parser.add_argument('album_artist',type=str,help="Album Artist is required",required=True)

    @jwt_required()
    @creator_required
    def post(self):
        data =  request.get_json()
        album_name=data['album_name']
        album_artist=data['album_artist']

        new_album=models.Album(album_name=album_name,album_artist=album_artist,creator = get_current_user().user_id)
        db.session.add(new_album)
        db.session.commit()
        return{"message":"Album Added Successfully"},200
    
    album_patch_parser=reqparse.RequestParser()
    album_patch_parser.add_argument("album_id",type=int,help="Album ID is required",required=True)
    album_patch_parser.add_argument("album_name",type=str,help="Album Name is required",required=True)
    album_patch_parser.add_argument("album_artist",type=str,help="Album Artist is required",required=True)

    @jwt_required()
    @creator_required
    def patch(self):
        req_args=self.album_patch_parser.parse_args()
        album_id=req_args["album_id"]
        album_name=req_args["album_name"]
        album_artist=req_args["album_artist"]
        album=models.Album.query.filter_by(album_id=album_id).first()
        if not album:
            return {"message": "Album Not Found"},404
        else:
            album.album_name=album_name
            album.album_artist=album_artist
            db.session.commit()
            return {"message":"Album Updated Successfully"}

    @jwt_required()
    @creator_required
    def delete(self,album_id):
        
        # check if album_id is None
        if album_id is None:
            return {"message":"Album ID is required"},400
        
        try:
            album_id=int(album_id)
        except ValueError:
            return {"message": "Invalid album ID format"},400
        
        album=models.Album.query.get(album_id)

        if album:
            db.session.delete(album)
            db.session.commit()

            return {"message":"Album deleted successfully"},200
        else:
            return {"message":"Album Not Found"},404
        

    
class Song(Resource):
    song_fields={
    "song_id":fields.Integer,
    "song_name":fields.String,
    "lyrics":fields.String,
    "genre":fields.String,
    "duration":fields.String,
    "rating":fields.Integer,
    "average_rating":fields.Float,
    "date_created":fields.String,
    "album_name": fields.String(attribute=lambda song: song.album.album_name if hasattr(song, 'album') else None),
    "album_artist": fields.String(attribute=lambda song: song.album.album_artist if hasattr(song, 'album') else None)
        }
    @jwt_required()
    #@admin_required
    @marshal_with(song_fields)
    def get(self):
       songs = models.Song.query.all()
       if not songs:
           return {"message": "No Songs Found"}, 404
       else:
           return songs, 200
            
    song_post_parser=reqparse.RequestParser()
    song_post_parser.add_argument("song_name",type=str,help="Song Name is required",required=True)
    #song_post_parser.add_argument("rating",type=int,help="Rating is required",required=True)
    song_post_parser.add_argument("album_id",type=int,help="Album id is required",required=True)
    song_post_parser.add_argument("lyrics",type=str,help="Lyrics is required",required=True)
    song_post_parser.add_argument("genre",type=str,help="Genre is required",required=True)
    song_post_parser.add_argument("duration",type=str,help="Duration is required",required=True)
    song_post_parser.add_argument("date_created",type=str,required=False)

    
    @jwt_required()
    @creator_required

    def post(self):
        req_args=self.song_post_parser.parse_args()
        song_name=req_args["song_name"]
        #rating=req_args["rating"]
        #song_id=req_args["song_id"]
        lyrics=req_args["lyrics"]
        genre=req_args["genre"]
        duration=req_args["duration"]
        date_created_str=req_args.get('date_created')
        album_id=req_args["album_id"]
        if date_created_str:
            date_created=datetime.strptime(date_created_str,"%Y-%m-%d")
        else:
            date_created=datetime.now()


        album=models.Album.query.filter_by(album_id=album_id).first()
        if not album:
            return {"message":"Album not found"},404
        else:
            new_song=models.Song(song_name=song_name,lyrics=lyrics,genre=genre,duration=duration,date_created=date_created,collection=album_id)
            db.session.add(new_song)
            db.session.commit()
            return {"message": "Song added Successfully"},200
            
    song_patch_parser=reqparse.RequestParser()
    song_patch_parser.add_argument("song_name",type=str,help="Song name is required",required=True)
    song_patch_parser.add_argument("lyrics",type=str,help="Lyrics is required",required=True)
    song_patch_parser.add_argument("genre",type=str,help="Genre is required",required=True)
    song_patch_parser.add_argument("duration",type=str,help="Duration is required",required=True)
    song_patch_parser.add_argument("song_id",type=int,help="Song ID is required",required=True)
    #song_patch_parser.add_argument("rating",type=int,help="Integer is required",required=True)
    song_patch_parser.add_argument("date_created",type=str,help="date created is required")

    @jwt_required()
    @creator_required
    def patch(self):
        song_id=request.args.get('song_id')
        if song_id is None:
            return {"message":"Please provide a song_id"},400
        
        req_args=self.song_patch_parser.parse_args()

        song_name=req_args["song_name"]
        #rating=req_args["rating"]
        lyrics=req_args["lyrics"]
        genre=req_args["genre"]
        duration=req_args["duration"]
        date_created_str=req_args["date_created"]

        if date_created_str:
            date_created=datetime.strptime(date_created_str,"%Y-%m-%d")
        else:
            date_created=None
        song=models.Song.query.get(int(song_id))
        if not song:
            return {"message":"Song not found"}, 404
        else:
            song.song_name=song_name
            #song.rating=rating
            song.lyrics=lyrics
            song.genre=genre
            song.duration=duration
            song.date_created=date_created

            db.session.commit()
            return {"message":"Song updated successfully"},200
        
    @jwt_required()
    def delete(self):
        data = request.json
        song_id = data.get('song_id')
        
        # Check if song_id is None
        if song_id is None:
            return {"message": "Song ID is required"}, 400
        
        try:
            song_id = int(song_id)
        except ValueError:
            return {"message": "Invalid song ID format"}, 400
        
        song = models.Song.query.get(song_id)
        
        if song:
            db.session.delete(song)
            db.session.commit()
            
            return {"message": "Song deleted successfully"}, 200
        else:
            return {"message": "Song Not Found"}, 404

                

# class Playlist(Resource):
#     @jwt_required()
#     def get(self, playlist_id):
#         playlist = models.Playlist.query.get(playlist_id)
#         if not playlist:
#             return {"message": "Playlist not found"}, 404

#         playlist_data = {
#             "playlist_id": playlist.playlist_id,
#             "user_id": playlist.user_id,
#             # Assuming songs is a list of song objects in the playlist
#             "songs": [{"song_id": song.song_id, "song_name": song.song_name} for song in playlist.songs]
#         }

#         return {"playlist": playlist_data}, 200
    
#     @jwt_required()
#     def put(self, playlist_id):
#         req_data = request.get_json()
#         song_id = req_data.get("song_id")

#         playlist = models.Playlist.query.get(playlist_id)
#         if not playlist:
#             return {"message": "Playlist not found"}, 404

#         if self.add_song(playlist, song_id):
#             return {"message": "Song added to playlist successfully"}, 200
#         else:
#             return {"message": "Failed to add song to playlist"}, 400

#     @jwt_required()
#     def delete(self, playlist_id):
#         req_data = request.get_json()
#         song_id = req_data.get("song_id")

#         playlist = models.Playlist.query.get(playlist_id)
#         if not playlist:
#             return {"message": "Playlist not found"}, 404

#         if self.remove_song(playlist, song_id):
#             return {"message": "Song removed from playlist successfully"}, 200
#         else:
#             return {"message": "Failed to remove song from playlist"}, 400

#     def add_song(self, playlist, song_id):
#         try:
#             # Append the song object directly, assuming song_id is an object
#             playlist.songs.append(song_id)
#             db.session.commit()
#             return True
#         except Exception as e:
#             print(e)
#             db.session.rollback()
#             return False

#     def remove_song(self, playlist, song_id):
#         try:
#             # Remove the song object directly, assuming song_id is an object
#             playlist.songs.remove(song_id)
#             db.session.commit()
#             return True
#         except Exception as e:
#             print(e)
#             db.session.rollback()
#             return False

class Search(Resource):
    search_song_fields = {
        "songs": fields.List(fields.Nested({
            'song_id': fields.Integer,
            'song_name': fields.String,
            "rating": fields.Integer,
            "duration": fields.String,
            "genre": fields.String,
            "average_rating":fields.Float,
            "lyrics": fields.String,
            "album_id":fields.Integer,
            "album_name":fields.String,
            "album_artist":fields.String
        }))
    }

    @jwt_required()
    @marshal_with(search_song_fields)
    #@cache.cached(timeout=600)
    def get(self):
        try:
            search_query = request.args.get('searchQuery')
            if not search_query:
                return {"message": "Search query is missing"}, 400

            songs = models.Song.query.join(models.Album).filter(
                (models.Song.song_name.like("%" + search_query + "%")) |
                (models.Song.average_rating.like("%" + search_query + "%")) |
                (models.Song.genre.like("%" + search_query + "%")) |
                (models.Album.album_name.like("%" + search_query + "%")) |
                (models.Album.album_artist.like("%" + search_query + "%"))
            ).all()

            formatted_song_list = []
            for song in songs:
                formatted_song = {
                    'song_id': song.song_id,
                    'song_name': song.song_name,
                    'average_rating': song.average_rating,
                    'genre': song.genre,
                    'duration': song.duration,
                    'lyrics': song.lyrics,
                    'album_id':song.collection,
                    'album_name':song.album.album_name,
                    'album_artist':song.album.album_artist
                }
                formatted_song_list.append(formatted_song)

            return {"songs": formatted_song_list}, 200
        except Exception as e:
            return {"message": "An error occurred while processing the request", "error": str(e)}, 500

class CreatorStats(Resource):
    @jwt_required()
    @admin_required
    def get(self):
        try:
            # Count the number of creators
            num_creators = models.User.query.filter_by(is_creator=True).count()
            
            # Query to get statistics for each creator
            creators = models.User.query.filter_by(is_creator=True).all()
            creator_stats = []
            for creator in creators:
                num_albums = models.Album.query.filter_by(creator=creator.user_id).count()
                num_songs = models.Song.query.join(models.Album).filter(models.Album.creator == creator.user_id).count()
                avg_rating = db.session.query(func.avg(models.Song.average_rating)).join(models.Album).filter(models.Album.creator == creator.user_id).scalar()
                avg_rating = round(avg_rating, 2) if avg_rating else 0  # Round to two decimal places
                creator_stats.append({
                    'user_id': creator.user_id,
                    'name': creator.name,
                    'num_albums': num_albums,
                    'num_songs': num_songs,
                    'avg_rating': avg_rating
                })

            # Return the statistics as a JSON response
            return {
                'num_creators': num_creators,
                'creator_stats': creator_stats
            }, 200
        except Exception as e:
            return {'error': str(e)}, 500
class RateSong(Resource):
    @jwt_required()
    def post(self):
        try:
            # Get the song ID and rating from the request body
            song_id = request.json.get('song_id')
            rating = request.json.get('rating')
            
            # Validate the rating (ensure it's between 1 and 5, for example)
            if not (1 <= rating <= 5):
                return {'error': 'Invalid rating. Rating must be between 1 and 5.'}, 400
            
            # Find the song by its ID
            song = models.Song.query.get(song_id)
            if not song:
                return {'error': 'Song not found'}, 404
            
            # Update the song's rating attributes
            song.rating_sum += rating
            song.rating_count += 1
            song.average_rating = song.rating_sum / song.rating_count
            
            # Commit the changes to the database
            db.session.commit()
            
            return {'message': 'Song rating updated successfully'}, 200
        except Exception as e:
            return {'error': str(e)}, 500

class Export_albums(Resource):
    @jwt_required()
    @creator_required
    def get(self):
        album_id=request.args.get('album_id')

        res=export_data.delay(album_id)

        while not res.ready():
            print("Still in progress")
            print(album_id)

            time.sleep(2)

        if not res.get()[0]:
            return {"message":res.get()[1]},400
        else:
            return {"message":res.get()[1]},200

'''class CreatorStats(Resource):
    @jwt_required()
    @admin_required
    def get(self, user_id):
        creator = models.User.query.get(user_id)
        if not creator:
            return {'error': 'User not found'}, 404
        
        num_albums = models.Album.query.filter_by(creator=user_id).count()
        num_songs = models.Song.query.join(models.Album).filter(models.Album.creator == user_id).count()
        avg_rating = db.session.query(func.avg(models.Song.average_rating)).join(models.Album).filter(models.Album.creator == user_id).scalar()
        avg_rating = round(avg_rating, 2) if avg_rating else 0  # Round to two decimal places
        
        # Return the statistics as a JSON response
        return {
            'user_id': user_id,
            'name': creator.name,
            'num_albums': num_albums,
            'num_songs': num_songs,
            'avg_rating': avg_rating
        }

class RateSong(Resource):
    @jwt_required()
    def post(self, song_id):
        data = request.get_json()

        # Extract rating from the request data
        rating = data.get('rating')

        # Validate the rating
        if not rating or not isinstance(rating, int) or rating < 1 or rating > 5:
            return {"message": "Invalid rating. Rating must be an integer between 1 and 5."}, 400

        # Fetch the song from the database
        song = models.Song.query.get(song_id)

        # Check if the song exists
        if not song:
            return {"message": "Song not found."}, 404

        # Update the song's rating attributes
        try:
            # Update rating sum, count, and average rating
            song.rating_sum += rating
            song.rating_count += 1
            song.average_rating = song.rating_sum / song.rating_count
        except ZeroDivisionError:
            # Handle the case where ratings_count is 0 to avoid division by zero
            song.average_rating = rating

        # Commit changes to the database
        db.session.commit()

        return {"message": f"Rating for song {song_id} updated successfully."}, 200       



       '''     