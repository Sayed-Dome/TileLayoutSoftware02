import pygame
import pickle
import sys
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

# Define the selected tile
selected_tile = None

# Define the snapping threshold
snapping_threshold = 10

# Define the tile palette
tile_palette = [
    {"color": (255, 0, 0), "name": "Red"},
    {"color": (0, 255, 0), "name": "Green"},
    {"color": (0, 0, 255), "name": "Blue"}
]

# Define the save and load functions
def save_layout(filename):
    with open(filename, "wb") as f:
        pickle.dump(grid, f)

def load_layout(filename):
    with open(filename, "rb") as f:
        return pickle.load(f)

# Main loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            # Get the mouse position
            mouse_x, mouse_y = event.pos

            # Check if a tile is being clicked in the palette
            for i, tile in enumerate(tile_palette):
                if (i * tile_size < mouse_x < (i + 1) * tile_size and
                        screen_height - tile_size < mouse_y < screen_height):
                    # Set the selected tile
                    selected_tile = tile
                    break

            # Check if a tile is being clicked in the grid
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

            # Snap the tile to the grid
            snapped_x = round(mouse_x / tile_size) * tile_size
            snapped_y = round(mouse_y / tile_size) * tile_size

            # Check if the snapped position is within the snapping threshold
            if abs(snapped_x - mouse_x) < snapping_threshold and abs(snapped_y - mouse_y) < snapping_threshold:
                # Move the dragged tile to the snapped position
                grid[dragged_tile[1]][dragged_tile[0]] = 0
                grid[snapped_y // tile_size][snapped_x // tile_size] = 1
            else:
                # Move the dragged tile to the new position
                grid[dragged_tile[1]][dragged_tile[0]] = 0
                grid[mouse_y // tile_size][mouse_x // tile_size] = 1

        elif event.type == pygame.MOUSEBUTTONDOWN and selected_tile is not None:
            # Get the mouse position
            mouse_x, mouse_y = event.pos

            # Add the selected tile to the grid
            grid[mouse_y // tile_size][mouse_x // tile_size] = 1

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_s:
                # Save the layout
                save_layout("layout.dat")
                print("Layout saved!")
            elif event.key == pygame.K_l:
                # Load the layout
                grid = load_layout("layout.dat")
                print("Layout loaded!")

    # Draw the grid
    screen.fill((255, 255, 255))
    for i in range(grid_size):
        for j in range(grid_size):
            if grid[j][i] == 1:
                pygame.draw.rect(screen, tile_colors[0], (i * tile_size, j * tile_size, tile_size, tile_size))
            pygame.draw.rect(screen, (0, 0, 0), (i * tile_size, j * tile_size, tile_size, tile_size), 1)

    # Draw the tile palette
    for i, tile in enumerate(tile_palette):
        pygame.draw.rect(screen, tile["color"], (i * tile_size, screen_height - tile_size, tile_size, tile_size))
        pygame.draw.rect(screen, (0, 0, 0), (i * tile_size, screen_height - tile_size, tile_size, tile_size), 1)

    # Update the screen
    pygame.display.flip()
