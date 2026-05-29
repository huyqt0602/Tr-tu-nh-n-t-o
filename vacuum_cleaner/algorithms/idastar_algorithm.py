class IDAStarAlgorithm:

    def heuristic(self, current, goal):

        return abs(current[0] - goal[0]) + abs(current[1] - goal[1])

    def search(self, environment, start, goal):

        threshold = self.heuristic(start, goal)

        path = [start]

        path_set = {start}

        while True:

            result = self._dfs(
                environment,
                path,
                path_set,
                0,
                threshold,
                goal
            )

            if isinstance(result, list):
                return result

            if result == float('inf'):
                return []

            threshold = result

    def _dfs(
        self,
        environment,
        path,
        path_set,
        g,
        threshold,
        goal
    ):

        current = path[-1]

        f = g + self.heuristic(current, goal)

        if f > threshold:
            return f

        if current == goal:
            return list(path)

        minimum = float('inf')

        for neighbor in environment.get_neighbors(current):

            if neighbor not in path_set:

                path.append(neighbor)
                path_set.add(neighbor)

                result = self._dfs(
                    environment,
                    path,
                    path_set,
                    g + 1,
                    threshold,
                    goal
                )

                if isinstance(result, list):
                    return result

                minimum = min(minimum, result)

                path.pop()
                path_set.discard(neighbor)

        return minimum
