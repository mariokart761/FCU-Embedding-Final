import discord
from discord.ext import commands
from core.classes import Cog_Extension
import json


with open('setting.json', 'r', encoding='utf8') as jfile:
    bot_setting = json.load(jfile)

class Event(Cog_Extension):
    # 成員加入提示
    @commands.Cog.listener()
    async def on_member_join(self, member):
        #print(f'{member} join!')
        channel = self.bot.get_channel(int(bot_setting["bot_channel"]))
        await channel.send(f'{member} join!')

    # 成員離開提示
    @commands.Cog.listener()
    async def on_member_remove(self, member):
        #print(f'{member} leave!')
        channel = self.bot.get_channel(int(bot_setting["bot_channel"]))
        await channel.send(f'{member} leave!')
        
    @commands.Cog.listener()
    async def on_message(self, msg):
        keyword = ['星爆', '星爆氣流斬', 'star burst stream']
        if msg.content in keyword and msg.author != self.bot.user:
            await msg.channel.send('抓到了! 偷星爆!') # 找到msg所在的channel發送訊息

async def setup(bot):
    await bot.add_cog(Event(bot))
