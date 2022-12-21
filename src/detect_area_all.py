from flask_restful import Api, Resource

from src.helpers.image_converter import *
from src.helpers.common import *
from src.api_responses import *


REQUIRED_PAYLOAD = [
    'threshold_value'
]


class DetectAreaAll(Resource):
    def post(self):
        try:
            payload = requests.get_json()
            check_required_payload(payload, REQUIRED_PAYLOAD)

            files_names = os.listdir('./input/images')
            threshold_value = payload['threshold_value']

            for file in files_names:
                image_string = convert_image_to_base64(f'./input/images/{file}')
                output_image_name = f"./output/images/{file}"
                input_image_name = f"./input/images/{file}"
                
                detected_rois = detect_area(input_image_name, output_image_name, threshold_value)

            response = {}

            return ApiResponse(response).get_response()

        except WrongPayload as wp:
            return wp.get_response()
