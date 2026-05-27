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
            (-1, 0),
            (1, 0),
            (0, -1),
            (0, 1)
        ]

        neighbors = []

        for dr, dc in directions:

            nr = row + dr
            nc = col + dc

            if (
                0 <= nr < self.rows
                and 0 <= nc < self.cols
                and self.grid[nr][nc] != -1
            ):
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