# QUESTCLASS

from selenium.webdriver.common.by import By


class Elm:
    def __init__(self, driver):
        self.driver = driver
        self.old_text = None

    def find_locations(self):
        lokacje = []
        lok = []
        poluj = self.driver.find_elements(By.XPATH, "//img[contains(@src, 'img/lokacje/s/')]")
        for elem in poluj:
            # print(i.get_attribute('src'))
            source = elem.get_attribute('src').split('/')
            lokacje.append(source[6])

        for loc in lokacje:
            a_loc = str(loc).replace("%20", " ")
            b_loc = str(a_loc).replace(".jpg", "")
            lok.append(b_loc)

        return lok

    def find_team(self):
        team = []
        fight = self.driver.find_elements(By.XPATH, "//form[contains(@name, 'poke_')]")
        for elem in fight:
            source = elem.get_attribute('name')
            team.append(source)
        return team

    def new_quest(self):
        # a id = "learn-arrow-miasto" a href="/codzienne"
        cth = self.driver.find_element(By.XPATH, "//a[@id='learn-arrow-miasto']")
        cth.click()
        cth = self.driver.find_element(By.XPATH, "//a[@href='/codzienne']")
        cth.click()
        action = self.driver.find_element(By.XPATH, "//input[@name='use_daily_ticket']")
        action.click()
        # może przeczytaj ile to będzie kosztować

    def show_elm(self):
        try:
            cth = self.driver.find_element(By.XPATH, "//div[@title='Zadanie codzienne']")
            cth.click()
        except:
            print("nie naduszono elm")

    def get_progress(self):
        active = 0
        try:
            tasks = self.driver.find_element(By.XPATH, "//div[@class='action-to-choose current selected']")
            active = int(tasks.text)
        except:
            return -1

        return active
    
    def get_daily_quest_info(self):
        try:
            info_panel = self.driver.find_element(By.XPATH, "//div[@class='info-box-transparent_panel']")
            location_img = info_panel.find_element(By.XPATH, "//img[contains(@src, 'img/lokacje/s/')]")
            
            source = location_img.get_attribute('src').split('/')
            location = source[6]
            location = location.replace(".jpg", "")

            return location
        except:
            # check if there is an item to give
            # else go, to the picked location 
            return "none"


class Samson:
    def __init__(self, driver):
        self.driver = driver













