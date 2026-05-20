from collections import deque
from algorithms.base_algorithm import SearchAlgorithm


class BFSAlgorithm(SearchAlgorithm):

    def search(self, environment, start, goal):

        queue = deque()
        queue.append((start, [start]))

        visited = set()

        while queue:

            current, path = queue.popleft()

            if current == goal:
                return path

            if current in visited:
                continue

            visited.add(current)

            for neighbor in environment.get_neighbors(current):

                if neighbor not in visited:
                    queue.append(
                        (neighbor, path + [neighbor])
                    )

        return []