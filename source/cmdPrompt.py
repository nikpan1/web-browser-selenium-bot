import asyncio

import discord
from discord.ext import commands
import configparser
from main import Schedule


def screenshot(driver):
    import os
    from datetime import datetime
    current_time = datetime.now()
    time_string = current_time.strftime("%H-%M-%S")
    filename = f"screenshots/screenshot{time_string}.png"

    directory = "screenshot"
    if not os.path.exists(directory):
        os.makedirs(directory)
    
    screenshot_path = os.path.join(directory, filename)

    driver.save_screenshot(screenshot_path)
    return screenshot_path
 
class cmdPrompt:
    def __init__(self, mode):  # terminal | discord
        self.schedule = Schedule(True, True, True)
        self.running = False
 
        self.setup_discord_bot()
        self.discord_input()
        self.bot.run(self.TOKEN)
    
    def setup_discord_bot(self):
        self.bot = commands.Bot(command_prefix='!', intents=discord.Intents.all())

        # load token from config.ini
        config = configparser.ConfigParser()
        config.read("config/config.ini")
        self.TOKEN = config["DISCORD"]["TOKEN"]

    def discord_input(self):
        # event when the Client has established a connection to Discord
        @self.bot.event 
        async def on_ready():
            print('\nBot is ready!\n')

        @self.bot.command()
        async def start(ctx):
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
            await ctx.send(f"Pokemon = {self.schedule.team[self.schedule.FIGHT_POKEMON]}\n 
                             Location = {self.schedule.loc[self.schedule.FIGHT_LOCATION}")

        @self.bot.command()
        async def screenshot(ctx):
            filepath = screenshot(self.schedule.driver)
            await ctx.send(file = discord.File(filepath))

        @self.bot.command()
        async def show(ctx, arg):
            if arg == "img":
                filepath = screenshot(self.schedule.driver)
                await.ctx.send(file = discord.File(filepath))
            elif arg == "list":
                await ctx.send(self.print_info())
            elif arg == "status":
                await ctx.send(self.print_status())
 

    async def main(self):
        print_task = asyncio.create_task(self.bot_loop())
        await asyncio.gather(print_task)
    
    async def bot_loop(self):
        while True:
            self.user_input()
            if self.running:
                self.schedule.travel()
            await asyncio.sleep(0.1)
   
    def print_status(self):
        result = ""
        if self.running:
            result += print(f'XXXXXX RUNNING XXXXXX')
        else:
            result += print(f'XXXXXX WAITING XXXXXX')
            result += (f'  elm = {self.schedule.elm_status}%')
            result += (f'  rezerwa = {self.schedule.rezerwa_count}%')
            result += (f'  {self.schedule.FIGHT_POKEMON} | 
                       {self.schedule.FIGHT_LOCATION}')
    
    def print_info(self):
        BOLD_ON = '\033[1m'
        BOLD_OFF = '\033[0m'
        
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
    asyncio.run(cp.main())
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
