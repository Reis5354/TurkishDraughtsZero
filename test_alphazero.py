from game import Game
import numpy as np

def test_alphazero_interface():
    game = Game()
    
    # Test başlangıç durumu
    board = game.getInitBoard()
    print("Başlangıç tahtası:")
    print(board)
    
    # Test tahta boyutları
    print("\nTahta boyutları:", game.getBoardSize())
    
    # Test hamle sayısı
    print("Toplam olası hamle sayısı:", game.getActionSize())
    
    # Test geçerli hamleler
    valid_moves = game.getValidMoves(board, 1)  # 1: Siyah oyuncu
    print("\nGeçerli hamle sayısı:", np.sum(valid_moves))
    
    # Test örnek hamle
    action = np.where(valid_moves == 1)[0][0]  # İlk geçerli hamle
    next_board, next_player = game.getNextState(board, 1, action)
    print("\nHamle sonrası tahta:")
    print(next_board)
    print("Sıradaki oyuncu:", "Siyah" if next_player == 1 else "Beyaz")
    
    # Test oyun sonu kontrolü
    game_result = game.getGameEnded(next_board, 1)
    print("\nOyun durumu:", game_result)

if __name__ == "__main__":
    test_alphazero_interface()