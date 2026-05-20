class VacuumAgent:

    def __init__(
        self,
        environment,
        algorithm,
        start_position
    ):

        self.environment = environment

        self.algorithm = algorithm

        self.position = start_position

        self.visited = set()

        self.visited.add(start_position)

    def find_nearest_dirt(self):

        dirt_cells = self.environment.get_dirty_cells()

        if not dirt_cells:
            return None

        nearest = None

        min_distance = float("inf")

        for dirt in dirt_cells:

            distance = (
                abs(dirt[0] - self.position[0]) +
                abs(dirt[1] - self.position[1])
            )

            if distance < min_distance:

                min_distance = distance

                nearest = dirt

        return nearest

    def optimize_path(self, path):

        optimized = []

        local_visited = set()

        for pos in path:

            if pos not in local_visited:

                optimized.append(pos)

                local_visited.add(pos)

        return optimized


    def run(self):

        final_path = []

        while True:

            target = self.find_nearest_dirt()

            if target is None:
                break

            path = self.algorithm.search(
                self.environment,
                self.position,
                target
            )

            path = self.optimize_path(path)

            if final_path and path:

                if final_path[-1] == path[0]:
                    path = path[1:]

            final_path.extend(path)

            for pos in path:
                self.visited.add(pos)

            self.position = target

            self.environment.clean(target)

        return final_path