import random

class StochasticHillClimbingAlgorithm:

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

            current_value = self.value(current, goal)

            better_neighbors = [
                n for n in neighbors
                if n not in visited
                and self.value(n, goal) > current_value
            ]

            if not better_neighbors:
                break  

            next_state = random.choice(better_neighbors)

            path.append(next_state)
            visited.add(next_state)
            current = next_state

        return path