from flask import Blueprint
from flask_restful import Api
from .auth import Signup,Login,Logout,BecomeCreator,ApproveCreatorRequest,CreatorRequests
from .views import Home,Export_albums, Album, Song, Search,CreatorStats,RateSong
api_bp =Blueprint('api', __name__)
api=Api(api_bp)

#Authorisation API
api.add_resource(Signup,'/signup')
api.add_resource(Login,'/login')
api.add_resource(Logout,'/logout')

#Home API

api.add_resource(Home,'/home')
#Album API
api.add_resource(Album,'/album','/album/<int:album_id>')
#Song API
api.add_resource(Song,'/song')
#Playlist API

#Playlist Song API
#api.add_resource(Playlist,'/playlist')
#Creator API
api.add_resource(BecomeCreator,'/become_creator')
#Approve Creator Request
api.add_resource(ApproveCreatorRequest,'/approve_creator/<int:user_id>')
api.add_resource(CreatorRequests, '/creator_requests')
#Export API
api.add_resource(Export_albums,'/export')
#Search API
api.add_resource(CreatorStats, '/stats')

api.add_resource(Search,'/search')

api.add_resource(RateSong, '/rate_song')


