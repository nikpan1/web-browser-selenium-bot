# STATEMENTSCLASS
from selenium.webdriver.common.by import By

import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from CoreSettings import *

class Statements:
    def __init__(self, driver):
        self.driver = driver
    
    def is_fained(self):
        # div class box gray round center not-full-health 
        try:
            search = self.driver.find_element(By.XPATH, "//div[@class='box gray round center not-full-health']")
        except:
            return False
        return True 
        
    def found_item(self):
        try:
            search = self.driver.find_element(By.XPATH, "//div[@class='alert-box info']")
            if "Brawo! Podczas w" in search.text:   # wędrówki znalazłeś _ x ___.
                # if found money -> skip
                if "¥" in search.text:
                    return "money", 1
                #if "ball" in search.text or "Berry" in search.text:
                #    return " ", 0
                i = search.text.index("x") + 1
                
                item = search.text[i:-1]
                item = item.strip()

                amount_arr = search.text[:(i - 2)].split()
                amount = amount_arr[-1]

                print("found item: ", item, amount)
                return item, int(amount)
            else:
                return " ", 0
        except:
            return " ", 0
    
    def is_trying_not_right(self):
        # Nie masz wyst.
        try:
            search = self.driver.find_element(By.XPATH, "//div[@class='alert-box error']")
            if "Bilety wymagane" in search.text or "Nie masz wyst" in search.text or "Nie posiadasz Pok" in search.text:
                return True
            else:
                return False 
        except:
            return False

    def met_trader(self):
        # wymieni
        try:
            search = self.driver.find_element(By.XPATH, "//div[@class='alert-box info']")
            if "wymieni" in search.text:
                return True
            else:
                return False 
        except:
            return False
   
    def is_PA_event(self):
        # Regenerujesz  | Tracisz
        try:
            search = self.driver.find_element(By.XPATH, "//div[@class='alert-box info']")
            if "Regenerujesz" in search.text or "Tracisz" in search.text:
                return True
            else:
                return False 
        except:
            return False
   

    def found_nothing_interesting(self):
        #nic ciekawego.
        try:
            search = self.driver.find_element(By.XPATH, "//div[@class='alert-box error']")
            if "nic ciekawego." in search.text:
                return True
            else:
                return False 
        except:
            return False
      
    def is_team(self):
        try:
            search = self.driver.find_element(By.XPATH, "//div[@class='alert-box info']")
            if "eam" in search.text:
                return True
            else:
                return False 
        except:
            return False
   
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
            if int(search.text) < 7:
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

        with open(WHITELIST_DIR, 'r') as file:     # @TODO read the whitelist once
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

    def is_alola_challange(self):
        try:
            search = self.driver.find_element(By.XPATH, "//div[@class='alert-box info']")
            return "regionu Alola" in search.text
        except:
            return False

