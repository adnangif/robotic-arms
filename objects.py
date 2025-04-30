import tkinter as tk
import math
import random

class Object:
    def __init__(self, canvas, x, y, color):
        self.canvas = canvas
        self.x = x
        self.y = y
        self.color = color
        self.size = 15
        self.placed = False
        
        # Create a shape for the object
        self.id = self.create_shape(x, y, self.size, color)
    
    def create_shape(self, x, y, size, color):
        # Randomly select a shape type
        shape_type = random.choice(["circle", "square", "diamond", "triangle"])
        
        if shape_type == "circle":
            return self.canvas.create_oval(
                x - size, y - size, x + size, y + size,
                fill=color, outline="#333333", width=2
            )
        elif shape_type == "square":
            return self.canvas.create_rectangle(
                x - size, y - size, x + size, y + size,
                fill=color, outline="#333333", width=2
            )
        elif shape_type == "diamond":
            return self.canvas.create_polygon(
                x, y - size*1.2,  # top
                x + size*1.2, y,  # right
                x, y + size*1.2,  # bottom
                x - size*1.2, y,  # left
                fill=color, outline="#333333", width=2
            )
        elif shape_type == "triangle":
            return self.canvas.create_polygon(
                x, y - size*1.2,  # top
                x + size, y + size,  # bottom right
                x - size, y + size,  # bottom left
                fill=color, outline="#333333", width=2
            )
    
    def is_near(self, x, y, threshold):
        distance = math.sqrt((self.x - x) ** 2 + (self.y - y) ** 2)
        return distance < threshold
    
    def move_to(self, x, y):
        dx = x - self.x
        dy = y - self.y
        self.canvas.move(self.id, dx, dy)
        self.x = x
        self.y = y
    
    def is_in_target(self, target_x, target_y, target_width, target_height):
        return (target_x <= self.x <= target_x + target_width and 
                target_y <= self.y <= target_y + target_height)
    
    def mark_placed(self):
        self.placed = True
        # Change appearance when placed
        self.canvas.itemconfig(self.id, outline="gold", width=3) 