# Car Detection and Speed Estimation

Detects and tracks cars in a video with YOLO26n and estimates their speed. The project has two versions of the same idea: one written by hand with OpenCV, and one built on the Ultralytics `SpeedEstimator`.

## Files

- `speed_estimate_manually.py`: Method 1. Tracks cars, counts line crossings, and calculates speed between two lines.
- `speed_estimation_ultra.py`: Method 2. Uses the Ultralytics `SpeedEstimator`, with the line drawn by clicking on the first frame.
- `veh2.mp4`: input video.
- `output_ultra.mp4`: video produced by Method 2.
- `yolo26n.pt`: YOLO26n weights. If the file is missing, Ultralytics downloads the official weights on first run (internet required).

## Install

```bash
pip install opencv-python numpy ultralytics
```

## Run

From this folder:

```bash
python speed_estimate_manually.py
```

```bash
python speed_estimation_ultra.py
```

Paths are resolved relative to each script, so you can run them from any directory. Press the space bar to stop playback.

## Method 1: Manual

- Tracks cars with ByteTrack and increases a counter each time a car crosses the first line. The counter counts crossings, not unique cars, so a car that crosses again is counted again.
- Speed is the known distance between the two lines divided by the time the car takes to travel between them. It is only reliable for cars moving downward in the image. Crossings in either direction are counted.
- `distance_between_lines` is set to `20` meters as a placeholder. Replace it with the real distance for realistic numbers.
- The first line sits at two thirds of the video height, and the second is `200` pixels below it.
- Output is shown on screen only. No video is saved.

## Method 2: Ultralytics SpeedEstimator

1. The first frame is shown. Click two points to define the line (ideally one on each side of the road). The line is previewed for two seconds, then the video starts.
2. `SpeedEstimator` detects and tracks cars (class `car` only) and draws each car's speed on the frame.
3. The annotated video is saved at the original resolution to `output_ultra.mp4`.

Notes:

- Clicks are mapped back to the original frame size, so the display size (960 px wide) does not affect the result. Detection and speed estimation always run on the original frame.
- If `output_ultra.mp4` already exists, the script plays the video without saving. Delete the file to generate a new one.
- Speeds are estimates. They depend on camera angle and on the pixel-to-meter scale, so they are not calibrated. For better accuracy, compare against a car with a known speed.
- Stop with the space bar so the output file is closed properly.

## Comparison

| | Method 1 (Manual) | Method 2 (Ultralytics) |
|---|---|---|
| Code length | Long | Short |
| Line setup | Fixed in code | Chosen by clicking |
| Control over details | Full | Limited |
| Car counter | Yes | No |
| Saves output video | No | Yes (if it doesn't exist) |
| Best for | Understanding how speed is calculated | Quick estimation |