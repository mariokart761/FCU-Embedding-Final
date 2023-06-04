import time
from adafruit_servokit import ServoKit

servoKit = ServoKit(channels=16)

def lid_open():
    start_angle = 90
    end_angle = 0
    step = 5

    if end_angle > start_angle:
        for angle in range(start_angle, end_angle + 1, step):
            servoKit.servo[0].angle = angle
            servoKit.servo[4].angle = 180 - angle
            time.sleep(0.05)
    else:
        for angle in range(start_angle, end_angle - 1, -step):
            servoKit.servo[0].angle = angle
            servoKit.servo[4].angle = 180 - angle
            time.sleep(0.05)


def lid_close():
    start_angle = 0
    end_angle = 90
    step = 5

    if end_angle > start_angle:
        for angle in range(start_angle, end_angle + 1, step):
            servoKit.servo[0].angle = angle
            servoKit.servo[4].angle = 180 - angle
            time.sleep(0.05)
    else:
        for angle in range(start_angle, end_angle - 1, -step):
            servoKit.servo[0].angle = angle
            servoKit.servo[4].angle = 180 - angle
            time.sleep(0.05)
lid_open()
lid_close()