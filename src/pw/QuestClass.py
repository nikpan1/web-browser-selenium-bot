from selenium.webdriver.common.by import By
#from recorder import * 
from pynput.mouse import Controller, Listener, Button
import time

def wait_for_mouse_click():
    global cords
    cords = [0,0]
    def on_click(x, y, button, pressed):
        if pressed and button == Button.left:
            cords[0] = x
            cords[1] = y
            # Stop listening for mouse events
            listener.stop()

    # Create a listener for mouse events
    with Listener(on_click=on_click) as listener:
        listener.join()
    
    return cords 

def press_pos(x, y):
    mouse = Controller()

    mouse.position = (x, y)
    mouse.click(Button.left)


class Elm:
    def __init__(self, driver):
        self.driver = driver
        self.old_text = None
        self.daily_cords = [0, 0]

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
        
        # class="niceButton full_width big_padding"
        
        cth = self.driver.find_element(By.XPATH, "//input[@class='niceButton full_width big_padding']")
        cth.click()
        
        time.sleep(2)

        try:
            # class="vex-dialog-buttons"
            popup = self.driver.find_element(By.XPATH, "//div[@class='vex-dialog-buttons']")
            print("o")
            # class="vex-dialog-button-primary vex-dialog-button vex-first"
            accept = popup.find_element(By.XPATH, "//button[@class='vex-dialog-button-primary vex-dialog-button vex-first']")
            accept.click()
            return 1
        except:
            print("new quest ups")
            return 0 

        return 1

    def quest_difficulty(self):
        time.sleep(5) # wait until the popup vanishes
        if self.daily_cords == [0,0]:
            self.daily_cords[0], self.daily_cords[1] = wait_for_mouse_click()
        
        press_pos(self.daily_cords[0], self.daily_cords[1])
             
        try:
            cth = self.driver.find_element(By.XPATH, "//input[@class='niceButton orange full_width big']")
            cth.click()
            return 1
        except:
            return 0

    def show_elm(self):
        try:
            cth = self.driver.find_element(By.XPATH, "//div[@title='Zadanie codzienne']")
            cth.click()
            return 1
        except:
            return 0
    
    def is_warsztat_quest(self)
        try:
            cth = self.driver.find_element(By.XPATH, "//div[@title='action-name']")
            print(cth.text)
            if "przedmiot z Warsztatu" in cth.text:
                return 1
            
            # @TODO następnie niech sprawdza czy może oddać C:

        except:
            return 0
        return 0

    def get_progress(self):
        active = -1
        try:
            tasks = self.driver.find_element(By.XPATH, "//div[@class='action-to-choose current selected']")
            active = int(tasks.text)
        except:
            return -1 

        return active

    def get_daily_quest_info(self, loc):
        try:
            info_panel = self.driver.find_element(By.XPATH, "//div[@class='info-box-transparent_panel']")
            table = info_panel.find_elements(By.XPATH, ".//td")
            
            avg_len = self.calculate_avg_len(loc) - 2

            for td in table:
                found_id, similiarity_percentage = self.find_most_similar_position(td.text, loc) 
                if similiarity_percentage > 70:#%
                    # we found it!
                    print("found location = ", loc[found_id], " |",similiarity_percentage)
                    return found_id
            return "none"
        except:
            return "none"       # czy aby napewno?
    
    def calculate_avg_len(self, loc):
        sum = 0
        for l in loc:
            sum += len(l)
        return sum/len(loc)

    # source: chat gpt 
    def find_most_similar_position(self, target_string, string_list):
        max_similarity = 0
        most_similar_position = None

        for i, string in enumerate(string_list):
            similarity = self.calculate_similarity(target_string, string)
            if similarity > max_similarity:
                max_similarity = similarity
                most_similar_position = i

        return most_similar_position, max_similarity

    def calculate_similarity(self, string1, string2):
        len1 = len(string1)
        len2 = len(string2)
        max_len = max(len1, len2)

        if max_len == 0:
            return 100.0

        common_chars = 0

        for char1 in string1:
            if char1 in string2:
                common_chars += 1
                string2 = string2.replace(char1, '', 1)

        similarity = (common_chars / max_len) * 100.0
        return similarity


