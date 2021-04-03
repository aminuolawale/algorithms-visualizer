from tkinter import *
import math
from typing import Tuple, List
from time import sleep
from queue import SimpleQueue as Queue


class ShortestPath:
    def __init__(self, cell_size=30, grid_size=(20, 20)):
        self.root = Tk()
        self.canvas = Canvas(self.root)
        self.cell_size = cell_size
        self.rows = grid_size[0]
        self.cols = grid_size[1]
        self.padding = 10
        self.start_set = False
        self.start_color = "#005eff"
        self.end_set = False
        self.end_color = "#00ff44"
        self.obstacles_set = False
        self.grid = [[0 for _ in range(self.cols)] for _ in range(self.rows)]
        self.visited = []

    def draw(self):
        start_button = Button(text="Start Search", command=self.start_search)
        reset_button = Button(text="Reset", command=self.reset)
        for i in range(self.rows):
            for j in range(self.cols):
                c = self.canvas.create_rectangle(
                    self.padding + j * self.cell_size,
                    self.padding + i * self.cell_size,
                    self.padding + (j + 1) * self.cell_size,
                    self.padding + (i + 1) * self.cell_size,
                    outline="#c9c9c9",
                    fill="#fff",
                )
        start_button.pack()
        reset_button.pack()
        self.canvas.bind("<Button-1>", lambda e: self.callback(e))
        self.canvas.pack(fill=BOTH, expand=1)
        self.root.mainloop()

    def reset(self):
        self.start_set = False
        self.end_set = False
        self.grid = [[0 for _ in range(self.cols)] for _ in range(self.rows)]
        for i, r in enumerate(self.grid):
            for j, _ in enumerate(r):
                self.canvas.itemconfig(j + 1 + self.cols * i, fill="#fff")

    def callback(self, e):
        xclick = e.x
        yclick = e.y
        jlock = math.ceil(float(xclick - self.padding) / self.cell_size) - 1
        ilock = math.ceil(float(yclick - self.padding) / self.cell_size) - 1
        coordinate_index = jlock + 1 + self.cols * ilock
        coordinate = (ilock, jlock)
        if not self.start_set:
            self.start_set = True
            self.start = coordinate
            color = self.start_color
        elif not self.end_set:
            if coordinate == self.start:
                return
            self.end_set = True
            self.end = coordinate
            color = self.end_color
        else:
            if coordinate in [self.start, self.end]:
                return
            self.obstacle_set = True
            self.grid[ilock][jlock] = 1 if not self.grid[ilock][jlock] else 0
            color = "#000" if self.grid[ilock][jlock] else "#fff"
        self.canvas.itemconfig(coordinate_index, fill=color)

    def start_search(self):
        if not self.start_set and not self.end_set:
            print("start and end not set")

        path = self.shortest_path(self.start, self.end, self.grid)
        for a in path[1:-1]:
            self.canvas.itemconfig(a[1] + 1 + self.cols * a[0], fill="#fff200")

    def shortest_path(
        self, start: Tuple[int, int], end: Tuple[int, int], grid: List[List[int]]
    ) -> List[int]:
        num_rows = len(grid)
        num_cols = len(grid[0])
        grid_size = num_rows * num_cols
        ancestors = [None for _ in range(grid_size)]
        visited = [False for _ in range(grid_size)]
        if start == end:
            return [start]
        if grid[start[0]][start[1]] == 1:
            print("invalid start position")
            return []
        if grid[end[0]][end[1]] == 1:
            print("invalid end position")
            return []

        def bfs(start) -> List[int]:
            nonlocal grid
            nonlocal ancestors
            nonlocal visited
            nonlocal num_rows
            nonlocal num_cols
            q = Queue()
            q.put(start)
            visited[self.coordinate_to_index(start, num_rows, num_cols)] = True

            while not q.empty():
                position = q.get()
                neighbors = self.get_neighbors(position, grid)
                for neighbor in neighbors:
                    if (
                        grid[neighbor[0]][neighbor[1]] == 0
                        and not visited[
                            self.coordinate_to_index(neighbor, num_rows, num_cols)
                        ]
                    ):
                        q.put(neighbor)
                        visited[
                            self.coordinate_to_index(neighbor, num_rows, num_cols)
                        ] = True

                        ancestors[
                            self.coordinate_to_index(neighbor, num_rows, num_cols)
                        ] = position
            return ancestors

        ancestor_array = bfs(start)
        return self.build_path(start, end, ancestor_array, num_rows, num_cols)

    def get_neighbors(
        self, position: Tuple[int, int], grid: List[List[int]]
    ) -> List[Tuple[int, int]]:
        # north south west east
        result = []
        row_offset = [-1, 1, 0, 0]
        col_offset = [0, 0, -1, 1]
        cardinal_directions = 4
        for i in range(cardinal_directions):
            r = position[0] + row_offset[i]
            c = position[1] + col_offset[i]
            if r > -1 and r < len(grid) and c > -1 and c < len(grid[0]):
                if grid[r][c] == 0:
                    result.append((r, c))
        return result

    def coordinate_to_index(
        self, coord: Tuple[int, int], num_rows: int, num_cols: int
    ) -> int:
        return coord[1] + coord[0] * num_cols

    def build_path(
        self,
        start: Tuple[int, int],
        end: Tuple[int, int],
        ancestor_array: List[int],
        num_rows: int,
        num_cols: int,
    ) -> List[int]:
        path = []
        iterator = end
        while True:
            path.append(iterator)
            if iterator == start:
                break
            ancestor = ancestor_array[
                self.coordinate_to_index(iterator, num_rows, num_cols)
            ]
            iterator = ancestor
        path = list(reversed(path))
        return path


if __name__ == "__main__":
    shortest_path = ShortestPath()
    shortest_path.draw()