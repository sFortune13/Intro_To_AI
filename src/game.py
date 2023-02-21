import pygame

from const import *

class Game:

    def __init__(self):
        pass

    
    # Show methods


    def show_bg(self, surface):
        
        for row in range(ROWS):
            for col in range(COLS):

                if (row + col) % 2 == 0:
                    colour = (169,169,169)          #Light square
                else:
                    colour = (66,104,124)           #Dark sqaure


                rectangle = (col * SQSIZE, row * SQSIZE, SQSIZE, SQSIZE)


                pygame.draw.rect(surface, colour, rectangle)