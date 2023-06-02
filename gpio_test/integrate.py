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
# GPIO mode 為TEGRA_SOC (mode 1000)
Trig_Pin = "DAP4_DIN" # BOARD38 / BCM20 
Echo_Pin = "DAP4_DOUT" # BOARD40 / BCM21 
GPIO.setup(Trig_Pin, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(Echo_Pin, GPIO.IN)
servoKit = ServoKit(channels=16)

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
            if (distance is not None and distance >= 10):
                print('Distance: %0.2f cm' % distance)
            elif (distance is not None and distance < 10):
                # 控制Servo
                print('Distance: %0.2f cm' % distance)
                servoKit.servo[0].angle = 180
                servoKit.servo[4].angle = 180
                time.sleep(1)
                servoKit.servo[0].angle = 90
                servoKit.servo[4].angle = 90
            else:
                print('Measurement timeout')
            time.sleep(1)
    except KeyboardInterrupt:
        print('Bye')
    finally:
        GPIO.cleanup()
