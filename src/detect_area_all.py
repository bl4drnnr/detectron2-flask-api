from flask import request
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
            payload = request.get_json()
            check_required_payload(payload, REQUIRED_PAYLOAD)

            threshold_value = payload['threshold_value']
            all_files = os.listdir('./input/images')
            response = []

            if len(all_files) == 0:
                response = {"message": "no input files"}
                return ApiResponse(response).get_response()

            for file_name in all_files:
                output_image_name = f"./output/images/{file_name}"
                input_image_name = f"./input/images/{file_name}"
                
                detected_rois = detect_area(input_image_name, output_image_name, threshold_value)

                out_image_base = convert_image_to_base64(output_image_name)
                save_encoded_string(f'./output/string_images/OUTPUT_BASE_{file_name.split(".")[0]}.txt', out_image_base)
                out_image_string = out_image_base.decode('UTF-8')

                out_partial_image_table = []
                for i in range(len(detected_rois)):
                    out_part_image_base = convert_image_to_base64(
                        f'./output/images/OUTPUT_PARTIAL_IMAGE_{file_name.split(".")[0]}_{i}.jpg'
                    )
                    
                    save_encoded_string(
                        f'./output/string_images/OUTPUT_PARTIAL_IMAGE_BASE_{file_name.split(".")[0]}_{i}.txt', 
                        out_part_image_base
                    )

                    out_partial_image_string = out_part_image_base.decode('UTF-8')
                    out_partial_image_table.append({f'partial_image_{i}': out_partial_image_string})
                
                response.append({
                    'input_image_name': file_name,
                    'detected_bounding_boxes': detected_rois,
                    'partial_images': out_partial_image_table,
                    'output_image': out_image_string
                })

            return ApiResponse(response).get_response()

        except WrongPayload as wp:
            return wp.get_response()
