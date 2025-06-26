import tkinter as tk
from tkinter import ttk, messagebox
import random
from collections import deque
import heapq
import time

class MazeGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Maze Path Finder")
        self.cell_size = 30
        self.maze = []
        self.rows = 10
        self.cols = 10
        self.start = (0, 0)
        self.goal = (9, 9)
        self.path = []
        self.setup_gui()

    def setup_gui(self):
        # Control frame
        control_frame = ttk.Frame(self.root)
        control_frame.grid(row=0, column=0, padx=5, pady=5, sticky="ew")

        # Size inputs
        ttk.Label(control_frame, text="Rows:").grid(row=0, column=0, padx=5)
        self.rows_entry = ttk.Entry(control_frame, width=5)
        self.rows_entry.insert(0, "10")
        self.rows_entry.grid(row=0, column=1, padx=5)

        ttk.Label(control_frame, text="Cols:").grid(row=0, column=2, padx=5)
        self.cols_entry = ttk.Entry(control_frame, width=5)
        self.cols_entry.insert(0, "10")
        self.cols_entry.grid(row=0, column=3, padx=5)

        # Algorithm selection
        ttk.Label(control_frame, text="Algorithm:").grid(row=0, column=4, padx=5)
        self.algo_var = tk.StringVar(value="DFS")
        algo_menu = ttk.OptionMenu(control_frame, self.algo_var, "DFS", "DFS", "BFS", "A*")
        algo_menu.grid(row=0, column=5, padx=5)

        # Buttons
        ttk.Button(control_frame, text="Generate Maze", command=self.generate_maze).grid(row=0, column=6, padx=5)
        ttk.Button(control_frame, text="Find Path", command=self.find_path).grid(row=0, column=7, padx=5)
        ttk.Button(control_frame, text="Clear", command=self.clear_canvas).grid(row=0, column=8, padx=5)

        # Canvas for maze
        self.canvas = tk.Canvas(self.root, width=300, height=300, bg="white")
        self.canvas.grid(row=1, column=0, padx=5, pady=5)

    def generate_maze(self):
        try:
            self.rows = int(self.rows_entry.get())
            self.cols = int(self.cols_entry.get())
            if self.rows < 5 or self.cols < 5 or self.rows > 50 or self.cols > 50:
                messagebox.showerror("Error", "Rows and columns must be between 5 and 50.")
                return
        except ValueError:
            messagebox.showerror("Error", "Please enter valid numbers for rows and columns.")
            return

        self.maze = [[1 for _ in range(self.cols)] for _ in range(self.rows)]

        # Generate maze using recursive backtracking
        stack = [(1, 1)]
        self.maze[1][1] = 0
        directions = [(0, 2), (2, 0), (0, -2), (-2, 0)]

        while stack:
            x, y = stack[-1]
            random.shuffle(directions)
            neighbors = []

            for dx, dy in directions:
                nx, ny = x + dx, y + dy
                if 0 < nx < self.rows-1 and 0 < ny < self.cols-1 and self.maze[nx][ny] == 1:
                    neighbors.append((nx, ny))

            if neighbors:
                nx, ny = random.choice(neighbors)
                self.maze[nx][ny] = 0
                self.maze[x + (nx-x)//2][y + (ny-y)//2] = 0
                stack.append((nx, ny))
            else:
                stack.pop()

        # Find valid start and goal points from open cells
        open_cells = [(i, j) for i in range(self.rows) for j in range(self.cols) if self.maze[i][j] == 0]
        if len(open_cells) < 2:
            messagebox.showerror("Error", "Maze generation failed to create enough open paths.")
            return
        self.start = open_cells[0]
        self.goal = open_cells[-1]  # Choose different points, ideally far apart
        self.maze[self.start[0]][self.start[1]] = 0
        self.maze[self.goal[0]][self.goal[1]] = 0

        self.draw_maze()

    def draw_maze(self):
        self.canvas.delete("all")
        canvas_width = self.cols * self.cell_size
        canvas_height = self.rows * self.cell_size
        self.canvas.config(width=canvas_width, height=canvas_height)

        for i in range(self.rows):
            for j in range(self.cols):
                x1 = j * self.cell_size
                y1 = i * self.cell_size
                x2 = x1 + self.cell_size
                y2 = y1 + self.cell_size
                color = "black" if self.maze[i][j] == 1 else "white"
                if (i, j) == self.start:
                    color = "green"
                elif (i, j) == self.goal:
                    color = "red"
                self.canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline="gray")

    def find_path(self):
        if not self.maze:
            messagebox.showerror("Error", "Please generate a maze first.")
            return

        algo = self.algo_var.get()
        if algo == "DFS":
            self.path = self.dfs()
        elif algo == "BFS":
            self.path = self.bfs()
        else:
            self.path = self.a_star()

        if not self.path:
            messagebox.showinfo("Result", "No path found!")
        else:
            self.animate_path()

    def dfs(self):
        stack = [(self.start, [self.start])]
        visited = set()

        while stack:
            (x, y), path = stack.pop()
            if (x, y) == self.goal:
                return path
            if (x, y) in visited:
                continue
            visited.add((x, y))

            for dx, dy in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
                nx, ny = x + dx, y + dy
                if 0 <= nx < self.rows and 0 <= ny < self.cols and self.maze[nx][ny] == 0 and (nx, ny) not in visited:
                    stack.append(((nx, ny), path + [(nx, ny)]))
        return []

    def bfs(self):
        queue = deque([(self.start, [self.start])])
        visited = set()

        while queue:
            (x, y), path = queue.popleft()
            if (x, y) == self.goal:
                return path
            if (x, y) in visited:
                continue
            visited.add((x, y))

            for dx, dy in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
                nx, ny = x + dx, y + dy
                if 0 <= nx < self.rows and 0 <= ny < self.cols and self.maze[nx][ny] == 0 and (nx, ny) not in visited:
                    queue.append(((nx, ny), path + [(nx, ny)]))
        return []

    def a_star(self):
        def heuristic(a, b):
            return abs(a[0] - b[0]) + abs(a[1] - b[1])

        open_list = [(0, self.start, [self.start])]
        closed = set()
        g_score = {self.start: 0}

        while open_list:
            f, (x, y), path = heapq.heappop(open_list)
            if (x, y) == self.goal:
                return path
            if (x, y) in closed:
                continue
            closed.add((x, y))

            for dx, dy in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
                nx, ny = x + dx, y + dy
                if 0 <= nx < self.rows and 0 <= ny < self.cols and self.maze[nx][ny] == 0 and (nx, ny) not in closed:
                    new_g = g_score[(x, y)] + 1
                    if (nx, ny) not in g_score or new_g < g_score[(nx, ny)]:
                        g_score[(nx, ny)] = new_g
                        f_score = new_g + heuristic((nx, ny), self.goal)
                        heapq.heappush(open_list, (f_score, (nx, ny), path + [(nx, ny)]))
        return []

    def animate_path(self):
        self.draw_maze()
        for i, (x, y) in enumerate(self.path[1:-1], 1):
            self.canvas.after(i * 100, self.draw_path_cell, x, y)
        self.root.update()

    def draw_path_cell(self, x, y):
        x1 = y * self.cell_size
        y1 = x * self.cell_size
        x2 = x1 + self.cell_size
        y2 = y1 + self.cell_size
        self.canvas.create_rectangle(x1, y1, x2, y2, fill="blue", outline="gray")

    def clear_canvas(self):
        self.maze = []
        self.path = []
        self.canvas.delete("all")

if __name__ == "__main__":
    root = tk.Tk()
    app = MazeGame(root)
    root.mainloop()