# STATEMENTSCLASS

from selenium.webdriver.common.by import By


def search_in_text(word, long):
    for i in range(0, len(long)):
        if long[i] == word[0]:
            if word == long[i:(i + len(word))]:
                return True
    return False


class Statements:
    def __init__(self, driver):
        self.driver = driver

    def is_full(self):
        search = self.driver.find_element(By.CLASS_NAME, "rezerwa_info")
        st = search.text.split(" ")

        if int(st[1]) > 26:
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
            print("I took the item!")
        except:
            pass
            #print("Error: have_item()")

    def is_pokemon(self):
        try:
            search = self.driver.find_element(By.XPATH, "//div[@class='alert-box info']")
            if search_in_text("dzikiego", search.text):
                sr = search.text.split(" ")
                print(sr[-1])
            return search_in_text("dzikiego", search.text)
        except:
            return False

    def is_shiny(self):
        try:
            search = self.driver.find_element(By.XPATH, "//div[@class='alert-box info']")
            return search_in_text("Shiny", search.text)
        except:
            return False

    def is_trainer(self):
        try:
            search = self.driver.find_element(By.XPATH, "//div[@class='alert-box info']")
            return search_in_text("drodze trenera", search.text)
        except:
            return False

    def is_empty(self):
        search = self.driver.find_element(By.XPATH, "//div[@class='alert-box error']")
        return search_in_text("nic ciekawego", search.text)

    def is_egg(self):
        try:
            search = self.driver.find_element(By.XPATH, "//div[@class='alert-box info']")
            print(search.text)
            return search_in_text("Inkubatora", search.text)
        except:
            return False

    def is_pole_magne(self):
        try:
            search = self.driver.find_element(By.XPATH, "//div[@class='alert-box info']")
            return search_in_text("etyczne", search.text)
        except:
            return False

    def is_porosnieta_ska(self):
        try:
            search = self.driver.find_element(By.XPATH, "//div[@class='alert-box info']")
            return search_in_text("poczu", search.text)
        except:
            return False

    def is_tm(self):
        try:
            search = self.driver.find_element(By.XPATH, "//div[@class='alert-box info']")
            return search_in_text("Ci TM", search.text)
        except:
            return False

    def if_this_pokemon(self, pokemon="aaaaa"):
        try:
            search = self.driver.find_element(By.XPATH, "//div[@class='alert-box info']")
            return search_in_text(pokemon, search.text)
        except:
            return False

    def if_is_alola(self):
        try:
            search = self.driver.find_element(By.XPATH, "//div[@class='alert-box info']")
            return search_in_text("Alola", search.text)
        except:
            return False

    def is_healthy(self):
        pass
