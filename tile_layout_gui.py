import tkinter as tk
from tkinter import messagebox
from tile_layout import Calculator

class GUI:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Tile Layout Software")
        self.calculator = Calculator()

        # Create input fields for polygon points
        self.points_label = tk.Label(self.window, text="Enter polygon points (x, y):")
        self.points_label.pack()
        self.points_entry = tk.Entry(self.window)
        self.points_entry.pack()

        # Create button to calculate and display results
        self.calculate_button = tk.Button(self.window, text="Calculate", command=self.calculate_and_display_results)
        self.calculate_button.pack()

        # Create label to display results
        self.results_label = tk.Label(self.window, text="")
        self.results_label.pack()

    def calculate_and_display_results(self):
        points = self.points_entry.get()
        points = [tuple(map(float, point.split(", "))) for point in points.split("; ")]
        polygon_area = self.calculator.calculate_polygon_area(points)
        number_of_tiles = self.calculator.calculate_number_of_tiles(polygon_area, 1)  # Assume tile size is 1 for now
        tile_layout = self.calculator.generate_tile_cutting_layout(sg.Polygon(points), 1)  # Assume tile size is 1 for now

        results_text = f"Polygon area: {polygon_area:.2f}\nNumber of tiles: {number_of_tiles}\nTile layout: {tile_layout}"
        self.results_label.config(text=results_text)

    def run(self):
        self.window.mainloop()

class TileLayoutGUI:
    def __init__(self):
        self.states = []
        self.current_state = 0

    def add_state(self, state):
        self.states.append(state)
        self.current_state += 1

    def undo(self):
        if self.current_state > 0:
            self.current_state -= 1
            return self.states[self.current_state]
        else:
            return None

    def redo(self):
        if self.current_state < len(self.states) - 1:
            self.current_state += 1
            return self.states[self.current_state]
        else:
            return None


if __name__ == "__main__":
    gui = GUI()
    gui.run()
