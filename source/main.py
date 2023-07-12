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

        self.login()

        self.usr_cmd = " "
        self.rezerwa_count = 0
        self.running = True
        self.rezerwa_count = 0
        self.elm = 0

        self.login()
        asyncio.run(self.main())

    async def user_input(self):
        while True:
            self.usr_cmd = await asyncio.get_event_loop().run_in_executor(None, input, '> ')

    async def terminal_stats(self):
        while True:
            self.clear_terminal()
            await asyncio.sleep(3)
     
    async def bot_loop(self):
        while self.running:
            self.travel()
            
            # user command handle
            # here

    async def main(self):
        await asyncio.gather(self.user_input(), self.terminal_stats(), self.bot_loop())
    
    def clear_cmd_input(self):
        self.usr_cmd = " "

    def exception_break(self):
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
        print(f'\t elm = {self.elm}%')
        print(f'\t rezerwa = {self.rezerwa_count}/30 \t')
        print(f'-> {self.FIGHT_POKEMON} | {self.FIGHT_LOCATION}')
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

    #
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

    #
    def drink_oak(self):
        search = self.driver.find_element(By.XPATH, "//img[@title='Wypij Napój Profesora Oaka']")
        search.click()

    def rezerwa_info(self):
        amount = self.driver.find_element(By.XPATH, "//span[@class='rezerwa-count']")
        self.rezerwa_percentage = int(amount.text)/30

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
            
            poluj = self.driver.find_element(By.XPATH, f"//img[@src='img/lokacje/s/{hunt_location}.jpg']")
            poluj.click()
        except:
            # locations need to be refreshed    @TODO handle it
            exception_break()
    
    def pokemon_events(self):
        if self.st.is_shiny() or self.st.is_on_whitelist():
            exception_break()
        else:
            self.fight_pokemon()
            self.catch_pokemon()
            self.st.have_item()

    def other_events(self):
        if self.st.is_trainer():
            self.heal_all()     # for now it's okay if the first pokemon in the team is weak
                                # although @TODO make a handle popup window "everyone is healed"

        if self.st.is_end_pa():
            self.drink_oak()
#       if self.st.is_tm() or self.st.is_porosnieta_ska() \
#           or self.st.is_pole_magne() or self.st.if_is_alola():        # @TODO make a whitelist for items, this is not working currectly I think
#           gui.user_reaction()

    def manage_elm(self):
        self.loc = self.elm.find_locations()
        self.elm.open_elm_bar()

        old_elm_progress = None

        while True:
            self.hunt()
            elm_progress = self.elm.get_progress()

            # NOT working
            if old_elm_progress != elm_progress and old_elm_progress is not None:
                exception_break()
            else:
                old_elm_progress = elm_progress

            if self.st.is_pokemon():
                self.pokemon_events()
                break
            else:
                self.other_events()

    def travel(self):
        # if player pause ... update here
        if True: #if not pause
            self.rezerwa_info()
            if self.st.is_full():
                self.sell_all()

            self.hunt()

            if self.st.is_pokemon():
                self.pokemon_events()
            else:       # why? if not self.st.is_pokemon():
                self.other_events()


if __name__ == "__main__":
    bot = Schedule()
    exit(0)

