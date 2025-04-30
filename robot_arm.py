import tkinter as tk
import math
from typing import List, Tuple

class RobotArm:
    def __init__(self, canvas, x, y, lengths=(240, 180, 60)):  # Proportion 4:3:1
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
        
        # Colors for the arm
        self.colors = {
            "base": "#313244",
            "segments": ["#89B4FA", "#74C7EC", "#89DCEB"],  # Blue gradient
            "joints": "#F9E2AF",  # Yellow
            "gripper_open": "#A6E3A1",  # Light green
            "gripper_closed": "#F38BA8"  # Pink
        }
        
        self.draw()
    
    def draw(self):
        # Clear previous segments
        for segment in self.segments:
            self.canvas.delete(segment)
        self.segments = []
        
        # Calculate joint positions
        self.joints = self.calculate_joints()
        
        # Draw fancy base
        base_size = 30
        base = self.canvas.create_rectangle(
            self.base_x - base_size, self.base_y - base_size/2,
            self.base_x + base_size, self.base_y + base_size/2,
            fill=self.colors["base"], outline="#555555", width=2
        )
        self.segments.append(base)
        
        base_circle = self.canvas.create_oval(
            self.base_x - 15, self.base_y - 15,
            self.base_x + 15, self.base_y + 15,
            fill="#555555", outline="#888888", width=2
        )
        self.segments.append(base_circle)
        
        # Draw arm segments with more detailed appearance
        for i in range(len(self.joints) - 1):
            x1, y1 = self.joints[i]
            x2, y2 = self.joints[i + 1]
            
            # Calculate segment angle
            segment_angle = math.atan2(y2 - y1, x2 - x1)
            
            # Create width for the segment (thicker near base, thinner at end)
            segment_width = 14 - i * 4
            
            # Calculate perpendicular points to create a rectangle
            dx = math.sin(segment_angle) * segment_width
            dy = -math.cos(segment_angle) * segment_width
            
            # Create points for segment polygon
            points = [
                x1 - dx/2, y1 - dy/2,  # Top left
                x1 + dx/2, y1 + dy/2,  # Bottom left
                x2 + dx/2, y2 + dy/2,  # Bottom right
                x2 - dx/2, y2 - dy/2   # Top right
            ]
            
            # Draw segment as polygon
            segment = self.canvas.create_polygon(
                points, fill=self.colors["segments"][i], outline="#444444", width=1
            )
            self.segments.append(segment)
            
            # Draw joints as larger circles with details
            if i > 0:  # Don't draw for base joint (already has base circle)
                joint_outer = self.canvas.create_oval(
                    x1 - 10, y1 - 10, x1 + 10, y1 + 10,
                    fill="#555555", outline="#333333", width=1
                )
                self.segments.append(joint_outer)
            
            joint_inner = self.canvas.create_oval(
                x1 - 5, y1 - 5, x1 + 5, y1 + 5,
                fill=self.colors["joints"], outline="#FFCC00"
            )
            self.segments.append(joint_inner)
        
        # Draw more sophisticated gripper
        tip_x, tip_y = self.joints[-1]
        gripper_size = 18
        if self.gripper_closed:
            gripper_size = 8
            gripper_color = self.colors["gripper_closed"]
        else:
            gripper_color = self.colors["gripper_open"]
        
        # Draw wrist joint
        wrist_joint = self.canvas.create_oval(
            tip_x - 8, tip_y - 8, tip_x + 8, tip_y + 8,
            fill="#555555", outline="#333333", width=1
        )
        self.segments.append(wrist_joint)
        
        wrist_joint_inner = self.canvas.create_oval(
            tip_x - 4, tip_y - 4, tip_x + 4, tip_y + 4,
            fill=self.colors["joints"], outline="#FFCC00"
        )
        self.segments.append(wrist_joint_inner)
        
        # Calculate gripper angle
        angle_sum = sum(self.angles)
        
        # Draw gripper prongs
        prong_length = 15
        
        # Left prong
        left_angle = angle_sum - math.pi/4
        left_dx = math.cos(left_angle) * prong_length
        left_dy = math.sin(left_angle) * prong_length
        left_x = tip_x + left_dx
        left_y = tip_y + left_dy
        
        # Right prong
        right_angle = angle_sum + math.pi/4
        right_dx = math.cos(right_angle) * prong_length
        right_dy = math.sin(right_angle) * prong_length
        right_x = tip_x + right_dx
        right_y = tip_y + right_dy
        
        # Position adjustment based on closed/open state
        offset = gripper_size / 2
        
        # Left prong points
        left_points = [
            tip_x, tip_y,
            tip_x - offset * math.sin(angle_sum), tip_y + offset * math.cos(angle_sum),
            left_x - offset * math.sin(angle_sum), left_y + offset * math.cos(angle_sum),
            left_x, left_y
        ]
        
        # Right prong points
        right_points = [
            tip_x, tip_y,
            tip_x + offset * math.sin(angle_sum), tip_y - offset * math.cos(angle_sum),
            right_x + offset * math.sin(angle_sum), right_y - offset * math.cos(angle_sum),
            right_x, right_y
        ]
        
        # Draw both prongs
        left_prong = self.canvas.create_polygon(
            left_points, fill=gripper_color, outline="#333333", width=1
        )
        right_prong = self.canvas.create_polygon(
            right_points, fill=gripper_color, outline="#333333", width=1
        )
        
        self.segments.append(left_prong)
        self.segments.append(right_prong)
        self.gripper = [left_prong, right_prong]  # Store both prongs
    
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

    def get_tip_position(self):
        if self.joints:
            return self.joints[-1]
        return None
        
    def get_max_reach(self):
        return sum(self.lengths) 