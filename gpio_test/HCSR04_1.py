import time
from RPi import GPIO

GPIO.setmode(GPIO.BCM)
Trig_Pin = 20
Echo_Pin = 21
GPIO.setup(Trig_Pin, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(Echo_Pin, GPIO.IN)
time.sleep(1)

def get_distance():
    GPIO.output(Trig_Pin, GPIO.HIGH)
    # 将Trig脚位拉高电位输出超声波信号，等待100微秒之后关闭输出
    time.sleep(0.000100) # wait at least 10 microsecond
    GPIO.output(Trig_Pin, GPIO.LOW)
    
    # 在Echo收到信号前后分别记录时间
    timeout = time.time() + 0.5  # 设置超时时间为0.5秒钟
    while not GPIO.input(Echo_Pin):
        if time.time() > timeout:
            return None  # 如果超时则返回None
    t1 = time.time()
    
    timeout = time.time() + 0.5  # 设置超时时间为0.5秒钟
    while GPIO.input(Echo_Pin):
        if time.time() > timeout:
            return None  # 如果超时则返回None
    t2 = time.time()
    
    # 最后套用速度公式算出距离返回
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
