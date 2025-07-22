import time
import os
import RPi.GPIO as GPIO

# === Motor Pins ===
ENA = 27
IN1 = 17
IN2 = 18
ENB = 10
IN3 = 22
IN4 = 23

TRIG = 21
ECHO = 20

IR_LEFT = 5
IR_RIGHT = 6

LABELS_FOLDER = 'runs/detect/exp/labels'
# '25 MPH'=3 '45 MPH'=7 'red'=52 'stop'=8 'Person'=52
STOP_CLASS_IDS = [76, 8, 52]  # Stop sign, person, red light
SPEED_UP_CLASS_IDS = {3: 20, 7: 30}  # {class_id: duty_cycle}



# === Setup ===
GPIO.setmode(GPIO.BCM)
GPIO.setup([ENA, IN1, IN2, ENB, IN3, IN4, TRIG], GPIO.OUT)
GPIO.setup([ECHO, IR_LEFT, IR_RIGHT], GPIO.IN)

pwm_left = GPIO.PWM(ENA, 1000)
pwm_right = GPIO.PWM(ENB, 1000)
pwm_left.start(40)
pwm_right.start(40)

# === Motor Functions ===
def move_forward():
    GPIO.output(IN1, GPIO.LOW)
    GPIO.output(IN2, GPIO.HIGH)
    GPIO.output(IN3, GPIO.HIGH)
    GPIO.output(IN4, GPIO.LOW)

def turn_left():
    GPIO.output(IN1, GPIO.HIGH)
    GPIO.output(IN2, GPIO.LOW)
    GPIO.output(IN3, GPIO.HIGH)
    GPIO.output(IN4, GPIO.LOW)

def turn_right():
    GPIO.output(IN1, GPIO.LOW)
    GPIO.output(IN2, GPIO.HIGH)
    GPIO.output(IN3, GPIO.LOW)
    GPIO.output(IN4, GPIO.HIGH)

def stop_motors():
    GPIO.output([IN1, IN2, IN3, IN4], GPIO.LOW)

def measure_distance():
    GPIO.output(TRIG, False)
    time.sleep(0.01)
    GPIO.output(TRIG, True)
    time.sleep(0.00001)
    GPIO.output(TRIG, False)

    start_time = time.time()
    stop_time = time.time()

    while GPIO.input(ECHO) == 0:
        start_time = time.time()
    while GPIO.input(ECHO) == 1:
        stop_time = time.time()

    elapsed = stop_time - start_time
    distance = (elapsed * 34300) / 2
    return distance

# === Label Checking Functions ===
def get_latest_label():
    files = [os.path.join(LABELS_FOLDER, f) for f in os.listdir(LABELS_FOLDER) if f.endswith('.txt')]
    if not files:
        return None
    latest_file = max(files, key=os.path.getctime)
    return latest_file

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


# === Main Loop ===
try:
    while True:
        if check_for_stop():
            print("STOP detected from label file. Stopping motors.")
            stop_motors()
        else:
            new_speed = check_for_speed_up()
            if new_speed is not None:
                print(f"Speed sign detected! Setting speed to {new_speed}% duty cycle.")
                pwm_left.ChangeDutyCycle(new_speed)
                pwm_right.ChangeDutyCycle(new_speed)

            dist = measure_distance()
            left = GPIO.input(IR_LEFT)
            right = GPIO.input(IR_RIGHT)

            if dist < 15:
                print(f"Obstacle at {dist:.1f} cm! Stopping.")
                stop_motors()
            else:
                if left == 0 and right == 0:
                    move_forward()
                elif left == 1 and right == 0:
                    turn_right()
                elif left == 0 and right == 1:
                    turn_left()
                else:
                    stop_motors()

        time.sleep(0.05)


except KeyboardInterrupt:
    print("Program stopped manually.")

finally:
    pwm_left.stop()
    pwm_right.stop()
    GPIO.cleanup()