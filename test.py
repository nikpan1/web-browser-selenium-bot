# TEST
import time

import pygame
from Colors import Colors

pygame.init()
screen = pygame.display.set_mode((640, 480))
RED = pygame.Color('lightskyblue3')
BLUE = pygame.Color('dodgerblue2')
YELLOW = (222, 100, 0)


class Progressbar:
    def __init__(self, parent_screen, x_pos, y_pos, x_size, y_size, progress_color, layout_color, end_color, percent=0):
        self.screen = parent_screen
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.x_size = x_size
        self.y_size = y_size

        self.progress_color = progress_color
        self.layout_color = layout_color
        self.end_color = end_color
        self.percent = percent

        self.font = pygame.font.Font(None, 24)
        #

    def render_text(self):
        data = int(self.percent * 100)
        text = str(data) + "%"
        return text

    def draw(self):                     # do poprawy
        pygame.draw.rect(self.screen, (0, 0, 0),
                         [self.x_pos, self.y_pos, self.x_size, self.y_size])
        pygame.draw.rect(self.screen, self.layout_color,
                         [self.x_pos + 1, self.y_pos + 1, self.x_size - 2, self.y_size - 2])

        # progress
        pygame.draw.rect(self.screen, self.progress_color, [self.x_pos + 2, self.y_pos + 2,
                                                            (self.x_size - 3) * self.percent,
                                                            (self.y_size - 3)])

        if self.percent > 0.98:
            pygame.draw.rect(self.screen, self.end_color,
                             [self.x_pos + 1, self.y_pos + 1, self.x_size - 2, self.y_size - 2])

        # text %
        txt = self.font.render(self.render_text(), True, (0, 0, 0))
        text_rect = txt.get_rect(center=(self.x_pos + self.x_size // 2, self.y_pos + self.y_size // 2))
        self.screen.blit(txt, text_rect)

    def change_percent(self, new_pr):
        # sus
        if new_pr > 1:
            return False

        self.percent = new_pr


def main():

    clock = pygame.time.Clock()
    cl = Colors()
    pbar = Progressbar(screen, 20, 20, 150, 30, cl.ORANGE, cl.GRAY, cl.GREEN, 0)
    procent = 0.1
    while True:
        if procent == 1:
            time.sleep(1)
            break

        procent = procent + 0.1
        pbar.change_percent(procent)
        pbar.draw()
        pygame.display.update()

        clock.tick(3)


"""pygame.init()
screen = pygame.display.set_mode((640, 480))
RED = pygame.Color('lightskyblue3')
BLUE = pygame.Color('dodgerblue2')
YELLOW = (222, 100, 0)


def main():
    clock = pygame.time.Clock()
    input_box1 = TextBar(screen, 100, 60, 140, 32, "", "LOGIN", 12, False)
    input_box2 = TextBar(screen, 100, 110, 140, 32,"", "Haslo", 12, True)

    ld = LED(screen, 300, 300, "text")
    # def __init__(self, parent_screen, x_pos, y_pos, text=None):
    done = False

    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                if input_box1.is_interaction(pos):
                    input_box1.click()
                else:
                    input_box1.clicked = False
                if input_box2.is_interaction(pos):
                    input_box2.click()
                else:
                    input_box2.clicked = False

            if event.type == pygame.KEYDOWN:
                if input_box1.clicked:
                    input_box1.text_event(event)
                elif input_box2.clicked:
                    input_box2.text_event(event)
                if event.key == pygame.K_KP_ENTER:
                    break

        input_box1.draw()
        input_box2.draw()
        ld.draw()

        pygame.display.flip()
        clock.tick(30)
"""

if __name__ == '__main__':
    main()
    pygame.quit()
