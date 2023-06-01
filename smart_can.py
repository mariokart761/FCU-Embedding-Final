import discord
from discord.ext import commands
import json
import os
import asyncio


with open('setting.json', 'r', encoding='utf8') as jfile:
    bot_setting = json.load(jfile)

# Discord doc, link:https://discord.com/developers/docs/intro
# bot setting, link:https://discord.com/developers/applications
# 須將 Privileged Gateway Intents 下面的3個選項打勾
intent = discord.Intents.default()
intent.members = True
intent.message_content = True
bot = commands.Bot(command_prefix = '+++' , intents = intent)

# BOT上線提示
@bot.event
async def on_ready():
    print("[INFO] Bot is online!")

# load commands
@bot.command()
async def load(ctx, extension):
    await bot.load_extension(f'cogs.{extension}')
    await ctx.send(f'{extension} load!')

# unload commands
@bot.command()
async def unload(ctx, extension):
    await bot.unload_extension(f'cogs.{extension}')
    await ctx.send(f'{extension} unload!')

# reload commands
@bot.command()
async def reload(ctx, extension):
    await bot.reload_extension(f'cogs.{extension}')
    await ctx.send(f'{extension} reload!')

# async await 解決 bot.load_extension 的錯誤
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
    # BOT啟動
    # 需要Python 3.7+
    asyncio.run(main())
    try:
        while(1):
            ...    
        
    except KeyboardInterrupt:
        print("[INFO] Shutdown the bot...")
    finally:
        print("[INFO] Bot is offline.")