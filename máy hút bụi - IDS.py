from collections import deque
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

    def is_dirty(self, x, y):
        return self.grid[x][y] == 1

    def clean(self, x, y):
        self.grid[x][y] = 0

    def is_all_clean(self):
        for row in self.grid:
            if 1 in row:
                return False
        return True

    def display(self, agent_pos=None):

        for i in range(self.rows):

            row_display = []

            for j in range(self.cols):

                if agent_pos == (i, j):
                    row_display.append("X")

                elif self.grid[i][j] == 1:
                    row_display.append("D")  # Dirty

                else:
                    row_display.append("C")  # Clean

            print(row_display)

        print()

class Node:

    def __init__(self, state, position, path, depth):

        self.state = state
        self.position = position
        self.path = path
        self.depth = depth

class IDSVacuumAgent:

    def __init__(self, env, start_pos):
        self.env = env
        self.start_pos = start_pos
        self.moves = [
            (-1, 0, "UP"),
            (1, 0, "DOWN"),
            (0, -1, "LEFT"),
            (0, 1, "RIGHT")
        ]

    def goal_test(self, state):
        for row in state:
            if 1 in row:
                return False
        return True

    def expand(self, node):
        children = []
        x, y = node.position

        for dx, dy, action in self.moves:
            nx = x + dx
            ny = y + dy

            if 0 <= nx < self.env.rows and 0 <= ny < self.env.cols:
                # TỐI ƯU: Dùng list comprehension để copy nhanh
                new_state = [list(row) for row in node.state]

                # hút bụi nếu ô bẩn
                if new_state[nx][ny] == 1:
                    new_state[nx][ny] = 0

                child = Node(
                    new_state,
                    (nx, ny),
                    node.path + [action],
                    node.depth + 1
                )
                children.append(child)

        return children

    def depth_limited_search(self, limit):
        # TỐI ƯU: Dùng list comprehension
        initial_state = [list(row) for row in self.env.grid]
        x, y = self.start_pos

        # hút bụi vị trí đầu tiên
        if initial_state[x][y] == 1:
            initial_state[x][y] = 0

        root = Node(
            initial_state,
            self.start_pos,
            [],
            0
        )

        frontier = [root]
        
        # SỬA LỖI: Dùng dictionary lưu trạng thái kèm độ sâu ngắn nhất
        reached = {}

        while frontier:
            node = frontier.pop()

            state_tuple = (
                tuple(tuple(row) for row in node.state),
                node.position
            )

            # Nếu đã duyệt trạng thái này với số bước ngắn hơn hoặc bằng -> bỏ qua
            if state_tuple in reached and reached[state_tuple] <= node.depth:
                continue

            # Cập nhật độ sâu mới cho trạng thái này
            reached[state_tuple] = node.depth

            # KHÔI PHỤC PHẦN IN QUÁ TRÌNH DUYỆT CỦA BẠN
            print("================================")
            print("Depth:", node.depth)
            print("Position:", node.position)
            print("Path:", node.path)
            for row in node.state:
                print(row)
            print("================================")

            # GOAL TEST
            if self.goal_test(node.state):
                return node

            # GIỚI HẠN ĐỘ SÂU
            if node.depth < limit:
                children = self.expand(node)
                frontier.extend(children)

        return None

    def iterative_deepening_search(self, max_depth=20):
        for depth in range(max_depth):
            print("\n")
            print("################################################")
            print("SEARCH WITH DEPTH =", depth)
            print("################################################")

            result = self.depth_limited_search(depth)

            if result is not None:
                return result

        return None

grid = [
    [0, 0, 0],
    [1, 0, 1],
    [0, 0, 0]
]

env = VacuumEnvironment(grid)

print("TRẠNG THÁI BAN ĐẦU:")
env.display((1, 1))

agent = IDSVacuumAgent(env, (1, 1))

solution = agent.iterative_deepening_search()

if solution:

    print("\n\n===== ĐÃ TÌM THẤY LỜI GIẢI =====")

    print("Đường đi:")
    print(solution.path)

    print("\nTrạng thái cuối:")

    for row in solution.state:
        print(row)

else:
    print("Không tìm thấy lời giải")