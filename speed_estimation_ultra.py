from ultralytics import solutions
from pathlib import Path
import cv2

#--------------------------------------------

project_dir = Path(__file__).resolve().parent
model_path = project_dir / "yolo26n.pt"
video_path = project_dir / "veh2.mp4"
output_path = project_dir / "output_ultra.mp4"


if not video_path.is_file():
    raise FileNotFoundError(f"Video file not found: {video_path}")

#--------------------------------------------

cap = cv2.VideoCapture(video_path)
if not cap.isOpened():
    cap.release()
    raise RuntimeError(f"Could not open video file: {video_path}")

width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
fps = cap.get(cv2.CAP_PROP_FPS)

display_width = 960
display_height = int(display_width * height / width)
scale = width / display_width

#--------------------------------------------

save_video = not output_path.exists()
output = None

if save_video:
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    output = cv2.VideoWriter(str(output_path), fourcc, fps, (width, height))

#---------------------------------------------------------------
# to get line points
line = []

def mouse( event , x , y , flags , param):
    if event == cv2.EVENT_LBUTTONDOWN and len(line) < 2 :
        line.append((int(x * scale), int(y * scale)))


WINDOW = 'Estimation_Speed'
cv2.namedWindow(WINDOW)
cv2.setMouseCallback(WINDOW, mouse)

#----------------------------------------------------------------

# to display the line 

ret, first_frame = cap.read()
if not ret:
    raise RuntimeError("Could not read the first frame")

while len(line) < 2:
    
    for point in line:
        cv2.circle(first_frame, point, 8, (0, 0, 255), -1)


    cv2.imshow(WINDOW, cv2.resize(first_frame, (display_width, display_height)))

    if cv2.waitKey(20) & 0xFF == ord(' '):
        cap.release()
        cv2.destroyAllWindows()

#------------------------------------------

cv2.line(first_frame, line[0], line[1], (0, 0, 255), 5)

cv2.imshow(WINDOW, cv2.resize(first_frame, (display_width, display_height)))
cv2.waitKey(2000)

cap.set(cv2.CAP_PROP_POS_FRAMES, 0)

#--------------------------------------------
# object to estimate speed

speed_obj = solutions.SpeedEstimator(
    show=False,
    model=str(model_path),
    region=line,
    classes=[2],
    fps=fps,
)

#--------------------------------------------



while cap.isOpened(): 
 
    ret, frame = cap.read() 
 
    if not ret: 
        break 


    output_frame = speed_obj(frame).plot_im

    if save_video:
        output.write(output_frame)

    displayed = cv2.resize( output_frame , (display_width, display_height))
    cv2.imshow(WINDOW, displayed )

    if cv2.waitKey(1) & 0xFF == ord(' '):
        break


if save_video:
    output.release()

cap.release()
cv2.destroyAllWindows()
