# BUTTONCLASS

import pygame

FONT = "comicsansms"        # !!! wo wyjebania

"""
class            Button:
    def __init__(self, parent_screen, x_pos, y_pos, x_size, y_size, unclicked_color,
                 clicked_color, font_color, text=None):

class            List:
    def __init__(self, parent_screen, x_pos, y_pos, x_size, y_size,
                 unclicked_color, clicked_color, ls, font_color=FONT):

class            LED:
    def __init__(self, parent_screen, x_pos, y_pos, font_color,
                green, red, gray, text=None):
   
class            TextBar:
    def __init__(self, parent_screen, x_pos, y_pos, x_size, y_size, color_unclicked, 
                 color_clicked, color_background, color_error, font_color, 
                 text='', title="", longest=13, censored=False):
"""


# przycisk
class Button:
    def __init__(self, parent_screen, x_pos, y_pos, x_size, y_size, unclicked_color,
                 clicked_color, font_color=None, text=None):
        self.screen = parent_screen
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.x_size = x_size
        self.y_size = y_size
        self.text = text

        self.font_color = font_color
        self.unclicked_color = unclicked_color
        self.clicked_color = clicked_color

        self.color = self.unclicked_color

        font = pygame.font.Font(None, 24)
        self.txt = font.render(self.text, True, self.font_color)

    def draw(self):
        pygame.draw.rect(self.screen, self.color, [self.x_pos, self.y_pos, self.x_size, self.y_size])
        if self.text is not None:
            text_rect = self.txt.get_rect(center=(self.x_pos + self.x_size // 2, self.y_pos + self.y_size // 2))
            self.screen.blit(self.txt, text_rect)

    def is_interaction(self, mouse_pos):
        if mouse_pos[0] in range(self.x_pos, self.x_pos + self.x_size + 1):
            if mouse_pos[1] in range(self.y_pos, self.y_pos + self.y_size + 1):
                return True
        return False


# lista
class List:
    def __init__(self, parent_screen, x_pos, y_pos, x_size, y_size, unclicked_color, clicked_color, font_color, ls):
        self.screen = parent_screen

        self.font_color = font_color
        self.unclicked_color = unclicked_color
        self.clicked_color = clicked_color
        self.color = self.unclicked_color

        self.ls = ls
        self.bl = []
        self.clicked = False

        k = 0
        for i in ls:
            self.bl.append(Button(parent_screen, x_pos, y_pos + (y_size + 2) * k,
                                  x_size, y_size, unclicked_color, clicked_color,  font_color, i))
            k += 1
        self.bl[0].color = self.clicked_color

    def draw(self):
        for i in self.bl:
            i.draw()

    def is_interaction(self, mouse_pos):
        for i in self.bl:
            if i.is_interaction(mouse_pos):
                self.is_picked(i)
                return True
        return False

    def is_picked(self, i):
        i.color = self.clicked_color
        for p in self.bl:
            if p != i:
                p.color = self.unclicked_color

    def return_now_picked_loc(self):
        for i in self.bl:
            if i.color == self.clicked_color:         # ???
                return i.text


# led
class LED:
    def __init__(self, parent_screen, x_pos, y_pos, font_color, green, red, gray, text=None):
        self.screen = parent_screen
        self.x_pos = x_pos
        self.y_pos = y_pos

        self.green = green
        self.red = red
        self.gray = gray

        self.text = text
        self.font_size = 16
        self.font_color = font_color
        self.light = False

        self.radius = 8

    def draw(self):
        pygame.draw.circle(self.screen, self.gray, (self.x_pos, self.y_pos), self.radius)
        if self.light:
            pygame.draw.circle(self.screen, self.green, (self.x_pos, self.y_pos), self.radius - 3)
        else:
            pygame.draw.circle(self.screen, self.red, (self.x_pos, self.y_pos), self.radius - 3)

        if self.text is not None:
            font = pygame.font.SysFont(FONT, self.font_size)
            txt = font.render(self.text, True, self.font_color)
            self.screen.blit(txt, (self.x_pos + self.radius + 2, self.y_pos - 2 * self.radius + 3))

    def turn(self):
        if self.light:
            self.light = False
        else:
            self.light = True


# textbar
class TextBar:
    def __init__(self, parent_screen, x_pos, y_pos, x_size, y_size, color_unclicked, color_clicked, color_background,
                 color_error, font_color=(0,0,0), text='', title="", longest=13, censored=False):
        self.screen = parent_screen

        self.x_pos = x_pos
        self.y_pos = y_pos
        self.x_size = x_size
        self.y_size = y_size

        self.rect = pygame.Rect(x_pos, y_pos, x_size, y_size)

        self.color_unclicked = color_unclicked
        self.color_clicked = color_clicked
        self.color_background = color_background
        self.color_error = color_error
        self.font_color = font_color
        self.color = self.color_unclicked

        self.max_length = longest
        self.text = text
        self.title = title
        self.clicked = False

        self.censored = censored
        if censored:
            self.censored_text = ""
        self.ft = pygame.font.Font(None, 24)

        self.txt_surface = self.ft.render(self.text, True, self.font_color)
        self.title_surface = self.ft.render(self.title, True, self.font_color)

    def text_event(self, event):
        if self.clicked:
            if event.key == pygame.K_RETURN:
                self.clicked = not self.clicked
            elif event.key == pygame.K_BACKSPACE:
                self.text = self.text[:-1]
                if self.censored:
                    self.censored_text = self.censored_text[:-1]
                if len(self.text) < self.max_length:
                    self.color_clicked = self.color_clicked
                if not self.censored:
                    self.txt_surface = self.ft.render(self.text, True, self.color_clicked)
                else:
                    self.txt_surface = self.ft.render(self.censored_text, True, self.color_clicked)
                self.draw()
                pygame.display.update()
            else:
                if len(self.text) < self.max_length:
                    self.color_clicked = self.color_clicked
                    self.text += event.unicode
                    if not self.censored:
                        self.txt_surface = self.ft.render(self.text, True, self.color_clicked)
                    else:
                        self.censored_text += "*"
                        self.txt_surface = self.ft.render(self.censored_text, True, self.color_clicked)
                else:
                    print("ERROR - za długi string")
                    self.color_clicked = self.color_error
                self.draw()

    def click(self):
        if self.clicked:
            self.clicked = False
        else:
            self.clicked = True

    def draw(self):
        pygame.draw.rect(self.screen, self.color_background, [self.x_pos, self.y_pos, self.x_size, self.y_size])
        self.screen.blit(self.title_surface, (self.x_pos, self.y_pos - 14))
        if self.clicked:
            pygame.draw.rect(self.screen, self.color_clicked, self.rect, 2)
            self.screen.blit(self.txt_surface, (self.rect.x + 5, self.rect.y + 5))
        else:
            pygame.draw.rect(self.screen, self.color_unclicked, self.rect, 2)
            self.screen.blit(self.txt_surface, (self.rect.x + 5, self.rect.y + 5))

    def is_interaction(self, mouse_pos):
        if mouse_pos[0] in range(self.x_pos, self.x_pos + self.x_size + 1):
            if mouse_pos[1] in range(self.y_pos, self.y_pos + self.y_size + 1):
                return True
        return False

    def return_text(self):
        return self.text


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
        pygame.draw.rect(self.screen, (255, 255, 255),
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
