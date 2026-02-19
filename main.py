"""
Bz-x800 Microscope Automation
Simple GUI for automated grid-based image capture

Author: Ryan
Date: 2026
"""

import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import pyautogui
import json
import time
import threading
from pathlib import Path
from datetime import datetime


# ==============================================================================
# CONFIGURATION MANAGER
# ==============================================================================

class Config:
    """Handles loading and saving configuration"""
    
    def __init__(self):
        self.file = Path("config.json")
        self.data = self.load()
    
    def load(self):
        """Load config from file, or create default"""
        default = {
            "ok_button": None,
            "live_image_button": None,
            "capture_delay": 1.0,
            "ok_delay": 0.8,
            "live_delay": 0.5,
            "arrow_delay": 0.3
        }
        
        if self.file.exists():
            try:
                with open(self.file, 'r') as f:
                    return json.load(f)
            except:
                return default
        return default
    
    def save(self):
        """Save config to file"""
        with open(self.file, 'w') as f:
            json.dump(self.data, f, indent=2)
    
    def is_calibrated(self):
        """Check if buttons are calibrated"""
        return (self.data.get('ok_button') is not None and 
                self.data.get('live_image_button') is not None)


# ==============================================================================
# MICROSCOPE CONTROLLER
# ==============================================================================

class MicroscopeController:
    """Controls microscope via GUI automation"""
    
    def __init__(self, config):
        self.config = config
        
        # Get button positions from config
        self.ok_pos = config['ok_button']
        self.live_pos = config['live_image_button']
        
        # Get delays from config
        self.capture_delay = config['capture_delay']
        self.ok_delay = config['ok_delay']
        self.live_delay = config['live_delay']
        self.arrow_delay = config['arrow_delay']
        
        # Safety: move mouse to corner to abort
        pyautogui.FAILSAFE = True
    
    def click_ok(self):
        """Click the OK button"""
        pyautogui.click(self.ok_pos[0], self.ok_pos[1])
        time.sleep(self.ok_delay)
    
    def click_live_image(self):
        """Click the Live Image button"""
        pyautogui.click(self.live_pos[0], self.live_pos[1])
        time.sleep(self.live_delay)
    
    def move_stage(self, direction, log_callback=None):
        """Move stage with arrow keys"""
        arrow_keys = {
            'right': 'right',
            'left': 'left',
            'down': 'down',
            'up': 'up'
        }
        if log_callback:
            log_callback(f"    → Pressing {direction} arrow")
        pyautogui.press(arrow_keys[direction])
        time.sleep(self.arrow_delay)
        if log_callback:
            log_callback(f"    ✓ {direction.upper()} key pressed")
    
    def capture_sequence(self):
        """Execute full capture: wait -> OK -> Live Image"""
        time.sleep(self.capture_delay)  # Wait for capture
        self.click_ok()                 # Close save dialog
        self.click_live_image()         # Return to live view


# ==============================================================================
# GRID NAVIGATOR
# ==============================================================================

class GridNavigator:
    """Generates serpentine path through grid"""
    
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.total = width * height
    
    def get_path(self):
        """
        Generate serpentine path
        
        Example 3x3:
        (0,0) -> (0,1) -> (0,2)
                           |
        (1,2) <- (1,1) <- (1,0)
          |
        (2,0) -> (2,1) -> (2,2)
        """
        path = []
        
        for row in range(self.height):
            if row % 2 == 0:
                # Even rows: left to right
                for col in range(self.width):
                    path.append((row, col))
            else:
                # Odd rows: right to left
                for col in range(self.width - 1, -1, -1):
                    path.append((row, col))
        
        return path
    
    def get_movement(self, current_pos, next_pos):
        """Calculate movement direction between two positions"""
        curr_row, curr_col = current_pos
        next_row, next_col = next_pos
        
        if next_row > curr_row:
            return 'down'
        elif next_col > curr_col:
            return 'right'
        elif next_col < curr_col:
            return 'left'
        else:
            return 'right'


# ==============================================================================
# CALIBRATION WINDOW
# ==============================================================================

class CalibrationWindow:
    """Window for calibrating button positions"""
    
    def __init__(self, parent_app):
        self.parent = parent_app
        self.window = tk.Toplevel(parent_app.root)
        self.window.title("Button Calibration")
        self.window.geometry("500x500")
        self.window.grab_set()  # Make modal
        
        self.setup_ui()
    
    def setup_ui(self):
        """Build calibration interface"""
        # Title
        tk.Label(
            self.window,
            text="Button Calibration",
            font=("Arial", 16, "bold")
        ).pack(pady=20)
        
        # Instructions
        tk.Label(
            self.window,
            text="Click a button below, then click the matching button\n"
                 "in the Viewer window within 5 seconds.",
            font=("Arial", 10),
            justify="center"
        ).pack(pady=10)
        
        # OK Button calibration
        tk.Button(
            self.window,
            text="1. Calibrate OK Button",
            font=("Arial", 11, "bold"),
            bg="#3498db",
            fg="white",
            padx=20,
            pady=15,
            command=lambda: self.calibrate('ok_button')
        ).pack(pady=10)
        
        # Live Image button calibration
        tk.Button(
            self.window,
            text="2. Calibrate Live Image Button",
            font=("Arial", 11, "bold"),
            bg="#3498db",
            fg="white",
            padx=20,
            pady=15,
            command=lambda: self.calibrate('live_image_button')
        ).pack(pady=10)
        
        # Status
        status_frame = tk.LabelFrame(self.window, text="Status", padx=20, pady=15)
        status_frame.pack(padx=20, pady=20, fill="both", expand=True)
        
        self.ok_status = tk.Label(status_frame, text="✗ OK Button: Not calibrated", fg="#e74c3c")
        self.ok_status.pack(pady=5)
        
        self.live_status = tk.Label(status_frame, text="✗ Live Image: Not calibrated", fg="#e74c3c")
        self.live_status.pack(pady=5)
        
        # Update status if already calibrated
        self.update_status()
        
        # Save button
        tk.Button(
            self.window,
            text="Save and Close",
            font=("Arial", 11, "bold"),
            bg="#27ae60",
            fg="white",
            padx=30,
            pady=10,
            command=self.save_and_close
        ).pack(pady=20)
    
    def calibrate(self, button_name):
        """Calibrate a button position"""
        # Inform user
        messagebox.showinfo(
            "Ready",
            f"Click OK, then click the {button_name.replace('_', ' ')} in Viewer.\n"
            f"You have 5 seconds."
        )
        
        # Countdown and capture
        for i in range(5, 0, -1):
            self.window.title(f"Calibration - Click in {i}...")
            self.window.update()
            time.sleep(1)
        
        # Capture position
        pos = pyautogui.position()
        self.parent.config.data[button_name] = [pos.x, pos.y]
        
        # Reset title and update status
        self.window.title("Button Calibration")
        self.update_status()
        
        messagebox.showinfo("Success", f"Position captured: ({pos.x}, {pos.y})")
    
    def update_status(self):
        """Update status labels"""
        if self.parent.config.data.get('ok_button'):
            pos = self.parent.config.data['ok_button']
            self.ok_status.config(text=f"✓ OK Button: ({pos[0]}, {pos[1]})", fg="#27ae60")
        
        if self.parent.config.data.get('live_image_button'):
            pos = self.parent.config.data['live_image_button']
            self.live_status.config(text=f"✓ Live Image: ({pos[0]}, {pos[1]})", fg="#27ae60")
    
    def save_and_close(self):
        """Save calibration and close window"""
        if not self.parent.config.data.get('ok_button'):
            messagebox.showerror("Incomplete", "Please calibrate the OK button.")
            return
        
        if not self.parent.config.data.get('live_image_button'):
            messagebox.showerror("Incomplete", "Please calibrate the Live Image button.")
            return
        
        self.parent.config.save()
        messagebox.showinfo("Saved", "Calibration saved!")
        self.window.destroy()


# ==============================================================================
# ARROW CALIBRATION WINDOW
# ==============================================================================

class ArrowCalibrationWindow:
    """Window for testing arrow key movements"""
    
    def __init__(self, parent_app):
        self.parent = parent_app
        self.window = tk.Toplevel(parent_app.root)
        self.window.title("Arrow Key Calibration")
        self.window.geometry("600x600")
        self.window.grab_set()
        
        self.controller = MicroscopeController(parent_app.config.data)
        self.setup_ui()
    
    def setup_ui(self):
        """Build calibration interface"""
        # Title
        tk.Label(
            self.window,
            text="Arrow Key Calibration",
            font=("Arial", 16, "bold")
        ).pack(pady=20)
        
        # Instructions
        instructions = [
            "Test each arrow direction to ensure the microscope stage moves correctly.",
            "Watch the microscope viewer to confirm movement.",
            "Test all 4 directions before starting automation."
        ]
        
        instr_frame = tk.Frame(self.window, bg="#ecf0f1", relief="ridge", bd=2)
        instr_frame.pack(padx=20, pady=10, fill="x")
        
        for instruction in instructions:
            tk.Label(
                instr_frame,
                text=f"• {instruction}",
                font=("Arial", 10),
                bg="#ecf0f1",
                anchor="w",
                justify="left"
            ).pack(fill="x", padx=15, pady=3)
        
        # Arrow buttons in cross pattern
        arrow_frame = tk.Frame(self.window)
        arrow_frame.pack(pady=30)
        
        # UP
        tk.Button(
            arrow_frame,
            text="▲ UP",
            font=("Arial", 12, "bold"),
            bg="#3498db",
            fg="white",
            width=10,
            height=2,
            command=lambda: self.test_arrow('up')
        ).grid(row=0, column=1, padx=5, pady=5)
        
        # LEFT
        tk.Button(
            arrow_frame,
            text="◄ LEFT",
            font=("Arial", 12, "bold"),
            bg="#3498db",
            fg="white",
            width=10,
            height=2,
            command=lambda: self.test_arrow('left')
        ).grid(row=1, column=0, padx=5, pady=5)
        
        # RIGHT
        tk.Button(
            arrow_frame,
            text="RIGHT ►",
            font=("Arial", 12, "bold"),
            bg="#3498db",
            fg="white",
            width=10,
            height=2,
            command=lambda: self.test_arrow('right')
        ).grid(row=1, column=2, padx=5, pady=5)
        
        # DOWN
        tk.Button(
            arrow_frame,
            text="▼ DOWN",
            font=("Arial", 12, "bold"),
            bg="#3498db",
            fg="white",
            width=10,
            height=2,
            command=lambda: self.test_arrow('down')
        ).grid(row=2, column=1, padx=5, pady=5)
        
        # Multiple presses
        multi_frame = tk.LabelFrame(self.window, text="Multiple Moves", padx=20, pady=15)
        multi_frame.pack(padx=20, pady=10, fill="x")
        
        tk.Label(multi_frame, text="Number of presses:").pack(side="left", padx=5)
        self.count_var = tk.StringVar(value="3")
        tk.Entry(multi_frame, textvariable=self.count_var, width=5, font=("Arial", 12)).pack(side="left", padx=5)
        
        tk.Button(
            multi_frame,
            text="Test Pattern (Right → Down → Left → Up)",
            font=("Arial", 10, "bold"),
            bg="#e67e22",
            fg="white",
            padx=15,
            pady=8,
            command=self.test_pattern
        ).pack(side="left", padx=10)
        
        # Log
        log_frame = tk.LabelFrame(self.window, text="Test Log", padx=10, pady=10)
        log_frame.pack(padx=20, pady=10, fill="both", expand=True)
        
        self.log_text = scrolledtext.ScrolledText(log_frame, height=10, font=("Courier", 9))
        self.log_text.pack(fill="both", expand=True)
        
        # Close button
        tk.Button(
            self.window,
            text="Done",
            font=("Arial", 11, "bold"),
            bg="#27ae60",
            fg="white",
            padx=30,
            pady=10,
            command=self.window.destroy
        ).pack(pady=20)
        
        self.log("Ready to test arrow movements")
    
    def log(self, message):
        """Add message to log"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        self.log_text.insert(tk.END, f"[{timestamp}] {message}\n")
        self.log_text.see(tk.END)
        self.window.update()
    
    def test_arrow(self, direction):
        """Test a single arrow direction"""
        self.log(f"Testing {direction.upper()} arrow...")
        self.controller.move_stage(direction, log_callback=self.log)
        self.log(f"Check if microscope moved {direction}")
        self.log("")
    
    def test_pattern(self):
        """Test all 4 directions in sequence"""
        try:
            count = int(self.count_var.get() or 1)
            if count < 1:
                count = 1
        except:
            self.log("Invalid count, using 1")
            count = 1
        
        self.log(f"=== Testing pattern ({count} moves each) ===")
        directions = ['right', 'down', 'left', 'up']
        
        for direction in directions:
            for i in range(count):
                self.log(f"{direction.upper()} move {i+1}/{count}")
                self.controller.move_stage(direction, log_callback=self.log)
        
        self.log("=== Pattern complete ===")
        self.log("")


# ==============================================================================
# MAIN APPLICATION
# ==============================================================================

class MicroscopeApp:
    """Main application window"""
    
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Bz-x800 Microscope Automation")
        self.root.geometry("600x700")
        
        # Load configuration
        self.config = Config()
        
        # State
        self.running = False
        self.stop_requested = False
        
        # Build UI
        self.setup_ui()
        
        # Check calibration
        if not self.config.is_calibrated():
            self.show_calibration_prompt()
    
    def setup_ui(self):
        """Build the user interface"""
        # Title
        tk.Label(
            self.root,
            text="Bz-x800 Microscope Automation",
            font=("Arial", 18, "bold")
        ).pack(pady=20)
        
        # Instructions
        instructions_frame = tk.LabelFrame(
            self.root,
            text="Instructions",
            font=("Arial", 11, "bold"),
            padx=20,
            pady=15
        )
        instructions_frame.pack(padx=20, pady=10, fill="x")
        
        for step in [
            "1. Open Bz-x800 Viewer",
            "2. Position microscope at TOP-LEFT corner",
            "3. Set focus",
            "4. Ensure save folder is configured",
            "",
            "⌨️ ESC or Ctrl+C to stop automation"
        ]:
            tk.Label(instructions_frame, text=step, anchor="w").pack(fill="x", pady=2)
        
        # Grid input
        grid_frame = tk.LabelFrame(
            self.root,
            text="Grid Size",
            font=("Arial", 11, "bold"),
            padx=20,
            pady=15
        )
        grid_frame.pack(padx=20, pady=10, fill="x")
        
        # Width
        width_row = tk.Frame(grid_frame)
        width_row.pack(fill="x", pady=5)
        tk.Label(width_row, text="Width:", width=15, anchor="w").pack(side="left")
        self.width_var = tk.StringVar(value="5")
        tk.Entry(width_row, textvariable=self.width_var, font=("Arial", 12), width=10).pack(side="left")
        
        # Height
        height_row = tk.Frame(grid_frame)
        height_row.pack(fill="x", pady=5)
        tk.Label(height_row, text="Height:", width=15, anchor="w").pack(side="left")
        self.height_var = tk.StringVar(value="8")
        tk.Entry(height_row, textvariable=self.height_var, font=("Arial", 12), width=10).pack(side="left")
        
        # Total
        self.total_label = tk.Label(grid_frame, text="Total: 40", font=("Arial", 10, "bold"))
        self.total_label.pack(pady=10)
        
        self.width_var.trace('w', self.update_total)
        self.height_var.trace('w', self.update_total)
        
        # Progress
        progress_frame = tk.LabelFrame(
            self.root,
            text="Progress",
            font=("Arial", 11, "bold"),
            padx=20,
            pady=15
        )
        progress_frame.pack(padx=20, pady=10, fill="both", expand=True)
        
        self.status_label = tk.Label(progress_frame, text="Ready", font=("Arial", 10))
        self.status_label.pack(pady=5)
        
        self.progress_var = tk.DoubleVar()
        self.progress_bar = ttk.Progressbar(
            progress_frame,
            variable=self.progress_var,
            maximum=100,
            length=500
        )
        self.progress_bar.pack(pady=10)
        
        self.progress_text = tk.Label(progress_frame, text="0 / 0", font=("Arial", 10, "bold"))
        self.progress_text.pack(pady=5)
        
        self.log_text = scrolledtext.ScrolledText(progress_frame, height=8, font=("Courier", 9))
        self.log_text.pack(fill="both", expand=True, pady=10)
        
        # Buttons
        button_frame = tk.Frame(self.root)
        button_frame.pack(pady=20)
        
        self.start_button = tk.Button(
            button_frame,
            text="START",
            font=("Arial", 12, "bold"),
            bg="#27ae60",
            fg="white",
            padx=30,
            pady=15,
            command=self.start
        )
        self.start_button.pack(side="left", padx=10)
        
        self.stop_button = tk.Button(
            button_frame,
            text="STOP",
            font=("Arial", 12, "bold"),
            bg="#e74c3c",
            fg="white",
            padx=30,
            pady=15,
            command=self.stop,
            state="disabled"
        )
        self.stop_button.pack(side="left", padx=10)
        
        tk.Button(
            button_frame,
            text="⚙ Calibrate Buttons",
            font=("Arial", 10),
            bg="#95a5a6",
            fg="white",
            padx=20,
            pady=10,
            command=self.open_calibration
        ).pack(side="left", padx=10)
        
        tk.Button(
            button_frame,
            text="🎯 Test Arrows",
            font=("Arial", 10),
            bg="#9b59b6",
            fg="white",
            padx=20,
            pady=10,
            command=self.open_arrow_calibration
        ).pack(side="left", padx=10)
        
        # Keyboard shortcuts
        self.root.bind('<Escape>', lambda e: self.stop() if self.running else None)
        self.root.bind('<Control-c>', lambda e: self.stop() if self.running else None)
    
    def update_total(self, *args):
        """Update total images label"""
        try:
            w = int(self.width_var.get() or 0)
            h = int(self.height_var.get() or 0)
            self.total_label.config(text=f"Total: {w * h}")
        except:
            self.total_label.config(text="Total: --")
    
    def log(self, message):
        """Add message to log"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        self.log_text.insert(tk.END, f"[{timestamp}] {message}\n")
        self.log_text.see(tk.END)
        self.root.update()
    
    def show_calibration_prompt(self):
        """Prompt user to calibrate"""
        response = messagebox.askyesno(
            "Calibration Needed",
            "Button positions need to be calibrated.\n\nCalibrate now?"
        )
        if response:
            self.open_calibration()
    
    def open_calibration(self):
        """Open calibration window"""
        CalibrationWindow(self)
    
    def open_arrow_calibration(self):
        """Open arrow calibration window"""
        if not self.config.is_calibrated():
            messagebox.showwarning(
                "Calibrate Buttons First",
                "Please calibrate the OK and Live Image buttons first.\n\n"
                "This ensures the controller is properly initialized."
            )
            self.open_calibration()
            return
        ArrowCalibrationWindow(self)
    
    def start(self):
        """Start automation"""
        # Validate input
        try:
            width = int(self.width_var.get())
            height = int(self.height_var.get())
            if width < 1 or height < 1:
                raise ValueError()
        except:
            messagebox.showerror("Invalid Input", "Enter valid positive numbers.")
            return
        
        # Check calibration
        if not self.config.is_calibrated():
            messagebox.showerror("Not Calibrated", "Calibrate buttons first.")
            self.open_calibration()
            return
        
        # Confirm
        total = width * height
        response = messagebox.askyesno(
            "Ready?",
            f"Capture {width} × {height} = {total} images?\n\n"
            "Make sure:\n"
            "✓ Viewer is open\n"
            "✓ Microscope at TOP-LEFT\n"
            "✓ Focus is set"
        )
        if not response:
            return
        
        # Prepare
        self.start_button.config(state="disabled")
        self.stop_button.config(state="normal")
        self.running = True
        self.stop_requested = False
        self.log_text.delete(1.0, tk.END)
        
        # Run in thread
        thread = threading.Thread(target=self.run_automation, args=(width, height), daemon=True)
        thread.start()
    
    def run_automation(self, width, height):
        """Main automation loop"""
        self.log("=== STARTED ===")
        self.log(f"Grid: {width} × {height}")
        
        # Initialize
        controller = MicroscopeController(self.config.data)
        navigator = GridNavigator(width, height)
        path = navigator.get_path()
        
        start_time = time.time()
        captured = 0
        
        try:
            for i, pos in enumerate(path):
                if self.stop_requested:
                    self.log("STOPPED by user")
                    break
                
                row, col = pos
                
                # Update UI
                progress = (i + 1) / navigator.total * 100
                self.progress_var.set(progress)
                self.progress_text.config(text=f"{i + 1} / {navigator.total}")
                self.status_label.config(text=f"Row {row}, Col {col}")
                
                self.log(f"[{i+1}/{navigator.total}] Row {row}, Col {col}")
                
                # Move (skip first position)
                if i > 0:
                    movement = navigator.get_movement(path[i-1], pos)
                    self.log(f"  Moving {movement}...")
                    controller.move_stage(movement, log_callback=self.log)
                
                # Capture
                self.log(f"  Capturing...")
                controller.capture_sequence()
                captured += 1
            
            # Done
            elapsed = time.time() - start_time
            self.log("=== COMPLETED ===")
            self.log(f"Captured: {captured}")
            self.log(f"Time: {elapsed/60:.1f} min")
            
            self.status_label.config(text="✓ Complete!")
            messagebox.showinfo("Complete", f"Captured {captured} images!")
            
        except Exception as e:
            self.log(f"ERROR: {e}")
            self.status_label.config(text="✗ Error")
            messagebox.showerror("Error", str(e))
        
        finally:
            self.running = False
            self.start_button.config(state="normal")
            self.stop_button.config(state="disabled")
    
    def stop(self):
        """Request stop"""
        if self.running:
            self.stop_requested = True
            self.log("Stop requested...")
            self.stop_button.config(state="disabled")
    
    def run(self):
        """Start the application"""
        self.root.mainloop()


# ==============================================================================
# ENTRY POINT
# ==============================================================================

if __name__ == "__main__":
    app = MicroscopeApp()
    app.run()
