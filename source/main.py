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
# @TODO skip found egg
# z poziomu drivera przybliżenie ekranu na 60%?


class Schedule:
    def __init__(self):
        LOAD_IMAGES = False
        POKEWARS = "https://pokewars.pl"
        self.FIGHT_POKEMON = 4
        self.FIGHT_LOCATION = 4

        options = webdriver.FirefoxOptions()
        options.add_argument('--disable-blink-features=AutomationControlled')

        if LOAD_IMAGES:
            options.set_preference("permissions.default.image", 2)

        self.driver = webdriver.Firefox(options=options, service=FirefoxService(GeckoDriverManager().install()))
        self.driver.get(POKEWARS)

        self.pb = Throw(self.driver)
        self.st = Statements(self.driver)
        self.elm = Elm(self.driver)

        self.loc = []
        self.team = []

        self.usr_cmd = " "
        self.rezerwa_count = 0
        self.running = False
        self.elm = 0

        self.login()

        self.debug_input()
        asyncio.run(self.main())

    def debug_input(self):
        a = input()
        self.driver.find_element(XPath, a)
    async def main(self):
        await asyncio.gather(self.terminal_stats(), self.bot_loop())
 
    def user_input(self):
        if len(self.usr_cmd) > 1:
            return
        if self.usr_cmd == "stop":
            self.running = False
        if self.usr_cmd == "start":
            self.running = True 
            
            arguments = self.usr_cmd.split()
            if len(arguments) == 2:
                self.FIGHT_POKEMON = int(arguments[0])
                self.FIGHT_LOCATION = int(arguments[1])

            self.usr_cmd = " "

    async def terminal_stats(self):
        while True:
            self.clear_terminal()
            self.user_input()
            self.usr_cmd = await asyncio.get_event_loop().run_in_executor(None, input, '> ')
#await asyncio.sleep(3)
     
    async def bot_loop(self):
        while True:
            while self.running:
                self.travel()
   
    def exception_break(self):
        self.running = False
        while not self.running:
            pass

    def clear_terminal(self):
        os.system('cls' if os.name == 'nt' else 'clear')

        print("_____________________")
        if self.running == True:
            print(f'XXXXXX RUNNING XXXXXX')
        else:
            print(f'XXXXXX WAITING XXXXXX')
        print("_____________________")       
        print(f'  elm = {self.elm}%')
        print(f'  rezerwa = {self.rezerwa_count}%')
        print(f'  {self.FIGHT_POKEMON} | {self.FIGHT_LOCATION}')
        print(f"cmd={self.usr_cmd}")
        print("_____________________")
    
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
        time.sleep(1)

    def screenshot(self):
        current_time = datetime.now().time()
        self.driver.save_screenshot(f"screenshot{current_time}.png")

#-------------------

    def heal_all(self):
        try:
            search1 = self.driver.find_element(By.XPATH, "//img[@title='Wylecz wszystkie Pokemony']")
            search1.click()
        except:
            print("Error: heal_all()")
        try:
            time.sleep(3)
            search = self.driver.find_element(By.XPATH, "//button[@class='vex-dialog-button-primary vex-dialog-button vex-first']")
            search.click()
        except:
            print("Error: submit heal ok()")

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
    rezerwa self.rezerwa_percentage

# -----------

    def catch_pokemon(self):
        self.pb.throw("Netball")
        self.pb.throw("Levelball")

    def fight_pokemon(self):
        try:
            # attack with the choosen pokemon
            pickedPokemon = self.team[self.FIGHT_POKEMON]
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
           exception_break()
    
    def hunt(self):
        try:
            # click the picked location button
            hunt_location = self.loc[self.FIGHT_LOCATION]
            
            poluj = self.driver.find_element(By.XPATH, f"//img[@src='img/lokacje/s/{self.FIGHT_LOCATION}.jpg']")
            poluj.click()
        except:
            exception_break()
    
    def pokemon_events(self):
        if self.st.is_shiny() or self.st.is_on_whitelist():
            self.running = False
            # @todo coś z tym zrobić
        else:
            self.fight_pokemon()
            self.catch_pokemon()
            self.st.have_item()

    def other_events(self):
        if self.st.is_end_pa():
            self.drink_oak()
        # handle rezerwa

    def manage_elm(self):
        self.loc = self.elm.find_locations()
        self.elm.open_elm_bar()
        self.elm_status = self.elm.get_status()
# dwie pierwsze funkcje dać osobno by tylko raz się odpaliły 

    def travel(self):
        self.manage_elm()
        if self.rezerwa_info() > 80:#%
            self.sell_all()

        self.hunt()

        if self.st.is_pokemon():
            self.pokemon_events()
        else:
            self.other_events()


if __name__ == "__main__":
    bot = Schedule()
    exit(0)


