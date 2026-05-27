from algorithms.base_algorithm import SearchAlgorithm
import heapq

class UCSAlgorithm:

    def search(self, environment, start, goal):

        pq = []

        heapq.heappush(
            pq,
            (0, start, [start])
        )

        visited = set()

        while pq:

            cost, current, path = heapq.heappop(pq)

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
                            cost + 1,
                            neighbor,
                            path + [neighbor]
                        )
                    )

        return []