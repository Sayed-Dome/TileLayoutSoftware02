import pygame

# Initialize Pygame
pygame.init()

# Set the screen dimensions
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))

# Set the title of the window
pygame.display.set_caption("Tile Layout Editor")

# Define the grid size and tile size
grid_size = 10
tile_size = 50

# Create a 2D array to represent the grid
grid = [[0 for _ in range(grid_size)] for _ in range(grid_size)]

# Define the tile colors
tile_colors = [(255, 0, 0), (0, 255, 0), (0, 0, 255)]

# Define the tile being dragged
dragged_tile = None

# Main loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            # Get the mouse position
            mouse_x, mouse_y = event.pos

            # Check if a tile is being clicked
            for i in range(grid_size):
                for j in range(grid_size):
                    if (i * tile_size < mouse_x < (i + 1) * tile_size and
                            j * tile_size < mouse_y < (j + 1) * tile_size):
                        # Set the dragged tile
                        dragged_tile = (i, j)
                        break
        elif event.type == pygame.MOUSEBUTTONUP:
            # Reset the dragged tile
            dragged_tile = None
        elif event.type == pygame.MOUSEMOTION and dragged_tile is not None:
            # Get the mouse position
            mouse_x, mouse_y = event.pos

            # Move the dragged tile to the new position
            grid[dragged_tile[1]][dragged_tile[0]] = 0
            grid[mouse_y // tile_size][mouse_x // tile_size] = 1

    # Draw the grid
    screen.fill((255, 255, 255))
    for i in range(grid_size):
        for j in range(grid_size):
            if grid[j][i] == 1:
                pygame.draw.rect(screen, tile_colors[0], (i * tile_size, j * tile_size, tile_size, tile_size))
            pygame.draw.rect(screen, (0, 0, 0), (i * tile_size, j * tile_size, tile_size, tile_size), 1)

    # Update the screen
    pygame.display.flip()
