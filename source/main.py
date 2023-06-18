# MAIN

import random
import time
import datetime

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

from GUI import GUI
from StatementsClass import Statements
from PokeballsClass import Throw
from QuestClass import Elm  #

import logging, logging.config


def wait(a, b):
    gui.keyboard_interaction()
    time.sleep(0.1)


def random_wait():
    pass


class Schedule:
    def __init__(self):
        LOGGER = logging.getLogger(__name__)
        LOGGER.debug("TESTOWA INFORMACJA")

        POKEWARS = "https://pokewars.pl"
        options = webdriver.ChromeOptions()
        PATH = "C:/Program Files (x86)/chromedriver.exe"
        self.driver = webdriver.Chrome(PATH)
        self.driver.get(POKEWARS)

        self.pb = Throw(self.driver)
        self.st = Statements(self.driver)
        self.elm = Elm(self.driver)

        self.where_hunt = None
        self.poke_id = None

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
            search2 = self.driver.find_element(By.XPATH, "//div[@class='vex-dialog-form']")
            search1.click()
        except:
            print("wyleczono pokemony bez przeszkod")
            pass
    #
    def sell_all(self):
        try:
            search = self.driver.find_element(By.XPATH, "//input[@title='Sprzedaj wszystkie pokemony']")
            search.click()

            try:
                wait(0, 1)
                search = self.driver.find_element(By.XPATH, "//button[@type='submit']")
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
        print(percentage)
        gui.rezerwa_bar.change_percent(percentage)

    #
    def catch_pokemon(self):
        wait(0.1, 0.3)
        self.pb.throw("Netball")

        wait(0, 0.2)
        self.pb.throw("Levelball")

    #
    def catch_shiny(self):
        wait(0.1, 0.55)
        self.pb.throw("Netball")

        catched = True
        while not catched:
            if self.pb.throw("Repeatball"):
                catched = False

    #
    def fight_pokemon(self):
        wait(0, 1)

        try:
            cth = self.driver.find_element(By.XPATH, f"//form[@name='{self.poke_id}']")
            cth.click()
        except:
            self.heal_all()
            cth = self.driver.find_element(By.XPATH, f"//form[@name='{self.poke_id}']")
            cth.click()
            print("Error: pokemon fight_pokemon().")

        wait(0, 1)

        try:
            cth = self.driver.find_element(By.XPATH, "//a[@href='#wynik_walki']")
            cth.click()
        except:
            print("Error: wyniki_walki, fight_pokemon()")

    #
    def hunt(self):
        try:
            poluj = self.driver.find_element(By.XPATH, f"//img[@src='img/lokacje/s/{self.where_hunt}.jpg']")
            poluj.click()
        except:
            print("Error: hunt()")
            gui.user_reaction()

    #
    def pokemon_events(self):
     #  if self.st.if_this_pokemon("..."):
        if self.st.is_shiny():
            gui.user_reaction()
        else:
            self.fight_pokemon()
            self.catch_pokemon()
            self.st.have_item()

    #
    def other_events(self):
        if self.st.is_trainer():
            time.sleep(14)
            self.heal_all()
            pass
        elif self.st.is_end_pa():
            self.drink_oak()

        if self.st.is_tm() or self.st.is_porosnieta_ska() \
                or self.st.is_pole_magne() or self.st.if_is_alola():
            gui.user_reaction()

    #
    def manage_elm(self):
        self.loc = self.elm.find_locations()
        self.where_hunt = self.loc[0]

        while True:
            self.hunt()
            if self.st.is_pokemon():
                self.team = self.elm.find_team()
                self.poke_id = self.team[2]

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
            random_wait()

            self.rezerwa_info()
            if self.st.is_full():
                gui.user_reaction()

            self.hunt()

            if self.st.is_pokemon():
                self.pokemon_events()
            elif not self.st.is_pokemon():
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
        self.manage_elm()

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
