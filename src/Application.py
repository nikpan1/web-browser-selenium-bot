import asyncio
import configparser

import selenium
from selenium.webdriver.common.by import By

import discord
from discord.ext import commands

from Core import Schedule
from CoreSettings import *
from Screenshooter import make_screenshot


class cmdPrompt:
    def __init__(self, mode):  # @TODO modes: terminal | discord
        self.get_config()
        self.schedule = Schedule(self.login, self.password, True, True, True)
        self.running = False
        
        # for send message/image without context
        self.guild_id = 0 
        self.channel_id = 0 

        self.setup_discord_bot()
        self.discord_input()
       
        self.schedule.init_elm()
        self.start()

    def get_config(self):
        # load token from config.ini
        config = configparser.ConfigParser()
        config.read(CONFIG_FILE)

        self.TOKEN = config["DISCORD"]["TOKEN"]
        self.login = config["LOGGING_IN"]["LOGIN"]
        self.password = config["LOGGING_IN"]["PASSWORD"]

    def setup_discord_bot(self):
        self.bot = commands.Bot(command_prefix='!', intents=discord.Intents.all())
        # --! !--

    def discord_input(self):
        # event when the Client has established a connection to Discord
        @self.bot.event 
        async def on_ready():
            print("Bot is ready!\n")

        @self.bot.command()
        async def start(ctx):
            self.guild_id = ctx.guild.id
            self.channel_id = ctx.channel.id 
            self.running = True
            await ctx.send("Bot is working!")

        @self.bot.command()
        async def stop(ctx):
            self.running = False
            await ctx.send("Bot is waiting!")

        @self.bot.command()
        async def reset(ctx):
            self.running = False
            self.schedule.loc = self.schedule.elm.find_locations()
            self.schedule.team = self.schedule.get_team_data()

            self.running = True
            await ctx.send("Reseting Location and Pokemon lists:" + self.print_info())
     
        @self.bot.command()
        async def set(ctx, fight, loc):
            self.schedule.FIGHT_POKEMON = int(fight)
            self.schedule.DEFAULT_FIGHT_LOCATION = int(loc)
            self.schedule.FIGHT_LOCATION = int(loc)
            await ctx.send(f"Pokemon = {self.schedule.team[self.schedule.FIGHT_POKEMON]}\n" + 
                           f"Location = {self.schedule.loc[self.schedule.FIGHT_LOCATION]}")

        @self.bot.command()
        async def screenshot(ctx):
            filepath = make_screenshot(self.schedule.driver)
            await ctx.send(file = discord.File(filepath))

        @self.bot.command()
        async def show(ctx, arg):
            if arg == "img":
                filepath = make_screenshot(self.schedule.driver)
                await ctx.send(file = discord.File(filepath))
            elif arg == "list":
                await ctx.send(self.print_info())
            elif arg == "status":
                await ctx.send(self.print_status())
        
        @self.bot.command()
        async def debug(ctx, text):
            try:
                cth = self.schedule.driver.find_element(By.XPATH, text) 
                await ctx.send("text was found!: ", cth.text)
            except:
                await ctx.send("text was *not* found!")
        
        @self.bot.command()
        async def login(ctx):
            self.schedule.login_user()
            await ctx.send("Logged in!")

    
    async def send_message(self, message):
        try:
            server = self.bot.get_guild(int(self.guild_id))
            channel = server.get_channel(int(self.channel_id))

            await channel.send(message)
        except Exception as e:
            print(f"Error sending the message: {e}")

    async def send_image(self, filename, message=""):
        try:
            server = self.bot.get_guild(int(self.guild_id))
            channel = server.get_channel(int(self.channel_id))

            await channel.send(file = discord.File(filename))
        except Exception as e:
            print(f"Error sending the message: {e}")

    def start(self):
        loop = asyncio.get_event_loop()
        loop.create_task(self.bot_loop())
        loop.run_until_complete(self.start_discord_bot())
 
    async def start_discord_bot(self):
        await self.bot.start(self.TOKEN)
       
    async def bot_loop(self):
        print("Main loop just started.")
        while True:
            if self.schedule.wait_request:
                self.schedule.wait_request = False
                self.running = False
                if self.schedule.wait_img_buffor != " ":
                    await self.send_image(self.schedule.wait_img_buffor)
                    self.schedule.wait_img_buffor = " "
                else:
                    await self.send_message(self.schedule.wait_message)
                    self.schedule.wait_message = " "
            if self.running:
                self.schedule.travel()
            await asyncio.sleep(0.1)

#____________________


    def print_status(self):
        result = ""
        if self.running:
            result += print(f'XXXXXX RUNNING XXXXXX')
        if not self.running:
            result += print(f'XXXXXX WAITING XXXXXX')
        
        result += print(f'XXXXXX WAITING XXXXXX')
        result += (f'elm = {self.schedule.elm_status}%')
        result += (f'rezerwa = {self.schedule.rezerwa_count}%')
        result += (f'fight_pokemon = {self.schedule.FIGHT_POKEMON} \n' +  
                   f'fight_location = {self.schedule.FIGHT_LOCATION}')
    
    def print_info(self):
      # BOLD_ON, BOLD_OFF = '\033[1m', '\033[0m'
        BOLD_ON, BOLD_OFF = '*', "*" 
        
        result = "\n"
        for lo, index in enumerate(self.schedule.loc):
            if self.schedule.FIGHT_LOCATION:
                result += BOLD_ON + index + ". " + lo + BOLD_OFF
            else:        
                result += index + ". " + lo
        
        for t, index in enumerate(self.schedule.team):
            if self.schedule.FIGHT_POKEMON:
                result += BOLD_ON + index + ". " + t + BOLD_OFF
            else:
                result += index + ". " + t
        
        return result
    

if __name__ == "__main__":
    cp = cmdPrompt("terminal")
    exit(0)


# niech wybiera tm, nie czeka
# niech automatycznie bierze nowe zadanie  

# @TODO zrobić counter znalezionych itemów/złapanych pokemonów
# @TODO elm quests handling
# @TODO default settings
# @TODO filtrowanie rezerwy
# @TODO przed sprzedażą niech wszystkich ewo

# zoom out - press ctrl - 2 times on start 
# instead of creating a new driver instance, attach it to a active one 