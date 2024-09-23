import logging
from tile_layout import TileLayout
from tile import Tile

def main():
    # Create a tile layout
    layout = TileLayout(10, 10)

    # Create some tiles
    tile1 = Tile(0, 0, 2, 2)
    tile2 = Tile(2, 0, 2, 2)
    tile3 = Tile(4, 0, 2, 2)

    # Add tiles to the layout
    layout.add_tile(tile1)
    layout.add_tile(tile2)
    layout.add_tile(tile3)

    # Print the layout
    print(layout)

if __name__ == "__main__":
    main()
