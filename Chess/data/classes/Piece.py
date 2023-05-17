import pygame

class Piece:
    def __init__(self, pos, colour, board):
        self.pos = pos
        self.x = pos[0]
        self.y = pos[1]
        self.colour = colour
        self.has_moved = False

    def get_moves(self, board):
        output = []
        for direction in self.get_possible_moves(board):
            for square in direction:
                if square.occupying_piece is not None:
                    if square.occupying_piece.colour == self.colour:
                        break
                    else:
                        output.append(square)
                        break
                else:
                    output.append(square)
        return output

    def get_valid_moves(self, board):
        output = []
        for square in self.get_moves(board):
            if not board.is_in_check(self.colour, board_change=[self.pos, square.pos]):
                output.append(square)
        return output

    def move(self, board, square, force=False):
        for i in board.squares:
            i.highlight = False
        if square in self.get_valid_moves(board) or force:
            prev_square = board.get_square_from_pos(self.pos)
            self.pos, self.x, self.y = square.pos, square.x, square.y
            prev_square.occupying_piece = None
            square.occupying_piece = self
            board.selected_piece = None
            self.has_moved = True
            # pawn promotion, for now keeping it to auto queen promotion. 
            if self.notation == ' ':
                if self.y == 0 or self.y == 7:
                    from data.classes.Queen import Queen
                    square.occupying_piece = Queen(
                        (self.x, self.y),
                        self.colour,
                        board
                    )
            # pls fix rook while castling. FIXED!!!
            if self.notation == 'K':
                if prev_square.x - self.x == 2:
                    rook = board.get_piece_from_pos((0, self.y))
                    rook.move(board, board.get_square_from_pos((3, self.y)), force=True)
                elif prev_square.x - self.x == -2:
                    rook = board.get_piece_from_pos((7, self.y))
                    rook.move(board, board.get_square_from_pos((5, self.y)), force=True)
            return True
        else:
            board.selected_piece = None
            return False

    def attacking_squares(self, board):
        return self.get_moves(board)