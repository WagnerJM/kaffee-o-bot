from flask import request
from flask_restful import Resource
from flask_jwt_extended import get_jwt_identity, jwt_required

from app.api.rechnung.models import Rechnung


class RechnungApi(Resource):
    def get(self):
        # TODO: Mir überlegen wie ich das machen muss
        pass
