import pygame
from data.classes.Square import Square
from data.classes.Rook import Rook
from data.classes.Bishop import Bishop
from data.classes.Knight import Knight
from data.classes.Queen import Queen
from data.classes.King import King
from data.classes.Pawn import Pawn

class Board:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.tile_width = width // 8
        self.tile_height = height // 8
        self.selected_piece = None
        self.turn = 'white'
        self.config = [
            ['bR', 'bN', 'bB', 'bQ', 'bK', 'bB', 'bN', 'bR'],
            ['bP', 'bP', 'bP', 'bP', 'bP', 'bP', 'bP', 'bP'],
            ['','','','','','','',''],
            ['','','','','','','',''],
            ['','','','','','','',''],
            ['','','','','','','',''],
            ['wP', 'wP', 'wP', 'wP', 'wP', 'wP', 'wP', 'wP'],
            ['wR', 'wN', 'wB', 'wQ', 'wK', 'wB', 'wN', 'wR'],
        ]
        self.squares = self.generate_squares()
        self.setup_board()

    def generate_squares(self):
        output = []
        for y in range(8):
            for x in range(8):
                output.append(
                    Square(x,  y, self.tile_width, self.tile_height)
                )
        return output
    
    def get_square_from_pos(self, pos):
        for square in self.squares:
            if (square.x, square.y) == (pos[0], pos[1]):
                return square

    def get_piece_from_pos(self, pos):
        return self.get_square_from_pos(pos).occupying_piece

    def setup_board(self):
        for y, row in enumerate(self.config):
            for x, piece in enumerate(row):
                if piece != '':
                    square = self.get_square_from_pos((x, y))
                    # Pls fix this wrong color spawning. FIXED!!!
                    if piece[1] == 'R':
                        square.occupying_piece = Rook(
                            (x, y), 'white' if piece[0] == 'w' else 'black', self
                        )
                    elif piece[1] == 'N':
                        square.occupying_piece = Knight(
                            (x, y), 'white' if piece[0] == 'w' else 'black', self
                        )
                    elif piece[1] == 'B':
                        square.occupying_piece = Bishop(
                            (x, y), 'white' if piece[0] == 'w' else 'black', self
                        )
                    elif piece[1] == 'Q':
                        square.occupying_piece = Queen(
                            (x, y), 'white' if piece[0] == 'w' else 'black', self
                        )
                    elif piece[1] == 'K':
                        square.occupying_piece = King(
                            (x, y), 'white' if piece[0] == 'w' else 'black', self
                        )
                    elif piece[1] == 'P':
                        square.occupying_piece = Pawn(
                            (x, y), 'white' if piece[0] == 'w' else 'black', self
                        )
    def handle_click(self, mx, my):
        x = mx // self.tile_width
        y = my // self.tile_height
        clicked_square = self.get_square_from_pos((x, y))
        if self.selected_piece is None:
            if clicked_square.occupying_piece is not None:
                if clicked_square.occupying_piece.colour == self.turn:
                    self.selected_piece = clicked_square.occupying_piece
        elif self.selected_piece.move(self, clicked_square):
            self.turn = 'white' if self.turn == 'black' else 'black'
        elif clicked_square.occupying_piece is not None:
            if clicked_square.occupying_piece.colour == self.turn:
                self.selected_piece = clicked_square.occupying_piece
                
    def is_in_check(self, colour, board_change=None): # !!!! remember: board_change = [(x1, y1), (x2, y2)]
        output = False
        king_pos = None
        changing_piece = None
        king = None
        old_square = None
        new_square = None
        new_square_old_piece = None
        if board_change is not None:
            for square in self.squares:
                if square.pos == board_change[0]:
                    changing_piece = square.occupying_piece
                    old_square = square
                    old_square.occupying_piece = None
            for square in self.squares:
                if square.pos == board_change[1]:
                    new_square = square
                    new_square_old_piece = new_square.occupying_piece
                    new_square.occupying_piece = changing_piece
        pieces = [i.occupying_piece for i in self.squares if i.occupying_piece is not None]
        if changing_piece is not None:
            if changing_piece.notation == 'K':
                king_pos = new_square.pos
                king = changing_piece

        if king_pos == None:
            for piece in pieces:
                if piece.notation == 'K' and piece.colour == colour:
                        king_pos = piece.pos
                        king = piece

        for piece in pieces:
            if piece.colour != colour:
                for square in piece.attacking_squares(self):
                    if square.pos == king_pos:
                        output = True 
                        king.incheck = True
                        king.cant_castle = True
                        #print("CHECK!")

        if board_change is not None:
            old_square.occupying_piece = changing_piece
            new_square.occupying_piece = new_square_old_piece
        return output
    
    def is_in_checkmate(self, colour):
        output = ''
        mate = False
        mypiece = None
        mydefpiece = None
        opppiece_pos = None
        pieces = [
            i.occupying_piece for i in self.squares if i.occupying_piece is not None
        ]
        #pls fix incorrect checkmate where a piece can defend but program doesn't forsee it. FIXED!!!
        #pls fix no mate trigger after a single call of failed mate attempt. FIXED!!!
        if self.is_in_check(colour):
            for piece in pieces:
                if piece.notation == 'K' and piece.colour == colour:
                    king = piece
                    king_pos = piece.pos

               
            for piece in pieces:
                if piece.colour != colour:
                    for square in piece.attacking_squares(self):
                        if square.pos == king_pos:
                            opppiece_pos = piece.pos

            for piece in pieces:
                if piece.colour == colour:
                    for square in piece.attacking_squares(self):
                        if square.pos == opppiece_pos:
                            mypiece = piece
                            mate = False
                            # print("ITS NOT MATE!")
                        elif piece.get_valid_moves(self) != []:
                            mydefpiece = piece
                            mate  = False
                        elif piece.get_valid_moves(self) == []:
                            mate = True
                            #print("No possible moves")
            
            if mypiece != None:
                if mypiece.get_valid_moves(self) != []:
                    mate = False
            if mydefpiece != None:
                if mydefpiece.get_valid_moves(self) != []:
                    mate = False
            if king.get_valid_moves(self) == []:
                if mate == True:
                    output = 'mate'
        else:
            i = 0
            clrpiece = []
            for piece in pieces:
                if piece.colour == colour:
                    clrpiece.append(piece)
                    if piece.get_valid_moves(self) == []:
                        i += 1
            if i == len(clrpiece):
                output = 'stalemate'
        
        return output
    
    #Testing for stalemate is causing performance issues. FIXED!!! (To an extent)
    #castling is still possible in check for some reason. FIXED!!!
    
    def draw(self, display):
        if self.selected_piece is not None:
            self.get_square_from_pos(self.selected_piece.pos).highlight = True
            for square in self.selected_piece.get_valid_moves(self):
                square.highlight = True
        for square in self.squares:
            square.draw(display)