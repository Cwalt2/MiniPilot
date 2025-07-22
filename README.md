<!-- README Template for MiniPilot Project -->
# MiniPilot 🚗🤖

## **Autonomous robot powered by Raspberry Pi 4 and YOLOv5n**

### 🌟 Project Overview

**MiniPilot** is a DIY robot platform leveraging a custom-trained [YOLOv5n](https://github.com/ultralytics/yolov5) neural network for object detection and navigation. Built on a Raspberry Pi 4, MiniPilot aims to provide a simple yet powerful starting point for robotics and AI enthusiasts.

### 🛠️ Features

- Real-time object detection with YOLOv5n
- Custom-trained model for specific environments
- Raspberry Pi 4 hardware integration
- Modular Python codebase
- Easy to extend for your own robot builds

### 📦 Hardware Stack

- Raspberry Pi 4
- USB Camera (compatible with Pi)
- Motors and motor driver (e.g., L298N)
- Chassis & wheels
- Power supply (8x AA)
- Ultrasonic sensors, IR sensors

### 💻 Software Stack

- Python 3.10
- PyTorch
- YOLOv5n (custom-trained weights)
- OpenCV for image processing
- GPIO libraries for hardware control

### 🚀 Setup

Clone this repository:

``` bash

git clone https://github.com/Cwalt2/yolov5-x-MiniPilot.git
 ```

Install dependencies:

``` bash

pip install -r requirements.txt
```

Download your custom YOLOv5n weights and place them in the `weights/` directory or use the custom trained model `traffic.pt`.
Connect your Pi4 to the robot hardware.
Run the hardware movement script:

``` bash

python ir_move.py
```

Run the AI detect script:

On Windows:

``` bash

python .\detect.py --weights weights/traffic.pt --source 0 --img 640 --conf 0.4 --device cpu --save-txt --project runs/detect --name exp --exist-ok
```

On Linux:

``` bash

python detect-linux.py --weights weights/traffic.pt --source 0 --img 640 --conf 0.4 --device cpu --save-txt --project runs/detect --name exp --exist-ok
```

### :books: Documentation

The Raspberry Pi 4 runs the AI detect script with the custom trained model that detects traffic signs and people. At the same time starting the ir_move.py script that contains the IR sensor, ultrasonic sensor, motor control, and IDs for the script to stop the motors when a label is detected.

We chose the yolov5 framework because this repository has a pre-built detect.py script with the option to save logs.

``` bash

python .\detect.py --weights weights/traffic.pt --source 0 --img 640 --conf 0.4 --device cpu --save-txt --project runs/detect --name exp --exist-ok
```

Breaking down this line to start the AI you can see there is a `--save-txt` option along with `--project runs/detect --name exp --exist-ok` that follows it.

This forces the script to save label IDs, x, y, width, and height that looks like this:

``` bash
76 0.766406 0.533333 0.229687 0.291667
```

This is saved as a text file in the `runs/detect/exp/labels` folder

The saved file is then read by the separate script `ir_move.py`.

`ir_move.py` instantly reads the front of the text file and depending on the label ID it determines whether it should stop or go.

``` Python

# ir_move.py
def get_latest_label():
    files = [os.path.join(LABELS_FOLDER, f) for f in os.listdir(LABELS_FOLDER) if f.endswith('.txt')]
    if not files:
        return None
    latest_file = max(files, key=os.path.getctime)
    return latest_file
```

This code snippet instantiates the label IDs for stop and go/speed up

``` Python

# ir_move.py
LABELS_FOLDER = 'runs/detect/exp/labels'
# '25 MPH'=3 '45 MPH'=7 'red'=52 'stop'=8 'Person'=52
STOP_CLASS_IDS = [76, 8, 52]  # Stop sign, person, red light
SPEED_UP_CLASS_IDS = {3: 20, 7: 30}  # {class_id: duty_cycle}
```

Speeding up and stopping functions

``` Python

# ir_move.py
def check_for_stop():
    label_file = get_latest_label()
    if label_file:
        with open(label_file, 'r') as f:
            lines = f.readlines()
            for line in lines:
                class_id = int(line.split()[0])
                if class_id in STOP_CLASS_IDS:
                    return True
    return False

def check_for_speed_up():
    label_file = get_latest_label()
    if label_file:
        with open(label_file, 'r') as f:
            lines = f.readlines()
            for line in lines:
                class_id = int(line.split()[0])
                if class_id in SPEED_UP_CLASS_IDS:
                    return SPEED_UP_CLASS_IDS[class_id]
    return None
```

The next part is in the main function that stops or speeds the motors up depending on which label is in the text file it read most recently

``` Python

# ir_move.py
if check_for_stop():
    print("STOP detected from label file. Stopping motors.")
    stop_motors()
else:
    new_speed = check_for_speed_up()
    if new_speed is not None:
        print(f"Speed sign detected! Setting speed to {new_speed}% duty cycle.")
        pwm_left.ChangeDutyCycle(new_speed)
        pwm_right.ChangeDutyCycle(new_speed)
```

This ends the documentation part. The hardware modules were controlled with simple 1's and 0's if you wanted to see how that works also you can check in the `ir_move.py` script.

### 📄 MiniPilot Media

  This section is to show the MiniPilot in early stages and final form

#### MiniPilot Testing Video

[![MiniPilot Testing](/content/mini-test-video.png)](https://www.youtube.com/watch?v=i7lNd4yu97I&t=354s)

#### :movie_camera: MiniPilot Final Project Video

[![MiniPilot Final Project](/content/mini-final-thumbnail.png)](https://www.youtube.com/watch?v=wfdWKDR5kUk)

### Versions

#### 1.0 (first build/prototype)

![MiniPilot v1](content/mini-1.png)
Video shown in content folder

#### 2.0

![MiniPilot v2](content/mini-2.png)

#### 3.0 (final)

![MiniPilot v3 Top](content/mini-top.png)
![MiniPilot v3 Bottom](content/mini-bottom.png)
