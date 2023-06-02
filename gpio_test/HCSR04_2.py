import time
from RPi import GPIO

GPIO.setmode(GPIO.BCM)
Trig_Pin = 19
Echo_Pin = 26
GPIO.setup(Trig_Pin, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(Echo_Pin, GPIO.IN)
time.sleep(1)

def get_distance():
    GPIO.output(Trig_Pin, GPIO.HIGH)
    time.sleep(0.000100) # wait at least 10 microsecond
    GPIO.output(Trig_Pin, GPIO.LOW)
    
    # Echo收到信號前分別記錄時間
    timeout = time.time() + 0.5  # 設定timeout時間為0.5秒
    while not GPIO.input(Echo_Pin):
        if time.time() > timeout:
            return None  # 超時則return None
    t1 = time.time()
    
    timeout = time.time() + 0.5  # 設定timeout時間為0.5秒
    while GPIO.input(Echo_Pin):
        if time.time() > timeout:
            return None  # 超時則return None
    t2 = time.time()
    
    # return 套速度公式計算出的距離
    return (t2-t1)*340*100/2

if __name__ == "__main__":
    try:
        while True:
            distance = get_distance()
            if distance is not None:
                print('Distance: %0.2f cm' % distance)
            else:
                print('Measurement timeout')
            time.sleep(1)
    except KeyboardInterrupt:
        print('Bye')
    finally:
        GPIO.cleanup()
