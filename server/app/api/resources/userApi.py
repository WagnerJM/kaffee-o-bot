from flask import request
from flask_restful import Resource
from flask_jwt_extended import jwt_required, create_access_token, get_jwt_identity, get_raw_jwt

from app.utils import str2uuid
from app.api.models.user import User
#from app.api.models.coffee_hist import CoffeeHistory
from app.security import TokenBlacklist

class UserRegisterApi(Resource):
    def post(self):

        data = request.get_json()

        if User.find_by_username(data.get('username')):
            return {
                "msg": "Dieser Username ist leider bereits vergeben."
            }, 500

        user = User(**data)
        try:
            user.save()
            return {
                "msg": "Der User wurde erfolgreich angelegt."
            }, 201
        except:
            return {
                "msg": "Der User konnte nicht angelegt werde. Ein Fehler ist passiert."
            }, 500


class UserLoginApi(Resource):
    def post(self):
        data = request.get_json()
        user = User.find_by_username(data.get('username'))

        if user and user.check_password(data.get('password'), user._password):
            access_token = create_access_token(identity=str(user.id), fresh=True)
            return {
                "access_token": access_token,
                "username": user.username
            }, 200
        return {
            "msg": "Invalid credentials"
        }, 401

class UserLogoutApi(Resource):
    @jwt_required
    def post(self):
        jti = get_raw_jwt()['jti']
        token = TokenBlacklist(jti=jti)

        try:
            token.save()
            return {
                "msg": "Sie wurden erfolgreich ausgeloggt."
            }, 200
        except:
            return {
                "msg": "Es ist ein Fehler beim Ausloggen auftreten."
            }, 500

class UserApi(Resource):
    @jwt_required
    def get(self):

        user = User.find_by_id(get_jwt_identity())
        history = user.coffee_hist

        if not user:
            return {
                "msg": "User nicht gefunden."
            }, 404

        return {
            "user": user.json(),
            "history": [ hist.json() for hist in history ]
        }, 201

    @jwt_required
    def put(self):
        user = User.find_by_id(get_jwt_identity())
        data = request.get_json()

        if not user:
            return {
                "msg": "Kein User gefunden!"
            }, 404

        else:
            for key, value in user.items():
                user[key] = data[key]

        try:
            user.save()
            return {
                "msg": "Daten wurden gespeichert."
            }, 201
        except:
            return {
                "msg": "Etwas ist beim Speicher der User-Daten falsch gelaufen."
            }, 500
