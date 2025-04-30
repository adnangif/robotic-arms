import tkinter as tk
import math
import random
from dataclasses import dataclass
from typing import List, Tuple, Optional

class RobotArm:
    def __init__(self, canvas, x, y, lengths=(100, 80, 60)):
        self.canvas = canvas
        self.base_x = x
        self.base_y = y
        self.lengths = lengths  # Length of each arm segment
        self.angles = [0, 0, 0]  # Angles of joints in radians
        self.joints = []  # Store joint positions
        self.segments = []  # Store canvas segment ids
        self.gripper = None
        self.gripper_closed = False
        self.holding_object = None
        self.draw()
    
    def draw(self):
        # Clear previous segments
        for segment in self.segments:
            self.canvas.delete(segment)
        self.segments = []
        
        # Calculate joint positions
        self.joints = self.calculate_joints()
        
        # Draw base
        base = self.canvas.create_oval(
            self.base_x - 10, self.base_y - 10,
            self.base_x + 10, self.base_y + 10,
            fill="gray"
        )
        self.segments.append(base)
        
        # Draw arm segments
        for i in range(len(self.joints) - 1):
            x1, y1 = self.joints[i]
            x2, y2 = self.joints[i + 1]
            segment = self.canvas.create_line(x1, y1, x2, y2, width=5, fill="black")
            self.segments.append(segment)
            
            # Draw joints
            joint = self.canvas.create_oval(
                x1 - 5, y1 - 5, x1 + 5, y1 + 5, fill="red"
            )
            self.segments.append(joint)
        
        # Draw gripper
        tip_x, tip_y = self.joints[-1]
        gripper_size = 10
        if self.gripper_closed:
            gripper_size = 5
        
        self.gripper = self.canvas.create_rectangle(
            tip_x - gripper_size, tip_y - gripper_size,
            tip_x + gripper_size, tip_y + gripper_size,
            outline="blue", width=2
        )
        self.segments.append(self.gripper)
    
    def calculate_joints(self) -> List[Tuple[float, float]]:
        joints = [(self.base_x, self.base_y)]
        x, y = self.base_x, self.base_y
        angle_sum = 0
        
        for i, length in enumerate(self.lengths):
            angle_sum += self.angles[i]
            x += length * math.cos(angle_sum)
            y += length * math.sin(angle_sum)
            joints.append((x, y))
        
        return joints
    
    def set_angles(self, angles):
        self.angles = angles
        self.draw()
        
        # Update held object position if holding one
        if self.holding_object and self.gripper_closed:
            tip_x, tip_y = self.joints[-1]
            self.holding_object.move_to(tip_x, tip_y)
    
    def move_joint(self, joint_idx, delta):
        if 0 <= joint_idx < len(self.angles):
            self.angles[joint_idx] += delta
            self.draw()
            
            # Update held object position if holding one
            if self.holding_object and self.gripper_closed:
                tip_x, tip_y = self.joints[-1]
                self.holding_object.move_to(tip_x, tip_y)
    
    def toggle_gripper(self, objects):
        self.gripper_closed = not self.gripper_closed
        tip_x, tip_y = self.joints[-1]
        
        if self.gripper_closed:
            # Try to grab object
            for obj in objects:
                if obj.is_near(tip_x, tip_y, 20) and not obj.placed:
                    self.holding_object = obj
                    break
        else:
            # Release object
            self.holding_object = None
            
        self.draw()


class Object:
    def __init__(self, canvas, x, y, color):
        self.canvas = canvas
        self.x = x
        self.y = y
        self.color = color
        self.size = 15
        self.placed = False
        self.id = self.canvas.create_oval(
            x - self.size, y - self.size,
            x + self.size, y + self.size,
            fill=color
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
        self.canvas.itemconfig(self.id, outline="gold", width=2)


class RobotArmSimulator:
    def __init__(self, root):
        self.root = root
        self.root.title("Robot Arm Simulator")
        
        # Create canvas
        self.canvas_width = 800
        self.canvas_height = 600
        self.canvas = tk.Canvas(root, width=self.canvas_width, height=self.canvas_height,
                               background="white")
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Create control panel
        self.control_panel = tk.Frame(root, width=200, padx=10, pady=10)
        self.control_panel.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Create robot arm
        self.arm = RobotArm(self.canvas, 400, 300)
        
        # Create target zone
        self.target_x = 600
        self.target_y = 400
        self.target_width = 150
        self.target_height = 100
        self.target = self.canvas.create_rectangle(
            self.target_x, self.target_y,
            self.target_x + self.target_width, self.target_y + self.target_height,
            fill="light blue", outline="blue", width=2
        )
        
        # Create objects
        self.objects = []
        self.create_objects(5)
        
        # Setup controls
        self.setup_controls()
        
        # Bind keyboard controls
        self.root.bind("<Key>", self.key_press)
        
        # Status label
        self.status_var = tk.StringVar()
        self.status_var.set("Controls: 1/2/3 + Up/Down = Move joints, G = Toggle gripper")
        self.status_label = tk.Label(self.control_panel, textvariable=self.status_var, 
                                    wraplength=180, justify=tk.LEFT)
        self.status_label.pack(side=tk.BOTTOM, pady=10)
        
        # Score tracking
        self.score = 0
        self.score_var = tk.StringVar()
        self.score_var.set(f"Objects placed: {self.score}/{len(self.objects)}")
        self.score_label = tk.Label(self.control_panel, textvariable=self.score_var)
        self.score_label.pack(side=tk.BOTTOM, pady=5)
    
    def create_objects(self, count):
        colors = ["red", "green", "purple", "orange", "pink", "cyan"]
        for i in range(count):
            # Create objects in left side of screen, away from target zone
            x = random.randint(50, 300)
            y = random.randint(100, 500)
            color = random.choice(colors)
            self.objects.append(Object(self.canvas, x, y, color))
    
    def setup_controls(self):
        # Joint control sliders
        tk.Label(self.control_panel, text="Joint Controls:").pack(anchor=tk.W, pady=(0, 5))
        
        for i in range(3):
            frame = tk.Frame(self.control_panel)
            frame.pack(fill=tk.X, pady=5)
            
            tk.Label(frame, text=f"Joint {i+1}:").pack(side=tk.LEFT)
            
            decrease = tk.Button(frame, text="-", command=lambda idx=i: self.arm.move_joint(idx, -0.1))
            decrease.pack(side=tk.LEFT, padx=5)
            
            increase = tk.Button(frame, text="+", command=lambda idx=i: self.arm.move_joint(idx, 0.1))
            increase.pack(side=tk.LEFT)
        
        # Gripper control
        gripper_frame = tk.Frame(self.control_panel)
        gripper_frame.pack(fill=tk.X, pady=10)
        
        tk.Label(gripper_frame, text="Gripper:").pack(side=tk.LEFT)
        self.gripper_button = tk.Button(gripper_frame, text="Toggle", 
                                       command=lambda: self.arm.toggle_gripper(self.objects))
        self.gripper_button.pack(side=tk.LEFT, padx=5)
        
        # Reset button
        tk.Button(self.control_panel, text="Reset Arm Position", 
                 command=self.reset_arm).pack(pady=10)
        
        # Instructions
        instructions = "Instructions:\n" \
                      "1. Use the controls to move the robot arm\n" \
                      "2. Pick up all objects\n" \
                      "3. Place them in the blue target zone"
        
        tk.Label(self.control_panel, text=instructions, 
                justify=tk.LEFT, wraplength=180).pack(pady=10)
    
    def reset_arm(self):
        self.arm.set_angles([0, 0, 0])
        self.arm.gripper_closed = False
        self.arm.holding_object = None
        self.arm.draw()
    
    def key_press(self, event):
        key = event.keysym.lower()
        
        if key == "g":
            self.arm.toggle_gripper(self.objects)
            self.check_placement()
        elif key == "1":
            if event.keysym == "1":  # Lowercase
                self.arm.move_joint(0, 0.1)
            else:  # Shift+1
                self.arm.move_joint(0, -0.1)
        elif key == "2":
            if event.keysym == "2":  # Lowercase
                self.arm.move_joint(1, 0.1)
            else:  # Shift+2
                self.arm.move_joint(1, -0.1)
        elif key == "3":
            if event.keysym == "3":  # Lowercase
                self.arm.move_joint(2, 0.1)
            else:  # Shift+3
                self.arm.move_joint(2, -0.1)
        elif key == "up":
            current_joint = 0  # Default to first joint
            self.arm.move_joint(current_joint, 0.1)
        elif key == "down":
            current_joint = 0  # Default to first joint
            self.arm.move_joint(current_joint, -0.1)
    
    def check_placement(self):
        # If we just released an object, check if it's in the target
        if not self.arm.gripper_closed and self.arm.holding_object is None:
            for obj in self.objects:
                if (not obj.placed and 
                    obj.is_in_target(self.target_x, self.target_y, 
                                    self.target_width, self.target_height)):
                    obj.mark_placed()
                    self.score += 1
                    self.score_var.set(f"Objects placed: {self.score}/{len(self.objects)}")
                    
                    # Check if all objects are placed
                    if self.score == len(self.objects):
                        self.status_var.set("Congratulations! All objects placed!")


if __name__ == "__main__":
    root = tk.Tk()
    app = RobotArmSimulator(root)
    root.mainloop()