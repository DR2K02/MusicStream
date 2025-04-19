from .database import db
from flask_login import UserMixin
from sqlalchemy.sql import func
from datetime import date

class User(db.Model,UserMixin):
    user_id=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String(),unique=True,nullable=False)
    email=db.Column(db.String(),unique=True,nullable=False)
    password=db.Column(db.String(),nullable=False)
    is_admin=db.Column(db.Boolean,default=False)
    is_creator=db.Column(db.Boolean,default=False)
    #blacklisted=db.Column(db.Boolean,default=False)
    requested_creator = db.Column(db.Boolean, default=False) 
    #playlists=db.relationship('Playlist',backref='user')
    albums=db.relationship('Album',backref='user')

    def __repr__(self) -> str:
        return f"<User name={self.name} email={self.email} is_admin={self.is_admin} ,is_creator={self.is_creator}>"
    
    def request_creator(self):
        if not self.is_creator and not self.requested_creator:
            self.requested_creator=True
            db.session.commit()
            return True
        return False
    
class Album(db.Model):
    album_id=db.Column(db.Integer,primary_key=True)
    album_name=db.Column(db.String(250),nullable=False)
    album_artist=db.Column(db.String(250),nullable=False)
    creator = db.Column(db.Integer, db.ForeignKey('user.user_id'), nullable=False)
    songs=db.relationship('Song',backref='album',lazy=True)

    def __repr__(self) -> str:
        return f"<id={self.album_id} Album name={self.album_name} Album Artist={self.album_artist} creator={self.creator} songs={self.songs}>"
       
class Song(db.Model):
    song_id=db.Column(db.Integer,primary_key=True)
    song_name=db.Column(db.String(250))
    lyrics=db.Column(db.String())
    rating=db.Column(db.Integer(),default=0)
    rating_sum=db.Column(db.Integer,default=0)
    rating_count=db.Column(db.Integer,default=0)
    average_rating=db.Column(db.Float,default=0)

    genre=db.Column(db.String())
    duration=db.Column(db.String())
    date_created=db.Column(db.DateTime(timezone=True),default=func.now())
    collection = db.Column(db.Integer, db.ForeignKey('album.album_id', ondelete = 'CASCADE'), nullable = False)
    #favourites = db.Column(db.Integer, db.ForeignKey('playlist.playlist_id'))
    #favourites=db.relationship('Playlist',cascade='all,delete-orphan')

    def __repr__(self) -> str:
        return f"<id={self.song_id} song name={self.song_name} lyrics={self.lyrics} >"


# class Playlist(db.Model):
#     playlist_id = db.Column(db.Integer, primary_key=True)
#     user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'), nullable=False)
#     song_id = db.Column(db.Integer, db.ForeignKey('song.song_id'), nullable=False)

#     def __repr__(self) -> str:
#         return f"<id={self.playlist_id} user_id={self.user_id} song_id={self.song_id}>"

