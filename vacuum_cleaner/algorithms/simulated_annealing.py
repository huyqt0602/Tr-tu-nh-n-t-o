import random
import math


class SimulatedAnnealingAlgorithm:
    """
    Ủ mô phỏng (Simulated Annealing).

    Pseudocode (theo slide):
        SimulatedAnnealing(start, goal):
            current_state = start;  T = T0
            while T > Tmin:
                if current_state == goal: return current_state
                next_state = RandomNeighbor(current_state)
                Δ = h(next_state) − h(current_state)
                if Δ < 0:
                    current_state = next_state
                else:
                    p = exp(−Δ / T)
                    if Random(0,1) < p:
                        current_state = next_state
                T = α × T
            return current_state
    """

    def __init__(
        self,
        T0:    float = 50.0,
        Tmin:  float = 0.5,
        alpha: float = 0.98,
    ):
        self.T0    = T0
        self.Tmin  = Tmin
        self.alpha = alpha

    def h(self, state, goal) -> float:
        """Heuristic: khoảng cách Manhattan đến goal (tối thiểu hoá)."""
        return abs(state[0] - goal[0]) + abs(state[1] - goal[1])

    def search(self, environment, start, goal):

        if start == goal:
            return [start]

        current    = start
        T          = self.T0
        parent     = {start: None}   # lần đầu đến mỗi ô
        best_state = start

        while T > self.Tmin:

            # Kiểm tra đích
            if current == goal:
                return self._trace(parent, goal)

            # Cập nhật best
            if self.h(current, goal) < self.h(best_state, goal):
                best_state = current

            # RandomNeighbor(current_state)
            neighbors = environment.get_neighbors(current)
            if not neighbors:
                break
            next_state = random.choice(neighbors)

            # Δ = h(next_state) − h(current_state)
            delta = self.h(next_state, goal) - self.h(current, goal)

            accepted = False
            if delta < 0:                              # tốt hơn → luôn chấp nhận
                accepted = True
            else:                                      # tệ hơn → xác suất
                p = math.exp(-delta / T)
                if random.random() < p:
                    accepted = True

            if accepted:
                # Ghi parent trước khi cập nhật current
                if next_state not in parent:
                    parent[next_state] = current
                current = next_state

            T = self.alpha * T   # T = α × T

        # Hết vòng lặp: trả về đường đến best_state
        if best_state in parent:
            return self._trace(parent, best_state)
        return [start]

    def _trace(self, parent: dict, end) -> list:
        """Truy vết ngược qua bảng parent → đường đi không lặp."""
        path, node = [], end
        while node is not None:
            path.append(node)
            node = parent.get(node)
        path.reverse()
        return path