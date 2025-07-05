import os
import time
import heapq
from mazeSamples import maze_test_cases

# Constants
GREEN  = "\033[1;32m"  # Color for start point
RED    = "\033[1;31m"  # Color for end point
HEAD   = "\033[1;34m"  # Color for current position
BLUE   = "\033[1;36m"  # Color for current path
YELLOW = "\033[0;33m"  # Color for traversed nodes

# Function definitions
def manhattan_distance(point_a, point_b):
    """
    Calculate Manhattan distance between two points.
    
    Args:
        point_a (tuple): (x, y) coordinates.
        point_b (tuple): (x, y) coordinates.
    
    Returns:
        int: Manhattan distance.
    """
    return abs(point_a[0] - point_b[0]) + abs(point_a[1] - point_b[1])

def get_neighbors(position, maze):
    """
    Get valid neighboring positions (walkable cells only).
    
    Args:
        position (tuple): Current position (x, y).
        maze (list): 2D grid representing the maze.
        
    Returns:
        list: List of valid neighboring positions.
    """
    x, y = position
    neighbors = []
    for dx, dy in [(0, 1), (1, 0), (0, -1), (-1, 0)]:  # Up, Right, Down, Left
        nx, ny = x + dx, y + dy
        if 0 <= nx < len(maze) and 0 <= ny < len(maze[0]) and maze[nx][ny] == 0:
            neighbors.append((nx, ny))
    return neighbors

def visualize_maze(maze, start, end, current_path, traversed_nodes, step):
    """
    Visualize the maze with current path and traversed nodes.
    
    Args:
        maze (list): The maze grid.
        start (tuple): Starting position.
        end (tuple): Goal position.
        current_path (list): Current path being explored.
        traversed_nodes (list): Nodes that have been traversed.
        step (int): Current step number.
    """
    os.system('cls' if os.name == 'nt' else 'clear')
    
    if not hasattr(visualize_maze, 'prev_path'):
        visualize_maze.prev_path = []
    
    current_position = current_path[-1] if current_path else start
    backtracking = False
    if visualize_maze.prev_path:
        if not (len(current_path) == len(visualize_maze.prev_path) + 1 and 
                all(current_path[i] == visualize_maze.prev_path[i] for i in range(len(visualize_maze.prev_path)))):
            backtracking = True

    visualize_maze.prev_path = current_path.copy()
    h_value = manhattan_distance(current_position, end)
    print(f"Current position: {current_position}, Heuristic (Manhattan distance): {h_value}")
    print(f"Nodes expanded: {len(traversed_nodes)}")
    
    delay = 0.1
    if step == 1:
        explanation = "Starting search from initial position..."
    elif current_position == end:
        explanation = "Goal reached! Path found."
    elif backtracking:
        delay = 0.5
        explanation = "Backtracking: Exploring a different path with better cost..."
    else:
        explanation = "Exploring: Moving to a promising position..."
    
    print(explanation)
    
    for i in range(len(maze)):
        for j in range(len(maze[0])):
            pos = (i, j)
            if pos == start:
                print(f"{GREEN}S", end="\033[0m ")
            elif pos == end:
                print(f"{RED}E", end="\033[0m ")
            elif pos == current_position:
                print(f"{HEAD}@", end="\033[0m ")
            elif pos in current_path:
                print(f"{BLUE}*", end="\033[0m ")
            elif pos in traversed_nodes:
                print(f"{YELLOW}.", end="\033[0m ")
            elif maze[i][j] == 1:
                print("0", end=" ")
            else:
                print(" ", end=" ")
        print()
    print()
    time.sleep(delay)

def astar(start, end, maze, visualize=False):
    """
    Solve the maze using A* algorithm.
    
    Args:
        start (list): Starting position [x, y].
        end (list): Goal position [x, y].
        maze (list): 2D grid representing the maze.
        visualize (bool): Whether to visualize the search process.
        
    Returns:
        tuple: (path, nodes_expanded, time_taken, traversed_nodes)
    """
    start_time = time.time()
    start, end = tuple(start), tuple(end)
    
    position_id = 0  # Tie-breaker for items with same priority
    # Priority queue: (f_score, position_id, current, path, g_score)
    frontier = [(manhattan_distance(start, end), position_id, start, [start], 0)]
    heapq.heapify(frontier)
    
    visited = {start: 0}  # Track visited nodes with their g_scores
    nodes_traversed = 0
    traversed_nodes = []
    step = 0

    while frontier:
        f_score, _, current, path, g_score = heapq.heappop(frontier)
        traversed_nodes.append(current)
        nodes_traversed = len(traversed_nodes)
        
        if visualize:
            visualize_maze(maze, start, end, path, traversed_nodes, nodes_traversed)
        
        if current == end:
            time_taken = time.time() - start_time
            if visualize:
                visualize_maze(maze, start, end, path, traversed_nodes, step + 1)
                print("Path found! Press Enter to continue...")
                input()
            return path, nodes_traversed, time_taken, traversed_nodes
        
        for neighbor in get_neighbors(current, maze):
            new_g_score = g_score + 1  # Cost to move to neighbor
            if neighbor not in visited or new_g_score < visited[neighbor]:
                visited[neighbor] = new_g_score
                h_score = manhattan_distance(neighbor, end)
                f_score = new_g_score + h_score
                new_path = path + [neighbor]
                position_id += 1
                heapq.heappush(frontier, (f_score, position_id, neighbor, new_path, new_g_score))
    
    time_taken = time.time() - start_time
    if visualize:
        visualize_maze(maze, start, end, [], traversed_nodes, step + 1)
        print("No path found! Press Enter to continue...")
        input()
    return [], nodes_traversed, time_taken, traversed_nodes

def solve_mazes():
    """
    Solve all maze test cases and print a summary of the results.
    """
    results = []
    print("Tip: Visualize only if using an IDE or CLI rather than an online compiler.")
    visualize_option = input("Do you want to visualize maze traversals? (y/n): ").strip().lower() == 'y'
    
    if visualize_option:
        while True:
            print("\nWhich test case would you like to visualize?")
            for i, test_case in enumerate(maze_test_cases, 1):
                start_point = tuple(test_case["start"])
                end_point = tuple(test_case["end"])
                print(f"  {i}. Case {i}: Start {start_point} -> End {end_point}")
            print("  0. Exit visualization and run all tests")
    
            try:
                choice = int(input("Enter your choice: "))
                if choice == 0:
                    break
                if 1 <= choice <= len(maze_test_cases):
                    test_case = maze_test_cases[choice - 1]
                    astar(test_case["start"], test_case["end"], test_case["maze"], visualize=True)
                else:
                    print("Invalid choice. Please try again.")
            except ValueError:
                print("Invalid input. Please enter a number.")
    print("\nRunning all test cases to generate summary...")
    
    for i, test_case in enumerate(maze_test_cases, 1):
        maze = test_case["maze"]
        start_point = test_case["start"]
        end_point = test_case["end"]
        path, nodes_expanded, time_taken, traversed_nodes = astar(start_point, end_point, maze, visualize=False)
    
        solution_found = bool(path)
        steps = len(path) - 1 if solution_found else 0
        results.append({
            "maze_num": i,
            "start": start_point,
            "end": end_point,
            "solution_found": "Yes" if solution_found else "No",
            "steps": steps,
            "time": time_taken,
            "nodes_expanded": nodes_expanded,
        })
    
    # Print summary tables
    print("\nTest Result")
    print("+--------+----------+----------+----------------+")
    print("| Maze # | Start    | Goal     | Solution Found |")
    print("+--------+----------+----------+----------------+")
    for result in results:
        print(f"| {result['maze_num']:^6} | "
              f"{str(tuple(result['start'])):^8} | "
              f"{str(tuple(result['end'])):^8} | "
              f"{result['solution_found']:^14} |")
    print("+--------+----------+----------+----------------+")
    
    print("\n\nAlgorithm Performance Metrics for A*")
    print("+--------+---------------------+-------------------+-------------------+-------------------+")
    print("| Maze # | Time (s)            | Nodes Traversed   | Path Length       | Branching Factor  |")
    print("+--------+---------------------+-------------------+-------------------+-------------------+")
    for result in results:
        path_length = result['steps'] + 1 if result['solution_found'] == "Yes" else 0
        branching_factor = (result['nodes_expanded'] / path_length) if path_length > 0 else 0
        print(f"| {result['maze_num']:^6} | "
              f"{result['time']:<19.16f} | "
              f"{result['nodes_expanded']:^17} | "
              f"{path_length:^17} | "
              f"{branching_factor:^17.2f} |")
    print("+--------+---------------------+-------------------+-------------------+-------------------+")

if __name__ == "__main__":
    solve_mazes()