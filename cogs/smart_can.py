import discord
from discord.ext import tasks, commands
from core.classes import Cog_Extension
from adafruit_servokit import ServoKit
import json
import asyncio
import time

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

# 讀取頻道
with open('setting.json', 'r', encoding='utf8') as jfile:
    bot_setting = json.load(jfile)

# 讀取sensor data
def read_data_from_file():
    with open('sensor_data.json', 'r') as f:
        data = json.load(f)
    return data    

class SmartCan(Cog_Extension):
    def __init__(self, bot):
        self.bot = bot
        self.servoKit = ServoKit(channels=16)
        self.NOTIFY_THRESHOLD = 26 # 距離多近才啟動SERVO，偵測單位為cm
        self.DISTANCE_CHECK_INTERVAL = 10 # 距離偵測間隔，單位為秒
        self.servoKit = ServoKit(channels=16)
        self.check_can_isfull.start()
        
    @tasks.loop(seconds=5.0)
    async def check_can_isfull(self):
        print("[INFO] IsFull loop on Duty!")
        data = read_data_from_file()    
        if bool(data["isFull"]) == True:
            print("[INFO] 垃圾桶已滿")
            channel = self.bot.get_channel(int(bot_setting["bot_channel"]))
            print(f"[INFO] Channel:{channel}")
            await channel.send(":exclamation: 垃圾桶滿囉~ 請進行清理 :exclamation:")
            print("[INFO] 發送訊息完成")
            
    @check_can_isfull.before_loop
    async def before_printer(self):
        await self.bot.wait_until_ready()
        print("[INFO] IsFull loop is ready!")
        
    # 開蓋速度控制
    def lid_open(self):
        start_angle = 90
        end_angle = 0
        step = 5

        if end_angle > start_angle:
            for angle in range(start_angle, end_angle + 1, step):
                self.servoKit.servo[0].angle = angle
                self.servoKit.servo[4].angle = 180 - angle
                time.sleep(0.05)
        else:
            for angle in range(start_angle, end_angle - 1, -step):
                self.servoKit.servo[0].angle = angle
                self.servoKit.servo[4].angle = 180 - angle
                time.sleep(0.05)
                
    # 關蓋速度控制
    def lid_close(self):
        start_angle = 0
        end_angle = 90
        step = 5

        if end_angle > start_angle:
            for angle in range(start_angle, end_angle + 1, step):
                self.servoKit.servo[0].angle = angle
                self.servoKit.servo[4].angle = 180 - angle
                time.sleep(0.05)
        else:
            for angle in range(start_angle, end_angle - 1, -step):
                self.servoKit.servo[0].angle = angle
                self.servoKit.servo[4].angle = 180 - angle
                time.sleep(0.05)
    
    
    # DC打開蓋子
    @commands.command(aliases = ["open", "lid open", "打開蓋子"])
    async def lid_opening(self, ctx):
        # 打開蓋子
        self.lid_open()
        # self.servoKit.servo[0].angle = 0
        # self.servoKit.servo[4].angle = 180
        await ctx.send('蓋子已開啟')
    
    # DC關閉蓋子
    @commands.command(aliases = ["close", "lid close", "關閉蓋子"])
    async def lid_closing(self, ctx):
        # 關閉蓋子
        self.lid_close()
        # self.servoKit.servo[0].angle = 90
        # self.servoKit.servo[4].angle = 90
        await ctx.send('蓋子已關閉')
    

    
async def setup(bot):
    await bot.add_cog(SmartCan(bot))
