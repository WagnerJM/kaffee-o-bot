from flask import request
from flask_restful import Resource
from flask_jwt_extended import jwt_required, create_access_token, get_jwt_identity, get_raw_jwt

from app.utils import str2uuid

from app.api.user.models import User, CoffeeHistory
from app.api.system.models import SystemSetting
from app.security import TokenBlacklist
from app.api.tasks import create_invoice


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

class AdminAllUserApi(Resource):
    @jwt_required
    def get(self):
        admin = User.find_by_id(get_jwt_identity())
        if not user.is_admin:
            return {
                "msg": "Sie haben nicht die notwendigen Rechte."
            }, 500

        users = User.get_all()
        return {
             "users": [ user.json() for user in users ]
         }

class AdminUserApi(Resource):
    @jwt_required
    def put(self):
        admin = User.find_by_id(get_jwt_identity())
        data = request.get_json()

        user = User.find_by_id(data[user_id])

        if not admin.is_admin:
            return {
                "msg": "Sie haben nicht die notwendigen Rechte."
            }, 500

        if not user:
            return {
                "msg": "User konnte nicht gefunden werden."
            }, 404
        else:
            for key, value in user.items():
                user[key] = data[key]

        try:
            user.save()
            return {
                "msg": "User {username}/{vorname} wurde geupdatet.".format(username=user.username, vorname=user.vorname)
            }
        except:
            return {
                "msg": "Ein Fehler ist beim Speichern aufgetreten."
            }, 500

class AdminSysSettingApi(Resource):
    @jwt_required
    def get(self):
        sysSetting = SystemSetting.query.filter().first()
        user = User.find_by_id(get_jwt_identity())

        if not user.is_admin:
            return {
                "msg": "Sie haben nicht die notwendigen Rechte."
            }, 500

        if not sysSetting:
            return {
                "msg": "Keine System Einstellungen eingerichtet."
            }, 404
        return {
            "systemSetting": sysSetting.json()
        }, 200

    @jwt_required
    def post(self):
        user = User.find_by_id(get_jwt_identit())

        if not user.is_admin:
            return {
                "msg": "Sie haben nicht die notwendigen Rechte."
            }, 500

        data = request.get_json()

        sysSetting = SystemSetting(**data)

        try:
            sysSetting.save()
            return {
                "msg": "System Einstellungen erfolgreich gespeichert."
            }, 201
        except:
            return {
                "msg": "Beim Speichern ist etwas schief gelaufen."
            }, 500


    @jwt_required
    def put(self):
        user = User.find_by_id(get_jwt_identit())

        if not user.is_admin:
            return {
                "msg": "Sie haben nicht die notwendigen Rechte."
            }, 500

        data = request.get_json()
        sysSetting = SystemSetting.query.filter().first()

        for key, value in sysSetting.items():
            sysSetting[key] = data[key]

        try:
            sysSetting.save()
            return {
                "msg": "System Einstellungen erfolgreich gespeichert."
            }
        except:
            return {
                "msg": "Beim Speichern ist etwas schief gelaufen."
            }, 500

class AdminInvoiceApi(Resource):
    @jwt_required
    def post(self):
        user = User.find_by_id(get_jwt_identit())

        if not user.is_admin:
            return {
                "msg": "Sie haben nicht die nötigen Rechte dies zu tun."
            }

        data = request.get_json()
        user_list = data['user_list']
        timeDelta = data['timeDelta']

        for each in user_list:
            create_invoice.delay(each['id'], timeDelta)

        return {
            "msg": "Emails werden gesendet."
        }, 201
