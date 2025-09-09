from simpleai.search import SearchProblem, astar, greedy
import time


class EightPuzzleProblem(SearchProblem):
    def __init__(self, initial_state, goal_state='123456780'):
        super(EightPuzzleProblem, self).__init__(initial_state=initial_state)
        self.goal_state = goal_state
        # Tạo map vị trí đích để tính heuristic nhanh hơn
        self.goal_positions = {char: (i // 3, i % 3) for i, char in enumerate(self.goal_state)}


    # Trả về các hành động có thể từ trạng thái hiện tại
    def actions(self, state):
        pos_0 = state.find('0')
        row_0, col_0 = pos_0 // 3, pos_0 % 3
        
        possible_actions = []
        if row_0 > 0: possible_actions.append('up')
        if row_0 < 2: possible_actions.append('down')
        if col_0 > 0: possible_actions.append('left')
        if col_0 < 2: possible_actions.append('right')
        
        return possible_actions


    # Áp dụng một hành động và trả về trạng thái mới
    def result(self, state, action):
        pos_0 = state.find('0')
        state_list = list(state)
        
        if action == 'up':
            swap_pos = pos_0 - 3
        elif action == 'down':
            swap_pos = pos_0 + 3
        elif action == 'left':
            swap_pos = pos_0 - 1
        elif action == 'right':
            swap_pos = pos_0 + 1
            
        state_list[pos_0], state_list[swap_pos] = state_list[swap_pos], state_list[pos_0]
        return "".join(state_list)


    def is_goal(self, state):
        return state == self.goal_state


    def heuristic(self, state):
        distance = 0
        for i, char in enumerate(state):
            if char != '0':
                current_row, current_col = i // 3, i % 3
                goal_row, goal_col = self.goal_positions[char]
                distance += abs(current_row - goal_row) + abs(current_col - goal_col)
        return distance


# Hàm in bàn cờ
def print_state(state):
    for i in range(0, 9, 3):
        print(" ".join(state[i:i+3]))


# Hàm in lời giải
def print_solution(result, algorithm_name, execution_time):
    if result is None:
        print(f"{algorithm_name}: Không tìm thấy lời giải.")
        return
    
    steps = len(result.path()) - 1
    cost = steps  # Chi phí = số bước di chuyển
    
    print(f"\n{algorithm_name}:")
    print(f"- Tìm thấy lời giải sau {steps} bước")
    print(f"- Chi phí (cost): {cost}")
    print(f"- Thời gian thực thi: {execution_time:.2f} ms")
    
    print("\nCác bước di chuyển:")
    for i, (action, state) in enumerate(result.path()):
        print(f"--- Bước {i} ---")
        if action:
            print(f"Hành động: {action}")
        print_state(state)


# Hàm kiểm tra tính hợp lệ của trạng thái
def is_valid_state(state):
    if len(state) != 9:
        return False
    return set(state) == set('012345678')


def input_state(prompt):
    while True:
        state = input(prompt).replace(" ", "").replace("\n", "")
        if is_valid_state(state):
            return state
        else:
            print("Trạng thái không hợp lệ! Vui lòng nhập 9 ký tự từ 0-8, mỗi ký tự xuất hiện đúng 1 lần.")


if __name__ == "_main_":
    print("=== BÀI TOÁN 8 Ô SỐ ===")
    print("Hướng dẫn: Nhập 9 số từ 0-8, trong đó 0 là ô trống")
    print("Ví dụ: 123046758 hoặc 1 2 3 0 4 6 7 5 8")
    
    # Nhập trạng thái ban đầu
    initial_state = input_state("\nNhập trạng thái ban đầu: ")
    
    # Nhập trạng thái đích
    print("\nTrạng thái đích mặc định: 123456780")
    use_default = input("Sử dụng trạng thái đích mặc định? (y/n): ").lower().strip()
    
    if use_default == 'y' or use_default == '':
        goal_state = '123456780'
    else:
        goal_state = input_state("Nhập trạng thái đích: ")
    
    # Tạo bài toán
    problem = EightPuzzleProblem(initial_state, goal_state)
    
    print("\nTrạng thái ban đầu:")
    print_state(initial_state)
    print("\nTrạng thái đích:")
    print_state(goal_state)
    print("\n" + "="*50)

    # Giải bằng A*
    print("\n🔍 Đang giải bằng A* Search...")
    start_time = time.time()
    result_astar = astar(problem, graph_search=True)
    end_time = time.time()
    execution_time_astar = (end_time - start_time) * 1000  # Chuyển sang ms
    print_solution(result_astar, "A* Search", execution_time_astar)
    
    print("\n" + "="*50)

    
    print("\n🔍 Đang giải bằng Greedy Best-First Search...")
    start_time = time.time()
    result_greedy = greedy(problem, graph_search=True)
    end_time = time.time()
    execution_time_greedy = (end_time - start_time) * 1000  
    print_solution(result_greedy, "Greedy Best-First Search", execution_time_greedy)
    
   
    print("\n" + "="*50)
    print("📊 SO SÁNH KẾT QUẢ:")
    
    if result_astar:
        astar_steps = len(result_astar.path()) - 1
        astar_cost = astar_steps
        print(f"A*: {astar_steps} bước, Chi phí: {astar_cost}, Thời gian: {execution_time_astar:.2f} ms")
    else:
        print("A*: Không tìm thấy lời giải")
        
    if result_greedy:
        greedy_steps = len(result_greedy.path()) - 1
        greedy_cost = greedy_steps
        print(f"Greedy: {greedy_steps} bước, Chi phí: {greedy_cost}, Thời gian: {execution_time_greedy:.2f} ms")
    else:
        print("Greedy: Không tìm thấy lời giải")