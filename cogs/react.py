import discord
from discord.ext import commands
from core.classes import Cog_Extension
import random
import json

with open('setting.json', 'r', encoding='utf8') as jfile:
    bot_setting = json.load(jfile)

class React(Cog_Extension):
        
    #星爆氣流斬
    @commands.command()
    async def starburst(self, ctx):
        starburst_img = random.choice(bot_setting["starburst_img"])
        send_img = discord.File(starburst_img)
        await ctx.send('星爆氣流斬')
        await ctx.send(file = send_img)
        
async def setup(bot):
    await bot.add_cog(React(bot))