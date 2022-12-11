import requests
import json
import os
import sys
import cv2
import base64

from flask import Flask, jsonify, request
from flask_restful import Api, Resource
from pathlib import Path

from src.detect_area import *
from src.image_converter import *

PORT = 5000

app = Flask(__name__)
api = Api(app)


@app.route('/api')
def main():
    return f'<h1>The Flask App has been started on port {PORT}</h1>'


def generate_return_dictionary(status, msg):
    return {
        'status': status,
        'msg': msg
    }


def check_posted_data(posted_data, function_name):
    if function_name == 'detect_area':
        return 301
    elif 'threshold_value' not in posted_data:
        return 302
    elif 'image_string' not in posted_data:
        return 303
    else:
        return 200


class DetectArea(Resource):
    def post(self):
        posted_data = request.get_json()
        status_code = check_posted_data(posted_data, 'detect_area')

        if status_code != 200:
            response = {
                'status_code': status_code,
                'message': 'An error has occured',
            }
            return jsonify(response)

        image_name = posted_data['image_name']
        threshold_value = posted_data['threshold_value']
        image_string = posted_data['image_string']

        create_image_from_string('INPUT_IMAGE.jpg', bytes(image_string, 'utf-8'))
        detected_rois = detect_area(image_name, threshold_value)

        out_image_base = convert_image_to_base64('./output/images/OUTPUT_IMAGE.jpg')
        save_encoded_string('./output/string_images/OUTPUT_JSON_BASE.txt', out_image_base)
        out_image_string = out_image_base.decode('UTF-8')

        out_partial_image_table = []
        for i in range(len(detected_rois)):
            out_part_image_base = convert_image_to_base64(f'./output/images/OUTPUT_PARTIAL_IMAGE_{i}.jpg')
            
            save_encoded_string(f'./output/string_images/OUTPUT_PARTIAL_IMAGE_JSON_BASE_{i}.txt', out_part_image_base)

            out_partial_image_string = out_part_image_base.decode('UTF-8')
            out_partial_image_table.append({f'partial_image_{i}': out_partial_image_string})
        
        response = {
            'a_status_code': status_code,
            'b_message': 'Detected area',
            'c_detected_bounding_boxes': detected_rois,
            'd_partial_images': out_partial_image_table,
            'e_output_image': out_image_string
        }

        return jsonify(response)


api.add_resource(DetectArea, '/detect-area')


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=PORT, debug=True)
