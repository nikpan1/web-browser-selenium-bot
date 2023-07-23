import time
import datetime
import os

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.service import Service as FirefoxService
from webdriver_manager.firefox import GeckoDriverManager

from StatementsClass import Statements
from PokeballsClass import Throw
from QuestClass import Elm  
from userActions import UserActions


class Schedule:
    def __init__(self, load_img, skip_egg, skip_tutor):
        # settings
        self.load_images = load_img
        self.skip_eggs = skip_egg
        self.skip_tutor = skip_tutor

        POKEWARS = "https://pokewars.pl"        
        options = webdriver.FirefoxOptions()
        options.add_argument('--disable-blink-features=AutomationControlled')
        if not self.load_images:
            options.set_preference("permissions.default.image", 2)
        self.driver = webdriver.Firefox(options=options, 
                                        service=FirefoxService(GeckoDriverManager().install()))
        self.driver.get(POKEWARS)

        self.pb = Throw(self.driver)
        self.st = Statements(self.driver)
        self.elm = Elm(self.driver)
        self.actions = UserActions(self.driver)

        self.FIGHT_POKEMON = 3
        self.FIGHT_LOCATION = 2 
        self.DEFAULT_FIGHT_LOCATION = 2

        self.rezerwa_count = 0
        
        self.init_elm()        

    def init_elm(self):
        self.login()

        self.loc = self.elm.find_locations()
        
        self.elm.show_elm()
        self.elm_status = self.elm.get_progress()
        self.elm_location = self.elm.get_daily_quest_info(self.loc)
        
        if self.elm_location in self.loc:
            self.FIGHT_LOCATION = self.loc.index(self.elm_location)

        while True:
            pk = self.loc[self.FIGHT_POKEMON()]
            if not self.actions.hunt(pk):
                self.exception_break()
            if self.st.is_pokemon():
                self.team = self.elm.find_team()
                break

        self.print_info()        

    def print_info(self):
        BOLD_ON = '\033[1m'
        BOLD_OFF = '\033[0m'

        for lo, index in enumerate(self.loc):
            if self.FIGHT_LOCATION:
                print(BOLD_ON + index + ". " + lo + BOLD_OFF)
            else:        
                print(index + ". " + lo)
        
        for t, index in enumerate(self.team):
            if self.FIGHT_POKEMON:
                print(BOLD_ON + index + ". " + t + BOLD_OFF)
            else:
                print(index + ". " + t)

    def exception_break(self):
        print("exception_break") 
        self.running = False

    def login(self):
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
        time.sleep(3)

    def fight_pokemon(self):
        pickedPokemon = self.team[self.FIGHT_POKEMON]
        
        try:
            # attack with the choosen pokemon
            cth = self.driver.find_element(By.XPATH, f"//form[@name='{pickedPokemon}']")
            cth.click()
        except:
            # if not possible, heal all and press again
            self.actions.heal_all()
            cth = self.driver.find_element(By.XPATH, f"//form[@name='{pickedPokemon}']")
            cth.click()
        try:
            cth = self.driver.find_element(By.XPATH, "//a[@href='#wynik_walki']")
            cth.click()
        except:
            print("exception: fight_pokemon")
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
            self.actions.drink_oak()

        self.manage_elm()
        if self.rezerwa_info() > 80:#%
            self.actions.sell_all()

        if self.st.is_egg() and self.skip_eggs:
            print("Found an egg!(skip)")
            if not self.actions.skip_egg():
                self.exception_break()
        elif self.st.is_egg() and not self.skip_eggs:
            print("Found an egg!")
            self.exception_break()
        if self.st.is_tm():
            print("TM!")
            self.exception_break()
        if self.st.is_tma() and self.skip_tutor:
            print("TMA!")
            if not self.actions.skip_tma():
                self.exception_break()

    def manage_elm(self):
        progress = self.elm.get_progress()
        if progress == -1:
            print("new quest needed")
            #self.elm.new_quest()
            progress = self.elm.get_progress()
            if progress == -1:
                print("manage_elm")
                
        if self.elm_status != progress:
            self.elm_status = progress
            print("quest part ended!")

            quest_loc = self.elm.get_daily_quest_info(self.loc)
            if quest_loc == "none":
                self.FIGHT_LOCATION = self.DEFAULT_FIGHT_LOCATION  
            else:
                # check if there is an item to give else:
                self.FIGHT_LOCATION = quest_loc

    def travel(self):
        pk = self.loc[self.FIGHT_LOCATION]
        if not self.actions.hunt(pk):
            self.exception_break()

        if self.st.is_pokemon():
            self.pokemon_events()
        else:
            self.other_events()

    def rezerwa_info(self):
        amount = self.driver.find_element(By.XPATH, "//span[@class='rezerwa-count']")
        self.rezerwa_percentage = 100 * int(amount.text)/30
        return self.rezerwa_percentage


