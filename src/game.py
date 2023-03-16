import pygame

from const import *
from board import Board
from dragger import Dragger


class Game:

    def __init__(self):
        
        self.next_player = "white"
        self.hovered_sqr = None
        self.board = Board()
        self.dragger = Dragger()

    
    # blit methods


    def show_bg(self, surface):
        
        for row in range(ROWS):
            for col in range(COLS):

                if (row + col) % 2 == 0:
                    colour = (140,140,140)          #Light square
                else:
                    # colour = (66,104,124)           #Dark sqaure
                    colour = (0, 80, 100)


                rectangle = (col * SQSIZE, row * SQSIZE, SQSIZE, SQSIZE)


                pygame.draw.rect(surface, colour, rectangle)

    
    def show_pieces(self, surface):
        
        for row in range(ROWS):
            for col in range(COLS):

                #check for piece on specific square
                if self.board.squares[row][col].has_piece():
                    piece = self.board.squares[row][col].piece


                    #all pieces except dragger piece
                    if piece is not self.dragger.piece:
                        
                        piece.set_texture(size=80)
                        img = pygame.image.load(piece.texture)
                        img_center = col * SQSIZE + SQSIZE // 2, row * SQSIZE + SQSIZE // 2
                        piece.texture_rect = img.get_rect(center=img_center)

                        surface.blit(img, piece.texture_rect)


    def show_moves(self, surface):
        
        if self.dragger.dragging:
            piece = self.dragger.piece

            # loop all valid moves
            for move in piece.moves:
                # colour
                colour = "#C86464" if (move.final.row + move.final.col) % 2 == 0 else "#C84646" 
                # rect
                rect = (move.final.col * SQSIZE, move.final.row * SQSIZE, SQSIZE, SQSIZE)
                # blit
                pygame.draw.rect(surface, colour, rect)


    def show_last_move(self, surface):

        if self.board.last_move:

            initial = self.board.last_move.initial
            final = self.board.last_move.final

            for pos in [initial, final]:

                # colour
                colour = (244, 247, 116) if (pos.row + pos.col) % 2 == 0 else (172, 195, 51)
                # rect
                rect = (pos.col * SQSIZE, pos.row * SQSIZE, SQSIZE, SQSIZE)
                # blit
                pygame.draw.rect(surface, colour, rect)


    def show_hover(self, surface):
        
        if self.hovered_sqr:

            # colour
            colour = (200, 200, 200)
            # rect
            rect = (self.hovered_sqr.col * SQSIZE, self.hovered_sqr.row * SQSIZE, SQSIZE, SQSIZE)
            # blit
            pygame.draw.rect(surface, colour, rect, width = 3)


    # other methods

    def next_turn(self):

        self.next_player = "white" if self.next_player == "black" else "black"


    def set_hover(self, row, col):

        self.hovered_sqr = self.board.squares[row][col]