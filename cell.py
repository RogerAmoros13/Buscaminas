import pygame
from settings import *

class Cell:
    def __init__(self, position, size, bomb=False):
        pygame.font.init()
        self.font = pygame.font.SysFont("Comic Sans MS", size)
        self.invisible = True
        self.bomb = bomb
        self.disabled = False
        offset = int(0.1 * size)
        self.adjacent_bombs = 0
        self.flaged = False

        position1, position2 = position[0] * size, position[1] * size
        self.coordinates = (position1, position2, size, size)
        self.coordinates2 = (position1+offset, position2+offset, size-offset, size-offset)
        self.coordinates3 = (position1+offset, position2+offset, size-2 * offset, size-2 * offset)

        self.color = (0, 0, 0)
        self.position = (position1, position2)
        self.screen = pygame.display.get_surface()
        self.size = size

    def get_color(self):
        if self.adjacent_bombs:
            if self.adjacent_bombs == 1:
                self.color = BOMB_1
            elif self.adjacent_bombs == 2:
                self.color = BOMB_2
            elif self.adjacent_bombs == 3:
                self.color = BOMB_3
            else:
                self.color = BOMB_4

    def draw(self):
        if self.invisible:
            pygame.draw.rect(self.screen, GREY1, self.coordinates) 
            pygame.draw.rect(self.screen, GREY2, self.coordinates2)
            pygame.draw.rect(self.screen, GREY3, self.coordinates3)
            if self.flaged:
                pygame.draw.rect(
                        self.screen, 
                        RED,
                        (
                            self.position[0] + self.size * 0.2, 
                            self.position[1] + self.size * 0.2, 
                            self.size * 0.5,
                            self.size * 0.3
                        )
                    )
                pygame.draw.line(
                        self.screen,
                        BLACK,
                        (
                            self.position[0] + self.size * 0.7,
                            self.position[1] + self.size * 0.2,
                            ),
                        (
                            self.position[0] + self.size * 0.7,
                            self.position[1] + self.size * 0.8
                            )
                        )

        else:
            if self.bomb:
                if self.disabled:
                    color = GREEN
                else: 
                    color = RED
                pygame.draw.rect(self.screen, color, self.coordinates)
                pygame.draw.circle(
                        self.screen, 
                        BLACK, 
                        (
                            self.position[0] + self.size / 2, 
                            self.position[1] + self.size / 2
                        ),
                        (0.8 * self.size) / 2
                    )
            else:
                if self.adjacent_bombs:
                    self.screen.blit(
                        self.font.render(
                            str(self.adjacent_bombs), 
                            False, 
                            self.color 
                        ), 
                        (
                            self.position[0]+self.size//3, 
                            self.position[1]+self.size//4
                        ) 
                    )







