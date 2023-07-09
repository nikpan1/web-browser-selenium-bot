# MAIN

import time
import datetime

from selenium import webdriver
from selenium.webdriver.firefox.service import Service as FirefoxService
from webdriver_manager.firefox import GeckoDriverManager 

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

from GUI import GUI
from StatementsClass import Statements
from PokeballsClass import Throw
from QuestClass import Elm  #

import logging, logging.config
# @TODO remake logging system
# @TODO zrobić counter znalezionych itemów/złapanych pokemonów
# @TODO elm quests handling
# @TODO default settings
# @TODO filtrowanie rezerwy
# @TODO przed sprzedażą niech wszystkich ewo
# @TODO skip found egg

def wait(a, b):
    gui.keyboard_interaction()
    time.sleep(0.1)


class Schedule:
    def __init__(self):
        LOGGER = logging.getLogger(__name__)
        LOGGER.debug("TESTOWA INFORMACJA")

        POKEWARS = "https://pokewars.pl"

        options = webdriver.ChromeOptions()
        PATH = "C:/Program Files (x86)/chromedriver.exe"

        options = webdriver.FirefoxOptions()
        options.set_preference("permissions.default.image", 2)

        self.driver = webdriver.Firefox(options=options, service=FirefoxService(GeckoDriverManager().install()))
        self.driver.get(POKEWARS)

        self.pb = Throw(self.driver)
        self.st = Statements(self.driver)
        self.elm = Elm(self.driver)

        self.where_hunt = None
        self.poke_id = 4

        self.loc = []
        self.team = []

    #
    def login(self):
        gui.login_interaction()
        log, password = gui.return_inputs()

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


    def screenshot(self):
        x = datetime.datetime.now()
        file_name = x.strftime("%b-%d_%HH%MM%SS")
        self.driver.save_screenshot(f"SCREENSHOTS/{file_name}.png")

        """
        passy do konta:
        nibafe7858@votooe.com
        nikodemtoszefunciudobraes
        haslo_do_alta
        """

    #
    def heal_all(self):
        try:
            search1 = self.driver.find_element(By.XPATH, "//img[@title='Wylecz wszystkie Pokemony']")
            search1.click()
        except:
            print("Error: heal_all()")
        try:
            time.sleep(1)
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

        wait(0, 1)

    #
    def drink_oak(self):
        search = self.driver.find_element(By.XPATH, "//img[@title='Wypij Napój Profesora Oaka']")
        search.click()

        wait(0, 1)

    def rezerwa_info(self):
        amount = self.driver.find_element(By.XPATH, "//span[@class='rezerwa-count']")
        percentage = int(amount.text)/30
        gui.rezerwa_bar.change_percent(percentage)

    #
    def catch_pokemon(self):
        self.pb.throw("Netball")
        self.pb.throw("Levelball")

    #
    def catch_shiny(self):
        self.pb.throw("Netball")

        catched = True
        while not catched:              # @TODO error
            if self.pb.throw("Repeatball"):
                catched = False

    #
    def fight_pokemon(self):
        try:
            # attack with the choosen pokemon
            cth = self.driver.find_element(By.XPATH, f"//form[@name='{self.poke_id}']")
            cth.click()
        except:
            # if not possible, heal all and press again
            self.heal_all()
            cth = self.driver.find_element(By.XPATH, f"//form[@name='{self.poke_id}']")
            cth.click()

        try:
            cth = self.driver.find_element(By.XPATH, "//a[@href='#wynik_walki']")
            cth.click()
        except:
            # is it even possible ?
            print("Error: wyniki_walki, fight_pokemon()")

    #
    def hunt(self):
        try:
            # click the picked location button
            poluj = self.driver.find_element(By.XPATH, f"//img[@src='img/lokacje/s/{self.where_hunt}.jpg']")
            poluj.click()
        except:
            # locations need to be refreshed    @TODO handle it
            gui.user_reaction()

    #
    def pokemon_events(self):
        if self.st.is_shiny() or self.st.is_on_whitelist():
            gui.user_reaction()
        else:
            self.fight_pokemon()
            self.catch_pokemon()
            self.st.have_item()

    #
    def other_events(self):
        if self.st.is_trainer():
            self.heal_all()     # for now it's okay if the first pokemon in the team is weak
                                # although @TODO make a handle popup window "everyone is healed"
            pass

        if self.st.is_end_pa():
            self.drink_oak()

        if self.st.is_tm() or self.st.is_porosnieta_ska() \
                or self.st.is_pole_magne() or self.st.if_is_alola():        # @TODO make a whitelist for items, this is not working currectly I think
            gui.user_reaction()

    #
    def manage_elm(self):
        self.loc = self.elm.find_locations()
        self.where_hunt = self.loc[0]
        self.elm.open_elm_bar()

        old_elm_progress = None

        while True:
            self.hunt()
            elm_progress = self.elm.get_progress()

            gui.elm_bar.change_percent(elm_progress)
            if old_elm_progress != elm_progress and old_elm_progress is not None:
                gui.user_reaction()
            else:
                old_elm_progress = elm_progress


            if self.st.is_pokemon():
                self.team = self.elm.find_team()
                self.poke_id = self.team[2]  # ?

                gui.recreate_buttons(self.loc, self.team)
                gui.stop()

                self.pokemon_events()
                break
            else:
                self.other_events()

    #
    def travel(self):
        if gui.pause:
            self.where_hunt = gui.loc_ls.return_now_picked_loc()
            self.poke_id = gui.team.return_now_picked_loc()

        elif not gui.pause:
            self.rezerwa_info()
            if self.st.is_full():
                self.sell_all()

            self.hunt()

            if self.st.is_pokemon():
                self.pokemon_events()
            else:       # why? if not self.st.is_pokemon():
                self.other_events()

    #
    def button_management(self):
        if gui.is_pressed() == "team":
            self.manage_elm()

        if gui.is_pressed() == "loc":
            self.manage_elm()

        if gui.is_pressed() == "heal":
            self.heal_all()

        if gui.is_pressed() == "ss":
            self.screenshot()

        gui.is_p = None

    #
    def run(self):
        self.login()
        time.sleep(5)
        #
        while gui.catching:
            gui.keyboard_interaction()
            self.button_management()
            self.travel()

        self.driver.close()


if __name__ == "__main__":
    option = webdriver.ChromeOptions()
    option.add_argument('--disable-blink-features=AutomationControlled')

    bot = Schedule()
    gui = GUI()

    bot.run()

    exit(0)
