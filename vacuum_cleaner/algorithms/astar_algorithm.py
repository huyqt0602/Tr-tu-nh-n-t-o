from algorithms.base_algorithm import SearchAlgorithm
import heapq

class AStarAlgorithm:

    def heuristic(self, current, goal):

        return abs(current[0] - goal[0]) + abs(current[1] - goal[1])

    def search(self, environment, start, goal):

        pq = []

        heapq.heappush(
            pq,
            (
                0,
                0,
                start,
                [start]
            )
        )

        visited = set()

        while pq:

            f, g, current, path = heapq.heappop(pq)

            if current == goal:
                return path

            if current in visited:
                continue

            visited.add(current)

            for neighbor in environment.get_neighbors(current):

                if neighbor not in visited:

                    new_g = g + 1

                    new_f = new_g + self.heuristic(
                        neighbor,
                        goal
                    )

                    heapq.heappush(
                        pq,
                        (
                            new_f,
                            new_g,
                            neighbor,
                            path + [neighbor]
                        )
                    )

        return []