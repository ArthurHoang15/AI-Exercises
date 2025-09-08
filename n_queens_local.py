import random
from simpleai.search import SearchProblem, hill_climbing, simulated_annealing, genetic

# Lớp định nghĩa bài toán N-Hậu cho tìm kiếm cục bộ
class NQueensLocalProblem(SearchProblem):
    def __init__(self, n):
        self.n = n
        # Tạo trạng thái ban đầu ngẫu nhiên
        initial_state = self.generate_random_state()
        super(NQueensLocalProblem, self).__init__(initial_state=initial_state)

    # Tạo một trạng thái ngẫu nhiên
    def generate_random_state(self):
        # Trạng thái là một tuple/list có độ dài n
        # state[i] là vị trí hàng của quân hậu ở cột i
        state = list(range(self.n))
        random.shuffle(state)
        return tuple(state)

    # Hành động: di chuyển một quân hậu trong cột của nó
    def actions(self, state):
        actions = []
        for col in range(self.n):
            for row in range(self.n):
                if state[col] != row:
                    actions.append((col, row)) # (cột để thay đổi, hàng mới)
        return actions

    # Áp dụng hành động để tạo trạng thái hàng xóm
    def result(self, state, action):
        col, new_row = action
        new_state = list(state)
        new_state[col] = new_row
        return tuple(new_state)

    # Hàm đánh giá: trả về SỐ ÂM của số cặp hậu tấn công nhau.
    # Các thuật toán này tối đa hóa giá trị, nên ta cần giá trị tiến về 0 từ phía âm.
    def value(self, state):
        attacks = 0
        for c1 in range(self.n):
            for c2 in range(c1 + 1, self.n):
                # Kiểm tra cùng hàng
                if state[c1] == state[c2]:
                    attacks += 1
                # Kiểm tra cùng đường chéo
                if abs(c1 - c2) == abs(state[c1] - state[c2]):
                    attacks += 1
        return -attacks

    # Phương thức lai tạo cho thuật toán di truyền
    def crossover(self, state1, state2):
        # Sử dụng phương pháp lai tạo một điểm
        crossover_point = random.randint(1, self.n - 1)
        new_state = state1[:crossover_point] + state2[crossover_point:]
        return new_state

    # Phương thức đột biến cho thuật toán di truyền
    def mutate(self, state):
        # Thay đổi ngẫu nhiên vị trí của một quân hậu
        new_state = list(state)
        col = random.randint(0, self.n - 1)
        new_row = random.randint(0, self.n - 1)
        new_state[col] = new_row
        return tuple(new_state)

    # Tạo cá thể ngẫu nhiên cho thuật toán di truyền
    def generate_random_state(self):
        # Trạng thái là một tuple/list có độ dài n
        # state[i] là vị trí hàng của quân hậu ở cột i
        state = list(range(self.n))
        random.shuffle(state)
        return tuple(state)

# Hàm in bàn cờ từ trạng thái lời giải
def print_solution(state, n):
    if state is None:
        print("Không tìm thấy lời giải.")
        return
        
    print(f"Lời giải cho {n}-Hậu:")
    for r in range(n):
        line = ""
        for c in range(n):
            if state[c] == r:
                line += "Q "
            else:
                line += ". "
        print(line)

if __name__ == "__main__":
    N = 8
    problem = NQueensLocalProblem(N)

    # --- Giải bằng Hill Climbing ---
    print("\n--- Giải bằng Hill Climbing ---")
    result_hc = hill_climbing(problem)
    print(f"Số cặp hậu tấn công cuối cùng: {-problem.value(result_hc.state)}")
    print_solution(result_hc.state, N)

    # --- Giải bằng Simulated Annealing ---
    print("\n--- Giải bằng Simulated Annealing ---")
    result_sa = simulated_annealing(problem, iterations_limit=10000)
    print(f"Số cặp hậu tấn công cuối cùng: {-problem.value(result_sa.state)}")
    print_solution(result_sa.state, N)
    
    # --- Giải bằng Genetic Algorithm ---
    # Lưu ý: GA của simpleAI có thể cần điều chỉnh tham số để hiệu quả hơn
    print("\n--- Giải bằng Genetic Algorithm ---")
    result_ga = genetic(problem, population_size=100, mutation_chance=0.2, iterations_limit=500)
    print(f"Số cặp hậu tấn công cuối cùng: {-problem.value(result_ga.state)}")
    print_solution(result_ga.state, N)
