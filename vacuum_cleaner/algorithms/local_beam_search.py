import random


class LocalBeamSearchAlgorithm:

    def __init__(self, k: int = 3, max_iterations: int = 500):
        self.k              = k
        self.max_iterations = max_iterations

    def h(self, state, goal) -> float:
        """Hàm mục tiêu: âm khoảng cách Manhattan (cực đại hoá)."""
        return -(abs(state[0] - goal[0]) + abs(state[1] - goal[1]))

    def search(self, environment, start, goal):

        if start == goal:
            return [start]

        # ── 1. Khởi tạo ───────────────────────────────────────────────────
        parent: dict = {start: None}

        start_neighbors = environment.get_neighbors(start)
        # Sắp xếp lân cận ban đầu theo h để chọn k-1 hướng tốt nhất ngay từ đầu
        start_neighbors.sort(key=lambda s: self.h(s, goal), reverse=True)
        initial_extra = start_neighbors[: self.k - 1]

        for nb in initial_extra:
            parent[nb] = start

        beam = [start] + initial_extra   # chùm ban đầu, tất cả liền kề start

        # ── 2. TRONG KHI (đúng) ───────────────────────────────────────────
        for _ in range(self.max_iterations):

            neighbor_states = []  # rỗng

            # 2.1. Sinh trạng thái lân cận
            for state in beam:
                for nb in environment.get_neighbors(state):
                    if nb not in parent:       # chưa thăm → liên thông qua parent
                        neighbor_states.append(nb)
                        parent[nb] = state

            if not neighbor_states:
                break

            # 2.2. Kiểm tra đích
            for nb in neighbor_states:
                if nb == goal:
                    return self._trace_path(parent, goal)

            # 2.3. Lựa chọn chùm: giữ k trạng thái tốt nhất
            neighbor_states.sort(key=lambda s: self.h(s, goal), reverse=True)
            beam = neighbor_states[: self.k]

        # Hết vòng lặp — trả về path đến trạng thái gần goal nhất
        best = min(parent, key=lambda s: abs(s[0]-goal[0]) + abs(s[1]-goal[1]))
        return self._trace_path(parent, best)

    def _trace_path(self, parent: dict, end) -> list:
        """Truy vết ngược từ end về start qua bảng parent → đường đi liên thông."""
        path, node = [], end
        while node is not None:
            path.append(node)
            node = parent.get(node)
        path.reverse()
        return path