# STATEMENTSCLASS
import time

from selenium.webdriver.common.by import By


class Statements:
    def __init__(self, driver):
        self.driver = driver

    def found_item(self):
        try:
            search = self.driver.find_element(By.XPATH, "//div[@class='alert-box info']")
            if "Brawo! Podczas w" in search.text:   # wędrówki znalazłeś _ x ___.
                index = search.text.index("x")
                item = search.text[(index + 2):(len(search.text - 1))]
                
                amount_arr = search.text[:index].split()
                amount = amount_arr[len(amount_arr) - 1]
                
                print(item, amount)
                return item, amount
        except:
             pass
        return "", "0"

   
    def is_full(self):
        try:
            search = self.driver.find_element(By.CLASS_NAME, "rezerwa_info")
            if int(search.text.split(" ")[1]) > 26:
                return True
            return False
        except:
            print("exception:is_full")
            return False

    def is_end_pa(self):
        try:
            search = self.driver.find_element(By.XPATH, "//span[@id='action_points_count']")
            if int(search.text) < 5:
                return True
            return False
        except:
            print("exception:is_end_pa")
            return False 

    def have_item(self):
        try:
            search = self.driver.find_element(By.XPATH, "//input[@name='zdejmij_przedmioty']")
            search.click()
        except:
            # if exception - pokemon doesn't any have iterm
            pass

    def is_pokemon(self):
        try:
            search = self.driver.find_element(By.XPATH, "//div[@class='alert-box info']")
            return "dzikiego" in search.text
        except:
            return False

    def is_shiny(self):
        try:
            search = self.driver.find_element(By.XPATH, "//div[@class='alert-box info']")
            return "Shiny" in search.text
        except:
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
            return False

    def is_egg(self):
        try:
            search = self.driver.find_element(By.XPATH, "//div[@class='alert-box info']")
            #print(search.text)
            return "Inkubatora" in search.text
        except:
            return False

    def is_pole_magne(self):
        try:
            search = self.driver.find_element(By.XPATH, "//div[@class='alert-box info']")
            return "etyczne" in search.text
        except:
            return False

    def is_porosnieta_ska(self):
        try:
            search = self.driver.find_element(By.XPATH, "//div[@class='alert-box info']")
            return "poczu" in search.text
        except:
            return False

    def is_tm(self):
        try:
            search = self.driver.find_element(By.XPATH, "//div[@class='alert-box info']")
            return "Lidera Sali" in search.text
        except:
            return False

    def is_tma(self):
        try:
            search = self.driver.find_element(By.XPATH, "//div[@class='alert-box info']")
            return "nauczyciela" in search.text
        except:
            return False

    def if_this_pokemon(self, pokemon="aaaaa"):
        try:
            search = self.driver.find_element(By.XPATH, "//div[@class='alert-box info']")
            return pokemon in search.text
        except:
            return False

    def if_is_alola(self):
        try:
            search = self.driver.find_element(By.XPATH, "//div[@class='alert-box info']")
            return "Alola" in search.text
        except:
            return False

