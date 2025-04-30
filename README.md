# Robot Arm Simulator

A Python Tkinter application that simulates a robot arm with three joints that can pick up objects and place them in a target zone.

## Features

- Three-jointed robot arm with forward kinematics
- Configurable arm segments 
- Gripper that can open and close to pick up objects
- Multiple objects to be moved
- Target zone (blue box) where objects should be placed
- Controls via buttons and keyboard shortcuts
- Score tracking

## Controls

### Keyboard

- **1**: Rotate joint 1 clockwise
- **Shift+1**: Rotate joint 1 counterclockwise
- **2**: Rotate joint 2 clockwise
- **Shift+2**: Rotate joint 2 counterclockwise
- **3**: Rotate joint 3 clockwise
- **Shift+3**: Rotate joint 3 counterclockwise
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
2. Position the gripper over an object and close it to pick up the object
3. Move the object to the blue target zone
4. Open the gripper to release the object
5. Repeat until all objects are placed in the target zone

## Implementation Details

- The robot arm uses a simple forward kinematics system
- Collision detection between the gripper and objects
- Object placement verification in the target zone
- Visual feedback for successful placement (gold outline) 