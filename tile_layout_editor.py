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

# Main loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Draw the grid
    screen.fill((255, 255, 255))
    for i in range(grid_size):
        for j in range(grid_size):
            pygame.draw.rect(screen, (0, 0, 0), (i * tile_size, j * tile_size, tile_size, tile_size), 1)

    # Update the screen
    pygame.display.flip()
