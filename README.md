# Car Detection and Speed Estimation

Detects and tracks cars in a video with YOLO26n and estimates their speed. The project has two versions of the same idea: one written by hand with OpenCV, and one built on the Ultralytics `SpeedEstimator`.

<!-- Add a short demo GIF here once you have one: ![demo](demo.gif) -->

## Files

- `speed_estimation_manually.py`: Method 1. Tracks cars, counts line crossings, and calculates speed between two lines.
- `speed_estimation_ultra.py`: Method 2. Uses the Ultralytics `SpeedEstimator`, with the line drawn by clicking on the first frame.
- `sample.mp4`: short sample input video.
- `veh2.mp4`: full input video (not included in the repo, see [Input video](#input-video)).
- `output_ultra.mp4`: video produced by Method 2 (created on the first run).
- `yolo26n.pt`: YOLO26n weights. If the file is missing, Ultralytics downloads the official weights on first run (internet required).

## Input video

Both scripts look for `veh2.mp4` next to the script. If it is not found, they fall back to `sample.mp4`, so the project runs out of the box.

To use the full video, download it from the original source and place it next to the scripts as `veh2.mp4`:

- Source: https://github.com/AhmedIbrahimai/Car-speed-estimation-and-counting-using-YOLOv8-computer-vision

## Install

```bash
pip install opencv-python numpy ultralytics
```

## Run

From this folder:

```bash
python speed_estimation_manually.py
```

```bash
python speed_estimation_ultra.py
```

Paths are resolved relative to each script, so you can run them from any directory. Press the space bar to stop playback.

## Method 1: Manual

- Tracks cars with ByteTrack and increases a counter each time a car crosses the first line. The counter counts crossings, not unique cars, so a car that crosses again is counted again. Crossings in either direction are counted.
- Speed is the known distance between the two lines divided by the time the car takes to travel between them. It is only reliable for cars moving downward in the image.
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

## Limitations

- Speeds are estimates, not measurements. They depend on the camera angle and on the distance or pixel-to-meter scale, none of which are calibrated. For better accuracy, compare against a car with a known speed.
- In Method 1 the speed text is drawn at a fixed position, so labels of several cars can overlap.
- Only the `car` class is tracked.

## Acknowledgments

The test video comes from the project linked in [Input video](#input-video).
