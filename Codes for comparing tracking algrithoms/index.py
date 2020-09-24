import cv2
import sys
 
(major_ver, minor_ver, subminor_ver) = (cv2.__version__).split('.')


 
        # Set up tracker.
        # Instead of MIL, you can also use

tracker_types = ['BOOSTING', 'MIL','KCF', 'TLD', 'MEDIANFLOW', 'CSRT', 'MOSSE', 'GOTURN']
#tracker_type = tracker_types[7]
#for i in tracker_types:


# Read video
video = cv2.VideoCapture("./videos/53101508000815crop.mp4")

# Exit if video not opened.
if not video.isOpened():
    print("Could not open video")
    sys.exit()

# Read first frame.
ok, frame = video.read()
if not ok:
    print('Cannot read video file')
    sys.exit()

# Define an initial bounding box
bbox = (287, 23, 86, 320)

# Uncomment the line below to select a different bounding box
bbox = cv2.selectROI(frame, False)




# Initialize tracker with first frame and bounding box
tracker1 = cv2.TrackerBoosting_create()
ok1 = tracker1.init(frame, bbox)
tracker2 = cv2.TrackerMIL_create()
ok2 = tracker2.init(frame, bbox)
tracker3 = cv2.TrackerKCF_create()
ok3 = tracker3.init(frame, bbox)
tracker4 = cv2.TrackerTLD_create()
ok4 = tracker4.init(frame, bbox)
tracker5 = cv2.TrackerMedianFlow_create()
ok5 = tracker5.init(frame, bbox)
tracker6 = cv2.TrackerCSRT_create()
ok6 = tracker6.init(frame, bbox)
tracker7 = cv2.TrackerMOSSE_create()
ok7 = tracker7.init(frame, bbox)
tracker8 = cv2.TrackerGOTURN_create()
ok8 = tracker8.init(frame, bbox)
#     tracker = cv2.TrackerKCF_create()
# if tracker_type == 'TLD':
#     tracker = cv2.()
# if tracker_type == 'MEDIANFLOW':
#     tracker = cv2.()
# if tracker_type == 'CSRT':
#     tracker = cv2.()
# if tracker_type == 'MOSSE':
#     tracker = cv2.()
# if tracker_type == 'GOTURN':
#     tracker = cv2.TrackerGOTURN_create()

i =0
while True:
    i=i+1
    # Read a new frame
    ok, frame = video.read()
    if not ok:
        break

    # Start timer
    timer = cv2.getTickCount()

    # Update tracker

    # Calculate Frames per second (FPS)
    fps = cv2.getTickFrequency() / (cv2.getTickCount() - timer);


    ok1, bbox = tracker1.update(frame)
    if ok1:
        # Tracking success
        p1 = (int(bbox[0]), int(bbox[1]))
        p2 = (int(bbox[0] + bbox[2]), int(bbox[1] + bbox[3]))
        cv2.rectangle(frame, p1, p2, (255, 0, 0), 2, 1)
        print("BOOSTING")
        print(p1, p2)
        #cv2.putText(frame, "BOOSTING" , (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.55, (255, 0, 0),2);
    else:
        # Tracking failure
        cv2.putText(frame, "", (100, 80), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0, 0, 255),
                    2)


    ok2, bbox = tracker2.update(frame)
    if ok2:
        # Tracking success
        p1 = (int(bbox[0]), int(bbox[1]))
        p2 = (int(bbox[0] + bbox[2]), int(bbox[1] + bbox[3]))
        cv2.rectangle(frame, p1, p2, (255,125,0), 2, 1)
        print("MIL")
        print(p1, p2)
        #cv2.putText(frame, "MIL" , (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.55, (255,125,0), 2);
    else:
        # Tracking failure
        cv2.putText(frame, "", (100, 80), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0, 0, 255),
                    2)


    ok3, bbox = tracker3.update(frame)
    if ok3:
    # Tracking success
        p1 = (int(bbox[0]), int(bbox[1]))
        p2 = (int(bbox[0] + bbox[2]), int(bbox[1] + bbox[3]))
        cv2.rectangle(frame, p1, p2, (0,0,255), 2, 1)
        print("KCF")
        print(p1, p2)
        #cv2.putText(frame, "KCF" , (10, 70), cv2.FONT_HERSHEY_SIMPLEX, 0.55, (0,0,255),2);
    else:
    # Tracking failure
        cv2.putText(frame, "", (100, 80), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0, 0, 255),
                2)

    ok4, bbox = tracker4.update(frame)
    if ok4:
    # Tracking success
        p1 = (int(bbox[0]), int(bbox[1]))
        p2 = (int(bbox[0] + bbox[2]), int(bbox[1] + bbox[3]))
        cv2.rectangle(frame, p1, p2, (0,255,0), 2, 1)
        print("TLD")
        print(p1, p2)
        #cv2.putText(frame, "TLD" , (10, 90), cv2.FONT_HERSHEY_SIMPLEX, 0.55, (0,255,0),2);

    else:
    # Tracking failure
        cv2.putText(frame, "", (100, 80), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0, 0, 255),
                2)

    ok5, bbox = tracker5.update(frame)
    if ok5:
    # Tracking success
        p1 = (int(bbox[0]), int(bbox[1]))
        p2 = (int(bbox[0] + bbox[2]), int(bbox[1] + bbox[3]))
        cv2.rectangle(frame, p1, p2, (255,255,0), 2, 1)
        print("MEDIANFLOW")
        print(p1, p2)
        #cv2.putText(frame, "MEDIANFLOW" , (10, 110), cv2.FONT_HERSHEY_SIMPLEX, 0.55, (255,255,0),2);

    else:
    # Tracking failure
        cv2.putText(frame, "", (100, 80), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0, 0, 255),2)


    ok6, bbox = tracker6.update(frame)
    if ok6:
    # Tracking success
        p1 = (int(bbox[0]), int(bbox[1]))
        p2 = (int(bbox[0] + bbox[2]), int(bbox[1] + bbox[3]))
        cv2.rectangle(frame, p1, p2, (0,255,255), 2, 1)
        print("CSRT")
        print(p1, p2)
        #cv2.putText(frame, "CSRT" , (10, 130), cv2.FONT_HERSHEY_SIMPLEX, 0.55, (0,255,255),2);
    else:
    # Tracking failure
        cv2.putText(frame, "", (100, 80), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0, 0, 255),
                2)

    ok7, bbox = tracker7.update(frame)
    if ok7:
    # Tracking success
        p1 = (int(bbox[0]), int(bbox[1]))
        p2 = (int(bbox[0] + bbox[2]), int(bbox[1] + bbox[3]))
        cv2.rectangle(frame, p1, p2, (255,0,255), 2, 1)
        print("MOSSE")
        print(p1, p2)
        #cv2.putText(frame, "MOSSE", (10, 150), cv2.FONT_HERSHEY_SIMPLEX, 0.55, (255,0,255), 2);

    else:
    # Tracking failure
        cv2.putText(frame, "", (100, 80), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0, 0, 255),2)


    ok8, bbox = tracker8.update(frame)
    if ok8:
        # Tracking success
        p1 = (int(bbox[0]), int(bbox[1]))
        p2 = (int(bbox[0] + bbox[2]), int(bbox[1] + bbox[3]))
        cv2.rectangle(frame, p1, p2, (255, 255, 255), 2, 1)
        print("GOTURN")
        print(p1, p2)
        #cv2.putText(frame, "GOTURN", (10, 170), cv2.FONT_HERSHEY_SIMPLEX, 0.55, (255, 255, 255), 2);
    else:
        # Tracking failure
        cv2.putText(frame, "", (100, 80), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0, 0, 255),
                    2)




    # Draw bounding box


    # Display tracker type on frame
    # cv2.putText(frame, tracker_type + " Tracker", (100,20), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (50,170,50),2);

    # Display FPS on frame
    #cv2.putText(frame, "FPS : " + str(int(fps)), (100,50), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (50,170,50), 2);

    # Display result
    cv2.imwrite('./videos/frames' +str(i) + '.jpg', frame)
    cv2.imshow("Tracking", frame)

    # Exit if ESC pressed
    k = cv2.waitKey(1) & 0xff
    if k == 27 : break