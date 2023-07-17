# MAIN

import time
import datetime
import asyncio
import os

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

from selenium.webdriver.firefox.service import Service as FirefoxService
from webdriver_manager.firefox import GeckoDriverManager 
from StatementsClass import Statements
from PokeballsClass import Throw
from QuestClass import Elm  #

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


class Schedule:
    def __init__(self):
        # settings
        self.load_images = True 
        self.skip_eggs = True
        self.skip_tutor = True

        POKEWARS = "https://pokewars.pl"        
        options = webdriver.FirefoxOptions()
        options.add_argument('--disable-blink-features=AutomationControlled')
        if not self.load_images:
            options.set_preference("permissions.default.image", 2)
        self.driver = webdriver.Firefox(options=options, service=FirefoxService(GeckoDriverManager().install()))
        self.driver.get(POKEWARS)

        self.pb = Throw(self.driver)
        self.st = Statements(self.driver)
        self.elm = Elm(self.driver)


        self.FIGHT_POKEMON = 3
        self.FIGHT_LOCATION = 2 
        self.DEFAULT_FIGHT_LOCATION = 2

        self.usr_cmd = " "
        self.rezerwa_count = 0
        self.running = False
        
        self.login()

        self.loc = self.elm.find_locations()
        
        self.elm.show_elm()
        self.elm_status = self.elm.get_progress()
        self.elm_location = self.elm.get_daily_quest_info(self.loc)
        
        if self.elm_location in self.loc:
            self.FIGHT_LOCATION = self.loc.index(self.elm_location)
            print("elm_location = ", self.elm_location)


        while True:
            self.hunt()
            if self.st.is_pokemon():
                self.team = self.elm.find_team()
                break
 
        print(self.loc, "\n", self.team)


    async def read_user_input(self):
        while True:
            self.usr_cmd = await self.terminal_stats()

    async def terminal_stats(self):
        loop = asyncio.get_running_loop()
        return await loop.run_in_executor(None, input)

    async def main(self):
        await asyncio.gather(self.terminal_stats(), self.bot_loop())

    async def bot_loop(self):
        while True:
            self.user_input()
            if self.running:
                self.travel()
            await asyncio.sleep(0.1)

    def user_input(self):
        if len(self.usr_cmd) < 2:
            return
        if self.usr_cmd == "stop":
            print("STOP")
            self.running = False
        if self.usr_cmd == "start":
            print("START")
            self.running = True 
        if self.usr_cmd == "restart":
            print("RESTART")
            self.loc = self.elm.find_locations()
        if self.usr_cmd == "?":
            print("HELP")
            self.print_status()
        if self.usr_cmd == "ss":
            self.screenshot
            

        arguments = self.usr_cmd.split()
        if len(arguments) == 2:
            self.FIGHT_POKEMON = int(arguments[0])
            self.FIGHT_LOCATION = int(arguments[1])
            self.DEFAULT_FIGHT_LOCATION = int(arguments[0])

            print("POKEMON = ", self.team[self.FIGHT_POKEMON])
            print("LOCATION =  ", self.loc[self.FIGHT_LOCATION])
        
        self.usr_cmd = " "

    async def exception_break(self):
        print("exception_break") 
        self.running = False
        while True:
            self.user_input()
            if self.running == True:
                break
                
    def print_status(self):
        #os.system('cls' if os.name == 'nt' else 'clear')
        if self.running == True:
            print(f'XXXXXX RUNNING XXXXXX')
        else:
            print(f'XXXXXX WAITING XXXXXX')
        print(f'  elm = {self.elm_status}%')
        print(f'  rezerwa = {self.rezerwa_count}%')
        print(f'  {self.FIGHT_POKEMON} | {self.FIGHT_LOCATION}')
    
    def login(self):
        log = " "
        if len(log) < 2:  # @TODO do zmiany
            import configparser
            config = configparser.ConfigParser()
            config.read("config/config.ini")
            log = config["LOGGING_IN"]["LOGIN"]
            password = config["LOGGING_IN"]["PASSWORD"]

        search = self.driver.find_element(By.NAME, "login")
        search.send_keys(log)

        search = self.driver.find_element(By.NAME, "pass")
        search.send_keys(password)

        search.send_keys(Keys.RETURN)
        time.sleep(5)

    def screenshot(self):
        current_time = datetime.now().time()
        self.driver.save_screenshot(f"screenshot{current_time}.png")

    def fight_pokemon(self):
        pickedPokemon = self.team[self.FIGHT_POKEMON]
        
        try:
            # attack with the choosen pokemon
            cth = self.driver.find_element(By.XPATH, f"//form[@name='{pickedPokemon}']")
            cth.click()
        except:
            # if not possible, heal all and press again
            self.heal_all()
            cth = self.driver.find_element(By.XPATH, f"//form[@name='{pickedPokemon}']")
            cth.click()
        try:
            cth = self.driver.find_element(By.XPATH, "//a[@href='#wynik_walki']")
            cth.click()
        except:
            print("fight_pokemon")
            self.exception_break()

    def hunt(self):
        try:
            # click the picked location button
            hunt_location = self.loc[self.FIGHT_LOCATION]
            poluj = self.driver.find_element(By.XPATH, f"//img[@src='img/lokacje/s/{hunt_location}.jpg']")
            poluj.click()
        except:
            print("hunt")
            self.exception_break()
            
    def pokemon_events(self):
        if self.st.is_shiny() or self.st.is_on_whitelist():
            self.running = False
            # @todo coś z tym zrobić
        else:
            self.fight_pokemon()
            self.pb.throw("Netball")
            self.pb.throw("Levelball")
            self.st.have_item()

    def other_events(self):
        if self.st.is_end_pa():
            self.drink_oak()

        self.manage_elm()
        if self.rezerwa_info() > 80:#%
            self.sell_all()

        if self.st.is_egg() and self.skip_eggs:
            print("Found an egg! Skipping c:")
            self.skip_egg()
        elif self.st.is_egg() and not self.skip_eggs:
            print("Found an egg!")
            self.exception_break()
        if self.st.is_tm():
            print("TM!")
            self.exception_break()
        if self.st.is_tma() and self.skip_tutor:
            print("TMA!")
            self.skip_tma()

    def skip_tma(self):
        try:
            cth = self.driver.find_element(By.XPATH, "//button[@class='vex-dialog-button-primary vex-dialog-button vex-first']")
            cth.click()
        except:
            print("skip_tma")
            self.exception_break()

    def skip_egg(self):
        try:
            cth = self.driver.find_element(By.XPATH, "//input[@name='poluj']")
            cth.click()
        except:
            print("skip_egg")
            self.exception_break()

    def manage_elm(self):
        progress = self.elm.get_progress()
        if progress == -1:
            print("new quest needed")
            #self.elm.new_quest()
            progress = self.elm.get_progress()
            if progress == -1:
                print("manage_elm")
                self.exception_break()
                
        if self.elm_status != progress:
            self.elm_status = progress
            print("quest part ended!")

            quest_loc = self.elm.get_daily_quest_info(self.loc)
            if quest_loc == "none":
                self.FIGHT_LOCATION = self.DEFAULT_FIGHT_LOCATION  
            else:
                # check if there is an item to give else:
                self.FIGHT_LOCATION = quest_loc

        #if -1 then press elm_status, if still -1, then click new QuestClass
        # tutaj dać by czytało każde zadanie

    def travel(self):
        self.hunt()

        if self.st.is_pokemon():
            self.pokemon_events()
        else:
            self.other_events()

    def heal_all(self):
        try:
            search1 = self.driver.find_element(By.XPATH, "//img[@title='Wylecz wszystkie Pokemony']")
            search1.click()
        except:
            print("Error: heal_all()")

    def sell_all(self):
        try:
            search = self.driver.find_element(By.XPATH, "//input[@title='Sprzedaj wszystkie pokemony']")
            search.click()

            try:
                time.sleep(1)
                search = self.driver.find_element(By.XPATH, "//button[@class='vex-dialog-button-primary vex-dialog-button vex-first']")
                search.click()
            except:
                print("Error: submit sell_rezerwa()")

        except:
            print("Error: sell_rezerwa()")

    def drink_oak(self):
        search = self.driver.find_element(By.XPATH, "//img[@title='Wypij Napój Profesora Oaka']")
        search.click()

    def rezerwa_info(self):
        amount = self.driver.find_element(By.XPATH, "//span[@class='rezerwa-count']")
        self.rezerwa_percentage = 100 * int(amount.text)/30
        return self.rezerwa_percentage


async def main():
    bot = Schedule()
    input_task = asyncio.create_task(bot.read_user_input())
    print_task = asyncio.create_task(bot.bot_loop())
    await asyncio.gather(input_task, print_task)

if __name__ == "__main__":
    asyncio.run(main())
    exit(0)


