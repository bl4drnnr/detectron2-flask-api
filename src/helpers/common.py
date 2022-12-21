import os
import sys
import cv2
import detectron2
import numpy as numpy
import matplotlib.pyplot as plt
import requests
import json
import base64

from pathlib import Path
from detectron2 import model_zoo
from detectron2.engine import DefaultPredictor
from detectron2.config import get_cfg
from detectron2.utils.visualizer import Visualizer, ColorMode
from PIL import Image


def check_required_payload(payload, REQUIRED_PAYLOAD):
    for payload_item in REQUIRED_PAYLOAD:
        if payload_item not in payload:
            raise WrongPayload()


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
