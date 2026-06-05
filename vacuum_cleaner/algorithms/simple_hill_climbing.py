class SimpleHillClimbingAlgorithm:

    def value(self, position, goal):

        return -(
            abs(position[0] - goal[0]) +
            abs(position[1] - goal[1])
        )

    def search(self, environment, start, goal):

        current = start

        path = [start]

        visited = {start}

        while current != goal:

            neighbors = environment.get_neighbors(current)

            moved = False

            for neighbor in neighbors:

                if neighbor not in visited:

                    if (
                        self.value(neighbor, goal) >
                        self.value(current, goal)
                    ):

                        path.append(neighbor)
                        visited.add(neighbor)
                        current = neighbor
                        moved = True
                        break  

            if not moved:
                break  

        return path