import discord
from discord.ext import commands
import random
import json
import os
import asyncio


with open('setting.json', 'r', encoding='utf8') as jfile:
    bot_setting = json.load(jfile)

#bot setting，link:https://discord.com/developers/applications
intent = discord.Intents.default()
intent.members = True
intent.message_content = True
bot = commands.Bot(command_prefix = '+++' , intents = intent)

# BOT上線提示
@bot.event
async def on_ready():
    print("[INFO] Bot is online!")

# 成員加入提示
@bot.event
async def on_member_join(member):
    #print(f'{member} join!')
    channel = bot.get_chanel(int(bot_setting["bot_channel"]))
    await channel.send(f'{member} join!')

# 成員離開提示
@bot.event
async def on_member_remove(member):
    #print(f'{member} leave!')
    channel = bot.get_chanel(int(bot_setting["bot_channel"]))
    await channel.send(f'{member} leave!')

# load commands
@bot.command()
async def load(ctx, extension):
    bot.load_extension(f'cmd.{extension}')
    await ctx.send(f'{extension} 載入成功!')

# unload commands
@bot.command()
async def unload(ctx, extension):
    bot.unload_extension(f'cmd.{extension}')
    await ctx.send(f'{extension} 載入成功!')

# reload commands
@bot.command()
async def reload(ctx, extension):
    bot.reload_extension(f'cmd.{extension}')
    await ctx.send(f'{extension} 載入成功!')

# 用 async await 解決 bot.load_extension 出現的錯誤
# link:https://stackoverflow.com/questions/71504627/runtimewarning-coroutine-botbase-load-extension-was-never-awaited-after-upd
async def load_extensions():
    for filename in os.listdir("./cogs"):
        if filename.endswith(".py"):
            # cut off the .py from the file name
            await bot.load_extension(f"cogs.{filename[:-3]}")

async def main():
    async with bot:
        await load_extensions()
        await bot.start(bot_setting["BOT_TOKEN"])

if __name__ == "__main__":
    #BOT啟動
    asyncio.run(main())