import cv2
from trackers.tracker import add_new_blobs, remove_duplicates
from collections import OrderedDict
from detectors.detector import get_bounding_boxes
import time
from util.detection_roi import get_roi_frame, draw_roi
from counter import get_counting_line, is_passed_counting_line
from util.logger import log_info
import numpy as np
import random



import os
class VehicleCounter():

    def __init__(self, initial_frame, detector, tracker, droi, show_droi, mcdf, mctf, di, cl_position):
        self.frame = initial_frame # current frame of video
        self.detector = detector
        self.tracker = tracker
        self.droi =  droi # detection region of interest
        self.show_droi = show_droi
        self.mcdf = mcdf # maximum consecutive detection failures
        self.mctf = mctf # maximum consecutive tracking failures
        self.di = di # detection interval
        self.cl_position = cl_position # counting line position

        self.blobs = OrderedDict()
        self.f_height, self.f_width, _ = self.frame.shape
        self.frame_count = 0 # number of frames since last detection
        self.vehicle_count = 0 # number of vehicles counted
        self.types_counts = OrderedDict() # counts by vehicle type
        self.counting_line = None if cl_position == None else get_counting_line(self.cl_position, self.f_width, self.f_height)

        # create blobs from initial frame
        droi_frame = get_roi_frame(self.frame, self.droi)
        _bounding_boxes, _classes, _confidences = get_bounding_boxes(droi_frame, self.detector)
        #print (droi_frame)
        self.blobs = add_new_blobs(_bounding_boxes, _classes, _confidences, self.blobs, self.frame, self.tracker, self.counting_line, self.cl_position, self.mcdf)

    def get_count(self):
        return self.vehicle_count

    def get_blobs(self):
        return self.blobs

    def count(self, frame):
        log = []
        self.frame = frame

        for _id, blob in list(self.blobs.items()):
            # update trackers
            success, box = blob.tracker.update(self.frame)
            if success:
                blob.num_consecutive_tracking_failures = 0
                blob.update(box)
                log_info('Vehicle tracker updated.', {
                    'event': 'TRACKER_UPDATE',
                    'vehicle_id': _id,
                    'bounding_box': blob.bounding_box,
                    'centroid': blob.centroid,
                })
                f = './ProcessRecords/Vehicletrackerupdated58.txt'
                with open(f, "a") as file:
                    file.write('TRACKER_UPDATE' +'-'+ 'id' + str(_id) + '-'+'bounding_box'+ str(blob.bounding_box) +'-' + 'centroid' + str(
                        blob.centroid) + "\n")

            else:
                blob.num_consecutive_tracking_failures += 1

            # count vehicles that have left the frame if no counting line exists
            # or those that have passed the counting line if one exists
            if (self.counting_line == None and \
                    (blob.num_consecutive_tracking_failures == self.mctf or blob.num_consecutive_detection_failures == self.mcdf) and \
                    not blob.counted) \
                        or \
                    (self.counting_line != None and \
                    # don't count a blob if it was first detected at a position past the counting line
                    # this enforces counting in only one direction
                    not is_passed_counting_line(blob.position_first_detected, self.counting_line, self.cl_position) and \
                    is_passed_counting_line(blob.centroid, self.counting_line, self.cl_position) and \
                    not blob.counted):
                blob.counted = True
                self.vehicle_count += 1
                # count by vehicle type
                if blob.type != None:
                    if blob.type in self.types_counts:
                        self.types_counts[blob.type] += 1
                    else:
                        self.types_counts[blob.type] = 1
                log_info('Vehicle counted.', {
                    'event': 'VEHICLE_COUNT',
                    'id': _id,
                    'type': blob.type,
                    'count': self.vehicle_count,
                    'position_first_detected': blob.position_first_detected,
                    'position_counted': blob.centroid,
                    'counted_at':time.time(),
                    })
                f ='./ProcessRecords/Vehiclecounted58.txt'
                with open(f, "a") as file:
                    file.write( 'VEHICLE_COUNT'+'-' +'id'+ str(_id)+'-' +'type'+str(blob.type)+'-' +'count'+str(self.vehicle_count)+'-' +'position_first_detected'+str(blob.position_first_detected)+'-' +'position_counted'+str(blob.centroid)+'-' +'counted_at'+str(time.time())+"\n")

            if blob.num_consecutive_tracking_failures >= self.mctf:    
                # delete untracked blobs
                del self.blobs[_id]

        if self.frame_count >= self.di:
            # rerun detection
            droi_frame = get_roi_frame(self.frame, self.droi)
            _bounding_boxes, _classes, _confidences = get_bounding_boxes(droi_frame, self.detector)
            self.blobs = add_new_blobs(_bounding_boxes, _classes, _confidences, self.blobs, self.frame, self.tracker, self.counting_line, self.cl_position, self.mcdf)
            self.blobs = remove_duplicates(self.blobs)
            self.frame_count = 0

        self.frame_count += 1

        return log

    # def trajectory(self, frame):
    #     self.frame = frame
    #     for _id, blob in self.blobs.items():



    def visualize(self):
        frame = self.frame


        # draw and label blob bounding boxes
        for _id, blob in self.blobs.items():
            (x, y, w, h) = [int(v) for v in blob.bounding_box]
            cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)
            a = (2 * x + w) / 2  # x,y更新了？
            b = (2 * y + h) / 2
            #blob.center = ([a, b])

            #file = open(_id+r".txt", "a")
            #point2 = (a+300, b+300)
            #points=np.loadtxt(_id + r".txt")

            #新添加的
            path=r"D:\ZHOUSHENGHUA\Vehicle-Counting-master-CPU\Location\58"+'\\'+_id+r".txt"
            if os.path.exists(path):
                trace=np.append(np.loadtxt(path, delimiter=','),np.array([[a,b]]),axis=0,)

                #print (recent_trace)
                np.savetxt(path,trace,delimiter=',')
                #print (trace)
                a=random.randint(0,255)
                b=random.randint(0,255)
                c=random.randint(0,255)
                cv2.polylines(frame, np.int32([trace]), 0, (a, b, c),2)
            else:
                data=np.array([[a,b],[a,b]])
                np.savetxt(path, data, delimiter=',')
            # 新添加的
           # points = np.array(blob.center)
            #points=np.append([blob.center],[point2],axis=0)
            #points.append(blob.center,)
            #points.append([100,100])
            # points.dtype => 'int64'

            vehicle_label = 'ID: ' + _id[:8] \
                if blob.type == None else '{0} ({1}) '.format(blob.type, str(blob.type_confidence)[:4])
            # else 'ID: {0}, Type: {1} ({2})'.format(_id[:8], blob.type, str(blob.type_confidence)[:4])
            # change

            #np.int32([points])
            #cv2.putText(frame, vehicle_label, (x, y - 5), cv2.FONT_HERSHEY_DUPLEX, 0.3, (255, 0, 0), 1, cv2.LINE_AA) #0.3字体大小，0.5字体粗细
            #cv2.polylines(frame,[(300,300), (100,100),(200,500)], 0, (0, 0, 255))
        # draw counting line
        if self.counting_line != None:
            cv2.line(frame, self.counting_line[0], self.counting_line[1], (255, 0, 0), 3)
        # display vehicle count
        types_counts_str = ', '.join([': '.join(map(str, i)) for i in self.types_counts.items()])
        types_counts_str = ' (' + types_counts_str + ')' if types_counts_str != '' else types_counts_str
        #cv2.putText(frame, 'Count: ' + str(self.vehicle_count) + types_counts_str, (20, 60), cv2.FONT_HERSHEY_DUPLEX, 0.5, (255, 255, 0), 1, cv2.LINE_AA)
        # show detection roi
        if self.show_droi:
            frame = draw_roi(frame, self.droi)

        return frame