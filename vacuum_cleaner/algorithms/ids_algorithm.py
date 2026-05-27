from algorithms.base_algorithm import SearchAlgorithm
from collections import deque

class IDSAlgorithm:

    def search(self, environment, start, goal):

        depth = 0

        while True:

            visited = set()

            result = self.dls(
                environment,
                start,
                goal,
                depth,
                visited,
                [start]
            )

            if result:
                return result

            depth += 1

    def dls(
        self,
        environment,
        current,
        goal,
        depth,
        visited,
        path
    ):

        if current == goal:
            return path

        if depth == 0:
            return None

        visited.add(current)

        for neighbor in environment.get_neighbors(current):

            if neighbor not in visited:

                result = self.dls(
                    environment,
                    neighbor,
                    goal,
                    depth - 1,
                    visited,
                    path + [neighbor]
                )

                if result:
                    return result

        return None