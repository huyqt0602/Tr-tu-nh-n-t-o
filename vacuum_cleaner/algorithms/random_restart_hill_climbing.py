import random


class RandomRestartHillClimbingAlgorithm:
   
    MAX_RESTART = 20

    def value(self, position, goal):
        return -(
            abs(position[0] - goal[0]) +
            abs(position[1] - goal[1])
        )

    def search(self, environment, start, goal):

        # Lấy tất cả các ô hợp lệ (không phải vật cản) để chọn điểm khởi đầu ngẫu nhiên
        valid_cells = [
            (r, c)
            for r in range(environment.rows)
            for c in range(environment.cols)
            if environment.grid[r][c] != -1
        ]

        best_path = None
        best_end = None

        for i in range(1, self.MAX_RESTART + 1):

            # Lượt đầu: dùng start gốc; các lượt sau: chọn ngẫu nhiên
            if i == 1:
                current = start
            else:
                current = random.choice(valid_cells)

            path = [current]
            visited = {current}

            # Leo đồi từ current đến goal
            while current != goal:

                neighbors = environment.get_neighbors(current)

                current_value = self.value(current, goal)

                # Lọc Better_Neighbors: tốt hơn current VÀ chưa thăm
                better_neighbors = [
                    n for n in neighbors
                    if n not in visited
                    and self.value(n, goal) > current_value
                ]

                # Better_Neighbors RỖNG → bị kẹt, thoát vòng lặp TRONG KHI
                if not better_neighbors:
                    break

                # Chọn trạng thái tốt nhất từ Better_Neighbors
                next_state = max(
                    better_neighbors,
                    key=lambda n: self.value(n, goal)
                )

                path.append(next_state)
                visited.add(next_state)
                current = next_state

            # Kiểm tra đạt Goal chưa
            if current == goal:
                # Nếu lượt i > 1, cần nối đường từ start đến điểm khởi đầu ngẫu nhiên
                if i == 1 or path[0] == start:
                    return path
                else:
                    # Dùng BFS ngắn để nối start → điểm khởi đầu ngẫu nhiên
                    from algorithms.bfs_algorithm import BFSAlgorithm
                    bfs = BFSAlgorithm()
                    bridge = bfs.search(environment, start, path[0])
                    if bridge:
                        full_path = bridge + path[1:]
                        return full_path
                    return path

            # Lưu lại path tốt nhất (gần goal nhất) để fallback
            if best_end is None or self.value(current, goal) > self.value(best_end, goal):
                best_path = path
                best_end = current

        # Trả về "Thất bại": đã chạy hết MAX_RESTART lượt, không chạm được Goal
        # Trả về path tốt nhất tìm được để agent dùng BFS bổ sung
        return best_path if best_path else [start]
