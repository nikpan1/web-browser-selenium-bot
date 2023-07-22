#Tut: https://realpython.com/how-to-make-a-discord-bot-python/

import os
import discord
from discord.ext import commands
import configparser


class DiscordBot:
    def __init__(self):
        self.usr_cmd = " "
        # load token from config.ini
        config = configparser.ConfigParser()
        config.read("config/config.ini")
        self.TOKEN = config["DISCORD"]["TOKEN"]

        #client = discord.Client(intents=discord.Intents.default())
        _intents = discord.Intents.default()
        _intents.message_content = True
        self.bot = commands.Bot(command_prefix='!',intents=_intents)
        self.bot.run(self.TOKEN)

    #event when the Client has established a connection to Discord
    @self.bot.event 
    async def on_ready(self):
        print(f'{bot.user} is ready!')
        print (os.getcwd())

    @bot.command(name='start', help="Bot is starting work!")
    async def dstart(self, ctx):
        usr_cmd = "start"
        await ctx.send("o")

    @bot.command(name='stop', help="Bot is waiting!")
    async def dstop(self, ctx):
        usr_cmd = "stop"
        await ctx.send("o")

    @bot.command(name='restart', help="Bot is restarting!")
    async def drestart(self, ctx):
        usr_cmd = "restart"
        await ctx.send("I")

    @bot.command(name='show', help="")
    async def dshow(self, ctx, arg):
        if arg == "img":
            await ctx.send(file = discord.File('DiscordBot/minecraft.png'))
        elif arg == "list":
            await ctx.send(f"Location = {FIGHT_LOCATION}\nPOKEMON = {FIGHT_POKEMON}")
        elif arg == "status":
            await ctx.send("Stats\n")
      
    @bot.command(name='set', help="")
    async def dset(self, ctx, fight, loc):
        usr_cmd = fight + " " + loc
        await ctx.send("")
    
    @bot.command(name='ss', help="")
    async def dscreenshot(self, ctx):
        usr_cmd = "ss"
        await ctx.send(file = discord.File('DiscordBot/minecraft.png'))


