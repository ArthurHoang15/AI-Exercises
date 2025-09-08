from simpleai.search import SearchProblem, astar, greedy
import math

# Trạng thái đích
GOAL_STATE = '123456780'

# Lớp định nghĩa bài toán 8 ô số
class EightPuzzleProblem(SearchProblem):
    def __init__(self, initial_state):
        super(EightPuzzleProblem, self).__init__(initial_state=initial_state)
        # Tạo map vị trí đích để tính heuristic nhanh hơn
        self.goal_positions = {char: (i // 3, i % 3) for i, char in enumerate(GOAL_STATE)}

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

    # Kiểm tra trạng thái hiện tại có phải là đích không
    def is_goal(self, state):
        return state == GOAL_STATE

    # Hàm heuristic: Khoảng cách Manhattan
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
def print_solution(result):
    if result is None:
        print("Không tìm thấy lời giải.")
        return
    
    print(f"Tìm thấy lời giải sau {len(result.path()) - 1} bước.")
    for action, state in result.path():
        print("---")
        if action:
            print(f"Hành động: {action}")
        print_state(state)

if __name__ == "__main__":
    # Trạng thái ban đầu, 0 là ô trống
    initial_state = '123046758'
    problem = EightPuzzleProblem(initial_state)
    
    print("Trạng thái ban đầu:")
    print_state(initial_state)
    print("\n" + "="*20)

    # Giải bằng A*
    print("\n--- Giải bằng A* Search ---")
    result_astar = astar(problem, graph_search=True)
    print_solution(result_astar)
    
    print("\n" + "="*20)

    # Giải bằng Greedy Best-First Search
    print("\n--- Giải bằng Greedy Best-First Search ---")
    result_greedy = greedy(problem, graph_search=True)
    print_solution(result_greedy)
