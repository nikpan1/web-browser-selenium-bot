import asyncio
import os
import configparser
from datetime import datetime

import selenium
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver

import discord
from discord.ext import commands

from main import Schedule


def make_screenshot(driver: WebDriver, directory: str = "screenshots") -> str:
    try:
        if not os.path.exists(directory):
            os.makedirs(directory)

        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        filename = f"screenshot_{timestamp}.png"
        screenshot_path = os.path.join(directory, filename)

        driver.save_screenshot(screenshot_path)
        return screenshot_path
    except Exception as e:
        # Handle any exceptions that might occur during the screenshot process
        print(f"Error capturing screenshot: {e}")
        return ""


class cmdPrompt:
    def __init__(self, mode):  # terminal | discord
        self.get_config()
        self.schedule = Schedule(self.login, self.password, True, True, True)
        self.running = False
        
        self.guild_id = 0 
        self.channel_id = 0 
        self.setup_discord_bot()
        self.discord_input()
       
        self.schedule.init_elm()
        self.start()

    def get_config(self):
        # load token from config.ini
        config = configparser.ConfigParser()
        config.read("config/config.ini")

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
            print('\nBot is ready!\n')

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
                await ctx.send("text was found!")
            except:
                await ctx.send("text was *not* found!")

    async def send_message(self, message):
        try:
            server = self.bot.get_guild(int(self.guild_id))
            channel = server.get_channel(int(self.channel_id))

            await channel.send(message)
        except Exception as e:
            print(f"Error sending the message: {e}")

    async def send_image(self, filename):
        try:
            server = self.bot.get_guild(int(self.guild_id))
            channel = server.get_channel(int(self.channel_id))

            await channel.send(file = discord.File(filename))
        except Exception as e:
            print(f"Error sending the message: {e}")

    def start(self):
        loop = asyncio.get_event_loop()
        loop.create_task(self.bot_loop())
        loop.run_until_complete(self.start_bot())
 
    async def start_bot(self):
        await self.bot.start(self.TOKEN)
       
    async def bot_loop(self):
        print("starting main loop")
        while True:
            if self.schedule.wait_request:
                self.schedule.wait_request = False
                self.running = False
                if self.schedule.wait_img_buffor != " ":
                    await self.send_image(self.schedule.wait_img_buffor)
                    self.schedule.wait_img_buffor = " "
                # send message to dc 
            if self.running:
                self.schedule.travel()
            await asyncio.sleep(0.1)







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
# niech automatycznie wybiera zadanie bierze nowe zadanie  


# @TODO remake logging system
# @TODO zrobić counter znalezionych itemów/złapanych pokemonów
# @TODO elm quests handling
# @TODO default settings
# @TODO filtrowanie rezerwy
# @TODO przed sprzedażą niech wszystkich ewo

# if text contains "Brawo!" _. you found an item 
# if "nauczyciela" -> TMA
# if "Lidera" -> Lider sali
# EXCEPTION BREAK nie działa
# zoom out - press ctrl - 2 times on start 
# if img in daily contains src "img/items/" ->exception break
# instead of creating a new driver instance, attach it to a active one 
# if found egg -> input name="poluj"  
