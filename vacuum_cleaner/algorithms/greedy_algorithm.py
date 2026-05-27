from algorithms.base_algorithm import SearchAlgorithm
import heapq

class GreedyAlgorithm:

    def heuristic(self, current, goal):

        return abs(current[0] - goal[0]) + abs(current[1] - goal[1])

    def search(self, environment, start, goal):

        pq = []

        heapq.heappush(
            pq,
            (
                self.heuristic(start, goal),
                start,
                [start]
            )
        )

        visited = set()

        while pq:

            _, current, path = heapq.heappop(pq)

            if current == goal:
                return path

            if current in visited:
                continue

            visited.add(current)

            for neighbor in environment.get_neighbors(current):

                if neighbor not in visited:

                    heapq.heappush(
                        pq,
                        (
                            self.heuristic(neighbor, goal),
                            neighbor,
                            path + [neighbor]
                        )
                    )

        return []