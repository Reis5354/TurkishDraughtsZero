import numpy as np

def dotdict(d):
    """
    Nokta notasyonu ile erişilebilen sözlük
    d = dotdict({"foo": 123, "bar": 456})
    d.foo  # returns 123
    """
    d = dict(d)
    for k, v in d.items():
        if isinstance(v, dict):
            d[k] = dotdict(v)
    return type('dotdict', (dict,), dict(__getattr__=dict.__getitem__))(d)

def normalize_arrays(arrays):
    """
    Dizileri normalize et (toplam 1 olacak şekilde)
    """
    total = sum(arrays)
    if total > 0:
        return [x/total for x in arrays]
    return [1/len(arrays) for _ in arrays]

def augment_data(board, pi):
    """
    Veri artırma - tahta simetrileri
    Türk Daması'nda sadece yatay simetri kullanılabilir
    """
    # Orijinal veri
    augmented = [(board, pi)]
    
    # Yatay simetri
    flipped_board = np.fliplr(board)
    flipped_pi = np.copy(pi)
    
    # pi vektörünü de uygun şekilde değiştir
    board_size = board.shape[0]
    for i in range(len(pi)):
        if pi[i] > 0:
            from_row = i // (board_size ** 3)
            from_col = (i // (board_size ** 2)) % board_size
            to_row = (i // board_size) % board_size
            to_col = i % board_size
            
            # Sütun indekslerini çevir
            new_from_col = board_size - 1 - from_col
            new_to_col = board_size - 1 - to_col
            
            new_action = from_row * (board_size ** 3) + new_from_col * (board_size ** 2) + \
                        to_row * board_size + new_to_col
            flipped_pi[new_action] = pi[i]
    
    augmented.append((flipped_board, flipped_pi))
    return augmented

def encode_board(board, player):
    """
    Tahtayı sinir ağı için kodla
    4 kanal: Siyah taşlar, Beyaz taşlar, Siyah damalar, Beyaz damalar
    """
    encoded = np.zeros([4] + list(board.shape), dtype=np.float32)
    
    # Kanal 0: Siyah taşlar
    encoded[0] = (board == 1)
    # Kanal 1: Beyaz taşlar
    encoded[1] = (board == 2)
    # Kanal 2: Siyah damalar
    encoded[2] = (board == 3)
    # Kanal 3: Beyaz damalar
    encoded[3] = (board == 4)
    
    # Eğer beyaz oyuncunun sırası ise tahtayı çevir
    if player == -1:
        encoded = np.flip(encoded, axis=1)
    
    return encoded

def decode_board(encoded):
    """
    Kodlanmış tahtayı orijinal formata çevir
    """
    board = np.zeros(encoded.shape[1:], dtype=np.int8)
    board[encoded[0] == 1] = 1  # Siyah taşlar
    board[encoded[1] == 1] = 2  # Beyaz taşlar
    board[encoded[2] == 1] = 3  # Siyah damalar
    board[encoded[3] == 1] = 4  # Beyaz damalar
    return board

def get_valid_moves_mask(game, board, player):
    """
    Geçerli hamlelerin maskesini oluştur
    """
    valid_moves = game.getValidMoves(board, player)
    return valid_moves.astype(np.float32)

class AverageMeter(object):
    """
    Ortalama ve güncel değerleri takip et
    """
    def __init__(self):
        self.reset()

    def reset(self):
        self.val = 0
        self.avg = 0
        self.sum = 0
        self.count = 0

    def update(self, val, n=1):
        self.val = val
        self.sum += val * n
        self.count += n
        self.avg = self.sum / self.count