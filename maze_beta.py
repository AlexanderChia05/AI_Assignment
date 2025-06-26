import tkinter as tk
from tkinter import ttk, messagebox
import random
from queue import Queue
import heapq

class MazeGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Maze Sucker - Beta Ver")
        self.min_cell_size = 20
        self.max_cell_size = 50
        self.visited_color = "#ADD8E6"  # Light blue
        self.path_color = "#0000FF"     # Blue (unused as per request)
        self.final_path_color = "#FFFF00"  # Yellow
        self.wall_color = "#000000"     # Black
        self.start_color = "#00FF00"    # Green
        self.goal_color = "#FF0000"     # Red
        self.setup_gui()
        self.root.bind("<Configure>", self.resize_canvas)

    def setup_gui(self):
        self.control_frame = ttk.Frame(self.root)
        self.control_frame.pack(fill=tk.X, padx=10, pady=5)

        ttk.Label(self.control_frame, text="Rows:").pack(side=tk.LEFT, padx=5)
        self.rows_entry = ttk.Entry(self.control_frame, width=5)
        self.rows_entry.insert(0, "10")
        self.rows_entry.pack(side=tk.LEFT, padx=5)

        ttk.Label(self.control_frame, text="Cols:").pack(side=tk.LEFT, padx=5)
        self.cols_entry = ttk.Entry(self.control_frame, width=5)
        self.cols_entry.insert(0, "10")
        self.cols_entry.pack(side=tk.LEFT, padx=5)

        self.algo_var = tk.StringVar(value="BFS")
        algorithms = ["BFS", "DFS", "A*", "Hill Climbing"]
        ttk.Label(self.control_frame, text="Algorithm:").pack(side=tk.LEFT, padx=5)
        self.algo_menu = ttk.OptionMenu(self.control_frame, self.algo_var, "BFS", *algorithms)
        self.algo_menu.pack(side=tk.LEFT, padx=5)

        ttk.Button(self.control_frame, text="Generate Maze", command=self.generate_maze).pack(side=tk.LEFT, padx=5)
        ttk.Button(self.control_frame, text="Solve Maze", command=self.solve_maze).pack(side=tk.LEFT, padx=5)

        self.canvas_frame = ttk.Frame(self.root)
        self.canvas_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        self.canvas = tk.Canvas(self.canvas_frame, bg="white")
        self.canvas.pack(fill=tk.BOTH, expand=True)

        self.maze = None
        self.start = None
        self.goal = None
        self.cells = {}
        self.walls = []
        self.cell_size = self.min_cell_size

    def resize_canvas(self, event=None):
        if not self.maze:
            return
        canvas_width = self.canvas.winfo_width()
        canvas_height = self.canvas.winfo_height()
        rows, cols = len(self.maze), len(self.maze[0])
        # Ensure maze fits within 1920x1200 for 50x50, accounting for control frame (~100px)
        available_height = canvas_height - 100 if canvas_height > 100 else canvas_height
        self.cell_size = min(
            canvas_width // cols,
            available_height // rows,
            self.max_cell_size
        )
        self.cell_size = max(self.cell_size, self.min_cell_size)
        self.draw_maze()

    def generate_maze(self):
        try:
            rows = int(self.rows_entry.get())
            cols = int(self.cols_entry.get())
            if rows < 5 or cols < 5 or rows > 50 or cols > 50:
                messagebox.showerror("Error", "Rows and columns must be between 5 and 50.")
                return
        except ValueError:
            messagebox.showerror("Error", "Please enter valid numbers for rows and columns.")
            return

        # Initialize maze grid with all borders as walls
        self.maze = [[1 for _ in range(cols)] for _ in range(rows)]
        self.cells = {}
        self.walls = []

        # Generate maze using randomized DFS, starting from (1, 1) to preserve borders
        if rows > 2 and cols > 2:
            self.dfs_generate(1, 1, rows, cols)

        # Ensure distinct start and goal, avoiding all borders
        self.start = (1, 1)
        self.goal = (random.randint(1, rows - 2), random.randint(1, cols - 2))
        while self.start == self.goal:
            self.goal = (random.randint(1, rows - 2), random.randint(1, cols - 2))
        self.maze[self.start[0]][self.start[1]] = 0
        self.maze[self.goal[0]][self.goal[1]] = 0

        self.resize_canvas()

    def dfs_generate(self, x, y, rows, cols):
        self.maze[x][y] = 0
        directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
        random.shuffle(directions)
        for dx, dy in directions:
            nx, ny = x + dx * 2, y + dy * 2
            # Avoid carving into border cells
            if 1 <= nx < rows - 1 and 1 <= ny < cols - 1 and self.maze[nx][ny] == 1:
                self.maze[x + dx][y + dy] = 0
                self.dfs_generate(nx, ny, rows, cols)

    def draw_maze(self):
        self.canvas.delete("all")
        self.cells = {}
        self.walls = []
        rows, cols = len(self.maze), len(self.maze[0])
        for i in range(rows):
            for j in range(cols):
                x1 = j * self.cell_size
                y1 = i * self.cell_size
                x2 = x1 + self.cell_size
                y2 = y1 + self.cell_size
                cell_id = self.canvas.create_rectangle(x1, y1, x2, y2, fill="white", outline="")
                self.cells[(i, j)] = cell_id
                if self.maze[i][j] == 1:
                    self.canvas.itemconfig(cell_id, fill="black")
                elif (i, j) == self.start:
                    self.canvas.itemconfig(cell_id, fill=self.start_color)
                elif (i, j) == self.goal:
                    self.canvas.itemconfig(cell_id, fill=self.goal_color)

        # Draw internal walls
        for i in range(rows):
            for j in range(cols):
                x1 = j * self.cell_size
                y1 = i * self.cell_size
                x2 = x1 + self.cell_size
                y2 = y1 + self.cell_size
                if i < rows - 1 and (self.maze[i][j] == 1 or self.maze[i + 1][j] == 1):
                    wall_id = self.canvas.create_line(x1, y2, x2, y2, width=2, fill=self.wall_color)
                    self.walls.append(((i, j), (i + 1, j), wall_id))
                if j < cols - 1 and (self.maze[i][j] == 1 or self.maze[i][j + 1] == 1):
                    wall_id = self.canvas.create_line(x2, y1, x2, y2, width=2, fill=self.wall_color)
                    self.walls.append(((i, j), (i, j + 1), wall_id))

    def solve_maze(self):
        if not self.maze:
            messagebox.showerror("Error", "Please generate a maze first.")
            return
        algo = self.algo_var.get()
        path = None
        visited = set()
        if algo == "BFS":
            path, visited = self.bfs()
        elif algo == "DFS":
            path, visited = self.dfs()
        elif algo == "A*":
            path, visited = self.a_star()
        elif algo == "Hill Climbing":
            path, visited = self.hill_climbing()
        self.animate_solution(path, visited)

    def bfs(self):
        # Complete: Yes, Cost-Optimal: Yes, Time: O(V+E), Space: O(V)
        queue = Queue()
        queue.put([self.start])
        visited = {self.start}
        while not queue.empty():
            path = queue.get()
            x, y = path[-1]
            if (x, y) == self.goal:
                return path, visited
            for dx, dy in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
                nx, ny = x + dx, y + dy
                if 0 <= nx < len(self.maze) and 0 <= ny < len(self.maze[0]) and self.maze[nx][ny] == 0 and (nx, ny) not in visited:
                    visited.add((nx, ny))
                    queue.put(path + [(nx, ny)])
        return [], visited

    def dfs(self):
        # Complete: No (on infinite graphs), Cost-Optimal: No, Time: O(V+E), Space: O(V)
        stack = [[self.start]]
        visited = {self.start}
        while stack:
            path = stack.pop()
            x, y = path[-1]
            if (x, y) == self.goal:
                return path, visited
            for dx, dy in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
                nx, ny = x + dx, y + dy
                if 0 <= nx < len(self.maze) and 0 <= ny < len(self.maze[0]) and self.maze[nx][ny] == 0 and (nx, ny) not in visited:
                    visited.add((nx, ny))
                    stack.append(path + [(nx, ny)])
        return [], visited

    def a_star(self):
        # Complete: Yes, Cost-Optimal: Yes (with consistent heuristic), Time: O(E log V), Space: O(V)
        def heuristic(a, b):
            return abs(a[0] - b[0]) + abs(a[1] - b[1])
        pq = [(0, [self.start])]
        visited = {self.start}
        costs = {self.start: 0}
        while pq:
            f, path = heapq.heappop(pq)
            x, y = path[-1]
            if (x, y) == self.goal:
                return path, visited
            for dx, dy in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
                nx, ny = x + dx, y + dy
                if 0 <= nx < len(self.maze) and 0 <= ny < len(self.maze[0]) and self.maze[nx][ny] == 0 and (nx, ny) not in visited:
                    new_cost = costs[(x, y)] + 1
                    if (nx, ny) not in costs or new_cost < costs[(nx, ny)]:
                        costs[(nx, ny)] = new_cost
                        priority = new_cost + heuristic((nx, ny), self.goal)
                        heapq.heappush(pq, (priority, path + [(nx, ny)]))
                        visited.add((nx, ny))
        return [], visited

    def hill_climbing(self):
        # Complete: No, Cost-Optimal: No, Time: O(V), Space: O(1) for path
        def heuristic(a, b):
            return abs(a[0] - b[0]) + abs(a[1] - b[1])
        path = [self.start]
        visited = {self.start}
        current = self.start
        while current != self.goal:
            neighbors = []
            for dx, dy in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
                nx, ny = current[0] + dx, current[1] + dy
                if 0 <= nx < len(self.maze) and 0 <= ny < len(self.maze[0]) and self.maze[nx][ny] == 0 and (nx, ny) not in visited:
                    neighbors.append((nx, ny))
            if not neighbors:
                return [], visited
            next_cell = min(neighbors, key=lambda x: heuristic(x, self.goal))
            path.append(next_cell)
            visited.add(next_cell)
            current = next_cell
        return path, visited

    def animate_solution(self, path, visited):
        def update_cell(i):
            if i < len(visited_list):
                cell = visited_list[i]
                if cell != self.start and cell != self.goal:
                    self.canvas.itemconfig(self.cells[cell], fill=self.visited_color)
                self.root.after(50, update_cell, i + 1)
            elif i < len(visited_list) + len(path):
                cell = path[i - len(visited_list)]
                if cell != self.start and cell != self.goal:
                    self.canvas.itemconfig(self.cells[cell], fill=self.final_path_color)
                for (c1, c2, wall_id) in self.walls:
                    if (c1 == cell and c2 in path) or (c2 == cell and c1 in path):
                        self.canvas.itemconfig(wall_id, state="hidden")
                self.root.after(50, update_cell, i + 1)

        visited_list = list(visited - {self.start, self.goal})
        update_cell(0)

if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("1920x1200")  # Set initial window size to 1920x1200
    app = MazeGame(root)
    root.mainloop()