import numpy as np
from DamaConfig import DamaConfig

class DamaGame:
    def __init__(self):
        self.config = DamaConfig()
        self.board = self._initialize_board()
        self.current_player = self.config.BLACK
        self.moves_without_capture = 0
        self.game_history = []

    def _initialize_board(self):
        """Initialize the game board with starting positions for Turkish Draughts
        Her oyuncunun 16 taşı olmalı (2 sıra)
        Taşlar 1-2 ve 5-6 satırlara dizilir, 0 ve 7 boş kalır"""
        board = np.zeros((self.config.BOARD_SIZE, self.config.BOARD_SIZE), dtype=int)

        # Set up black pieces (1. ve 2. sıra - 16 taş)
        for row in range(1, 3):  # 1 ve 2. satırlar
            for col in range(self.config.BOARD_SIZE):
                board[row][col] = self.config.BLACK

        # Set up white pieces (5. ve 6. sıra - 16 taş)
        for row in range(5, 7):  # 5 ve 6. satırlar
            for col in range(self.config.BOARD_SIZE):
                board[row][col] = self.config.WHITE

        return board

    def display_board(self):
        piece_symbols = {
            self.config.EMPTY: ".",
            self.config.BLACK: "b",
            self.config.WHITE: "w",
            self.config.BLACK_KING: "B",
            self.config.WHITE_KING: "W"
        }

        print("   ", end="")
        for col in range(self.config.BOARD_SIZE):
            print(f" {col}", end="")
        print("\n")

        for row in range(self.config.BOARD_SIZE):
            print(f"{row:2d} ", end="")
            for col in range(self.config.BOARD_SIZE):
                piece = self.board[row][col]
                print(f" {piece_symbols[piece]}", end="")
            print()
        print()

    def get_valid_moves(self, row, col):
        moves = []
        piece = self.board[row][col]

        if piece == 0 or piece != self.current_player and piece != self.current_player + 2:
            return []

        # Normal taş hareketleri için yönler
        if piece == self.config.BLACK:
            directions = [(1, 0), (1, 1), (1, -1)]  # İleri ve çapraz
        elif piece == self.config.WHITE:
            directions = [(-1, 0), (-1, 1), (-1, -1)]  # İleri ve çapraz
        else:  # Dama taşları
            directions = [(1, 0), (1, 1), (1, -1), (-1, 0), (-1, 1), (-1, -1)]

        # Hamleleri kontrol et
        for dy, dx in directions:
            new_row, new_col = row + dy, col + dx
            if self._is_valid_position(new_row, new_col) and self.board[new_row][new_col] == self.config.EMPTY:
                moves.append((new_row, new_col))

        return moves

    def make_move(self, from_pos, to_pos):
        from_row, from_col = from_pos
        to_row, to_col = to_pos

        if not self._is_valid_move(from_pos, to_pos):
            return False

        piece = self.board[from_row][from_col]
        self.board[to_row][to_col] = piece
        self.board[from_row][from_col] = self.config.EMPTY

        # Dama olma kontrolü
        if (piece == self.config.BLACK and to_row == self.config.BOARD_SIZE - 1):
            self.board[to_row][to_col] = self.config.BLACK_KING
        elif (piece == self.config.WHITE and to_row == 0):
            self.board[to_row][to_col] = self.config.WHITE_KING

        self.current_player = self.config.WHITE if self.current_player == self.config.BLACK else self.config.BLACK
        self.game_history.append((from_pos, to_pos))
        return True

    def _is_valid_move(self, from_pos, to_pos):
        from_row, from_col = from_pos
        to_row, to_col = to_pos
        
        if not (self._is_valid_position(from_row, from_col) and self._is_valid_position(to_row, to_col)):
            return False

        piece = self.board[from_row][from_col]
        if piece == self.config.EMPTY or piece != self.current_player:
            return False

        if self.board[to_row][to_col] != self.config.EMPTY:
            return False

        # Normal taş hareketleri
        if piece == self.config.BLACK:
            if to_row <= from_row:
                return False
            if abs(to_row - from_row) != 1 or abs(to_col - from_col) > 1:
                return False
        elif piece == self.config.WHITE:
            if to_row >= from_row:
                return False
            if abs(to_row - from_row) != 1 or abs(to_col - from_col) > 1:
                return False
        elif piece in [self.config.BLACK_KING, self.config.WHITE_KING]:
            if abs(to_row - from_row) != 1 or abs(to_col - from_col) > 1:
                return False

        return True

    def _is_valid_position(self, row, col):
        return 0 <= row < self.config.BOARD_SIZE and 0 <= col < self.config.BOARD_SIZE

    def get_game_state(self):
        return {
            'board': self.board.copy(),
            'current_player': self.current_player,
            'moves_without_capture': self.moves_without_capture,
            'game_history': self.game_history.copy()
        }

    def is_game_over(self):
        if self.moves_without_capture >= self.config.MAX_MOVES_WITHOUT_CAPTURE:
            return True, "Draw by move limit"

        # Geçerli hamle kontrolü
        for row in range(self.config.BOARD_SIZE):
            for col in range(self.config.BOARD_SIZE):
                if (self.board[row][col] == self.current_player or 
                    self.board[row][col] == self.current_player + 2):
                    if self.get_valid_moves(row, col):
                        return False, None

        winner = "White" if self.current_player == self.config.BLACK else "Black"
        return True, f"{winner} wins by no valid moves"