
import time
import random
class GhostStrategyAI():
    def __init__(self, maze_grid, pacman_start=(0,0), min_distance=10):
        self.maze_grid = maze_grid
        self.pacman_start = pacman_start
        self.min_distance = min_distance
        self.proposed_spawn_locations = list()

    def bfs(self):
        """
        this function generated to run
        breadth-first algorithm -> find potential ghost spawn locations
        """
        # get input values
        maze = self.maze_grid # maze grid in 2D
        start = self.pacman_start # starting location of pacman
        min_distance = self.min_distance # minimum distance to run pacman

        # Determine the size of the maze
        rows, cols = len(maze), len(maze[0])
        # Directions in which to move: right, left, down, up
        directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]
        # Initialize the queue with the starting position and a distance of 0
        queue = [(start[0], start[1], 0)]
        # Set to keep track of visited cells
        visited = set()
        # Process the queue until it's empty
        while queue:
            # Pop the first element from the queue (FIFO)
            x, y, dist = queue.pop(0)
            # Skip if this cell has already been visited
            if (x, y) in visited:
                continue
            # Mark the cell as visited
            visited.add((x, y))
            # If the current cell is at least 'min_distance' steps away, add it to potential spawns
            if dist >= min_distance:
                self.proposed_spawn_locations.append((x, y))
            # Check all adjacent cells
            for dx, dy in directions:
                nx, ny = x + dx, y + dy
                # If the adjacent cell is within the maze, is a path, and not visited, add it to the queue
                if 0 <= nx < rows and 0 <= ny < cols and maze[nx][ny] == 1 and (nx, ny) not in visited:
                    queue.append((nx, ny, dist + 1))

        return self.proposed_spawn_locations

    def newGhostGeneration(self):
        candidate_spawn_locations = self.proposed_spawn_locations

        if len(candidate_spawn_locations)>0:
            max_number = len(candidate_spawn_locations)
            min_number = 0
            selected_index = random.randint(min_number, max_number-1)
            spawn_location = candidate_spawn_locations[selected_index]
            candidate_spawn_locations.pop(selected_index)
            return spawn_location
        else:
            return  None

"""

# Example maze and Pac-Man starting position
maze = [
    [1, 1, 1, 0, 1, 1, 1],
    [1, 0, 0, 0, 0, 0, 1],
    [1, 1, 1, 1, 1, 1, 1],
    [1, 0, 0, 0, 0, 0, 1],
    [1, 1, 1, 0, 1, 1, 1]
]
pacman_start = (0, 0)  # Starting position of Pac-Man
StrategyAI = GhostStrategyAI(maze, pacman_start=(0,0), min_distance=10) # init Ghost Strategy
potential_spawns = StrategyAI.bfs() # get potential spawns

print("Potential Ghost Spawn Locations:")
for loc in potential_spawns:
    print(loc)

i = 100000
last_ghost_spawn_time = time.time()
while i>0:
    i-=1
    if time.time()-last_ghost_spawn_time>60:
        spawn_location = StrategyAI.newGhostGeneration()
        if spawn_location != None:
            print("Generated Ghost Spawn Locations:")
            print(spawn_location)
        else:
            print("No Ghost Spawn Locations Left!")
            pass
        last_ghost_spawn_time = time.time()
"""





