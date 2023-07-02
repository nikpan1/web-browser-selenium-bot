# STATEMENTSCLASS
import time

from selenium.webdriver.common.by import By

class Statements:
    def __init__(self, driver):
        self.driver = driver

    def is_full(self):
        search = self.driver.find_element(By.CLASS_NAME, "rezerwa_info")
        if int(search.text.split(" ")[1]) > 26:
            return True
        return False

    def is_end_pa(self):
        search = self.driver.find_element(By.XPATH, "//span[@id='action_points_count']")
        if int(search.text) < 5:
            return True
        return False

    def have_item(self):
        try:
            search = self.driver.find_element(By.XPATH, "//input[@name='zdejmij_przedmioty']")
            search.click()
        except:
            pass

    def is_pokemon(self):
        try:
            search = self.driver.find_element(By.XPATH, "//div[@class='alert-box info']")
            #if "dzikiego" in search.text:
                #print(search.text.split(" ")[-1])
            return "dzikiego" in search.text
        except:
            pass
        return False

    def is_shiny(self):
        try:
            search = self.driver.find_element(By.XPATH, "//div[@class='alert-box info']")
            return "Shiny" in search.text
        except:
            pass
        return False

    def is_on_whitelist(self):
        try:
            search = self.driver.find_element(By.XPATH, "//div[@class='alert-box info']")
        except:
            pass

        with open("config/whitelist", 'r') as file:     # @TODO read the whitelist once
            pokemon_name = file.readline()
            search = self.driver.find_element(By.XPATH, "//div[@class='alert-box info']")
            if pokemon_name in search.text:
                return True

        return False

    def is_trainer(self):
        try:
            search = self.driver.find_element(By.XPATH, "//div[@class='alert-box info']")
            return "drodze trenera" in search.text
        except:
            pass
        return False

    def is_empty(self):
        search = self.driver.find_element(By.XPATH, "//div[@class='alert-box error']")
        return "nic ciekawego" in search.text

    def is_egg(self):
        try:
            search = self.driver.find_element(By.XPATH, "//div[@class='alert-box info']")
            print(search.text)
            return "Inkubatora" in search.text
        except:
            pass
        return False

    def is_pole_magne(self):
        try:
            search = self.driver.find_element(By.XPATH, "//div[@class='alert-box info']")
            return "etyczne" in search.text
        except:
            pass
        return False

    def is_porosnieta_ska(self):
        try:
            search = self.driver.find_element(By.XPATH, "//div[@class='alert-box info']")
            return "poczu" in search.text
        except:
            pass
        return False

    def is_tm(self):
        try:
            search = self.driver.find_element(By.XPATH, "//div[@class='alert-box info']")
            return "Ci TM" in search.text
        except:
            pass
        return False

    def if_this_pokemon(self, pokemon="aaaaa"):
        try:
            search = self.driver.find_element(By.XPATH, "//div[@class='alert-box info']")
            return pokemon in search.text
        except:
            pass
        return False

    def if_is_alola(self):
        try:
            search = self.driver.find_element(By.XPATH, "//div[@class='alert-box info']")
            return "Alola" in search.text
        except:
            pass
        return False

    def is_healthy(self):
        pass
