import random

class Maze:
    def __init__(self, level, ghostNumber):
        # Set the dimensions of the maze
        self.num_cells_x = 29
        self.num_cells_y = 26
        # Initialize all cells as walls (0)
        self.grid = [[0 for _ in range(self.num_cells_y)] for _ in range(self.num_cells_x)]
        # Stack for depth-first search algorithm
        self.stack = []
        # Wall list for Prim's algorithm
        self.walls = []
        # Ghost number to be added
        self.ghost_number = ghostNumber
        # Determine the starting cell based on the level
        level_start = random.randint(1, 10)
        #print(f"Level {level}, Starting Number: {level_start}")

        # Calculate starting cell based on level_start
        start_x = random.randint(1, self.num_cells_x - 2)
        start_y = random.randint(1, self.num_cells_y - 2)
        self.current_cell = (start_x, start_y)
        self.grid[self.current_cell[0]][self.current_cell[1]] = 1
        # For Prim's algorithm, add the neighboring walls of the starting cell
        self.add_walls(start_x, start_y)
        self.stack.append(self.current_cell)


    def generate(self, method='prims'):
        if method == 'prims':
            self.generate_prims()
        else:
            self.generate_dfs()


    def generate_dfs(self):
        # Run the DFS algorithm until the stack is empty
        while self.stack:
            self.step()

        # Enhance each array in the original list by adding a 0 at the beginning and at the end
        originalGrid = self.grid
        enhanced_list = [[0] + array + [0] for array in originalGrid]
        # Extend the list to size 31 by adding an array of size 28 filled with 0 at the beginning and at the end
        enhanced_list.insert(0, [0] * 28)  # Insert at the beginning
        enhanced_list.append([0] * 28)  # Append at the end
        # add wall aroun the maze
        self.grid = enhanced_list

    def step(self):
        # Process one step in the DFS
        cx, cy = self.stack[-1]
        neighbors = self.find_unvisited_neighbors(cx, cy)

        if neighbors:
            # Choose a random unvisited neighbor
            next_cell = random.choice(neighbors)
            # Remove wall between current cell and chosen neighbor
            self.remove_walls(cx, cy, next_cell)
            nx, ny = next_cell
            # Mark the new cell as a path
            self.grid[nx][ny] = 1
            # Add the new cell to the stack
            self.stack.append(next_cell)
        else:
            # Backtrack if no unvisited neighbors are found
            self.stack.pop()

    def find_unvisited_neighbors(self, x, y):
        # Find unvisited neighbors that are two cells away
        neighbors = []
        directions = [(-2, 0), (0, -2), (2, 0), (0, 2)]
        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            if 0 <= nx < self.num_cells_x and 0 <= ny < self.num_cells_y and self.grid[nx][ny] == 0:
                neighbors.append((nx, ny))
        return neighbors

    def remove_walls(self, x, y, next_cell):
        # Calculate the position of the wall between current and next cells
        nx, ny = next_cell
        mx, my = (x + nx) // 2, (y + ny) // 2
        # Remove the wall to create a path
        self.grid[mx][my] = 1


    def generate_prims(self):
        # Start with a random cell, mark it as part of the maze
        start_x = random.randint(1, self.num_cells_x - 2)
        start_y = random.randint(1, self.num_cells_y - 2)
        self.grid[start_x][start_y] = 1
        self.add_walls(start_x, start_y)

        while self.walls:
            # Choose a random wall from the list
            wall = random.choice(self.walls)
            self.walls.remove(wall)
            x, y = wall

            # Check if the wall divides a cell in the maze and a cell not in the maze
            if self.is_valid_wall(x, y):
                # Make the wall a passage
                self.grid[x][y] = 1
                # Add the neighboring walls of the cell to the wall list
                self.add_walls(x, y)

    def add_walls(self, x, y):
        # Add walls of a cell to the walls list if the opposite cell is not visited
        if x > 1 and self.grid[x - 2][y] == 0:
            self.walls.append((x - 1, y))
        if x < self.num_cells_x - 2 and self.grid[x + 2][y] == 0:
            self.walls.append((x + 1, y))
        if y > 1 and self.grid[x][y - 2] == 0:
            self.walls.append((x, y - 1))
        if y < self.num_cells_y - 2 and self.grid[x][y + 2] == 0:
            self.walls.append((x, y + 1))

    def is_valid_wall(self, x, y):
        # Check if the wall divides a cell in the maze and a cell not in the maze
        neighbors = [(x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)]
        visited_neighbors = [n for n in neighbors if self.grid[n[0]][n[1]] == 1]
        return len(visited_neighbors) == 1 and self.grid[x][y] == 0


    def place_ghosts(self, candidate_spawn_locations):
        # Place a specified number of ghosts ('G') randomly in the maze
        numberOfGhosts = self.ghost_number
        if candidate_spawn_locations == []:
            self.place_ghosts_randomly()
        else:
            for _ in range(numberOfGhosts):
                max_number = len(candidate_spawn_locations)
                min_number = 0
                selected_index = random.randint(min_number, max_number-1)
                x, y = candidate_spawn_locations[selected_index]
                self.grid[x][y] = 'G'
                candidate_spawn_locations.pop(selected_index)
                self.ghost_number-=1

    def place_ghosts_randomly(self):
        # Place a specified number of ghosts ('G') randomly in the maze
        numberOfGhosts = self.ghost_number
        for _ in range(numberOfGhosts):
            x, y = random.randint(0, self.num_cells_x - 1), random.randint(0, self.num_cells_y - 1)
            while self.grid[x][y] != 1:
                x, y = random.randint(0, self.num_cells_x - 1), random.randint(0, self.num_cells_y - 1)
            self.grid[x][y] = 'G'

    def get_maze(self):
        # Return the current state of the maze
        return self.grid


"""
#%%  Example usage
levelNumber = 1
ghostNumber = 2
maze = Maze(levelNumber, ghostNumber)
maze.generate() # generate maze
maze.place_ghosts(list())  # place ghosts
generated_maze = maze.get_maze() # get maze
# print maze
for row in generated_maze:
    print(' '.join(str(cell) for cell in row))
"""
