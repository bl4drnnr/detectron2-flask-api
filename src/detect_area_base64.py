import os
import sys
import cv2
import detectron2
import numpy as numpy
import matplotlib.pyplot as plt
import requests
import json
import base64

from flask import Flask, jsonify, request
from flask_restful import Api, Resource
from pathlib import Path
from detectron2.utils.logger import setup_logger
from detectron2 import model_zoo
from detectron2.engine import DefaultPredictor
from detectron2.config import get_cfg
from detectron2.utils.visualizer import Visualizer, ColorMode
from PIL import Image

from .image_converter import *

setup_logger()

class DetectAreaBase64(Resource):
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


def show_image(img, cmap=None):
    fig = plt.figure(figsize=(20, 10))
    ax = fig.add_subplot(111)
    ax.imshow(img, cmap=cmap)


def on_image_draw(image_path, predictor):
    im = cv2.imread(image_path)
    outputs = predictor(im)
    v = Visualizer(
        im[:,:,::-1],
        scale=0.7
    )
    v = v.draw_instance_predictions(outputs["instances"].to("cpu"))
    out_img = v.get_image()
    cv2.imwrite(
        'OUTPUT_IMAGE.jpg',
        cv2.cvtColor(out_img, cv2.COLOR_BGR2RGB)
    )
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


def detect_area(image_name, threshold):
    input_threshold = threshold
    input_threshold_float = float(input_threshold)

    cfg_pred = get_cfg()
    cfg_pred.merge_from_file(model_zoo.get_config_file("COCO-InstanceSegmentation/mask_rcnn_R_101_FPN_3x.yaml"))
    cfg_pred.MODEL.WEIGHTS = "./input/pth_model/model_final.pth"
    cfg_pred.MODEL.ROI_HEADS.NUM_CLASSES = 1
    cfg_pred.MODEL.SCORE_THRESH_TEST = input_threshold_float
    
    predictor = DefaultPredicator(cfg_pred)
    input_image_path = './input/images/INPUT_IMAGE.jpg'
    on_image_draw(input_image_path, predictor)
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
            f'OUTPUT_PARTIAL_IMAGE_{i}.jpg',
            cv2.cvtColor(image_np, cv2.COLOR_BGR2RGB)
        )
    return rois


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
