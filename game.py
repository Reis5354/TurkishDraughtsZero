from DamaGame import DamaGame
import numpy as np

class Game:
    """
    AlphaZero framework için Türk Daması oyunu arayüzü
    """
    def __init__(self):
        self.game = DamaGame()
        
    def getInitBoard(self):
        """Başlangıç tahtasını döndür"""
        return self.game._initialize_board()

    def getBoardSize(self):
        """Tahta boyutlarını döndür"""
        return (self.game.config.BOARD_SIZE, self.game.config.BOARD_SIZE)

    def getActionSize(self):
        """Tüm olası hamle sayısını döndür"""
        # Her taş için (başlangıç konumu + hedef konumu) = BOARD_SIZE^2 * BOARD_SIZE^2
        return self.game.config.BOARD_SIZE ** 4  # 8x8 tahta için 4096 olası hamle

    def getNextState(self, board, player, action):
        """Hamle sonrası durumu döndür"""
        # action'ı koordinatlara dönüştür
        board_size = self.game.config.BOARD_SIZE
        from_pos = (action // (board_size ** 3), (action // (board_size ** 2)) % board_size)
        to_pos = ((action // board_size) % board_size, action % board_size)
        
        # Kopya tahta oluştur
        next_board = np.copy(board)
        self.game.board = next_board
        self.game.current_player = self.game.config.BLACK if player == 1 else self.game.config.WHITE
        
        # Hamleyi yap
        if self.game.make_move(from_pos, to_pos):
            return next_board, -player
        return board, player

    def getValidMoves(self, board, player):
        """Geçerli hamleleri döndür"""
        self.game.board = np.copy(board)
        self.game.current_player = self.game.config.BLACK if player == 1 else self.game.config.WHITE
        
        valid_moves = np.zeros(self.getActionSize())
        board_size = self.game.config.BOARD_SIZE
        
        # Tüm taşlar için geçerli hamleleri kontrol et
        for from_row in range(board_size):
            for from_col in range(board_size):
                if board[from_row][from_col] == self.game.current_player:
                    moves = self.game.get_valid_moves(from_row, from_col)
                    for to_row, to_col in moves:
                        # Hamleyi action indeksine dönüştür
                        action = from_row * (board_size ** 3) + from_col * (board_size ** 2) + to_row * board_size + to_col
                        valid_moves[action] = 1
                        
        return valid_moves

    def getGameEnded(self, board, player):
        """Oyun durumunu kontrol et"""
        self.game.board = np.copy(board)
        self.game.current_player = self.game.config.BLACK if player == 1 else self.game.config.WHITE
        
        is_over, result = self.game.is_game_over()
        if not is_over:
            return 0
            
        if "Draw" in result:
            return 0.00001  # Küçük pozitif değer beraberlik için
        
        if ("Black wins" in result and player == 1) or ("White wins" in result and player == -1):
            return 1
        return -1

    def getCanonicalForm(self, board, player):
        """Kanonik form - siyah oyuncu için normal, beyaz için ters çevrilmiş tahta"""
        if player == 1:
            return board
        
        # Taşları ters çevir (siyah->beyaz, beyaz->siyah)
        canonical_board = np.copy(board)
        canonical_board[board == self.game.config.BLACK] = self.game.config.WHITE
        canonical_board[board == self.game.config.WHITE] = self.game.config.BLACK
        canonical_board[board == self.game.config.BLACK_KING] = self.game.config.WHITE_KING
        canonical_board[board == self.game.config.WHITE_KING] = self.game.config.BLACK_KING
        return canonical_board

    def stringRepresentation(self, board):
        """Tahtanın string gösterimi - MCTS için hash değeri"""
        return board.tobytes()

    def getSymmetries(self, board, pi):
        """Tahta simetrilerini döndür - Türk Daması için sadece orijinal tahta"""
        # Türk Daması'nda simetri yok (yön önemli)
        return [(board, pi)]