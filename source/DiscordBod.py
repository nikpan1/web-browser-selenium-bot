#Tutek: https://realpython.com/how-to-make-a-discord-bot-python/
#https://pythoninoffice.com/building-a-simple-python-discord-bot-with-discordpy-in-2022-2023/
import os

import discord
from discord.ext import commands
from dotenv import load_dotenv

# load token from config.ini
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

#client = discord.Client(intents=discord.Intents.default())
_intents = discord.Intents.default()
_intents.message_content = True
bot = commands.Bot(command_prefix='!',intents=_intents)

#event when the Client has established a connection to Discord
@bot.event 
async def on_ready():
    print(f'{bot.user} is ready!')
    print (os.getcwd())

#@bot.event
#async def on_message(message):
#    print(message.author, message.content, message.channel.id)

#@bot.command()
#async def hello(ctx):
#    channel = bot.get_channel(1076799647030452364)
#    await channel.send(f'hello there {ctx.author.mention}')

@bot.command(name='kop', help="Idzie kopac kobla")
async def command_kop(ctx, argSpot):
    await ctx.send(f"Idę kopać kobla na {argSpot}")
    #print(ctx.message.guild.name)

@bot.command(name='memik', help="Test wysyłania obrazów")
async def command_memik(ctx):
    await ctx.send(file = discord.File('DiscordBot/minecraft.png'))


bot.run(TOKEN)
