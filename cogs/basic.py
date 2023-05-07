import discord
from discord.ext import commands
from core.classes import Cog_Extension

class Basic(Cog_Extension):
    #ping(ms)
    @commands.command()
    async def ping(self, ctx):
        await ctx.send(f'{round(self.bot.latency*1000)} ms')

async def setup(bot):
    await bot.add_cog(Basic(bot))