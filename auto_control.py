#!/usr/bin/env python3
import time
from RPi import GPIO
from adafruit_servokit import ServoKit

"""
bcm #: 4 tegra: AUD_MCLK
bcm #: 17 tegra: UART2_RTS
bcm #: 18 tegra: DAP4_SCLK
bcm #: 27 tegra: SPI2_SCK
bcm #: 22 tegra: LCD_TE
bcm #: 23 tegra: SPI2_CS1
bcm #: 24 tegra: SPI2_CS0
bcm #: 10 tegra: SPI1_MOSI
bcm #: 9 tegra: SPI1_MISO
bcm #: 25 tegra: SPI2_MISO
bcm #: 11 tegra: SPI1_SCK
bcm #: 8 tegra: SPI1_CS0
bcm #: 7 tegra: SPI1_CS1
bcm #: 5 tegra: CAM_AF_EN
bcm #: 6 tegra: GPIO_PZ0
bcm #: 12 tegra: LCD_BL_PW
bcm #: 13 tegra: GPIO_PE6
bcm #: 19 tegra: DAP4_FS
bcm #: 16 tegra: UART2_CTS
bcm #: 26 tegra: SPI2_MOSI
bcm #: 20 tegra: DAP4_DIN
bcm #: 21 tegra: DAP4_DOUT
"""
class SmartCan:
    def __init__(self):
        # GPIO mode 為TEGRA_SOC (mode 1000)
        self.Trig_Pin = "DAP4_DIN" # BOARD38 / BCM20 
        self.Echo_Pin = "DAP4_DOUT" # BOARD40 / BCM21 
        self.SERVO_THRESHOLD = 26 # 距離多近才啟動SERVO，偵測單位為cm
        self.DISTANCE_CHECK_INTERVAL = 1 # 距離偵測間隔，單位為秒
        self.servoKit = ServoKit(channels=16)
        self.setup()
        
    def setup(self):
        GPIO.setup(self.Trig_Pin, GPIO.OUT, initial=GPIO.LOW)
        GPIO.setup(self.Echo_Pin, GPIO.IN)
    
    def get_distance(self):
        GPIO.output(self.Trig_Pin, GPIO.HIGH)
        time.sleep(0.000100) # wait at least 10 microsecond
        GPIO.output(self.Trig_Pin, GPIO.LOW)
        
        # Echo收到信號前分別記錄時間
        timeout = time.time() + 0.5  # 設定timeout時間為0.5秒
        while not GPIO.input(self.Echo_Pin):
            if time.time() > timeout:
                return None  # 超時則return None
        t1 = time.time()
        
        timeout = time.time() + 0.5  # 設定timeout時間為0.5秒
        while GPIO.input(self.Echo_Pin):
            if time.time() > timeout:
                return None  # 超時則return None
        t2 = time.time()
        
        # return 套速度公式計算出的距離
        return (t2-t1)*340*100/2

    def lid_opening_control(self):
        # 打開蓋子
        self.servoKit.servo[0].angle = 0
        self.servoKit.servo[4].angle = 180
        opening_time_count = 0 # 設定計時器
        OPENING_CHECK_TIME = 5 # 設定距離<SERVO_THRESHOLD時，超過N秒才關閉蓋子
        
        while True:
            # 連續 OPENING_CHECK_TIME秒的距離都>=SERVO_THRESHOLD才脫離迴圈，若中途偵測到距離<則重置計時
            distance = self.get_distance()
            if (distance is not None):
                print('[INFO] Opening: Distance: %0.2f cm' % distance)
                if (distance >= self.SERVO_THRESHOLD and opening_time_count >= OPENING_CHECK_TIME):
                    print('[INFO] 即將關閉')
                    time.sleep(1) # 再多等待1秒才將蓋子關閉
                    break
                elif (distance < self.SERVO_THRESHOLD): opening_time_count = 0
                opening_time_count += 1
            time.sleep(1) # 每秒check一次
        
        # 關閉蓋子
        self.servoKit.servo[0].angle = 90
        self.servoKit.servo[4].angle = 90
        
        return

if __name__ == "__main__":
    smartCan = SmartCan()
    try:
        print('[INFO] 感應式開蓋啟動')
        while True:
            distance = smartCan.get_distance()
            
            if (distance is not None and distance >= smartCan.SERVO_THRESHOLD):
                print('[INFO] Distance: %0.2f cm' % distance)
            elif (distance is not None and distance < smartCan.SERVO_THRESHOLD):
                # 偵測到距離<SERVO_THRESHOLD，則控制Servo
                print('[INFO] Distance: %0.2f cm' % distance)
                # 開蓋控制
                smartCan.lid_opening_control()
            else:
                # distance is None (表示timeout)
                print('[INFO] Detection timeout')
                
            time.sleep(1) # 每秒偵測一次距離
    except KeyboardInterrupt:
        print('[INFO] KeyboardInterrupt')
    finally:
        smartCan.servoKit.servo[0].angle = 90
        smartCan.servoKit.servo[4].angle = 90
        GPIO.cleanup()