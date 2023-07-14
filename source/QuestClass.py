# QUESTCLASS

from selenium.webdriver.common.by import By


class Elm:
    def __init__(self, driver):
        self.driver = driver
        self.old_text = None
        self.get_progress()

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
        try:
            a_div = self.driver.find_element_by_class_name("data-box light-blue daily-data-box")
            b_div = a_div.find_element_by_class_name("col w_2-10 actions-choose-container")
            c_div = b_div.find_element_by_class_name("action-to-choose current selected")

            print("len poluj = ", int(c_div.text))

            return int(c_div.text)
        except:
            print("nie znaleziono elma")
            return -1


class Samson:
    def __init__(self, driver):
        self.driver = driver
