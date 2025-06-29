import matplotlib.pyplot as plt
from collections import deque

# Define the maze (0 = path, 1 = wall)
maze = [
    [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
    [1,0,0,0,1,0,0,0,0,1,0,1,0,0,0,1,0,0,0,1],
    [1,1,1,0,1,0,1,1,0,1,0,1,1,1,0,1,1,1,0,1],
    [1,0,0,0,1,0,1,0,0,0,0,0,0,1,0,0,0,1,0,1],
    [1,0,1,1,1,0,1,0,1,1,1,1,0,1,1,1,0,1,0,1],
    [1,0,1,0,0,0,1,0,1,0,0,1,0,0,0,1,0,1,0,1],
    [1,0,1,0,1,1,1,0,1,0,1,1,1,1,0,1,0,1,0,1],
    [1,0,1,0,0,0,0,0,1,0,0,0,0,1,0,0,0,1,0,1],
    [1,0,1,1,1,1,1,1,1,1,1,1,0,1,1,1,0,1,0,1],
    [1,0,0,0,0,0,0,0,0,0,0,1,0,0,0,1,0,0,0,1],
    [1,1,1,1,1,1,1,1,1,1,0,1,1,1,0,1,1,1,1,1],
    [1,0,0,0,0,0,0,0,0,1,0,0,0,1,0,0,0,0,0,1],
    [1,0,1,1,1,1,1,1,0,1,1,1,0,1,1,1,1,1,0,1],
    [1,0,1,0,0,0,0,1,0,0,0,1,0,0,0,0,0,1,0,1],
    [1,0,1,0,1,1,0,1,1,1,0,1,1,1,1,1,0,1,0,1],
    [1,0,1,0,1,0,0,0,0,1,0,0,0,0,0,1,0,1,0,1],
    [1,0,1,1,1,1,1,1,0,1,1,1,1,1,0,1,0,1,0,1],
    [1,0,0,0,0,0,0,1,0,0,0,0,0,1,0,0,0,1,0,1],
    [1,1,1,1,1,1,0,1,1,1,1,1,0,1,1,1,1,1,0,1],
    [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
]

start = (1, 1)
goal = (17, 18)

# BFS function
def bfs(maze, start, goal):
    rows, cols = len(maze), len(maze[0])
    visited = set()
    came_from = {}
    queue = deque([start])
    visited.add(start)

    while queue:
        current = queue.popleft()
        if current == goal:
            break

        r, c = current
        for dr, dc in [(-1,0), (1,0), (0,-1), (0,1)]:
            nr, nc = r + dr, c + dc
            neighbor = (nr, nc)
            if (0 <= nr < rows and 0 <= nc < cols and 
                maze[nr][nc] == 0 and neighbor not in visited):
                queue.append(neighbor)
                visited.add(neighbor)
                came_from[neighbor] = current

    # Reconstruct path
    path = []
    node = goal
    while node in came_from:
        path.append(node)
        node = came_from[node]
    if path:
        path.append(start)
        path.reverse()
    return path

# Get the BFS path
path = bfs(maze, start, goal)

# Print result
if path:
    print(f"✅ Path found! Steps: {len(path)}")
    print("Path:", path)
else:
    print("❌ No path found.")

# Optional: Visualize
def plot_maze(maze, path):
    maze_display = [[1 if cell == 1 else 0.2 for cell in row] for row in maze]
    for r, c in path:
        maze_display[r][c] = 0.6

    plt.figure(figsize=(10, 10))
    plt.imshow(maze_display, cmap="gray")
    plt.title("BFS Path")
    plt.xticks([])
    plt.yticks([])
    plt.show()

# Uncomment to visualize:
# plot_maze(maze, path)
