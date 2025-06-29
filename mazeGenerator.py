import random

# Maze dimensions
WIDTH = 48
HEIGHT = 48

# Directions: North, East, South, West
DIRECTIONS = [(-2, 0), (0, 2), (2, 0), (0, -2)]

# Initialize maze with all walls (1)
maze = [[1 for _ in range(WIDTH)] for _ in range(HEIGHT)]

def is_valid(x, y):
    return 0 <= x < HEIGHT and 0 <= y < WIDTH

def count_adjacent_paths(x, y):
    """Count the number of adjacent path cells (0s) around (x, y)."""
    count = 0
    for dx, dy in [(-1,0),(1,0),(0,-1),(0,1)]:
        nx, ny = x + dx, y + dy
        if is_valid(nx, ny) and maze[nx][ny] == 0:
            count += 1
    return count

def carve(x, y):
    # Mark current cell as visited (carve it)
    maze[x][y] = 0

    # Shuffle directions to visit neighbors randomly
    random.shuffle(DIRECTIONS)

    for dx, dy in DIRECTIONS:
        nx, ny = x + dx, y + dy
        mx, my = x + dx//2, y + dy//2
        if is_valid(nx, ny) and maze[nx][ny] == 1:
            # Prevent loops: only carve if the midpoint and target have at most one adjacent path
            if count_adjacent_paths(mx, my) <= 1 and count_adjacent_paths(nx, ny) <= 1:
                maze[mx][my] = 0
                carve(nx, ny)

# Start carving from top-left corner (even coordinates required)
carve(1, 1)

# Add one space padding (border) to the bottom and right side
for row in maze:
    row.append(1)
maze.append([1] * (WIDTH + 1))
HEIGHT += 1
WIDTH += 1
# Print the maze
for row in maze:
    print(' '.join(' ' if cell == 0 else '1' for cell in row))

# Find all open cells (0s)
open_cells = [(i, j) for i in range(len(maze)) for j in range(len(maze[0])) if maze[i][j] == 0]

# Focus more on first and second quartile
open_cells_sorted = sorted(open_cells, key=lambda x: (x[0], x[1]))
n = len(open_cells_sorted)
q1 = open_cells_sorted[:n//2]  # First and second quartile (first half)

sampled_cells = random.sample(q1, 20)
random.shuffle(sampled_cells)

print("\n20 random open [row, col] locations (biased to first and second quartile):")
for cell in sampled_cells:
    print(list(cell))

# Output the maze as a Python list in a string
maze_str = "[\n" + ",\n".join(str(row) for row in maze) + "\n]"
print(maze_str)