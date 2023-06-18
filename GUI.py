# GUI

import pygame

from ButtonClass import Button
from ButtonClass import List
from ButtonClass import LED
from ButtonClass import TextBar
from ButtonClass import Progressbar
from Colors import Colors


class GUI:
    def __init__(self):
        pygame.init()
        WINDOW_WIDTH, WINDOW_HEIGHT = 800, 500

        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption('Pokewars bot')
        icon_img = pygame.image.load('images/app_icon.png')
        pygame.display.set_icon(icon_img)
        self.logo_img = pygame.image.load('images/pokewars-logo.png')  # 365 x 100

        self.cl = Colors()

        self.rectangle1 = pygame.Rect(0, 0, WINDOW_WIDTH, 48)
        self.rectangle2 = pygame.Rect(0, 48, WINDOW_WIDTH, 48)
        self.line1 = pygame.Rect(WINDOW_WIDTH//2, 0, 2, WINDOW_HEIGHT)
        self.line2 = pygame.Rect(0, WINDOW_HEIGHT//2, WINDOW_WIDTH//2, 2)
        self.line3 = pygame.Rect(WINDOW_WIDTH//4, WINDOW_HEIGHT//2, 2, WINDOW_WIDTH//2)     #

        font = pygame.font.Font(None, 24)
        tt = "ELM"
        self.title1 = font.render(tt, True, self.cl.WHITE)
        tt = "STATS"
        self.title2 = font.render(tt, True, self.cl.WHITE)
        self.st_hp = font.render("HP: 0 / X", True, self.cl.WHITE)
        self.st_pa = font.render("PA: 175 / 190", True, self.cl.WHITE)
        self.st_rezerwa = font.render("Rezerwa: 13 / 30", True, self.cl.WHITE)

        self.rezerwa_bar = Progressbar(self.screen, 210, 300, 180, 40, self.cl.ORANGE, self.cl.WHITE, self.cl.GREEN, 0.5)
        #210, 260
        self.pause_button = Button(self.screen, 10, 110, 124, 40,
                                   unclicked_color=self.cl.BLUE_1,
                                   clicked_color=self.cl.ORANGE,
                                   font_color=self.cl.WHITE,
                                   text="Start")

        self.end_app_button = Button(self.screen, 138, 110, 124, 40,
                                     unclicked_color=self.cl.BLUE_1,
                                     clicked_color=self.cl.BLUE_2,
                                     font_color=self.cl.WHITE,
                                     text="Quit")

        self.ss_button = Button(self.screen, 266, 110, 124, 40,
                                unclicked_color=self.cl.BLUE_1,
                                clicked_color=self.cl.BLUE_2,
                                font_color=self.cl.WHITE,
                                text="SS")

        self.loc_banner = Button(self.screen, 420, 110, 180, 40,
                                 unclicked_color=self.cl.BLUE_1,
                                 clicked_color=self.cl.BLUE_2,
                                 font_color=self.cl.BLACK,
                                 text="LOKACJE")

        self.team_banner = Button(self.screen, self.loc_banner.x_pos + self.loc_banner.x_size + 2,
                                  110, 180, 40,
                                  unclicked_color=self.cl.BLUE_1,
                                  clicked_color=self.cl.BLUE_2,
                                  font_color=self.cl.BLACK,
                                  text="DRUŻYNA")

        empty_ls = [" ", " ", " ", " ", " ", " ", " ", " "]
        # style3 = (cl.BLUE_1, cl.BLUE_2, cl.BLACK)
        self.loc_ls = List(self.screen, self.loc_banner.x_pos, self.loc_banner.y_pos + 2 + self.loc_banner.y_size,
                           self.loc_banner.x_size, self.loc_banner.y_size,
                           self.cl.BLUE_1, self.cl.ORANGE, self.cl.WHITE, empty_ls)
        self.team = List(self.screen, self.team_banner.x_pos, self.team_banner.y_pos + 2 + self.team_banner.y_size,
                         self.team_banner.x_size, self.team_banner.y_size,
                         self.cl.BLUE_1, self.cl.ORANGE, self.cl.WHITE, empty_ls)

        self.restart_loc = Button(self.screen, 10, 160, 60, 60, self.cl.BLUE_1, self.cl.BLUE_2, self.cl.WHITE, "Rl")
        self.restart_team = Button(self.screen, 76, 160, 60, 60, self.cl.BLUE_1, self.cl.BLUE_2, self.cl.WHITE, "Rt")
        self.heal = Button(self.screen, 142, 160, 60, 60, self.cl.BLUE_1, self.cl.BLUE_2, self.cl.WHITE, "heal")
        self.sell = Button(self.screen, 208, 160, 60, 60, self.cl.BLUE_1, self.cl.BLUE_2, self.cl.WHITE, "sell")

        # style4 = (cl.GRAY, cl.GREEN, cl.RED, cl.GRAY)         < = do poprawy
        self.led_run = LED(self.screen, 10, 290,
                           self.cl.GRAY, self.cl.GREEN, self.cl.RED, self.cl.GRAY, text="Stop")
        self.led_shiny = LED(self.screen, 100, 290,
                             self.cl.GRAY, self.cl.GREEN, self.cl.RED, self.cl.GRAY, text="Shiny")
        self.led_elm = LED(self.screen, 215, 475,
                           self.cl.GRAY, self.cl.GREEN, self.cl.RED, self.cl.GRAY, text="available")

        self.new_quest = Button(self.screen, 266, 255, 124, 40,
                                unclicked_color=self.cl.BLUE_1,
                                clicked_color=self.cl.BLUE_2,
                                font_color=self.cl.WHITE,
                                text="New Quest")

        style5 = (self.cl.BLUE_2, self.cl.BLUE_1, self.cl.GRAY, self.cl.ORANGE, self.cl.BLACK)
        self.login = Button(self.screen, 700, 6, 84, 84, self.cl.ORANGE, self.cl.ORANGE, self.cl.BLUE_1, "Login")
        self.input_box1 = TextBar(self.screen, 510, 6, 180, 40, self.cl.BLUE_2, self.cl.BLACK,
                                  self.cl.WHITE, self.cl.ORANGE, self.cl.BLACK, "", "", 18, False)
        self.input_box2 = TextBar(self.screen, 510, 50, 180, 40, self.cl.BLUE_2, self.cl.BLACK,
                                  self.cl.WHITE, self.cl.ORANGE, self.cl.BLACK, "", "", 18, True)

        self.draw()

        self.logging = False
        self.pause = False
        self.close = False
        self.is_p = None

    def recreate_buttons(self, parent_loc_list, parent_poke_list):

        self.loc_ls = List(self.screen, self.loc_banner.x_pos, self.loc_banner.y_pos + 2 + self.loc_banner.y_size,
                           self.loc_banner.x_size, self.loc_banner.y_size,
                           self.cl.BLUE_1, self.cl.ORANGE, self.cl.WHITE, parent_loc_list)
        self.team = List(self.screen, self.team_banner.x_pos, self.team_banner.y_pos + 2 + self.team_banner.y_size,
                         self.team_banner.x_size, self.team_banner.y_size,
                         self.cl.BLUE_1, self.cl.ORANGE, self.cl.WHITE, parent_poke_list)

        self.loc_ls.draw()
        self.team.draw()
        pygame.display.update()

    def generate_stats(self, hp, pa, rezerwa, progress, ev_now, ev_loc):
        font = pygame.font.Font(None, 30)
        self.st_hp = font.render("HP: " + hp, True, self.cl.WHITE)
        self.st_pa = font.render("PA: " + pa, True, self.cl.WHITE)
        self.st_rezerwa = font.render("Rezerwa: " + rezerwa, True, self.cl.WHITE)

        self.screen.blit(self.st_hp, (210, 260))
        self.screen.blit(self.st_pa, (210, 260))
        self.screen.blit(self.st_rezerwa, (210, 260))
        # 2x
        #
        #   # 1. rysujesz kwadrat resetujący
        #   # 2. tworzysz kolejne stringi i zapisujesz
        #

        # 3. obsługujesz progressbar
        pass

    def led_handle(self, o1, o2, o3):
        if o1:
            self.led_run.turn()
        if o2:
            self.led_shiny.turn()
        if o3:
            self.led_elm.turn()
    # w f uruchamiającej o1..3 muszą zostać po tym przyrównane znowu do False

    def draw(self):
        self.screen.fill(self.cl.YELLOW)
        pygame.draw.rect(self.screen, self.cl.BLUE_3, self.rectangle1)
        pygame.draw.rect(self.screen, self.cl.BLUE_4, self.rectangle2)
        pygame.draw.rect(self.screen, self.cl.GRAY, self.line1)
        pygame.draw.rect(self.screen, self.cl.GRAY, self.line2)
        pygame.draw.rect(self.screen, self.cl.GRAY, self.line3)

        self.screen.blit(self.title2, (10, 260))
        self.screen.blit(self.title1, (210, 260))

        self.pause_button.draw()
        self.end_app_button.draw()
        self.ss_button.draw()
        self.sell.draw()
        self.restart_loc.draw()
        self.restart_team.draw()

        self.loc_banner.draw()
        self.team_banner.draw()

        self.loc_ls.draw()
        self.team.draw()
        self.heal.draw()

        self.login.draw()
        self.input_box1.draw()
        self.input_box2.draw()

        self.led_run.draw()
        self.led_shiny.draw()
        self.led_elm.draw()
        self.new_quest.draw()

        self.rezerwa_bar.draw()

        self.screen.blit(self.logo_img, (0, 0))

        pygame.display.update()

    def login_interaction(self):
        self.input_box1.draw()
        self.input_box2.draw()
        working = True
        while working:
            for event in pygame.event.get():
                if event.type == pygame.QUIT or event.type == pygame.K_ESCAPE:
                    working = False
                    pygame.quit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos()
                    print(pos)
                    if self.input_box1.is_interaction(pos):
                        self.input_box1.click()
                    else:
                        self.input_box1.clicked = False
                    if self.input_box2.is_interaction(pos):
                        self.input_box2.click()
                    else:
                        self.input_box2.clicked = False

                    if self.end_app_button.is_interaction(pos):
                        pygame.quit()
                        self.close = True
                    if self.login.is_interaction(pos):
                        working = False
                if event.type == pygame.KEYDOWN:
                    if self.input_box1.clicked:
                        self.input_box1.text_event(event)
                    elif self.input_box2.clicked:
                        self.input_box2.text_event(event)

                self.input_box1.draw()
                self.input_box2.draw()
                pygame.display.update()

    #
    def keyboard_interaction(self):
        self.draw()
        for event in pygame.event.get():
            if event.type == pygame.QUIT or event.type == pygame.K_ESCAPE:
                pygame.quit()
                self.close = True

            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                if self.pause_button.is_interaction(pos):
                    if self.pause:
                        self.start()
                    elif not self.pause:
                        self.stop()
                    self.draw()
                if self.pause:
                    if self.loc_ls.is_interaction(pos):
                        self.draw()
                    if self.team.is_interaction(pos):
                        self.draw()

                if self.restart_team.is_interaction(pos):
                    self.is_p = "team"
                if self.restart_loc.is_interaction(pos):
                    self.is_p = "loc"
                if self.heal.is_interaction(pos):
                    self.is_p = "heal"
                if self.sell.is_interaction(pos):
                    self.is_p = "sell"

                if self.end_app_button.is_interaction(pos):
                    pygame.quit()
                    self.close = True

    def start(self):
        self.pause = False

        self.led_run.turn()
        self.led_run.draw()

        self.pause_button.color = self.pause_button.clicked_color
        self.pause_button.text = "Stop"
        self.pause_button.draw()

        pygame.display.update()

    def stop(self):
        self.pause = True

        self.led_run.turn()
        self.led_run.draw()

        self.pause_button.color = self.pause_button.unclicked_color
        self.pause_button.text = "Start"
        self.pause_button.draw()

        pygame.display.update()

    def user_reaction(self):
        print("Czekam na użytkownika.")
        self.stop()
        self.draw()     #

    def catching(self):
        return self.close

    def is_pressed(self):
        return self.is_p    #

    def return_inputs(self):
        return self.input_box1.return_text(), self.input_box2.return_text()


if __name__ == '__main__':
    g = GUI()
    g.keyboard_interaction()
    exit(0)
