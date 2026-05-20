from algorithms.base_algorithm import SearchAlgorithm


class DFSAlgorithm(SearchAlgorithm):

    def search(self, environment, start, goal):

        stack = [(start, [start])]

        visited = set()

        while stack:

            current, path = stack.pop()

            if current in visited:
                continue

            visited.add(current)

            if current == goal:
                return path

            neighbors = environment.get_neighbors(current)

            neighbors = sorted(neighbors)

            for neighbor in reversed(neighbors):

                if neighbor not in visited:

                    stack.append(
                        (
                            neighbor,
                            path + [neighbor]
                        )
                    )

        return []