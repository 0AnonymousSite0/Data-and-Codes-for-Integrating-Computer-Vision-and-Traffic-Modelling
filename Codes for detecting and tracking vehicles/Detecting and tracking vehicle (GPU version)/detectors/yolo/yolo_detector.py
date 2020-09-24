"""
Perform detection using models created with the YOLO (You Only Look Once) neural net.
https://pjreddie.com/darknet/yolo/
"""

import cv2
import numpy as np
import os
#from dotenv import load_dotenv


__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
#load_dotenv()
with open(r'D:\ZHOUSHENGHUA\Vehicle-Counting-master-CPU\model_data\coco_classes.txt', 'r') as classes_file:
    classes = dict(enumerate([line.strip() for line in classes_file.readlines()]))
    print(classes)
with open(r'D:\ZHOUSHENGHUA\Vehicle-Counting-master-CPU\model_data\classesinterested.txt', 'r') as coi_file:
    classes_of_interest = tuple([line.strip() for line in coi_file.readlines()])
    print(classes_of_interest)

# #_yolo = YOLO()
# def get_bounding_boxes(yolo, image):
#     _bounding_boxes, _classes, _confidences=yolo.detect_image_2(image)
#     out_classes=[]
#     print (len(out_classes))
#     print (len(_bounding_boxes))
#     print (len(_classes))
#     for i in range(0, len(_bounding_boxes)):
#         if _classes[i]==0:
#             out_classes.append('car')
#
#     return _bounding_boxes, out_classes, _confidences

def get_bounding_boxes(image):
    # create a YOLO v3 DNN model using pre-trained weights
   #net = cv2.dnn.readNet(os.getenv('\yolov3.weights'), os.getenv('\yolov3.cfg'))
    net = cv2.dnn.readNet(os.path.join(__location__, 'yolov3.weights'), os.path.join(__location__, 'yolov3.cfg'))

    # create image blob
    scale = 0.00392
    image_blob = cv2.dnn.blobFromImage(image, scale, (416, 416), (0, 0, 0), True, crop=False)

    # detect objects
    net.setInput(image_blob)
    layer_names = net.getLayerNames()
    output_layers = [layer_names[i[0] - 1] for i in net.getUnconnectedOutLayers()]
    outputs = net.forward(output_layers)

    _classes = []
    _confidences = []
    boxes = []
    conf_threshold = 0.5
    #float(os.getenv(0.5))
    nms_threshold = 0.4

    for output in outputs:
        for detection in output:
            scores = detection[5:]
            class_id = np.argmax(scores)
            confidence = scores[class_id]
            if confidence > 0.5 and classes[class_id] in classes_of_interest:
                width = image.shape[1]
                height = image.shape[0]
                center_x = int(detection[0] * width)
                center_y = int(detection[1] * height)
                w = int(detection[2] * width)
                h = int(detection[3] * height)
                x = center_x - w / 2
                y = center_y - h / 2
                _classes.append(classes[class_id])
                _confidences.append(float(confidence))
                boxes.append([x, y, w, h])

    # remove overlapping bounding boxes
    indices = cv2.dnn.NMSBoxes(boxes, _confidences, conf_threshold, nms_threshold)

    _bounding_boxes = []
    for i in indices:
        i = i[0]
        _bounding_boxes.append(boxes[i])
    #print (_bounding_boxes, _classes, _confidences)
    return _bounding_boxes, _classes, _confidences