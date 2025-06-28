import random

def generate_maze(width, height):
    # Initialize the maze with walls (1)
    maze = [[1] * width for _ in range(height)]

    def carve_path(x, y):
        directions = [(0, -2), (0, 2), (-2, 0), (2, 0)]  # Up, Down, Left, Right
        random.shuffle(directions)

        for dx, dy in directions:
            nx, ny = x + dx, y + dy

            if 0 <= nx < width and 0 <= ny < height and maze[ny][nx] == 1:
                maze[y + dy // 2][x + dx // 2] = 0
                maze[ny][nx] = 0
                carve_path(nx, ny)

    # Start carving from a random odd-numbered cell
    start_x, start_y = 1, 1
    maze[start_y][start_x] = 0
    carve_path(start_x, start_y)

    # Ensure the outer border is made of walls
    for i in range(width):
        maze[0][i] = 1
        maze[height - 1][i] = 1
    for i in range(height):
        maze[i][0] = 1
        maze[i][width - 1] = 1

    return maze

maze = generate_maze(30, 30)

for row in maze:
    row_str = ""
    for cell in row:
        if cell == 1:
            row_str += "#"
        else:
            row_str += " "
    print(row_str)