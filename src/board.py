from const import *
from piece import *
from square import Square
from move import Move

class Board:

    def __init__(self):

        self.squares = [[0,0,0,0,0,0,0,0] for col in range(COLS)]
        
        self.last_move = None
        self._create()
        self._add_pieces("white")
        self._add_pieces("black")

    def move(self, piece, move):
        
        initial = move.initial
        final = move.final

        # console board move update
        self.squares[initial.row][initial.col].piece = None             #where the piece is prior to the move
        self.squares[final.row][final.col].piece = piece                #where the piece ends up after move

        # pawn promotion
        if isinstance(piece, Pawn):
            self.check_promotion(piece, final)

        # king castling
        if isinstance(piece, King):
            if self.castling(initial, final):
                
                # recursion : checking if the King actually moved 2 sqaures
                # checking if the king castling was wueen side or king side
                # calling move() with the new rook from the if statement and sending the last rook move in calc_moves().king_moves()
                diff = final.col - initial.col
                rook = piece.left_rook if (diff < 0) else piece.right_rook
                self.move(rook, rook.moves[-1])

        # move
        piece.moved = True

        # clear valid moves
        piece.clear_moves()

        # set last move
        self.last_move = move


    def valid_move(self, piece, move):
        return move in piece.moves


    def check_promotion(self, piece, final):

        if final.row == 0 or final.row == 7:
            self.squares[final.row][final.col].piece = Queen(piece.colour)


    def castling(self, intial, final):
        
        return abs(intial.col - final.col) == 2


    def calc_moves(self, piece, row, col):
        '''
            Calcualte all the possible valid moves of a specific piece from specific position
        '''

        def pawn_moves():
            
            # steps
            steps = 1 if piece.moved else 2

            # vertical moves
            start = row + piece.dir
            end = row + (piece.dir * (1 + steps))
            for possible_move_row in range(start, end, piece.dir):
                
                if Square.in_range(possible_move_row):
                    if self.squares[possible_move_row][col].is_empty():
                        # create initial and final move squares
                        initial = Square(row, col)
                        final = Square(possible_move_row, col)
                        # create a new move
                        move = Move(initial, final)
                        piece.add_move(move)

                    # blocked
                    else: break
                # not in range
                else: break

            # diagonal moves
            move_row = row + piece.dir
            possible_move_cols = [col-1, col +1]

            for possible_move_col in possible_move_cols:
                if Square.in_range(possible_move_row, possible_move_col):
                    if self.squares[possible_move_row][possible_move_col].has_rival_piece(piece.colour):
                        # create initial and final move squares
                        initial = Square(row,col)
                        final = Square(possible_move_row, possible_move_col)
                        # create a new move
                        move = Move(initial, final)
                        # append new move
                        piece.add_move(move)

        def knight_moves():
            
            # 8 possible moves
            possible_moves = [
                (row-2, col+1),
                (row-1, col+2),
                (row+1, col+2),
                (row+2, col+1),
                (row+2, col-1),
                (row+1, col-2),
                (row-1, col-2),
                (row-2, col-1),
            ]

            for possible_move in possible_moves:
                possible_move_row, possible_move_col = possible_move

                if Square.in_range(possible_move_row, possible_move_col):
                    
                    if self.squares[possible_move_row][possible_move_col].isempty_or_rival(piece.colour):
                        # craete squares of the new move
                        initial = Square(row, col)
                        final = Square(possible_move_row, possible_move_col)

                        # create new move
                        move = Move(initial, final)
                        
                        # append new valid move
                        piece.add_move(move)

        def straightline_moves(incrs):
            
            for incr in incrs:
                row_incr, col_incr = incr
                possible_move_row = row + row_incr
                possible_move_col = col + col_incr

                while True:
                    if Square.in_range(possible_move_row, possible_move_col):

                        # create squares of a possible new move
                        initial = Square(row, col)
                        final = Square(possible_move_row, possible_move_col)
                        # create a possible new move
                        move = Move(initial, final)

                        # empty
                        if self.squares[possible_move_row][possible_move_col].is_empty():
                            # append new move
                            piece.add_move(move)

                        # has rival piece = add + break
                        if self.squares[possible_move_row][possible_move_col].has_rival_piece(piece.colour):
                            # append new move
                            piece.add_move(move)
                            break

                        # has team piece = break
                        if self.squares[possible_move_row][possible_move_col].has_team_piece(piece.colour):
                            # append new move
                            break


                    # not in range
                    else: break

                    # incrementing squares
                    possible_move_row = possible_move_row + row_incr
                    possible_move_col = possible_move_col + col_incr

        def king_moves():
            
            adjs = [
                (row-1, col+0),     #up
                (row-1, col+1),     #up right
                (row+0, col+1),     #right
                (row+1, col+1),     #dowm right
                (row+1, col+0),     #down
                (row+1, col-1),     #down left
                (row+0, col-1),     #left
                (row-1, col-1),     #up left
            ]

            for possible_move in adjs:
                possible_move_row, possible_move_col = possible_move

                if Square.in_range(possible_move_row, possible_move_col):

                    if self.squares[possible_move_row][possible_move_col].isempty_or_rival(piece.colour):
                        # create squares of new move
                        initial = Square(row, col)
                        final = Square(possible_move_row, possible_move_col)    #piece - piece

                        # create new move
                        move = Move(initial, final)

                        # append new valid move
                        piece.add_move(move)

            # castling moves
            if not piece.moved:

                # queen castling
                left_rook = self.squares[row][0].piece
                if isinstance(left_rook, Rook):
                    if not left_rook.moved:
                        for c in range(1,4):
                            # castling is not opssible because there are pieces in the way
                            if self.squares[row][c].has_piece():
                                break

                            if c == 3:
                                # adds left rook to King
                                piece.left_rook = left_rook

                                # rook move
                                initial = Square(row, 0)
                                final = Square(row, 3)
                                move = Move(initial, final)
                                left_rook.add_move(move)

                                # king move
                                initial = Square(row, col)
                                final = Square(row, 2)
                                move = Move(initial, final)
                                piece.add_move(move)

                # king castling
                right_rook = self.squares[row][7].piece
                if isinstance(right_rook, Rook):
                    if not right_rook.moved:
                        for c in range(5, 7):
                            # castling is not opssible because there are pieces in the way
                            if self.squares[row][c].has_piece():
                                break

                            if c == 6:
                                # adds right rook to King
                                piece.right_rook = right_rook

                                # rook move
                                initial = Square(row, 7)
                                final = Square(row, 5)
                                move = Move(initial, final)
                                right_rook.add_move(move)

                                # king move
                                initial = Square(row, col)
                                final = Square(row, 6)
                                move = Move(initial, final)
                                piece.add_move(move)


        if isinstance(piece, Pawn): 
            pawn_moves()

        elif isinstance(piece, Knight): 
            knight_moves()

        elif isinstance(piece, Bishop): 
            straightline_moves([
                (-1, +1),   #upper right
                (-1, -1),   #upper left
                (1,1),      #down right
                (1, -1)     #down left
            ])

        elif isinstance(piece, Rook): 
            straightline_moves([
                (-1,0),     #up
                (0,1),      #right
                (1,0),      #down
                (0,-1)      #left
            ])

        elif isinstance(piece, Queen): 
            straightline_moves([
                (-1, +1),   #upper right
                (-1, -1),   #upper left
                (1,1),      #down right
                (1, -1),     #down left
                (-1,0),     #up
                (0,1),      #right
                (1,0),      #down
                (0,-1)      #left
            ])

        elif isinstance(piece, King): 
            king_moves()


    def _create(self):
        
        for row in range(ROWS):
            for col in range(COLS):
                self.squares[row][col] = Square(row, col)                               #For every 0 (which represents a square on the board) a new Square object is assigned to it


    def _add_pieces(self,colour):

        row_pawn, row_other = (6,7) if colour == "white" else (1,0)
        

        #creating all pawns
        for col in range(COLS):
            self.squares[row_pawn][col] = Square(row_pawn, col, Pawn(colour))
            # self.squares[5][1] = Square(5, 1, Pawn(colour))


        #crating all knights
        self.squares[row_other][1] = Square(row_other, 1, Knight(colour))
        self.squares[row_other][6] = Square(row_other, 6, Knight(colour))
        # self.squares[3][3] = Square(3, 3, Knight(colour))

        #creating bishops
        self.squares[row_other][2] = Square(row_other, 2, Bishop(colour))
        self.squares[row_other][5] = Square(row_other, 5, Bishop(colour))
        # self.squares[4][3] = Square(4, 3, Bishop(colour))

        #creating rooks
        self.squares[row_other][0] = Square(row_other, 0, Rook(colour))
        self.squares[row_other][7] = Square(row_other, 7, Rook(colour))
        # self.squares[4][4] = Square(4, 4, Rook(colour))

        #creating queen
        self.squares[row_other][3] = Square(row_other, 3, Queen(colour))
        # self.squares[4][4] = Square(4, 4, Queen(colour))

        #creating king
        self.squares[row_other][4] = Square(row_other, 4, King(colour))
        # self.squares[2][2] = Square(2, 2, King(colour))