import time
from CoreSettings import *

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.service import Service as FirefoxService
from webdriver_manager.firefox import GeckoDriverManager

from pw.StatementsClass import Statements
from pw.PokeballsClass import Throw
from pw.QuestClass import Elm  
from pw.UserActions import UserActions

from Screenshooter import make_screenshot
from ItemDatabase import ItemDatabase


class Schedule:
    def __init__(self, log, psswd, load_img, skip_egg, skip_tutor):
        self.login = log
        self.password = psswd
        # settings     @TODO change to dictionary
        self.load_images = load_img
        self.skip_eggs = skip_egg
        self.skip_tutor = skip_tutor
        
        # driver setup      
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
        
        self.wait_request = False
        self.wait_img_buffor = " "
        self.wait_message = " "

        # database
        self.db_container = ItemDatabase()


    def init_elm(self):
        self.login_setup()
        self.loc = self.elm.find_locations()
        
        self.elm.show_elm()
        self.elm_status = self.elm.get_progress()
        self.elm_location = self.elm.get_daily_quest_info(self.loc)
        
        if self.elm_location in self.loc:
            self.FIGHT_LOCATION = self.loc.index(self.elm_location)

        while True:
            pk = self.loc[self.FIGHT_POKEMON]
            if not self.actions.hunt(pk):
                self.wait_request = True
                self.exception_break("Init")
            if self.st.is_pokemon():
                self.team = self.elm.find_team()
                break
        
        self.pokemon_events()

    def exception_break(self, message):
        self.wait_request = True
        self.wait_message = "Exception: " + message

    def login_setup(self):
        search = self.driver.find_element(By.NAME, "login")
        search.send_keys(self.login)

        search = self.driver.find_element(By.NAME, "pass")
        search.send_keys(self.password)

        search.send_keys(Keys.RETURN)
        time.sleep(1)

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
            self.exception_break("fight_pokemon")

    def pokemon_events(self):
        if self.st.is_shiny() or self.st.is_on_whitelist():
            search = self.driver.find_element(By.XPATH, "//div[@class='alert-box info']")
            with open(SHINY_DIR, "r") as file:
                for pokemon in file:
                    if pokemon in search.text:
                        print("found exclusive pokemon!")

            self.wait_request = True
            self.wait_img_buffor = make_screenshot(self.driver) 
        else:
            self.fight_pokemon()
            self.pb.throw("Netball")
            self.pb.throw("Levelball")
            self.st.have_item()

    def other_events(self):     # @TODO big refactor - take the ctx once, and pass it to the st. functions
        if self.st.is_end_pa():     # what if loc uses 6 PA @TODO 
            self.actions.drink_oak()

        self.manage_elm()
        if self.rezerwa_info() > 90:#%
            self.actions.sell_all()
        
        item, amount = self.st.found_item()
        if amount != 0:
            self.db_container.db_append(item, amount, self.FIGHT_LOCATION)
            return             

        if self.st.is_egg() and self.skip_eggs:
            print("Found an egg!(skip)")
            if not self.actions.skip_egg():
                self.wait_request = True
            return 
        elif self.st.is_egg() and not self.skip_eggs:
            print("Found an egg!")
            self.wait_request = True
        elif self.st.is_tm():
            print("TM!")
            self.wait_request = True
        elif self.st.is_tma() and self.skip_tutor:
            print("TMA!")
            if not self.actions.skip_tma():
                self.wait_request = True
            else:
                pass
                found_tms = ["0", "0"]
                # get list of TM's 
                with open(TMS_DIR, "r") as file:
                    for line in file:
                        for tm in found_tms:
                            if int(tm) == int(line):
                                # pick that TM 
                                pass
        else:
            print("found new event!")
            self.wait_request = True
            self.wait_img_buffor = make_screenshot(self.driver) 

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

            print("Changing location to: ", self.FIGHT_LOCATION)

    def travel(self):
        pk = self.loc[self.FIGHT_LOCATION]
        if not self.actions.hunt(pk):
            self.exception_break()

        if self.st.is_pokemon():
            self.pokemon_events()
        else:
            self.other_events()

    def rezerwa_info(self): # @TODO przenieść do Statements
        amount = self.driver.find_element(By.XPATH, "//span[@class='rezerwa-count']")
        self.rezerwa_percentage = 100 * int(amount.text)/30
        return self.rezerwa_percentage


