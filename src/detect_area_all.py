from flask_restful import Api, Resource

from src.helpers.image_converter import *
from src.helpers.common import *
from src.api_responses import *


class DetectAreaAll(Resource):
    def get(self):
        try:
            pass
        except WrongPayload as wp:
            return wp.get_response()
