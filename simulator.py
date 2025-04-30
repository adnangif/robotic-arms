import tkinter as tk
import math
import random
from robot_arm import RobotArm
from objects import Object

class Obstacle:
    def __init__(self, canvas, x, y, size=30):
        self.canvas = canvas
        self.x = x
        self.y = y
        self.size = size
        
        # Create a square obstacle
        self.id = self.canvas.create_rectangle(
            x - size, y - size, x + size, y + size,
            fill="#F38BA8", outline="#FFFFFF", width=2
        )
    
    def check_collision(self, x1, y1, x2, y2):
        # Check if line segment from (x1,y1) to (x2,y2) intersects with this obstacle
        # Using simplified rectangle-line intersection
        rect_left = self.x - self.size
        rect_right = self.x + self.size
        rect_top = self.y - self.size
        rect_bottom = self.y + self.size
        
        # Check if either endpoint is inside the rectangle
        if (rect_left <= x1 <= rect_right and rect_top <= y1 <= rect_bottom) or \
           (rect_left <= x2 <= rect_right and rect_top <= y2 <= rect_bottom):
            return True
            
        # Check if line intersects any of the rectangle's edges
        # Line equation: y = mx + b
        if x2 - x1 != 0:  # Avoid division by zero
            m = (y2 - y1) / (x2 - x1)
            b = y1 - m * x1
            
            # Calculate y-coordinates where line intersects with left and right edges
            left_y = m * rect_left + b
            right_y = m * rect_right + b
            
            # Check if these intersections are within the rectangle's y-range
            if (rect_top <= left_y <= rect_bottom and min(x1, x2) <= rect_left <= max(x1, x2)) or \
               (rect_top <= right_y <= rect_bottom and min(x1, x2) <= rect_right <= max(x1, x2)):
                return True
                
            # Calculate x-coordinates where line intersects with top and bottom edges
            if m != 0:  # Avoid division by zero
                top_x = (rect_top - b) / m
                bottom_x = (rect_bottom - b) / m
                
                # Check if these intersections are within the rectangle's x-range
                if (rect_left <= top_x <= rect_right and min(y1, y2) <= rect_top <= max(y1, y2)) or \
                   (rect_left <= bottom_x <= rect_right and min(y1, y2) <= rect_bottom <= max(y1, y2)):
                    return True
        
        return False

class RobotArmSimulator:
    def __init__(self, root):
        self.root = root
        self.root.title("Robot Arm")
        self.root.configure(bg="#1E1E2E")
        
        # Create canvas with modern color scheme
        self.canvas_width = 1000
        self.canvas_height = 600
        self.canvas = tk.Canvas(root, width=self.canvas_width, height=self.canvas_height,
                               background="#181825", highlightthickness=0)  # Dark background
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Create modern control panel
        self.control_panel = tk.Frame(root, width=220, padx=15, pady=15, bg="#1E1E2E")
        self.control_panel.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Create reference grid
        self.draw_grid()
        
        # Create target zone with new color
        self.target_x = 600
        self.target_y = 400
        self.target_width = 150
        self.target_height = 100
        self.target = self.canvas.create_rectangle(
            self.target_x, self.target_y,
            self.target_x + self.target_width, self.target_y + self.target_height,
            fill="#313244", outline="#89B4FA", width=2
        )
        
        # Create target zone label
        self.canvas.create_text(
            self.target_x + self.target_width/2,
            self.target_y - 10,
            text="DROP ZONE",
            fill="#CBA6F7",
            font=("Arial", 10, "bold")
        )
        
        # Create obstacles
        self.obstacles = []
        self.create_obstacles(3)  # Create 3 obstacles
        
        # Create robot arm
        self.arm = RobotArm(self.canvas, 400, 300)
        self.arm.set_obstacles(self.obstacles)  # Pass obstacles to the arm
        
        # Create objects
        self.objects = []
        self.create_objects(5)
        
        # Setup controls
        self.setup_controls()
        
        # Bind keyboard controls
        self.root.bind("<Key>", self.key_press)
        
        # Status label
        self.status_var = tk.StringVar()
        self.status_var.set("KEYS: 1/2/3 = CLOCKWISE, Q/W/E = COUNTERCLOCKWISE, G = GRIPPER")
        self.status_label = tk.Label(self.control_panel, textvariable=self.status_var, 
                                    wraplength=190, justify=tk.LEFT, bg="#1E1E2E", fg="#CDD6F4",
                                    font=("Arial", 8))
        self.status_label.pack(side=tk.BOTTOM, pady=10)
        
        # Score tracking with modern styling
        self.score = 0
        self.score_var = tk.StringVar()
        self.score_var.set(f"PROGRESS: {self.score}/{len(self.objects)}")
        self.score_label = tk.Label(self.control_panel, textvariable=self.score_var, 
                                   bg="#313244", fg="#CDD6F4", font=("Arial", 12, "bold"),
                                   padx=10, pady=5, relief="flat")
        self.score_label.pack(side=tk.BOTTOM, pady=10, fill=tk.X)
    
    def create_obstacles(self, count):
        max_reach = 350  # Approximate reach of the arm
        
        for i in range(count):
            # Place obstacles in various positions around the arm's reach
            angle = random.uniform(0, 2 * math.pi)
            distance = random.uniform(150, 350)  # Between inner and outer reach
            
            x = self.canvas_width / 2 + distance * math.cos(angle)
            y = self.canvas_height / 2 + distance * math.sin(angle)
            
            # Make sure obstacles don't overlap with the target zone
            while (self.target_x - 50 <= x <= self.target_x + self.target_width + 50 and
                   self.target_y - 50 <= y <= self.target_y + self.target_height + 50):
                angle = random.uniform(0, 2 * math.pi)
                distance = random.uniform(150, 350)
                x = self.canvas_width / 2 + distance * math.cos(angle)
                y = self.canvas_height / 2 + distance * math.sin(angle)
            
            # Create obstacle
            self.obstacles.append(Obstacle(self.canvas, x, y))
    
    def draw_grid(self):
        # Draw faint grid lines for reference
        grid_spacing = 50
        grid_color = "#313244"  # Subtle grid color
        
        # Horizontal grid lines
        for y in range(0, self.canvas_height, grid_spacing):
            self.canvas.create_line(0, y, self.canvas_width, y, fill=grid_color, width=1, dash=(2, 4))
            
        # Vertical grid lines
        for x in range(0, self.canvas_width, grid_spacing):
            self.canvas.create_line(x, 0, x, self.canvas_height, fill=grid_color, width=1, dash=(2, 4))
    
    def create_objects(self, count):
        colors = ["#F38BA8", "#A6E3A1", "#CBA6F7", "#FAB387", "#89DCEB", "#F9E2AF"]  # Modern palette
        max_reach = self.arm.get_max_reach() * 0.7  # Stay within 70% of max reach
        
        for i in range(count):
            # Create objects within arm's reach, avoiding obstacles
            valid_position = False
            x, y = 0, 0
            
            while not valid_position:
                angle = random.uniform(-math.pi/2, math.pi/2)  # Semicircle in front 
                distance = random.uniform(max_reach * 0.3, max_reach * 0.6)  # Within comfortable reach
                
                x = self.arm.base_x + distance * math.cos(angle)
                y = self.arm.base_y + distance * math.sin(angle)
                
                # Check if this position is clear of obstacles
                valid_position = True
                for obstacle in self.obstacles:
                    if math.sqrt((x - obstacle.x)**2 + (y - obstacle.y)**2) < obstacle.size + 20:
                        valid_position = False
                        break
            
            color = random.choice(colors)
            self.objects.append(Object(self.canvas, x, y, color))
    
    def setup_controls(self):
        # Title with modern styling
        title_label = tk.Label(self.control_panel, text="CONTROLS", bg="#1E1E2E", fg="#89B4FA", 
                              font=("Arial", 14, "bold"))
        title_label.pack(anchor=tk.CENTER, pady=(5, 15))
        
        # Separator
        separator = tk.Frame(self.control_panel, height=2, bg="#313244")
        separator.pack(fill=tk.X, pady=10)
        
        # Joint control section
        control_label = tk.Label(self.control_panel, text="CONTROLS", bg="#1E1E2E", fg="#CDD6F4", 
                                font=("Arial", 10, "bold"))
        control_label.pack(anchor=tk.W, pady=(5, 10))
        
        # Create a frame for each joint with new modern styling
        joint_names = ["BASE", "ELBOW", "WRIST"]
        
        for i in range(3):
            frame = tk.Frame(self.control_panel, bg="#1E1E2E")
            frame.pack(fill=tk.X, pady=5)
            
            tk.Label(frame, text=f"{joint_names[i]}:", bg="#1E1E2E", fg="#CDD6F4",
                    font=("Arial", 9)).pack(side=tk.LEFT)
            
            decrease = tk.Button(frame, text="◄", command=lambda idx=i: self.arm.move_joint(idx, -0.1),
                               bg="#313244", fg="#CDD6F4", activebackground="#45475A",
                               relief="flat", width=3, font=("Arial", 9, "bold"))
            decrease.pack(side=tk.LEFT, padx=5)
            
            increase = tk.Button(frame, text="►", command=lambda idx=i: self.arm.move_joint(idx, 0.1),
                               bg="#313244", fg="#CDD6F4", activebackground="#45475A",
                               relief="flat", width=3, font=("Arial", 9, "bold"))
            increase.pack(side=tk.LEFT)
        
        # Another separator
        separator2 = tk.Frame(self.control_panel, height=2, bg="#313244")
        separator2.pack(fill=tk.X, pady=10)
        
        # Gripper control with new styling
        gripper_frame = tk.Frame(self.control_panel, bg="#1E1E2E")
        gripper_frame.pack(fill=tk.X, pady=5)
        
        tk.Label(gripper_frame, text="GRIPPER:", bg="#1E1E2E", fg="#CDD6F4",
                font=("Arial", 9)).pack(side=tk.LEFT)
                
        self.gripper_button = tk.Button(gripper_frame, text="TOGGLE GRIP", 
                                       command=lambda: self.toggle_gripper(),
                                       bg="#F38BA8", fg="#1E1E2E", activebackground="#F38BA8",
                                       relief="flat", font=("Arial", 9, "bold"))
        self.gripper_button.pack(side=tk.LEFT, padx=5)
        
        # Reset button with new styling
        reset_button = tk.Button(self.control_panel, text="RESET POSITION", 
                               command=self.reset_arm, bg="#89B4FA", fg="#1E1E2E", 
                               activebackground="#89B4FA", relief="flat",
                               font=("Arial", 9, "bold"), padx=10, pady=5)
        reset_button.pack(pady=10, fill=tk.X)
        
        # Mission briefing with obstacles info
        mission_frame = tk.Frame(self.control_panel, bg="#313244", padx=10, pady=10)
        mission_frame.pack(fill=tk.X, pady=10)
        
        mission_title = tk.Label(mission_frame, text="MISSION BRIEFING", 
                              bg="#313244", fg="#FAB387", font=("Arial", 10, "bold"))
        mission_title.pack(anchor=tk.W)
        
        separator3 = tk.Frame(mission_frame, height=1, bg="#45475A")
        separator3.pack(fill=tk.X, pady=5)
        
        instructions = "1. Control the robotic arm\n" \
                     "2. AVOID RED OBSTACLES\n" \
                     "3. Pick up all objects\n" \
                     "4. Move them to drop zone\n" \
                     "5. Complete the mission"
        
        tk.Label(mission_frame, text=instructions, 
              justify=tk.LEFT, wraplength=190, bg="#313244", fg="#CDD6F4",
              font=("Arial", 9)).pack(pady=5)
        
        # Obstacle info
        obstacle_info = f"OBSTACLES: {len(self.obstacles)}"
        obstacle_label = tk.Label(mission_frame, text=obstacle_info, 
                               bg="#313244", fg="#F38BA8", font=("Arial", 9, "bold"))
        obstacle_label.pack(anchor=tk.W, pady=5)
    
    def reset_arm(self):
        self.arm.set_angles([0, 0, 0])
        self.arm.gripper_closed = False
        self.arm.holding_object = None
        self.arm.draw()
    
    def toggle_gripper(self):
        self.arm.toggle_gripper(self.objects)
        self.check_placement()
        
        # Update gripper button text based on state
        if self.arm.gripper_closed:
            self.gripper_button.config(text="RELEASE", bg="#A6E3A1")
        else:
            self.gripper_button.config(text="GRAB", bg="#F38BA8")
    
    def key_press(self, event):
        key = event.keysym.lower()
        
        if key == "g":
            self.toggle_gripper()
        elif key == "1":
            self.arm.move_joint(0, 0.1)   # Clockwise
        elif key == "q":
            self.arm.move_joint(0, -0.1)  # Counterclockwise
        elif key == "2":
            self.arm.move_joint(1, 0.1)   # Clockwise
        elif key == "w":
            self.arm.move_joint(1, -0.1)  # Counterclockwise
        elif key == "3":
            self.arm.move_joint(2, 0.1)   # Clockwise
        elif key == "e":
            self.arm.move_joint(2, -0.1)  # Counterclockwise
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
                    self.score_var.set(f"PROGRESS: {self.score}/{len(self.objects)}")
                    
                    # Check if all objects are placed
                    if self.score == len(self.objects):
                        self.status_var.set("MISSION ACCOMPLISHED! ALL OBJECTS SECURED!") 