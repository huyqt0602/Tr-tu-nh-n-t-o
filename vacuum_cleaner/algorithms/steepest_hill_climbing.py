class SteepestHillClimbingAlgorithm:
    
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

            best_neighbor = None

            best_value = self.value(current, goal)

            for neighbor in neighbors:

                if neighbor not in visited:

                    v = self.value(neighbor, goal)

                    if v > best_value:

                        best_value = v

                        best_neighbor = neighbor

            if best_neighbor is None:
                break  

            path.append(best_neighbor)
            visited.add(best_neighbor)
            current = best_neighbor

        return path