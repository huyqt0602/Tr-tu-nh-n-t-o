from algorithms.bfs_algorithm import BFSAlgorithm


class VacuumAgent:

    def __init__(self, environment, algorithm, start_position):

        self.environment  = environment
        self.algorithm    = algorithm
        self.position     = start_position
        self.visited      = {start_position}

    def find_nearest_dirt(self, exclude=None):

        exclude = exclude or set()

        dirty = [
            d for d in self.environment.get_dirty_cells()
            if d not in exclude
        ]

        if not dirty:
            return None

        return min(
            dirty,
            key=lambda d: (
                abs(d[0] - self.position[0]) +
                abs(d[1] - self.position[1])
            )
        )

    def optimize_path(self, path):

        if not path:
            return []

        result = [path[0]]

        for pos in path[1:]:
            if pos != result[-1]:
                result.append(pos)

        return result

    def join_paths(self, path_a, path_b):

        if not path_a:
            return path_b
        if not path_b:
            return path_a

        if path_a[-1] == path_b[0]:
            return path_a + path_b[1:]

        return path_a + path_b

    def run(self):

        final_path = []

        permanently_unreachable = set()
        bfs = BFSAlgorithm()

        while True:

            target = self.find_nearest_dirt(exclude=permanently_unreachable)

            if target is None:
                break

            algo_path = self.algorithm.search(
                self.environment, self.position, target
            )
            algo_path = self.optimize_path(algo_path)

            stuck_at = algo_path[-1] if algo_path else self.position

            if stuck_at != target:

                bfs_path = bfs.search(self.environment, stuck_at, target)

                if not bfs_path:
                    permanently_unreachable.add(target)
                    segment = self._merge_into_final(
                        final_path, algo_path
                    )
                    final_path = segment
                    self.position = stuck_at
                    continue

                combined = self.join_paths(algo_path, bfs_path)

            else:
                combined = algo_path

            final_path = self._merge_into_final(final_path, combined)

            for pos in combined:
                self.visited.add(pos)

            self.position = target
            self.environment.clean(target)

        return final_path

    def _merge_into_final(self, final_path, segment):

        if not segment:
            return final_path

        if final_path and final_path[-1] == segment[0]:
            return final_path + segment[1:]

        return final_path + segment
