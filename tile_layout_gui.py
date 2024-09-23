import sys
from PyQt5.QtWidgets import QApplication, QGraphicsView, QGraphicsScene, QGraphicsRectItem
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

    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.LeftButton:
            x = event.x()
            y = event.y()
            self.horizontalScrollBar().setValue(self._panStartXValue - (x - self._panStartX))
            self.verticalScrollBar().setValue(self._panStartYValue - (y - self._panStartY))

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.setCursor(Qt.ArrowCursor)

def main():
    app = QApplication(sys.argv)
    tile_layout = TileLayout(10, 10)
    tile1 = Tile(50, 50, 2, 2)
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
