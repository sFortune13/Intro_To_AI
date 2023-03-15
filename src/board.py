from const import *
from square import Square
from piece import *

class Board:

    def __init__(self):

        self.squares = [[0,0,0,0,0,0,0,0] for col in range(COLS)]
        
        self._create()
        self._add_pieces("white")
        self._add_pieces("black")


    def _create(self):
        
        for row in range(ROWS):
            for col in range(COLS):
                self.squares[row][col] = Square(row, col)                               #For every 0 (which represents a square on the board) a new Square object is assigned to it



    def _add_pieces(self,colour):

        row_pawn, row_other = (6,7) if colour == "white" else (1,0)
        

        #creating all pawns
        for col in range(COLS):
            self.squares[row_pawn][col] = Square(row_pawn, col, Pawn(colour))


        #crating all knights
        self.squares[row_other][1] = Square(row_other, 1, Knight(colour))
        self.squares[row_other][6] = Square(row_other, 6, Knight(colour))

        #creating bishops
        self.squares[row_other][2] = Square(row_other, 2, Bishop(colour))
        self.squares[row_other][5] = Square(row_other, 5, Bishop(colour))

        #creating rooks
        self.squares[row_other][0] = Square(row_other, 0, Rook(colour))
        self.squares[row_other][7] = Square(row_other, 7, Rook(colour))

        #creating queen
        self.squares[row_other][3] = Square(row_other, 3, Queen(colour))

        #creating king
        self.squares[row_other][4] = Square(row_other, 4, King(colour))