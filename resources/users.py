from flask.views import MethodView
from flask_smorest import Blueprint, abort
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from db import db
from models import UserModel
from schemas import NewUser, UserData, UserLogin
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from passlib.hash import pbkdf2_sha256

from flask import current_app

# blue print divides data into multiple segments
blp = Blueprint("tasks", __name__, description="Users APIs")


@blp.route("/register")
class Register(MethodView):
    @blp.arguments(NewUser)
    @blp.response(201)
    def post(self, user_data):
        if UserModel.query.filter(UserModel.username == user_data['username']).first():
            abort(409, "User with that username already exists!")
        user = UserModel(**user_data)
        db.session.add(user)
        db.session.commit()
   
       

@blp.route("/login")
class Login(MethodView):
    @blp.arguments(UserLogin)
    @blp.response(201)
    def post(self, user_data):
        try:
            user = UserModel.query.filter(UserModel.username == user_data['username']).first()
            if user and pbkdf2_sha256.verify(user.password, pbkdf2_sha256.hash(user_data['password'])):
                access_token = create_access_token(identity=user.id, fresh=True)
                return {
                    'access_token': access_token
                }
        except: 
            db.sessiona.abort()
            abort(401, "Invalid credentials!")
        
        
@blp.route("/protected")
class Protected(MethodView):
    @jwt_required() 
    @blp.response(200, UserData)
    def get(self):
        try: 
            user_id = get_jwt_identity()
            user = UserModel.query.get_or_404(user_id)
            return {
                "username": user.username,
                "favorite_quote": user.favorite_quote
            }, 200
        except:
            abort(500, message="Internal Server Error")
            
            
        
        
        
        
        
        


