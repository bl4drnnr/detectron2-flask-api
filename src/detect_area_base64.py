from flask import request
from flask_restful import Resource
from detectron2.utils.logger import setup_logger

from src.helpers.image_converter import *
from src.helpers.common import *
from src.api_responses import *

setup_logger()

REQUIRED_PAYLOAD = [
    'threshold_value',
    'image_string',
    'input_image_name',
    'output_image_name'
]


class DetectAreaBase64(Resource):
    def post(self):
        try:
            posted_data = request.get_json()
            status_code = check_required_payload(posted_data, REQUIRED_PAYLOAD)

            threshold_value = posted_data['threshold_value']
            image_string = posted_data['image_string']
            input_image_name = f"./input/images/{posted_data['input_image_name']}"
            output_image_name = f"./output/images/{posted_data['output_image_name']}"

            create_image_from_string(input_image_name, bytes(image_string, 'utf-8'))
            detected_rois = detect_area(input_image_name, output_image_name, threshold_value)

            out_image_base = convert_image_to_base64(output_image_name)
            save_encoded_string('./output/string_images/OUTPUT_JSON_BASE.txt', out_image_base)
            out_image_string = out_image_base.decode('UTF-8')

            out_partial_image_table = []
            for i in range(len(detected_rois)):
                out_part_image_base = convert_image_to_base64(
                    f'./output/images/OUTPUT_PARTIAL_IMAGE_{i}.jpg'
                )
                
                save_encoded_string(
                    f'./output/string_images/OUTPUT_PARTIAL_IMAGE_JSON_BASE_{i}.txt', out_part_image_base
                )

                out_partial_image_string = out_part_image_base.decode('UTF-8')
                out_partial_image_table.append({f'partial_image_{i}': out_partial_image_string})
            
            response = {
                'detected_bounding_boxes': detected_rois,
                'partial_images': out_partial_image_table,
                'output_image': out_image_string
            }

            return ApiResponse(response).get_response()

        except WrongPayload as wp:
            return wp.get_response()
