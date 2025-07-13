from collections import deque

def bfs(start, end, maze, visualize=False, ansi=True):
    """
    Solve the maze using Breadth-First Search (BFS).
    
    Args:
        start (list): Starting position [x, y].
        end (list): Goal position [x, y].
        maze (list): 2D grid representing the maze.
        visualize (bool): Whether to visualize the search process.
        ansi (bool): Whether to use ANSI color in visualization.
        
    Returns:
        tuple: (path, nodes_expanded, time_taken, traversed_nodes, peak_memory)
    """
    start_time = time.time()
    start, end = tuple(start), tuple(end)

    queue = deque()
    queue.append((start, [start]))

    visited = {start}
    traversed_nodes = []
    step = 0

    # Start tracing memory
    tracemalloc.start()

    while queue:
        current, path = queue.popleft()
        traversed_nodes.append(current)
        step += 1

        if visualize:
            visualize_maze(maze, start, end, path, traversed_nodes, step, ansi=ansi)

        if current == end:
            time_taken = time.time() - start_time
            peak_memory = tracemalloc.get_traced_memory()[1]
            tracemalloc.stop()
            if visualize:
                visualize_maze(maze, start, end, path, traversed_nodes, step + 1, ansi=ansi)
                print("Path found! Press Enter to continue...")
                input()
            return path, len(traversed_nodes), time_taken, traversed_nodes, peak_memory

        for neighbor in get_neighbors(current, maze):
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append((neighbor, path + [neighbor]))

    time_taken = time.time() - start_time
    peak_memory = tracemalloc.get_traced_memory()[1]
    tracemalloc.stop()
    if visualize:
        visualize_maze(maze, start, end, [], traversed_nodes, step + 1, ansi=ansi)
        print("No path found! Press Enter to continue...")
        input()
    return [], len(traversed_nodes), time_taken, traversed_nodes, peak_memory
