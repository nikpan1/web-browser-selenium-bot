#Tut: https://realpython.com/how-to-make-a-discord-bot-python/

import os
import discord
from discord.ext import commands
import configparser


class DiscordBot(commands.Bot):
    def __init__(self):
        _intents = discord.Intents.default()
        _intents.message_content = True
        super().__init__(command_prefix='!', intents=_intents)


class DCBotAPI:
    def __init__(self) -> None:
        self.bot = DiscordBot()
 
        self.usr_cmd = " "

        # load token from config.ini
        config = configparser.ConfigParser()
        config.read("config/config.ini")
        self.TOKEN = config["DISCORD"]["TOKEN"]

        #client = discord.Client(intents=discord.Intents.default())
        #self.bot = commands.Bot(command_prefix='!',intents=_intents)
        self.bot.run(self.TOKEN)

       
        #event when the Client has established a connection to Discord
        @self.bot.event 
        async def on_ready(self):
            print('\nBot is ready!\n')
            print (os.getcwd())

        @self.bot.command(name='start', help="Bot is starting work!")
        async def dstart(self, ctx):
            self.usr_cmd = "start"
            await ctx.send("Bot started his work!")

        @self.bot.command(name='stop', help="Bot is waiting!")
        async def dstop(self, ctx):
            self.usr_cmd = "stop"
            await ctx.send("Bot stopped his work!")

        @self.bot.command(name='restart', help="Bot is restarting!")
        async def drestart(self, ctx):
            self.usr_cmd = "restarting!"
            await ctx.send("I")

        @self.bot.command(name='show', help="")
        async def dshow(self, ctx, arg):
            if arg == "img":
                await ctx.send(file = discord.File('DiscordBot/minecraft.png'))
            elif arg == "list":
                await ctx.send(f"Location = FIGHT_LOCATION\nPOKEMON = FIGHT_POKEMON")
            elif arg == "status":
                await ctx.send("Stats\n")
      
        @self.bot.command(name='set', help="")
        async def dset(self, ctx, fight, loc):
            usr_cmd = fight + " " + loc
            await ctx.send("")
    
        @self.bot.command(name='ss', help="")
        async def dscreenshot(self, ctx):
            usr_cmd = "ss"
            await ctx.send(file = discord.File('DiscordBot/minecraft.png'))

if __name__ == "__main__":
    bot = DCBotAPI()
