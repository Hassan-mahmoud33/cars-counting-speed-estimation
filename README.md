# Car Detection and Speed Estimation

This project uses YOLOv8 to track cars in a video, count when they cross a line, and estimate their speed between two lines.

## Files

- `main.py`: the main script.
- `veh2.mp4`: the video processed by the script.
- `yolov8n.pt`: the YOLOv8n model weights.

## Run

Install Python and the required packages:

```bash
pip install opencv-python numpy ultralytics
```

Open a terminal in this folder and run:

```bash
python main.py
```

A window will show the video with tracking, two lines, and a counter. Press the space bar to stop playback.

## Counting and Speed Notes

- The script tracks the car class detected by YOLO and increases the counter whenever a car crosses the first line. The counter records crossings, not unique cars, so a car may be counted again if it crosses the line another time.
- Speed is estimated when a car moves downward in the image, crossing the first line and then the second. The counter detects crossings in either direction, but speed is not calculated reliably for cars moving upward.
- The script assumes the distance between the lines is `20` meters (`distance_between_lines`). This is a placeholder, not a calibrated measurement; set it to the real-world distance represented by the two lines in your video for a more realistic estimate.
- The first line's position depends on the video height, and the second line is placed `200` pixels below it. Speed accuracy depends on the video and the distance value you enter.
- Results are shown on screen only; the script does not save an output video.
