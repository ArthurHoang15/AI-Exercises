from simpleai.search import SearchProblem, depth_first

# Lớp định nghĩa bài toán N-Hậu (xây dựng giải pháp)
class NQueensProblem(SearchProblem):
    def __init__(self, n):
        self.n = n
        # Trạng thái ban đầu là bàn cờ trống (tuple rỗng)
        super(NQueensProblem, self).__init__(initial_state=())

    # Các hành động có thể là đặt một quân hậu vào cột tiếp theo
    def actions(self, state):
        # Cột tiếp theo để đặt quân hậu
        current_col = len(state)
        
        # Tìm các hàng hợp lệ ở cột hiện tại
        possible_rows = []
        for row in range(self.n):
            is_safe = True
            # Kiểm tra với các quân hậu đã đặt
            for col_placed, row_placed in enumerate(state):
                # Kiểm tra cùng hàng hoặc đường chéo
                if row == row_placed or abs(row - row_placed) == abs(current_col - col_placed):
                    is_safe = False
                    break
            if is_safe:
                possible_rows.append(row)
        return possible_rows

    # Áp dụng hành động: thêm vị trí hàng của quân hậu mới vào tuple trạng thái
    def result(self, state, action):
        return state + (action,)

    # Trạng thái đích là khi đã đặt đủ N quân hậu
    def is_goal(self, state):
        return len(state) == self.n

# Hàm in bàn cờ từ trạng thái lời giải
def print_solution(solution_state, n):
    if solution_state is None:
        print("Không tìm thấy lời giải.")
        return
        
    print(f"Lời giải cho {n}-Hậu:")
    for r in range(n):
        line = ""
        for c in range(n):
            if solution_state[c] == r:
                line += "Q "
            else:
                line += ". "
        print(line)

if __name__ == "__main__":
    N = 8
    problem = NQueensProblem(N)
    
    # Sử dụng thuật toán tìm kiếm theo chiều sâu để tìm lời giải
    result = depth_first(problem, graph_search=True)
    
    if result:
        print_solution(result.state, N)
    else:
        print(f"Không tìm thấy lời giải cho {N}-Hậu.")
