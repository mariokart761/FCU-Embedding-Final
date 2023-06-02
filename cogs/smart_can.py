import discord
from discord.ext import commands
from core.classes import Cog_Extension
from adafruit_servokit import ServoKit


class SmartCan(Cog_Extension):
    def __init__(self, bot):
        self.servoKit = ServoKit(channels=16)
            
    # DC打開蓋子
    @commands.command(aliases = ["open", "lid open", "打開蓋子"])
    async def lid_opening(self, ctx):
        # 打開蓋子
        self.servoKit.servo[0].angle = 0
        self.servoKit.servo[4].angle = 180
        await ctx.send('蓋子已開啟')
    
    # DC關閉蓋子
    @commands.command(aliases = ["close", "lid close", "關閉蓋子"])
    async def lid_closing(self, ctx):
        # 關閉蓋子
        self.servoKit.servo[0].angle = 90
        self.servoKit.servo[4].angle = 90
        await ctx.send('蓋子已關閉')
    
async def setup(bot):
    await bot.add_cog(SmartCan(bot))
