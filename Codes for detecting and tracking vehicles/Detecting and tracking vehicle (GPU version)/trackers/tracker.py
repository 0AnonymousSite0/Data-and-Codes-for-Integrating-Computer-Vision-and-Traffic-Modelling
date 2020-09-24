import sys
sys.path.append('..')
import numpy as np
from trackers.opencv.opencv_trackers import csrt_create, kcf_create
from trackers.camshift.camshift_tracker import camshift_create
from blobs.utils import get_centroid, get_area, get_iou
from counter import is_passed_counting_line
from util.vehicle_info import generate_vehicle_id
from util.logger import log_info
from util.bounding_box import get_box_image
from util.image import get_base64_image
import cv2

def create_blob(bounding_box, vehicle_type, type_confidence, frame, model):
    if model == 'csrt':
        return csrt_create(bounding_box, vehicle_type, type_confidence, frame)
    if model == 'kcf':
        return kcf_create(bounding_box, vehicle_type, type_confidence, frame)
    if model == 'camshift':
        return camshift_create(bounding_box, vehicle_type, type_confidence, frame)
    else:
        raise Exception('Invalid tracker model/algorithm specified (options: csrt, kcf, camshift)')

def remove_stray_blobs(blobs, matched_blob_ids, mcdf):
    # remove blobs that hang after a tracked object has left the frame
    for _id, blob in list(blobs.items()):
        if _id not in matched_blob_ids:
            blob.num_consecutive_detection_failures += 1
        if blob.num_consecutive_detection_failures > mcdf:
            del blobs[_id]
    return blobs




def add_new_blobs(boxes, classes, confidences, blobs, frame, tracker, counting_line, line_position, mcdf):
    # add new blobs or update existing ones
    matched_blob_ids = []
    print(classes)
    print(boxes)
    for i in range(len(boxes)):
        if classes != []:
            print(classes[i])
            _type = classes[i]
        else:
            _type=None
        print (confidences)
        if confidences != []:
            _confidence = confidences[i]
        else:
            _confidence=None

        box_centroid = get_centroid(boxes[i])
        box_area = get_area(boxes[i])
        match_found = False
        for _id, blob in blobs.items():
            #print (_id,blob)
            if blob.counted == False and get_iou(boxes[i], blob.bounding_box) > 0.5:
                match_found = True
                if _id not in matched_blob_ids:
                    blob.num_consecutive_detection_failures = 0
                    matched_blob_ids.append(_id)
                temp_blob = create_blob(boxes[i], _type, _confidence, frame, tracker) # TODO: update blob w/o creating temp blob
                blob.update(temp_blob.bounding_box, _type, _confidence, temp_blob.tracker)
                #blob.trajectory


                # Create a sequence of points to make a contour

                #contour=cv2.contourArea([(100,100),(200,200),(500,500)])
                #cv2.pointPolygonTest([(100,100),(200,200),(500,500)], box_centroid, false)


                log_info('Blob updated.', {
                    'event': 'BLOB_UPSERT',
                    'vehicle_id': _id,
                    'bounding_box': blob.bounding_box,
                    'type': blob.type,
                    'type_confidence': blob.type_confidence,
                    'center': box_centroid,
                    #'direction': direction
                    #'trajectory':trajectory.append
                    #'image': get_base64_image(get_box_image(frame, blob.bounding_box))
                })

                break

        if not match_found and not is_passed_counting_line(box_centroid, counting_line, line_position):
            _blob = create_blob(boxes[i], _type, _confidence, frame, tracker)
            blob_id = generate_vehicle_id()
            blobs[blob_id] = _blob

            log_info('Blob created.', {
                'event': 'BLOB_UPSERT',
                'vehicle_id': blob_id,
                'bounding_box': _blob.bounding_box,
                'type': _blob.type,
                'type_confidence': _blob.type_confidence,
                'centere': box_centroid

                #'image': get_base64_image(get_box_image(frame, _blob.bounding_box))
            })

    blobs = remove_stray_blobs(blobs, matched_blob_ids, mcdf)
    return blobs

def remove_duplicates(blobs):
    for id_a, blob_a in list(blobs.items()):
        for id_b, blob_b in list(blobs.items()):
            if blob_a == blob_b:
                break

            if get_iou(blob_a.bounding_box, blob_b.bounding_box) > 0.5 and id_a in blobs:
                del blobs[id_a]
    return blobs


# area_of_left_left=np.array([[1, 1], [10, 50], [50, 50]], dtype=np.int32)
# area_of_left_straight=np.array([[1, 1], [10, 50], [50, 50]], dtype=np.int32)
# area_of_left_right=np.array([[1, 1], [10, 50], [50, 50]], dtype=np.int32)
# area_of_left=np.array([[1, 1], [10, 50], [50, 50]], dtype=np.int32)
# if area_of_left=True:
#     left_left =object_in_polygon(frame, area_of_left_straight)
#     area_of_left_straight =object_in_polygon(frame, area_of_left_straight)
#     area_of_left_right =

# def direction_of_vehicle(area_of_left=np.array)
#     if
#     left_left = object_in_polygon(frame, area_of_left_straight)
#     area_of_left_straight = object_in_polygon(frame, area_of_left_straight)
#     area_of_left_right =
#
#
#
# def object_in_polygon(frame, area_of_straight_direction):
#     contours = [area_of_straight_direction]
#     for cnt in contours:
#         cv2.drawContours(cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY), [cnt], 0, (255, 255, 255), 2)
#     # _, contours, _ = cv2.findContours(cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
#     direction = cv2.pointPolygonTest(contours[0], box_centroid, False)
# #                 vert = [None] * 3
# #                 vert[0] = (100, 100)
# #                 vert[1] = (100, 200)
# #                 vert[2] = (200, 200)
#     return direction
#                 # Draw it in src
#                 #for i in range(3):
#                     #cv2.line(frame, vert[i], vert[(i + 1) % 3], (255), 3)
