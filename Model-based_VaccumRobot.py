import random
import time

class ModelBasedVacuumAgent:

    def __init__(self, rows, cols, obstacle_count):

        self.rows = rows
        self.cols = cols

        """
        QUY ƯỚC:
        0  = bẩn
        1  = sạch
        X = vật cản
        """      

        # Môi trường thật
        self.environment = [
            [random.randint(0, 1) for _ in range(cols)]
            for _ in range(rows)
        ]

        self.place_obstacles(obstacle_count)

        # VỊ TRÍ BẮT ĐẦU
        while True:

            self.x = random.randint(0, rows - 1)
            self.y = random.randint(0, cols - 1)

            if self.environment[self.x][self.y] != -1:
                break

        """
        INTERNAL MODEL
        Agent tự ghi nhớ:
        - ô đã đi
        - ô sạch
        - vật cản
        """
       
        self.model = {}

        # Đếm bước
        self.steps = 0

    def place_obstacles(self, obstacle_count):

        count = 0

        while count < obstacle_count:

            x = random.randint(0, self.rows - 1)
            y = random.randint(0, self.cols - 1)

            if self.environment[x][y] != -1:

                self.environment[x][y] = -1
                count += 1

    def display_environment(self):

        print("\nMôi trường:")

        for i in range(self.rows):

            for j in range(self.cols):

                if i == self.x and j == self.y:
                    print("R", end=" ")

                elif self.environment[i][j] == -1:
                    print("X", end=" ")

                else:
                    print(self.environment[i][j], end=" ")

            print()

    def percept(self):

        current_state = self.environment[self.x][self.y]

        percept_data = {
            "position": (self.x, self.y),
            "state": current_state
        }

        return percept_data

    def update_model(self, percept):

        position = percept["position"]
        state = percept["state"]

        # Agent ghi nhớ trạng thái ô
        self.model[position] = state

    # HÚT BỤI
    def suck(self):

        self.environment[self.x][self.y] = 1

        # cập nhật model
        self.model[(self.x, self.y)] = 1

        print(f"Hút bụi tại ({self.x}, {self.y})")

    # KIỂM TRA ĐÃ SẠCH HẾT
    def is_clean(self):

        for row in self.environment:

            for cell in row:

                if cell == 0:
                    return False

        return True

    # KIỂM TRA HỢP LỆ
    def is_valid(self, x, y):

        return (
            0 <= x < self.rows and
            0 <= y < self.cols and
            self.environment[x][y] != -1
        )

    # TÌM HƯỚNG DI CHUYỂN
    def possible_moves(self):

        directions = {
            "UP":    (self.x - 1, self.y),
            "DOWN":  (self.x + 1, self.y),
            "LEFT":  (self.x, self.y - 1),
            "RIGHT": (self.x, self.y + 1)
        }

        unvisited = []
        dirty = []
        clean = []

        for move, (nx, ny) in directions.items():

            if self.is_valid(nx, ny):

                # CHƯA KHÁM PHÁ
                if (nx, ny) not in self.model:
                    unvisited.append(move)

                # ĐÃ BIẾT LÀ BẨN
                elif self.model[(nx, ny)] == 0:
                    dirty.append(move)

                # ĐÃ SẠCH
                else:
                    clean.append(move)

        # ƯU TIÊN:
        # 1. Ô chưa khám phá
        # 2. Ô bẩn
        # 3. Ô sạch
        if unvisited:
            return unvisited

        if dirty:
            return dirty

        return clean

    # RULES
    def choose_action(self, percept):

        state = percept["state"]

        # RULE 1
        # Nếu bẩn -> hút
        if state == 0:
            return "SUCK"
        
        # RULE 2
        # Nếu sạch -> chọn move tốt nhất
        moves = self.possible_moves()

        if not moves:
            return "STOP"

        return random.choice(moves)

    # THỰC HIỆN ACTION
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

    # HIỂN THỊ INTERNAL MODEL
    def display_model(self):

        print("\nInternal Model:")

        for i in range(self.rows):

            for j in range(self.cols):

                if (i, j) == (self.x, self.y):
                    print("R", end=" ")

                elif self.environment[i][j] == -1:
                    print("X", end=" ")

                elif (i, j) not in self.model:
                    print("?", end=" ")

                else:
                    print(self.model[(i, j)], end=" ")

            print()

    # RUN
    def run(self):

        print("=== MODEL-BASED REFLEX AGENT ===")

        while True:

            self.steps += 1

            print(f"\n===== STEP {self.steps} =====")

            self.display_environment()

            percept = self.percept()

            # cập nhật model
            self.update_model(percept)

            print("Percept:", percept)

            self.display_model()

            # hoàn thành
            if self.is_clean():

                print("\n=== HOÀN THÀNH ===")
                print(f"Tổng số bước: {self.steps}")

                break

            action = self.choose_action(percept)

            if action == "STOP":

                print("\nKhông còn đường đi!")
                break

            self.execute_action(action)

            time.sleep(0.5)

# MAIN
rows = 3
cols = 3
obstacles = 2

agent = ModelBasedVacuumAgent(rows, cols, obstacles)

agent.run()