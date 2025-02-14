class DamaConfig:
    def __init__(self):
        # Board configuration
        self.BOARD_SIZE = 8
        
        # Piece values
        self.EMPTY = 0
        self.BLACK = 1
        self.WHITE = 2
        self.BLACK_KING = 3
        self.WHITE_KING = 4
        
        # Game rules
        self.MAX_MOVES_WITHOUT_CAPTURE = 40
        self.SHOW_BOARD = True