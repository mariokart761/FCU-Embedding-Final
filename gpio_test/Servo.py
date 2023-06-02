import time
from adafruit_servokit import ServoKit

# Set channels to the number of servo channels on your kit.
# 8 for FeatherWing, 16 for Shield/HAT/Bonnet.
servoKit = ServoKit(channels=16)

servoKit.servo[0].angle = 180
servoKit.servo[4].angle = 180
# kit.continuous_servo[1].throttle = 1
time.sleep(1)
# kit.continuous_servo[1].throttle = -1
# time.sleep(1)
servoKit.servo[0].angle = 90
servoKit.servo[4].angle = 90
servoKit.continuous_servo[1].throttle = 0