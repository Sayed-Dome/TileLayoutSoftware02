import shapely.geometry as sg

class Calculator:
    def __init__(self):
        pass

    def calculate_polygon_area(self, points):
        polygon = sg.Polygon(points)
        return polygon.area

    def calculate_number_of_tiles(self, polygon_area, tile_size):
        # Calculate the number of tiles needed based on the polygon area and tile size
        # For simplicity, assume a square tile with side length equal to tile_size
        tile_area = tile_size ** 2
        return int(polygon_area / tile_area) + 1  # Add 1 to account for partial tiles

    def generate_tile_cutting_layout(self, polygon, tile_size):
        # Generate a tile cutting layout based on the polygon shape and tile size
        # For simplicity, assume a square tile with side length equal to tile_size
        tile_layout = []
        for x in range(int(polygon.bounds[0]), int(polygon.bounds[2]), tile_size):
            for y in range(int(polygon.bounds[1]), int(polygon.bounds[3]), tile_size):
                tile = sg.box(x, y, x + tile_size, y + tile_size)
                if polygon.intersects(tile):
                    tile_layout.append(tile)
        return tile_layout

class TileLayout:
    def __init__(self, gui):
        self.gui = gui
        self.tiles = []

    def add_tile(self, tile):
        if tile not in self.tiles:
            self.tiles.append(tile)
            self.gui.add_state(self.tiles)

    def remove_tile(self, tile):
        if tile in self.tiles:
            self.tiles.remove(tile)
            self.gui.add_state(self.tiles)
