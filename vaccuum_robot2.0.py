import random
import time

class VacuumCleanerAgent:

    def __init__(self, rows, cols, obstacle_count):

        self.rows = rows
        self.cols = cols

        # KÝ HIỆU:
        # 0 = bẩn
        # 1 = sạch
        # -1 = vật cản

        # Tạo môi trường
        self.environment = [
            [random.randint(0, 1) for _ in range(cols)]
            for _ in range(rows)
        ]

        # TẠO VẬT CẢN NGẪU NHIÊN
        self.place_obstacles(obstacle_count)

        # VỊ TRÍ BẮT ĐẦU
        while True:

            self.x = random.randint(0, rows - 1)
            self.y = random.randint(0, cols - 1)

            # Không được spawn vào vật cản
            if self.environment[self.x][self.y] != -1:
                break

        self.visited = set()

        # Đếm bước
        self.steps = 0

    # TẠO VẬT CẢN
    def place_obstacles(self, obstacle_count):

        count = 0

        while count < obstacle_count:

            x = random.randint(0, self.rows - 1)
            y = random.randint(0, self.cols - 1)

            # Chưa phải vật cản
            if self.environment[x][y] != -1:

                self.environment[x][y] = -1
                count += 1

    def display_environment(self):

        print("\nMôi trường:")

        for i in range(self.rows):

            for j in range(self.cols):

                # Robot
                if i == self.x and j == self.y:
                    print("R", end=" ")

                # Vật cản
                elif self.environment[i][j] == -1:
                    print("X", end=" ")

                else:
                    print(self.environment[i][j], end=" ")

            print()

    def percept(self):

        # Ghi nhớ vị trí đã đi
        self.visited.add((self.x, self.y))

        return {
            "position": (self.x, self.y),
            "state": self.environment[self.x][self.y]
        }

    def suck(self):

        self.environment[self.x][self.y] = 1

        print(f"Hút bụi tại ({self.x}, {self.y})")

    def is_clean(self):

        for row in self.environment:

            for cell in row:

                # còn ô bẩn
                if cell == 0:
                    return False

        return True

    def possible_moves(self):

        unvisited_moves = []
        visited_moves = []

        directions = {
            "UP":    (self.x - 1, self.y),
            "DOWN":  (self.x + 1, self.y),
            "LEFT":  (self.x, self.y - 1),
            "RIGHT": (self.x, self.y + 1)
        }

        for move, (nx, ny) in directions.items():

            if (0 <= nx < self.rows and
                0 <= ny < self.cols and
                self.environment[nx][ny] != -1):

                # Ưu tiên ô chưa đi
                if (nx, ny) not in self.visited:
                    unvisited_moves.append(move)

                else:
                    visited_moves.append(move)

        if unvisited_moves:
            return unvisited_moves

        return visited_moves

    def choose_action(self, percept):

        state = percept["state"]

        # RULE 1:
        # Ô bẩn -> hút
        if state == 0:
            return "SUCK"

        # RULE 2:
        # Ô sạch -> di chuyển
        moves = self.possible_moves()

        # Không còn đường đi
        if not moves:
            return "STOP"

        return random.choice(moves)

    def execute_action(self, action):

        if action == "SUCK":

            self.suck()

        elif action == "UP":

            self.x -= 1

        elif action == "DOWN":

            self.x += 1

        elif action == "LEFT":

            self.y -= 1

        elif action == "RIGHT":

            self.y += 1

        print("Action:", action)

    # CHẠY AGENT
    def run(self):

        print("=== SIMPLE REFLEX VACUUM AGENT ===")

        while True:

            self.steps += 1

            print(f"\n===== STEP {self.steps} =====")

            self.display_environment()

            percept = self.percept()

            print("Percept:", percept)

            # Đã sạch hết
            if self.is_clean():

                print("\n=== HOÀN THÀNH ===")
                print(f"Tổng số bước: {self.steps}")

                break

            action = self.choose_action(percept)

            # Không còn đường đi
            if action == "STOP":

                print("\nRobot bị kẹt!")
                break

            self.execute_action(action)

            time.sleep(0.5)


# MAIN

rows = 3
cols = 3

# số lượng vật cản
obstacles = 1

agent = VacuumCleanerAgent(rows, cols, obstacles)

agent.run()