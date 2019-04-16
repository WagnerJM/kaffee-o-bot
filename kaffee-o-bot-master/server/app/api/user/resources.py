from flask import request
from flask_restful import Resource
from flask_jwt_extended import jwt_required, create_access_token, get_jwt_identity, get_raw_jwt

from app.utils import str2uuid
from app.utils.resource_extention import ResourceMixin

from app.security import TokenBlacklist

from app.api.user.models import User
from app.api.system.models import SystemSetting
from app.api.tasks import create_invoice

class UserLoginApi(Resource):

    def post(self):
        data = request.get_json()

        user = User.find_by_username(data['username'])

        if user and user.check_password(data['password'], user._password):
            access_token = create_access_token(identity=str(user.id), fresh=True)
            return {
                "token": access_token
            }, 200
        
        return {
            "msg": "Invalid credentials"
        }, 401

class UserLogoutApi(Resource, ResourceMixin):

    @jwt_required
    def post(self):
        jti = get_raw_jwt()['jti']
        token = TokenBlacklist(jti=jti)

        self.save_or_except(token)

class UserApi(Resource, ResourceMixin):
    
    @jwt_required
    def get(self):

        user = User.find_by_id(get_jwt_identity())

        return {
            "user": user.json()
        }, 200
    
    @jwt_required
    def patch(self):

        user = User.find_by_id(get_jwt_identity())

        data = request.get_json()

        for key in user.keys():
            user[key] = data[key]
        
        self.save_or_except(user)
        