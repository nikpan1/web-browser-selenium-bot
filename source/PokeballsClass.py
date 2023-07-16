# POKEBALLCLASS

from selenium.webdriver.common.by import By


# Throw poke ball
class Throw:
    def __init__(self, driver):
        self.driver = driver

    def throw(self, pokeball_name):
        try:
            cth = self.driver.find_element(By.XPATH, f"//form[@name='pokeball_{pokeball_name}']")
            cth.click()
        except:
            #print("Error:" + pokeball_name)
            return True

        return False
