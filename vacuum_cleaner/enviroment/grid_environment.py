class GridEnvironment:

    def __init__(self, grid):

        self.grid = grid

        self.rows = len(grid)

        self.cols = len(grid[0])

    def is_valid(self, row, col):

        return (
            0 <= row < self.rows
            and
            0 <= col < self.cols
            and
            self.grid[row][col] != -1
        )

    def get_neighbors(self, position):

        row, col = position

        directions = [
            (-1, 0),  # UP
            (1, 0),   # DOWN
            (0, -1),  # LEFT
            (0, 1)    # RIGHT
        ]

        neighbors = []

        for dr, dc in directions:

            nr = row + dr
            nc = col + dc

            if self.is_valid(nr, nc):
                neighbors.append((nr, nc))

        return neighbors

    def get_dirty_cells(self):

        dirty = []

        for r in range(self.rows):
            for c in range(self.cols):

                if self.grid[r][c] == 1:
                    dirty.append((r, c))

        return dirty

    def clean(self, position):

        r, c = position

        if self.grid[r][c] == 1:
            self.grid[r][c] = 0