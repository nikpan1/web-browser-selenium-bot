# POKEBALLCLASS

from selenium.webdriver.common.by import By


# Throw poke ball
class Throw:
    def __init__(self, driver):
        self.driver = driver

    def catch(self, pokeball_name):
        pokeball_name = pokeball_name[0].upper() + pokeball_name.lower()

        try:
            cth = self.driver.find_element(By.XPATH, "//form[@name='pokeball_" + pokeball_name + "']")
            cth.click()
        except:
            print("Error:" + pokeball_name)
            return True

        return False

    def netball(self):
        try:
            cth = self.driver.find_element(By.XPATH, "//form[@name='pokeball_Netball']")
            cth.click()
        except:
            print("Error: netball()")
            return True

    def levelball(self):
        try:
            cth = self.driver.find_element(By.XPATH, "//form[@name='pokeball_Levelball']")
            cth.click()
        except:
            print("Error: levelball()")
            return True

    def diveball(self):
        try:
            cth = self.driver.find_element(By.XPATH, "//form[@name='pokeball_Diveball']")
            cth.click()
        except:
            print("Error: Diveball()")
            return True

    def ultraball(self):
        try:
            cth = self.driver.find_element(By.XPATH, "//form[@name='pokeball_Ultraball']")
            cth.click()
        except:
            print("Error: ultraball()")
            return True

    def greatball(self):
        try:
            cth = self.driver.find_element(By.XPATH, "//form[@name='pokeball_Greatball']")
            cth.click()
        except:
            print("Error: greatball()")
            return True

    def repeatball(self):
        try:
            cth = self.driver.find_element(By.XPATH, "//form[@name='pokeball_Repeatball']")
            cth.click()
        except:
            print("Error: repeatball()")
            return True

