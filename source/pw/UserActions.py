from selenium.webdriver.common.by import By
import time

class UserActions:
    def __init__(self, driv):
        self.driver = driv

    def hunt(self, hunt_location):
        try:
            # click the picked location button
            # hunt_location = self.loc[self.FIGHT_LOCATION]
            poluj = self.driver.find_element(By.XPATH, f"//img[@src='img/lokacje/s/{hunt_location}.jpg']")
            poluj.click()
            return 1 
        except:
            print("exception: hunt")
            return 0

    def skip_tma(self):
        try:
            cth = self.driver.find_element(By.XPATH, "//button[@class='vex-dialog-button-primary vex-dialog-button vex-first']")
            cth.click()
            return 1
        except:
            print("exception: skip_tma")
            return 0

    def skip_egg(self):
        try:
            cth = self.driver.find_element(By.XPATH, "//input[@name='poluj']")
            cth.click()
            return 1 
        except:
            print("exception: skip_egg")
            return 0

    def heal_all(self):
        try:
            search1 = self.driver.find_element(By.XPATH, "//img[@title='Wylecz wszystkie Pokemony']")
            search1.click()
        except:
            print("exception: heal_all()")

    def sell_all(self):
        try:
            search = self.driver.find_element(By.XPATH, "//input[@title='Sprzedaj wszystkie pokemony']")
            search.click()

            try:
                time.sleep(1)
                search = self.driver.find_element(By.XPATH, "//button[@class='vex-dialog-button-primary vex-dialog-button vex-first']")
                search.click()
            except:
                print("exception: 2 submit sell_rezerwa()")
        
        except:
            print("exception: 1 sell_rezerwa()")

    def drink_oak(self):
        search = self.driver.find_element(By.XPATH, "//img[@title='Wypij Napój Profesora Oaka']")
        search.click()

