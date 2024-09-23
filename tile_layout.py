import logging

class TileLayout:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.tiles = []

    def add_tile(self, tile):
        self.tiles.append(tile)

    def remove_tile(self, tile):
        self.tiles.remove(tile)

    def get_tiles(self):
        return self.tiles

    def __repr__(self):
        return f"TileLayout(width={self.width}, height={self.height}, tiles={self.tiles})"
