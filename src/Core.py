import time
from CoreSettings import *

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
#from selenium.webdriver.firefox.service import Service as FirefoxService
#from webdriver_manager.firefox import GeckoDriverManager

from pw.StatementsClass import Statements
from pw.PokeballsClass import Throw
from pw.QuestClass import Elm  
from pw.UserActions import UserActions

from Screenshooter import make_screenshot
from ItemDatabase import ItemDatabase


class Schedule:
    def __init__(self, log, psswd, load_img, skip_egg, skip_tutor, instant_sell_rez = True):
        self.login = log
        self.password = psswd
        # settings     @TODO change to dictionary
        self.load_images = load_img
        self.skip_eggs = skip_egg
        self.skip_tutor = skip_tutor
        self.skip_sell_rezerwa = instant_sell_rez
        
        self.driver = self.get_driver()

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
        
        self.message_request = False
        self.message_buffor = " "

        # database
        self.db_container = ItemDatabase()

    def get_driver(self):
        options = webdriver.FirefoxOptions()
        options.add_argument('--disable-blink-features=AutomationControlled')

        if not self.load_images:
            options.set_preference("permissions.default.image", 2)
        firefoxDriver = webdriver.Firefox(options=options)
                                          #executable_path='ext/drivers/geckodriver')
                                        # service=FirefoxService(GeckoDriverManager().install()))
        firefoxDriver.get(POKEWARS)
        
        return firefoxDriver

    def init_elm(self):
        self.login_user()
        
        self.elm.show_elm()
        self.elm_status = self.elm.get_progress()

        self.loc = self.elm.find_locations()
        # self.team = 
        self.get_team_data()

    def get_team_data(self):
        if self.st.is_end_pa():
            self.actions.drink_oak()
        
        while True:
            pk = self.loc[0]
            if not self.actions.hunt(pk):   # if pressing hunt will fail 
                self.wait_request = True
                self.exception_break("Init")
            if self.st.is_pokemon():
                self.team = self.elm.find_team()
                break

        self.pokemon_events()

    def exception_break(self, message):
        self.wait_request = True
        self.wait_message = "Exception: " + message

    def login_user(self):
        search = self.driver.find_element(By.NAME, "login")
        search.send_keys(self.login)

        search = self.driver.find_element(By.NAME, "pass")
        search.send_keys(self.password)

        search.send_keys(Keys.RETURN)
        time.sleep(2)

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
                while True:
                    val = file.readline()
                    if not val or val == " ":
                        break
                    
                    val = val.strip()
                    
                    if val in search.text:
                        print("found exclusice pokemon: ", val)
                        # next: catch with repeatball
                        # last: go to rezerwa and take caught pokemon to pokebox
                        break 
                    # if not found lets ust quickball(?)

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
        if self.rezerwa_info() > 80:#%
            self.actions.sell_all()


        item, amount = self.st.found_item()
 
        if self.st.is_alola_challange():
            self.exception_break("alola!")

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
            result = self.actions.pick_tm()
            if result == 0:
                self.wait_request = True
        elif self.st.is_tma() and self.skip_tutor:
            print("TMA!")
            time.sleep(0)
            if not self.actions.skip_tma():
                self.wait_request = True
            else:
                pass # ?
        elif self.st.is_trainer():
            pass
        elif amount != 0:
            self.db_container.db_append(item, amount, self.loc[self.FIGHT_LOCATION])
            return
        elif self.st.is_team():
            self.wait_request = True
        elif self.st.found_nothing_interesting():
            #print("nothing interesting")
            pass
        elif self.st.is_trying_not_right():
            # dlaczego to się kurde odpala? @TODO
            pass
        elif self.st.is_PA_event():
            pass 
        elif self.st.met_trader():
            # skip
            pass 
        else:
            print("found new event!")
            self.wait_request = True
            self.wait_img_buffor = make_screenshot(self.driver) 
    
    def manage_elm(self):
        progress = self.elm.get_progress()
        if progress == -1:
            if not self.elm.show_elm():
                self.wait_request = True
                self.wait_message = "I need a new quest"
                print("new quest needed")
            
            progress = self.elm.get_progress()
            if progress == -1:
                print("manage_elm")
                
        if self.elm_status != progress:     # it means it started a new quest part 
            # if prize > 100.000 and last task:
            #   wait request - "end of quest"
            # if "Oddaj przedmiot" in wybrana akcja ?
            
            self.elm_status = progress

            quest_loc = self.elm.get_daily_quest_info(self.loc)
            if quest_loc == "none":                                                 # is it working?
                self.FIGHT_LOCATION = self.DEFAULT_FIGHT_LOCATION  
            else:
                # check if there is an item to give else:
                self.FIGHT_LOCATION = quest_loc

            self.message_request = True
            self.message_buffor = f"Changing location to {self.FIGHT_LOCATION}: "

    def travel(self):
        pk = self.loc[self.FIGHT_LOCATION]
        if not self.actions.hunt(pk):
            self.exception_break("travel")

        if self.st.is_pokemon():
            self.pokemon_events()
        else:
            self.other_events()

    def rezerwa_info(self): # @TODO przenieść do Statements
        amount = self.driver.find_element(By.XPATH, "//span[@class='rezerwa-count']")
        self.rezerwa_percentage = 100 * int(amount.text)/30
        return self.rezerwa_percentage


