from DamaGame import DamaGame

def test_game_mechanics():
    game = DamaGame()
    print("Türk Daması Test Senaryoları:")
    
    print("\nTest 1: Başlangıç durumu")
    game.display_board()
    
    print("\nTest 2: Siyah taş ileri hamle")
    move_result = game.make_move((2, 0), (3, 0))
    print(f"Hamle sonucu: {'Başarılı' if move_result else 'Başarısız'}")
    game.display_board()
    
    print("\nTest 3: Beyaz taş ileri hamle")
    move_result = game.make_move((5, 1), (4, 1))
    print(f"Hamle sonucu: {'Başarılı' if move_result else 'Başarısız'}")
    game.display_board()
    
    print("\nTest 4: Siyah taş çapraz hamle")
    move_result = game.make_move((2, 1), (3, 2))
    print(f"Hamle sonucu: {'Başarılı' if move_result else 'Başarısız'}")
    game.display_board()
    
    print("\nTest 5: Oyun geçmişi")
    print("Yapılan hamleler:", game.game_history)
    
    black_count = white_count = 0
    for row in range(game.config.BOARD_SIZE):
        for col in range(game.config.BOARD_SIZE):
            if game.board[row][col] == game.config.BLACK:
                black_count += 1
            elif game.board[row][col] == game.config.WHITE:
                white_count += 1
    
    print(f"\nTest 6: Taş sayımı")
    print(f"Siyah taş: {black_count}")
    print(f"Beyaz taş: {white_count}")
    
    print(f"\nTest 7: Sıra kontrolü")
    current_player = "Siyah" if game.current_player == game.config.BLACK else "Beyaz"
    print(f"Şu anki sıra: {current_player}")

if __name__ == "__main__":
    test_game_mechanics()