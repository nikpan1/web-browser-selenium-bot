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
    def __init__(self, log, psswd, load_img, skip_egg, skip_tutor, instant_sell_rez, ign_elm):
        self.login = log
        self.password = psswd
        
        # settings     @TODO change to dictionary
        self.load_images = load_img
        self.skip_eggs = skip_egg
        self.skip_tutor = skip_tutor
        self.sell_instant_full_rezerwa = instant_sell_rez
        self.ignore_elm = ign_elm

        self.driver = self.get_driver()

        self.pb = Throw(self.driver)
        self.st = Statements(self.driver)
        self.elm = Elm(self.driver)
        self.actions = UserActions(self.driver)

        self.FIGHT_POKEMON = 3
        self.FIGHT_LOCATION = 5
        self.DEFAULT_FIGHT_LOCATION = 5
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

        self.loc = self.elm.find_locations()
        self.get_team_data()
        
        self.elm.show_elm()
        self.elm_status = self.elm.get_progress()
        self.manage_elm()

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
            print("except:fight_pokemon")

    def pokemon_events(self):
        if self.st.is_fained():
            self.actions.heal_all()

        if self.st.is_shiny() or self.st.is_on_whitelist():
            search = self.driver.find_element(By.XPATH, "//div[@class='alert-box info']")
            
            with open(SHINY_DIR, "r") as file:
                while True:
                    val = file.readline()
                    val = val.strip()
                
                    if not val or val == " ":
                        print("booho")
                        break
                    elif val in search.text and val != " ":
                        print("found exclusice pokemon: |", val, "| ")
                        break    
            self.wait_request = True
            self.wait_img_buffor = make_screenshot(self.driver)

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
            if self.sell_instant_full_rezerwa:
                #success = self.actions.evolve_all()
                #if not success:
                #    self.exception_break("evolve")
                self.actions.sell_all()

            else:
                self.wait_message = "rezerwa full!"
                self.wait_request = True

        item, amount = self.st.found_item()
 
#        if self.st.is_alola_challange():
#            self.exception_break("alola!")

        if self.st.is_egg():
            print("Found an egg!")
            if self.skip_eggs:
                success = self.actions.skip_egg()
                if not success:
                    self.exception_break("egg")
            else:
                self.wait_message = "Go get the egg!"
                self.wait_request = True 
        elif self.st.is_tm():
            print("TM!")
            result = self.actions.pick_tm()
            if result == 0:
                self.wait_request = True
        elif self.st.is_tma() and self.skip_tutor:
            print("TMA!")
            pk = self.loc[0]
            self.actions.hunt(pk)   
            
            if not self.actions.skip_tma():
                self.wait_request = True
            else:
                pass # ?

            if self.st.is_pokemon():
                self.pokemon_events()
            else:
                self.other_events()


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
            print("progress -1")
            if not self.elm.show_elm(): #and not self.ignore_elm:
                print("new quest needed")
                if not self.elm.new_quest():        # a za ph?
                    self.exception_break("new quest needed")
                else:
                    #self.elm.quest_difficulty()
                    self.manage_elm()

        if self.elm_status != progress:     # it means it started a new quest part 
            if self.elm.is_warsztat_quest():
                self.exception_break("Last task is warsztat")
                #

            self.elm_status = progress

            quest_loc = self.elm.get_daily_quest_info(self.loc)
            if quest_loc == "none":                                          
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

    def rezerwa_info(self):
        amount = self.driver.find_element(By.XPATH, "//span[@class='rezerwa-count']")
        self.rezerwa_percentage = 100 * int(amount.text)/30
        return self.rezerwa_percentage

    def catch_rare(self):

        self.pb.throw("Netball")
        while self.pb.throw("Repeatball"):
            pass 

    def catch_common(self):
        self.pb.throw("Netball")
        self.pb.throw("Quickball")



