from easyAI import TwoPlayerGame, AI_Player, Negamax, Human_Player

# Lớp định nghĩa trò chơi Tic-Tac-Toe, kế thừa từ TwoPlayerGame của easyAI
class TicTacToe(TwoPlayerGame):
    def __init__(self, players):
        self.players = players
        # Người chơi 1 bắt đầu
        self.current_player = 1
        # Bàn cờ là một danh sách 9 ô, 0 là trống, 1 là X, 2 là O
        self.board = [0] * 9

    # Trả về danh sách các nước đi hợp lệ (các ô còn trống)
    def possible_moves(self):
        return [str(i + 1) for i, e in enumerate(self.board) if e == 0]

    # Thực hiện một nước đi
    def make_move(self, move):
        self.board[int(move) - 1] = self.current_player

    # Kiểm tra xem đối thủ có thắng hay không
    def loss_condition(self):
        possible_combinations = [
            [1, 2, 3], [4, 5, 6], [7, 8, 9],  # Hàng ngang
            [1, 4, 7], [2, 5, 8], [3, 6, 9],  # Hàng dọc
            [1, 5, 9], [3, 5, 7]               # Hàng chéo
        ]
        opponent = 3 - self.current_player
        return any(
            [all([(self.board[i - 1] == opponent) for i in c]) for c in possible_combinations]
        )

    # Kiểm tra xem trò chơi đã kết thúc chưa
    def is_over(self):
        return (self.possible_moves() == []) or self.loss_condition()

    # Hiển thị bàn cờ
    def show(self):
        print("\n" + "\n".join(
                [" ".join([".", "X", "O"][self.board[3 * j + i]] for i in range(3))
                for j in range(3)]
            )
        )

    # Tính điểm cho trạng thái hiện tại (dùng cho AI)
    def scoring(self):
        return -100 if self.loss_condition() else 0

if __name__ == "__main__":
    # Định nghĩa thuật toán cho AI
    # Negamax là một biến thể của Minimax và đã tích hợp sẵn cắt tỉa Alpha-Beta
    # Tham số 8 là độ sâu tìm kiếm (AI sẽ tính trước 8 nước đi để đảm bảo tối ưu)
    ai_algorithm = Negamax(8)

    # Bắt đầu trò chơi
    game = TicTacToe([Human_Player(), AI_Player(ai_algorithm)])
    
    print("Chào mừng đến với Tic-Tac-Toe!")
    print("Bạn là người chơi 'X'. Nhập số từ 1 đến 9 để đi.")
    print("Bàn cờ được đánh số như sau:")
    print("1 2 3")
    print("4 5 6")
    print("7 8 9")
    
    game.play()
    
    if game.loss_condition():
        print(f"\nNgười chơi {3 - game.current_player} thắng!")
    else:
        print("\nHòa!")
