from flask import Blueprint,request,flash,redirect,url_for,jsonify
from flask_restful import Resource,reqparse,abort,fields,marshal_with,Api
from flask_jwt_extended import jwt_required,create_access_token,get_jwt_identity,get_jwt_identity,get_jwt
from werkzeug.security import generate_password_hash,check_password_hash
from .models import User
from .database import db

auth=Blueprint('auth',__name__)

signup_parser=reqparse.RequestParser()
signup_parser.add_argument("name",type=str,help="Name of the User is required",required=True)
signup_parser.add_argument("password",type=str,help="Password is required",required=True)
signup_parser.add_argument("email",type=str,help="Email of the user is required",required=True)


user_fields={
    "user_id":fields.Integer,
    "name":fields.String,
    "email":fields.String,
    "token":fields.String,
    "is_admin":fields.Boolean
}
class Signup(Resource):
    @marshal_with(user_fields)
    def post(self):
        req_args=signup_parser.parse_args()
        name=req_args["name"]
        password=req_args["password"]
        email=req_args["email"]
        user=User.query.filter_by(email=email).first()
        if user:
            abort(403,message="User already is present")
        else:
            new_user=User(email=email,name=name,password=generate_password_hash(password,method='pbkdf2:sha256'))
            db.session.add(new_user)
            db.session.commit()
            access_token=create_access_token(identity=new_user.user_id)
            response={"user_id":new_user.user_id,"name":new_user.name,"email":new_user.email,"token":access_token,"is_admin":new_user.is_admin}
            return response,200

login_parser=reqparse.RequestParser()
login_parser.add_argument('email',type=str,help="this field cannot be blank",required=True)
login_parser.add_argument('password',type=str,help='This field cannot be blank',required=True)

login_fields={"user_id":fields.Integer,"token":fields.String,"is_admin":fields.Boolean}

class Login(Resource):
    def post(self):
        # Parse request arguments
        req_args = login_parser.parse_args()
        email = req_args['email']
        password = req_args['password']

        # Retrieve user by email
        user = User.query.filter_by(email=email).first()

        # Check if user exists
        if user:
            # Check if password matches
            if check_password_hash(user.password, password):
                # Create JWT access token
                access_token = create_access_token(identity=user.user_id)
                response = {
                    "user_id": user.user_id,
                    "token": access_token,
                    "is_admin": user.is_admin,
                    'is_creator': user.is_creator
                }
                return response, 200
            else:
                # Return 401 Unauthorized if password is incorrect
                abort(401, message="Wrong password")
        else:
            # Return 401 Unauthorized if user does not exist
            abort(401, message="User does not exist")

class CreatorRequests(Resource):
    @jwt_required()  # Requires authentication
    def get(self):
        current_user_id = get_jwt_identity()
        admin_user = User.query.get(current_user_id)
        
        # Check if the current user is an admin
        if not admin_user or not admin_user.is_admin:
            return {'message': 'Unauthorized'}, 401
        
        # Get the list of users who have requested to become creators
        creator_requests = User.query.filter_by(requested_creator=True).all()
        
        # Serialize the user data
        creator_requests_data = [{'id': user.user_id, 'email': user.email} for user in creator_requests]
        
        return creator_requests_data, 200
    
class BecomeCreator(Resource):
    @jwt_required()
    def post(self):
        current_user_id=get_jwt_identity()
        user=User.query.get(current_user_id)

        if not user:
            return {'message':'User Not Found'},404
        if user.request_creator():
            return {'message':'Request to become a creator submitted successfully'},200
        else:
            return {'message':'User is already a creator or the request failed'},400

class ApproveCreatorRequest(Resource):
    @jwt_required()
    def put(self, user_id):
        current_user_id = get_jwt_identity()
        admin_user = User.query.get(current_user_id)
        
        # Check if the current user is an admin
        if not admin_user or not admin_user.is_admin:
            return {'message': 'Unauthorized'}, 401
        
        # Get the user requesting to become a creator
        user = User.query.get(user_id)
        
        if not user:
            return {'message': 'User not found'}, 404
        
        # Check if the user has requested to become a creator
        if not user.requested_creator:
            return {'message': 'User has not requested to become a creator'}, 400
        
        # Option to approve or reject the user's request
        action = request.json.get('action')

        if action == 'approve':
            user.is_creator = True
            user.requested_creator = False  # Reset requested_creator flag
            db.session.commit()
            return {'message': 'User approved as a creator'}, 200
        elif action == 'reject':
            user.requested_creator = False  # Reset requested_creator flag
            db.session.commit()
            return {'message': 'User request to become a creator rejected'}, 200
        else:
            return {'message': 'Invalid action'}, 400
    
blacklist=set()
class Logout(Resource):
    @jwt_required()
    def post(self):
        jti=get_jwt()['jti']
        blacklist.add(jti)
        return {"message":"Successfully logged out"},200
    
