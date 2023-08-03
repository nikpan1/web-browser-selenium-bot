from selenium.webdriver.common.by import By
import time

TMS_DIR = "data/TMs"

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

    def pick_tm(self):
        try:
            # form id="tm-trade-form-698"
            titles = self.driver.find_elements(By.XPATH, "//form[contains(@id, 'tm-trade-form')]")
            print("titles", len(titles))
            parent_objs = [title.find_element(By.XPATH, "..") for title in titles]
            print("parents", len(parent_objs))
            # input class="niceButton big"
            buttons = [parent_obj.find_element(By.XPATH, "//input[@class='niceButton big']") for parent_obj in parent_objs]
            # span style="font-size: 18px; font-weight: bold;"
            TM_ids = [parent_obj.find_elements(By.XPATH, "//span[@style='font-size: 18px; font-weight: bold;']") for parent_obj in parent_objs]
            print(len(TM_ids))
            
            print("EOOO\n")
            print("\n", TM_ids[0].text, "\n")
            print("EOOO\n")

            TM_values = [ tm.text for tm in TM_ids]

            print(TM_values)

            found_tm_index = 0 
            # find in file the most expensive TM found
            with open(TMS_DIR, 'r') as file:
                while True:
                    val = int(file.readline())
                    if not val:
                        break
                    elif val in TM_values:
                        found_tm_index = TM_values.index(val)
                        print(val)
                        break 

            # buy the best option / or the first one 
            buttons[found_tm_index].click()
            
            # accept
            # button class="vex-dialog-button-primary vex-dialog-button vex-first"
            time.sleep(2)
            cth = self.driver.find_element(By.XPATH, "//button[@class='vex-dialog-button-primary vex-dialog-button vex-first']")
            cth.click()

            return 1
        except:
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

