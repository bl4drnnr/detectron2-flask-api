import os
import sys
import cv2
import detectron2
import numpy as numpy
import matplotlib.pyplot as plt
import requests
import json
import base64

from flask import request
from flask_restful import Resource
from pathlib import Path
from detectron2.utils.logger import setup_logger
from detectron2 import model_zoo
from detectron2.engine import DefaultPredictor
from detectron2.config import get_cfg
from detectron2.utils.visualizer import Visualizer, ColorMode
from PIL import Image

from src.helpers.image_converter import *
from src.api_responses import *

setup_logger()

REQUIRED_PAYLOAD = [
    'threshold_value',
    'image_string',
    'input_image_name',
    'output_image_name'
]


def check_required_payload(payload):
    for payload_item in REQUIRED_PAYLOAD:
        if payload_item not in payload:
            raise WrongPayload()


class DetectAreaBase64(Resource):
    def post(self):
        try:
            posted_data = request.get_json()
            status_code = check_required_payload(posted_data)

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


def on_image_draw(image_path, output_image_name, predictor):
    im = cv2.imread(image_path)
    outputs = predictor(im)
    v = Visualizer(im[:,:,::-1], scale=0.7)
    v = v.draw_instance_predictions(outputs["instances"].to("cpu"))
    out_img = v.get_image()
    cv2.imwrite(output_image_name, cv2.cvtColor(out_img, cv2.COLOR_BGR2RGB))
    return v


def on_image_get_points_scores(image_path, predictor):
    im = cv2.imread(image_path)
    outputs = predictor(im)
    scores = outputs['instances'].scores
    scores_all = [score_item.item() for score_item in scores]
    boxes_all = outputs['instances'].pred_boxes.tensor.cpu().numpy()
    return scores_all, boxes_all


def crop_object(image, box):
    x_top_left = box[0]
    y_top_left = box[1]
    x_bottom_right = box[2]
    y_bottom_right = box[3]
    return image.crop((int(x_top_left), int(y_top_left), int(x_bottom_right), int(y_bottom_right)))


def detect_area(input_image_name, output_image_name, threshold):
    input_threshold = threshold
    input_threshold_float = float(input_threshold)

    cfg_pred = get_cfg()
    cfg_pred.merge_from_file(model_zoo.get_config_file("COCO-InstanceSegmentation/mask_rcnn_R_101_FPN_3x.yaml"))
    cfg_pred.MODEL.WEIGHTS = "./input/pth_model/model_final.pth"
    cfg_pred.MODEL.ROI_HEADS.NUM_CLASSES = 1
    cfg_pred.MODEL.SCORE_THRESH_TEST = input_threshold_float
    cfg_pred.MODEL.DEVICE = "cpu"
    
    predictor = DefaultPredictor(cfg_pred)
    input_image_path = input_image_name
    on_image_draw(input_image_path, output_image_name, predictor)
    scores, boxes = on_image_get_points_scores(input_image_path, predictor)
    rois = [(
            {f'box_{i}': boxes[i].tolist()},
            {f'score_{i}': scores[i]}
        ) for i in range(len(scores))]

    example_image = cv2.imread(input_image_path)
    example_image_converted = cv2.cvtColor(example_image, cv2.COLOR_BGR2RGB)
    image_pil = Image.fromarray(example_image_converted)

    for i, box in enumerate(boxes):
        crop_image = crop_object(image_pil, box)
        image_np = numpy.asarray(crop_image)
        cv2.imwrite(
            f'./output/images/OUTPUT_PARTIAL_IMAGE_{i}.jpg',
            cv2.cvtColor(image_np, cv2.COLOR_BGR2RGB)
        )
    return rois
