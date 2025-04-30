# Robot Arm Simulator

A Python Tkinter application that simulates a robot arm with three joints that can pick up objects and place them in a target zone.

## Project Structure

- `main.py` - Entry point for the application
- `robot_arm.py` - Contains the RobotArm class that handles the arm's kinematics and drawing
- `objects.py` - Contains the Object class for managing objects that can be picked up
- `simulator.py` - Contains the RobotArmSimulator class that controls the main application window

## Features

- Visually detailed robot arm with 4:3:1 segment length proportions
- Modern arm design with articulated joints
- Enhanced gripper with animated prongs
- Multiple objects with various shapes (circles, squares, diamonds, triangles)
- Dark-themed interface with modern color scheme
- Target zone (dark blue box) where objects should be placed
- Obstacles that must be avoided by the robot arm
- Collision detection with visual warnings
- Controls via buttons and keyboard shortcuts
- Score tracking
- Reference grid for better spatial awareness

## Controls

### Keyboard

- **1**: Rotate joint 1 clockwise
- **Q**: Rotate joint 1 counterclockwise
- **2**: Rotate joint 2 clockwise
- **W**: Rotate joint 2 counterclockwise
- **3**: Rotate joint 3 clockwise
- **E**: Rotate joint 3 counterclockwise
- **G**: Toggle gripper (open/close)
- **Up/Down Arrow**: Rotate first joint

### Buttons

The control panel on the right side of the application has buttons to:
- Move each joint in both directions
- Toggle the gripper
- Reset the arm position

## How to Run

Make sure you have Python and Tkinter installed, then run:

```
python main.py
```

## Objective

1. Use the controls to move the robot arm
2. Navigate around obstacles (red squares)
3. Position the gripper over an object and close it to pick up the object
4. Move the object to the blue target zone
5. Open the gripper to release the object
6. Repeat until all objects are placed in the target zone

## Implementation Details

- The robot arm uses a forward kinematics system
- Arm segments follow a 4:3:1 length proportion similar to industrial robots
- All objects are placed within the reach of the robot arm
- Dark theme with blue/green accent colors
- Collision detection between the arm segments and obstacles
- Collision detection between the gripper and objects
- Object placement verification in the target zone
- Visual feedback for successful placement (gold outline)
- Visual warnings when collisions with obstacles are detected 