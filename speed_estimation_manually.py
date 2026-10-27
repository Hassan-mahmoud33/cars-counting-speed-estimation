from pathlib import Path

import cv2
from ultralytics import YOLO

project_dir = Path(__file__).resolve().parent
model_path = project_dir / "yolo26n.pt"
video_path = project_dir / "veh2.mp4"

if not video_path.is_file():
    raise FileNotFoundError(f"Video file not found: {video_path}")

model = YOLO(model_path)

cap = cv2.VideoCapture(video_path)
if not cap.isOpened():
    cap.release()
    raise RuntimeError(f"Could not open video file: {video_path}")
 
width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)) 
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)) 
 
y_line1 = int(height * 2 / 3)  
y_line2 = y_line1 + 200 
counter = 0 

track_history = {} 
speed_data = {}
start_times = {}
distance_between_lines = 20  # suppose this distance

cv2.namedWindow('COUNTING', cv2.WINDOW_NORMAL) 
cv2.resizeWindow('COUNTING', 1100, 600) 
 
while cap.isOpened(): 
 
    ret, frame = cap.read() 
 
    if not ret: 
        break 
 
    current_time = cap.get(cv2.CAP_PROP_POS_MSEC) / 1000
 
    results = model.track(
        frame,
        persist=True,
        classes=[2],
        conf=0.40,
        tracker='bytetrack.yaml'
    ) 
 
    if results[0].boxes.id is not None: 
 
        boxes = results[0].boxes.xywh.cpu()    
        ids = results[0].boxes.id.int().cpu().tolist() 
 
        for box, id in zip(boxes, ids): 
 
            x_center, y_center, w, h = box  
            x_center = float(x_center)
            y_center = float(y_center) 
 
 
            if id in track_history: 
                previous_location = track_history[id] 

                # =====================================
                # The First Side

                if previous_location < y_line1 <= y_center: 
                    counter += 1  
                    start_times[id] = current_time

 
                elif previous_location > y_line1 >= y_center: 
                    counter += 1
                    start_times[id] = current_time

                # =====================================
                # The Other Side

                if previous_location < y_line2 <= y_center:

                    if id in start_times:
                        elapsed_time = current_time - start_times[id]

                        if elapsed_time > 0:

                            speed_mps = distance_between_lines / elapsed_time
                            speed_kmh = speed_mps * 3.6
                            speed_data[id] = speed_kmh


                elif previous_location > y_line2 >= y_center:

                    if id in start_times:

                        elapsed_time = current_time - start_times[id]

                        if elapsed_time > 0:

                            speed_mps = distance_between_lines / elapsed_time

                            speed_kmh = speed_mps * 3.6

                            speed_data[id] = speed_kmh

 
            track_history[id] = y_center 
 
 
    annotated_frame = results[0].plot() 
 
    cv2.line(
        annotated_frame,
        (0, y_line1),
        (width, y_line1),
        (255, 255, 255),
        3
            ) 
     
    cv2.line(
        annotated_frame,
        (0, y_line2),
        (width, y_line2),
        (10, 10, 10),
        3
             ) 
 
    cv2.putText(
        annotated_frame,
        f'Counter: {counter}',
        (20, 50),
        cv2.FONT_HERSHEY_COMPLEX_SMALL,
        2,
        (0, 255, 0),
        5
                ) 

    if results[0].boxes.id is not None:

        boxes = results[0].boxes.xywh.cpu()
        ids = results[0].boxes.id.int().cpu().tolist()

        for box, id in zip(boxes, ids):

            x_center, y_center, w, h = box

            x_center = int(x_center)
            y_center = int(y_center)

            if id in speed_data :

                speed = speed_data[id]

                cv2.putText(
                    annotated_frame,
                    f'|  Id: {id}  Speed: {speed:.1f} Km/h',
                    ( 300,  50 ),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    1.5 ,
                    (0, 255, 0),
                    2
                )


     
    cv2.imshow('COUNTING', annotated_frame) 
 
    if cv2.waitKey(1) & 0xFF == ord(' '): 
        break 

 
cap.release() 
cv2.destroyAllWindows()
