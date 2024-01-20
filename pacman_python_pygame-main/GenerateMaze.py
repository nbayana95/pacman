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
        self.player_coordinate = None  # Initialize player_coordinate


    def generate(self, method='prims'):
        if method == 'prims':
            self.generate_prims()
        else:
            self.generate_dfs()

        self.place_player()
        self.place_powerups()
        self.open_portals()


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

    def dfs_step(self):
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
        # Start with a grid full of walls
        self.grid = [[0 for _ in range(self.num_cells_y)] for _ in range(self.num_cells_x)]
        
        # Start with a random cell, mark it as an open path
        start_x = random.randint(1, self.num_cells_x - 2)
        start_y = random.randint(1, self.num_cells_y - 2)
        self.grid[start_x][start_y] = 1

        # Add the walls of the starting cell to the list
        self.add_walls(start_x, start_y)

        while self.walls:
            wall = random.choice(self.walls)
            x, y = wall

            if self.is_valid_wall(x, y):
                self.grid[x][y] = 1  # Carve out a path by turning the wall into an open space
                nx, ny = self.get_opposite_cell(x, y)
                if 0 <= nx < self.num_cells_x and 0 <= ny < self.num_cells_y:
                    self.grid[nx][ny] = 1
                    self.add_walls(nx, ny)

            self.walls.remove(wall)


    def add_walls(self, x, y):
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            if 0 <= nx < self.num_cells_x and 0 <= ny < self.num_cells_y and self.grid[nx][ny] == 0:
                self.walls.append((nx, ny))



    def is_valid_wall(self, x, y):
        opposite_x, opposite_y = self.get_opposite_cell(x, y)
        if opposite_x == -1 or opposite_y == -1:
            return False
        if 0 <= opposite_x < self.num_cells_x and 0 <= opposite_y < self.num_cells_y:
            return self.grid[opposite_x][opposite_y] == 0 and self.grid[x][y] == 0
        return False

    def get_opposite_cell(self, x, y):
        # Determine the direction of the wall and get the opposite cell
        if x % 2 != 0:  # Vertical wall
            if x > 0 and self.grid[x - 1][y] == 0:
                return x - 1, y
            elif x < self.num_cells_x - 1 and self.grid[x + 1][y] == 0:
                return x + 1, y
        elif y % 2 != 0:  # Horizontal wall
            if y > 0 and self.grid[x][y - 1] == 0:
                return x, y - 1
            elif y < self.num_cells_y - 1 and self.grid[x][y + 1] == 0:
                return x, y + 1

        # Return an invalid coordinate if there's no valid opposite cell
        return -1, -1



    def open_portals(self, num_portals = 5):
        suitable_rows = []
        # Check each row for potential portal placement
        for i in range(1, self.num_cells_x - 1):  # Avoid the first and last row
            if self.grid[i][1] != 0 and self.grid[i][self.num_cells_y - 2] != 0:  # Check if 2nd and 2nd-last columns are not walls
                suitable_rows.append(i)

        # Randomly pick rows to open portals
        for _ in range(min(num_portals, len(suitable_rows))):
            row_to_open = random.choice(suitable_rows)
            suitable_rows.remove(row_to_open)  # Remove the chosen row from the list to avoid duplicate selection
            # Open portals by setting the first and last cells in the row to be passageways (not walls)
            self.grid[row_to_open][0] = 1
            self.grid[row_to_open][self.num_cells_y - 1] = 1

    def get_coordinates_that_arent_walls(self):
        not_wall_coordinates = []
        for x in range(1, self.num_cells_x - 1):
            for y in range(1, self.num_cells_y - 1):
                if self.grid[x][y] != 0:  # If the cell is not a wall
                    not_wall_coordinates.append((x, y))
        
        #print(not_wall_coordinates)
        return not_wall_coordinates

    def place_player(self):
        # Get a list of coordinates that are not walls
        not_wall_coordinates = self.get_coordinates_that_arent_walls()
        
        # Randomly select a coordinate from the list
        self.player_coordinate = random.choice(not_wall_coordinates)
        
        # Place the player at the selected coordinate by setting it to "P"
        x, y = self.player_coordinate
        #print("PLAYER COORDINATE", self.player_coordinate)
        self.grid[x][y] = "P"

    def update_player_position(self):
        # Update the player position by setting the previous position to a path
        x, y = self.player_coordinate
        self.grid[x][y] = 1

        # Get a list of coordinates that are not walls
        not_wall_coordinates = self.get_coordinates_that_arent_walls()

        # Randomly select a coordinate from the list
        self.player_coordinate = random.choice(not_wall_coordinates)

        # Place the player at the selected coordinate by setting it to "P"
        x, y = self.player_coordinate
        self.grid[x][y] = "P"
        return self.player_coordinate

    def place_powerups(self, num_powerups = 7):
        # Get a list of coordinates that are not walls
        not_wall_coordinates = self.get_coordinates_that_arent_walls()

        # Remove the player's coordinate from the list to avoid placing power-ups on the player
        if self.player_coordinate in not_wall_coordinates:
            not_wall_coordinates.remove(self.player_coordinate)

        # Randomly select unique coordinates for power-ups, ensuring no duplicates
        powerup_positions = random.sample(not_wall_coordinates, min(num_powerups, len(not_wall_coordinates)))
        
        # Place power-ups at the selected coordinates by setting them to "O"
        for x, y in powerup_positions:
            self.grid[x][y] = "O"


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



# Instantiate the maze with a level number and ghost number
levelNumber = 1
ghostNumber = 2
maze = Maze(levelNumber, ghostNumber)

# Generate the maze using Prim's algorithm
maze.generate(method='prims')

# Retrieve the generated maze
generated_maze = maze.get_maze()

# Print the maze
for row in generated_maze:
    print(' '.join(str(cell) for cell in row))