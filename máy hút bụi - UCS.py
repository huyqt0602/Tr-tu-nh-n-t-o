import heapq
import copy

# ==========================
# KÝ HIỆU
# 1 = ô bẩn
# 0 = ô sạch
# X = vị trí robot
# ==========================

class VacuumEnvironment:

    def __init__(self, grid):
        self.grid = grid
        self.rows = len(grid)
        self.cols = len(grid[0])

    def display(self, agent_pos=None):
        for i in range(self.rows):
            row_display = []
            for j in range(self.cols):
                if agent_pos == (i, j):
                    row_display.append("X")
                elif self.grid[i][j] == 1:
                    row_display.append("D")
                else:
                    row_display.append("C")
            print(row_display)
        print()

class Node:

    def __init__(self,
                 state,
                 position,
                 path,
                 cost):
        self.state = state
        self.position = position
        self.path = path
        self.cost = cost

    def __lt__(self, other):
        return self.cost < other.cost

class UCSVacuumAgent:

    def __init__(self, env, start_pos):
        self.env = env
        self.start_pos = start_pos

        # (dx, dy, action, cost)
        self.moves = [
            (-1, 0, "UP", 1),
            (1, 0, "DOWN", 1),
            (0, -1, "LEFT", 1),
            (0, 1, "RIGHT", 1)
        ]

    def goal_test(self, state):
        for row in state:
            if 1 in row:
                return False
        return True

    def expand(self, node):
        children = []
        x, y = node.position

        for dx, dy, action, move_cost in self.moves:
            nx = x + dx
            ny = y + dy

            if 0 <= nx < self.env.rows and 0 <= ny < self.env.cols:
                new_state = copy.deepcopy(node.state)
                total_cost = node.cost + move_cost

                # hút bụi nếu ô bẩn
                if new_state[nx][ny] == 1:
                    new_state[nx][ny] = 0
                    total_cost += 2

                child = Node(
                    new_state,
                    (nx, ny),
                    node.path + [action],
                    total_cost
                )
                children.append(child)

        return children

    def uniform_cost_search(self):
        initial_state = copy.deepcopy(self.env.grid)
        x, y = self.start_pos
        initial_cost = 0

        # hút bụi tại vị trí đầu tiên
        if initial_state[x][y] == 1:
            initial_state[x][y] = 0
            initial_cost += 2

        root = Node(
            initial_state,
            self.start_pos,
            [],
            initial_cost
        )

        frontier = []
        heapq.heappush(frontier, root)
        reached = {}

        while frontier:
            node = heapq.heappop(frontier)

            state_tuple = (
                tuple(map(tuple, node.state)),
                node.position
            )

            # tránh xét node cost lớn hơn
            if state_tuple in reached:
                if reached[state_tuple] <= node.cost:
                    continue

            reached[state_tuple] = node.cost

            print("===================================")
            print("Position:", node.position)
            print("Cost:", node.cost)
            print("Path:", node.path)

            for i in range(self.env.rows):
                row_display = []
                for j in range(self.env.cols):
                    if (i, j) == node.position:
                        row_display.append('X')
                    else:
                        row_display.append(node.state[i][j])
                print(row_display)

            print("===================================")

            # GOAL TEST
            if self.goal_test(node.state):
                return node

            # MỞ RỘNG
            children = self.expand(node)
            for child in children:
                heapq.heappush(frontier, child)

        return None

grid = [
    [1, 0, 1],
    [0, 1, 0],
    [1, 0, 1]
]

env = VacuumEnvironment(grid)

print("===== TRẠNG THÁI BAN ĐẦU =====")
env.display((1, 1))

agent = UCSVacuumAgent(env, (1, 1))
solution = agent.uniform_cost_search()

if solution:
    print("\n\n===== ĐÃ TÌM THẤY LỜI GIẢI =====")
    print("Tổng chi phí:", solution.cost)
    print("Đường đi:")
    print(solution.path)

    print("\nTrạng thái cuối:")
    
    # --- ĐÃ SỬA: CHÈN THÊM CHỮ X VÀO KẾT QUẢ CUỐI ---
    for i in range(len(solution.state)):
        row_display = []
        for j in range(len(solution.state[0])):
            if (i, j) == solution.position:
                row_display.append('X')
            else:
                row_display.append(solution.state[i][j])
        print(row_display)
    # ------------------------------------------------

else:
    print("Không tìm thấy lời giải")