from flask_restful import Api, Resource

from src.helpers.image_converter import *
from src.helpers.common import *
from src.api_responses import *


REQUIRED_PAYLOAD = [
    'image_names'
]


class DetectAreaByName(Resource):
    def post(self):
        try:
            payload = request.get_json()
            check_required_payload(payload, REQUIRED_PAYLOAD)

            response = {}

            return ApiResponse(response).get_response()

        except WrongPayload as wp:
            return wp.get_response()
