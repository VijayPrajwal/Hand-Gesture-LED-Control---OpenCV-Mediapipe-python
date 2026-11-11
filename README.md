# Hand Gesture Controlled LEDs using OpenCV, MediaPipe and Arduino

A beginner computer vision and Arduino project that controls five LEDs using hand movements captured through a webcam.

I built this project to learn how Python, real-time hand tracking, and physical hardware can work together.

## How it works

1. **OpenCV** captures live webcam video.
2. **MediaPipe** detects 21 hand landmarks.
3. Python checks the landmark coordinates to identify which fingers are raised.
4. **PyFirmata2** sends the finger states to an Arduino Uno over USB.
5. Each finger controls its corresponding LED.

| Finger | Arduino digital pin |
| --- | --- |
| Thumb | D6 |
| Index | D5 |
| Middle | D4 |
| Ring | D3 |
| Pinky | D2 |

A raised finger turns its corresponding LED on; a folded finger turns it off. Multiple LEDs can be on at once.

## Hardware

- Arduino Uno and USB cable
- Breadboard and jumper wires
- 5 LEDs
- 5 current-limiting resistors (e.g. 220 Ω, one per LED)
- Computer with a webcam

Wire each LED **in series with its own resistor**. Connect the LED circuits to D6–D2 as shown above and connect their return paths to Arduino GND.

## Software

- Python
- OpenCV (`opencv-python`)
- MediaPipe (the version used here needs the legacy `mp.solutions` API)
- PyFirmata2
- Arduino IDE (to upload the **StandardFirmata** sketch to the Arduino)

## Getting started

1. Connect the Arduino and build the LED circuit.
2. In the Arduino IDE, upload **File → Examples → Firmata → StandardFirmata** to the board.
3. Open this project folder in VS Code and select a Python interpreter compatible with your installed MediaPipe version.
4. Install the dependencies:

   ```bash
   python -m pip install -r requirements.txt
   ```

5. Run the webcam program:

   ```bash
   python "Hand Detection.py"
   ```

6. Raise or fold fingers to control the LEDs. Press **Q** to quit or **R** to record a short demo.

> The Arduino must be connected and running StandardFirmata before `LEDControl.py` is imported. MediaPipe's API has changed across releases, so tutorials using `mp.solutions` require a compatible installation.

## Project files

- `Hand Detection.py` — webcam capture, landmark detection, finger states and video overlays
- `LEDControl.py` — Arduino connection and five digital LED outputs
- `requirements.txt` — Python libraries

## What I Learned

This project was my first experience combining computer vision with Arduino hardware. Some key things I learned:

- Using OpenCV and MediaPipe to track hand movements and detect finger positions using landmarks.
- Understanding how MediaPipe uses 21 hand landmarks and how their coordinates can be used to detect raised or folded fingers.
- Organizing code into separate modules to make it easier to understand and troubleshoot.
- Debugging software and hardware issues while working on a real-time system.

## Challenges & Troubleshooting

A few issues I ran into while developing this project and how I worked through them:

- **Python Compatibility:** Faced compatibility issues with different Python and library versions. Explored Python 3.10 and switched interpreters in VS Code to get a compatible setup.
- **Thumb Detection:** The same vertical (y) coordinate logic used for other fingers didn't work well for the thumb. Used horizontal (x) coordinates instead to detect its position.
- **MediaPipe AttributeError:** Encountered the `module 'mediapipe' has no attribute 'solutions'` error. Tried different versions of MediaPipe and had to completely uninstall and reinstall the library to get it working.

## Known limitations & Next Steps

The current finger detection relies on simple coordinate comparisons, so it works when the fingers are pointing up and facing the camera. Different hand angles, or poor lighting can affect the hand landmark detection. Although MediaPipe can detect multiple hands, the current python code is set to detect one hand at a time.

Possible improvements I'd like to explore in the future:

- Improve finger detection to work more reliably across different hand orientations and lighting conditions.
- Expand the system to support independent gesture recognition and control using both hands.
- Integrate PyAutoGUI to go beyond controlling LEDs and use hand gestures for computer interactions, such as controlling the mouse, clicking, scrolling, and performing keyboard shortcuts.

## Portfolio

[View the project page](https://vijayprajwal.github.io/VijayPrajwalRajasekar-Portfolio/hand-gesture-led.html)
