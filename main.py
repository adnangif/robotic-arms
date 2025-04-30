import tkinter as tk
from simulator import RobotArmSimulator

def main():
    """Main entry point for the RoboManipulator 3000"""
    root = tk.Tk()
    root.title("Robot Arm")
    root.configure(bg="#1E1E2E")
    
    # Set window size and position
    window_width = 1220
    window_height = 620
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    
    center_x = int(screen_width/2 - window_width/2)
    center_y = int(screen_height/2 - window_height/2)
    
    root.geometry(f'{window_width}x{window_height}+{center_x}+{center_y}')
    root.resizable(False, False)
    
    app = RobotArmSimulator(root)
    root.mainloop()

if __name__ == "__main__":
    main()