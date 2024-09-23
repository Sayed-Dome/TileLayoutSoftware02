import sys
import json
import csv
from PyQt5.QtWidgets import QApplication, QGraphicsView, QGraphicsScene, QGraphicsRectItem, QGraphicsTextItem
from PyQt5.QtGui import QPainter, QColor
from PyQt5.QtCore import Qt
from tile_layout import TileLayout
from tile import Tile

class TileLayoutGUI(QGraphicsView):
    def __init__(self, tile_layout):
        super().__init__()
        self.tile_layout = tile_layout
        self.scene = QGraphicsScene()
        self.setScene(self.scene)
        self.initUI()
        self.selected_tile = None
        self.dragging = False
        self.resizing = False
        self.resize_edge = None
        self.undo_stack = []
        self.redo_stack = []

    def undo(self):
        if self.undo_stack:
            self.redo_stack.append(self.tile_layout.get_tiles())
            self.tile_layout.set_tiles(self.undo_stack.pop())
            self.drawTiles()

    def redo(self):
        if self.redo_stack:
            self.undo_stack.append(self.tile_layout.get_tiles())
            self.tile_layout.set_tiles(self.redo_stack.pop())
            self.drawTiles()

    def initUI(self):
        self.setGeometry(300, 300, 300, 300)
        self.setWindowTitle('Tile Layout GUI')
        self.show()

    def drawTiles(self):
        for tile in self.tile_layout.get_tiles():
            rect = QGraphicsRectItem(tile.x, tile.y, tile.width, tile.height)
            rect.setBrush(QColor(255, 0, 0))  # Red color
            self.scene.addItem(rect)

    def wheelEvent(self, event):
        angle = event.angleDelta().y()
        factor = 1.2 if angle > 0 else 1 / 1.2
        self.scale(factor, factor)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.setCursor(Qt.ClosedHandCursor)
            self._panStartX = event.x()
            self._panStartY = event.y()
            self._panStartXValue = self.horizontalScrollBar().value()
            self._panStartYValue = self.verticalScrollBar().value()
            self.selectTile(event)
            self.dragging = True
            self.checkResizeEdge(event)
            self.undo_stack.append(self.tile_layout.get_tiles())

    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.LeftButton:
            if self.dragging:
                self.moveTile(event)
            elif self.resizing:
                self.resizeTile(event)
            else:
                x = event.x()
                y = event.y()
                self.horizontalScrollBar().setValue(self._panStartXValue - (x - self._panStartX))
                self.verticalScrollBar().setValue(self._panStartYValue - (y - self._panStartY))
                self.undo_stack.append(self.tile_layout.get_tiles())

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.setCursor(Qt.ArrowCursor)
            self.dragging = False
            self.resizing = False
            self.undo_stack.append(self.tile_layout.get_tiles())

    def selectTile(self, event):
        pos = event.pos()
        items = self.scene.items(pos)
        if items:
            self.selected_tile = items[0]

    def moveTile(self, event):
        if self.selected_tile:
            pos = event.pos()
            self.selected_tile.setPos(pos.x(), pos.y())
            tile = self.getTileFromItem(self.selected_tile)
            if tile:
                tile.x = pos.x()
                tile.y = pos.y()

    def checkResizeEdge(self, event):
        if self.selected_tile:
            pos = event.pos()
            tile = self.getTileFromItem(self.selected_tile)
            if tile:
                if abs(pos.x() - tile.x) < 5:
                    self.resizing = True
                    self.resize_edge = 'left'
                elif abs(pos.x() - (tile.x + tile.width)) < 5:
                    self.resizing = True
                    self.resize_edge = 'right'
                elif abs(pos.y() - tile.y) < 5:
                    self.resizing = True
                    self.resize_edge = 'top'
                elif abs(pos.y() - (tile.y + tile.height)) < 5:
                    self.resizing = True
                    self.resize_edge = 'bottom'

    def resizeTile(self, event):
        if self.selected_tile:
            pos = event.pos()
            tile = self.getTileFromItem(self.selected_tile)
            if tile:
                if self.resize_edge == 'left':
                    tile.width = tile.width - (pos.x() - tile.x)
                    tile.x = pos.x()
                elif self.resize_edge == 'right':
                    tile.width = pos.x() - tile.x
                elif self.resize_edge == 'top':
                    tile.height = tile.height - (pos.y() - tile.y)
                    tile.y = pos.y()
                elif self.resize_edge == 'bottom':
                    tile.height = pos.y() - tile.y
                self.selected_tile.setRect(tile.x, tile.y, tile.width, tile.height)

    def export_tile_layout_as_json(self):
        tile_layout_data = {
            'tiles': [
                {
                    'x': tile.x,
                    'y': tile.y,
                    'width': tile.width,
                    'height': tile.height
                }
                for tile in self.tile_layout.get_tiles()
            ]
        }
        with open('tile_layout.json', 'w') as f:
            json.dump(tile_layout_data, f)

    def export_tile_layout_as_csv(self):
        tile_layout_data = [
            [tile.x, tile.y, tile.width, tile.height]
            for tile in self.tile_layout.get_tiles()
        ]
        with open('tile_layout.csv', 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['x', 'y', 'width', 'height'])
            writer.writerows(tile_layout_data)

    def getTileFromItem(self, item):
        for tile in self.tile_layout.get_tiles():
            if tile.x == item.x() and tile.y == item.y() and tile.width == item.boundingRect().width() and tile.height == item.boundingRect().height():
                return tile
        return None
    

def main():
    app = QApplication(sys.argv)
    tile_layout = TileLayout(10, 10)
    tile1 = Tile(0, 0, 2, 2)
    tile2 = Tile(2, 0, 2, 2)
    tile3 = Tile(4, 0, 2, 2)
    tile_layout.add_tile(tile1)
    tile_layout.add_tile(tile2)
    tile_layout.add_tile(tile3)
    gui = TileLayoutGUI(tile_layout)
    gui.drawTiles()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
