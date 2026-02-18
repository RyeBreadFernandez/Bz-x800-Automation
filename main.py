"""
Bz-x800 Microscope Automation - Main GUI Application
Simple interface for non-technical users
"""
import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import json
import time
import threading
from pathlib import Path
from datetime import datetime

from core.gui_automation import BzViewerController
from core.grid_navigator import GridNavigator


class MicroscopeAutomationApp:
    """Main GUI application"""
    
    def __init__(self, root):
        self.root = root
        self.root.title("Bz-x800 Microscope Automation")
        self.root.geometry("600x700")
        self.root.resizable(False, False)
        
        # Config file
        self.config_file = Path("config.json")
        self.config = self.load_config()
        
        # Automation state
        self.controller = None
        self.navigator = None
        self.automation_running = False
        self.stop_requested = False
        
        # Build UI
        self.setup_ui()
        
        # Check if calibrated
        if not self.is_calibrated():
            self.show_calibration_needed()
    
    def load_config(self):
        """Load configuration from file"""
        default_config = {
            "ok_button": None,
            "live_image_button": None,
            "capture_delay": 1.0,
            "ok_delay": 0.8,
            "live_delay": 0.5,
            "arrow_delay": 0.3
        }
        
        if self.config_file.exists():
            try:
                with open(self.config_file, 'r') as f:
                    return json.load(f)
            except:
                return default_config
        return default_config
    
    def save_config(self):
        """Save configuration to file"""
        with open(self.config_file, 'w') as f:
            json.dump(self.config, f, indent=2)
    
    def is_calibrated(self):
        """Check if GUI elements are calibrated"""
        return (self.config.get('ok_button') is not None and 
                self.config.get('live_image_button') is not None)
    
    def setup_ui(self):
        """Build the main user interface"""
        # Title
        title = tk.Label(
            self.root,
            text="Bz-x800 Microscope Automation",
            font=("Arial", 18, "bold"),
            fg="#2c3e50"
        )
        title.pack(pady=20)
        
        # Instructions frame
        instructions_frame = tk.LabelFrame(
            self.root,
            text="Instructions",
            font=("Arial", 11, "bold"),
            fg="#34495e",
            padx=20,
            pady=15
        )
        instructions_frame.pack(padx=20, pady=10, fill="x")
        
        instructions = [
            "1. Open Bz-x800 Viewer software",
            "2. Position microscope at TOP-LEFT corner of tissue",
            "3. Set focus (it will stay focused during capture)",
            "4. Make sure save folder is configured in Viewer"
        ]
        
        for instruction in instructions:
            lbl = tk.Label(
                instructions_frame,
                text=instruction,
                font=("Arial", 10),
                anchor="w"
            )
            lbl.pack(fill="x", pady=2)
        
        # Grid input frame
        grid_frame = tk.LabelFrame(
            self.root,
            text="Grid Size",
            font=("Arial", 11, "bold"),
            fg="#34495e",
            padx=20,
            pady=15
        )
        grid_frame.pack(padx=20, pady=10, fill="x")
        
        # Width input
        width_row = tk.Frame(grid_frame)
        width_row.pack(fill="x", pady=5)
        tk.Label(width_row, text="Width (images across):", font=("Arial", 10), width=20, anchor="w").pack(side="left")
        self.width_var = tk.StringVar(value="5")
        width_entry = tk.Entry(width_row, textvariable=self.width_var, font=("Arial", 12), width=10)
        width_entry.pack(side="left", padx=10)
        
        # Height input
        height_row = tk.Frame(grid_frame)
        height_row.pack(fill="x", pady=5)
        tk.Label(height_row, text="Height (images down):", font=("Arial", 10), width=20, anchor="w").pack(side="left")
        self.height_var = tk.StringVar(value="8")
        height_entry = tk.Entry(height_row, textvariable=self.height_var, font=("Arial", 12), width=10)
        height_entry.pack(side="left", padx=10)
        
        # Total images display
        self.total_label = tk.Label(
            grid_frame,
            text="Total images: 40",
            font=("Arial", 10, "bold"),
            fg="#16a085"
        )
        self.total_label.pack(pady=10)
        
        # Update total when values change
        self.width_var.trace('w', self.update_total)
        self.height_var.trace('w', self.update_total)
        
        # Progress frame
        progress_frame = tk.LabelFrame(
            self.root,
            text="Progress",
            font=("Arial", 11, "bold"),
            fg="#34495e",
            padx=20,
            pady=15
        )
        progress_frame.pack(padx=20, pady=10, fill="both", expand=True)
        
        # Status label
        self.status_label = tk.Label(
            progress_frame,
            text="Ready to start",
            font=("Arial", 10),
            fg="#7f8c8d"
        )
        self.status_label.pack(pady=5)
        
        # Progress bar
        self.progress_var = tk.DoubleVar()
        self.progress_bar = ttk.Progressbar(
            progress_frame,
            variable=self.progress_var,
            maximum=100,
            length=500
        )
        self.progress_bar.pack(pady=10)
        
        # Progress text
        self.progress_text = tk.Label(
            progress_frame,
            text="0 / 0 images",
            font=("Arial", 10, "bold")
        )
        self.progress_text.pack(pady=5)
        
        # Log output
        self.log_text = scrolledtext.ScrolledText(
            progress_frame,
            height=8,
            font=("Courier", 9),
            bg="#ecf0f1",
            fg="#2c3e50"
        )
        self.log_text.pack(fill="both", expand=True, pady=10)
        
        # Button frame
        button_frame = tk.Frame(self.root)
        button_frame.pack(pady=20)
        
        # Start button
        self.start_button = tk.Button(
            button_frame,
            text="START AUTOMATION",
            font=("Arial", 12, "bold"),
            bg="#27ae60",
            fg="white",
            padx=30,
            pady=15,
            command=self.start_automation,
            cursor="hand2"
        )
        self.start_button.pack(side="left", padx=10)
        
        # Stop button
        self.stop_button = tk.Button(
            button_frame,
            text="STOP",
            font=("Arial", 12, "bold"),
            bg="#e74c3c",
            fg="white",
            padx=30,
            pady=15,
            command=self.stop_automation,
            state="disabled",
            cursor="hand2"
        )
        self.stop_button.pack(side="left", padx=10)
        
        # Settings button
        settings_button = tk.Button(
            button_frame,
            text="⚙ Calibrate",
            font=("Arial", 10),
            bg="#95a5a6",
            fg="white",
            padx=20,
            pady=10,
            command=self.open_calibration,
            cursor="hand2"
        )
        settings_button.pack(side="left", padx=10)
    
    def update_total(self, *args):
        """Update total images display"""
        try:
            width = int(self.width_var.get() or 0)
            height = int(self.height_var.get() or 0)
            total = width * height
            self.total_label.config(text=f"Total images: {total}")
        except:
            self.total_label.config(text="Total images: --")
    
    def log(self, message, level="INFO"):
        """Add message to log"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        log_line = f"[{timestamp}] {message}\n"
        self.log_text.insert(tk.END, log_line)
        self.log_text.see(tk.END)
        self.root.update()
    
    def show_calibration_needed(self):
        """Show message that calibration is needed"""
        response = messagebox.askyesno(
            "Calibration Required",
            "Button positions need to be calibrated.\n\n"
            "This only needs to be done once.\n\n"
            "Open calibration now?",
            icon='warning'
        )
        if response:
            self.open_calibration()
    
    def open_calibration(self):
        """Open calibration window"""
        CalibrationWindow(self)
    
    def start_automation(self):
        """Start the automation process"""
        # Validate inputs
        try:
            width = int(self.width_var.get())
            height = int(self.height_var.get())
            if width < 1 or height < 1:
                raise ValueError()
        except:
            messagebox.showerror("Invalid Input", "Please enter valid positive numbers for width and height.")
            return
        
        # Check calibration
        if not self.is_calibrated():
            messagebox.showerror("Not Calibrated", "Please calibrate button positions first.")
            self.open_calibration()
            return
        
        # Confirm start
        total = width * height
        response = messagebox.askyesno(
            "Ready to Start?",
            f"Grid: {width} × {height} = {total} images\n\n"
            "Make sure:\n"
            "✓ Viewer is open\n"
            "✓ Microscope is at TOP-LEFT corner\n"
            "✓ Focus is set\n\n"
            "Start automation?",
            icon='question'
        )
        
        if not response:
            return
        
        # Disable inputs
        self.start_button.config(state="disabled")
        self.stop_button.config(state="normal")
        self.automation_running = True
        self.stop_requested = False
        
        # Clear log
        self.log_text.delete(1.0, tk.END)
        
        # Initialize components
        self.navigator = GridNavigator(width, height)
        self.controller = BzViewerController(self.config)
        
        # Run in separate thread
        thread = threading.Thread(target=self.run_automation, daemon=True)
        thread.start()
    
    def run_automation(self):
        """Run the automation loop (in separate thread)"""
        self.log("=== AUTOMATION STARTED ===")
        self.log(f"Grid: {self.navigator.width} × {self.navigator.height}")
        
        start_time = time.time()
        images_captured = 0
        
        try:
            for index, total, position, movement in self.navigator.iter_path_with_movements():
                if self.stop_requested:
                    self.log("STOPPED by user")
                    break
                
                row, col = position
                
                # Update UI
                progress = (index + 1) / total * 100
                self.progress_var.set(progress)
                self.progress_text.config(text=f"{index + 1} / {total} images")
                self.status_label.config(text=f"Capturing: Row {row}, Col {col}")
                
                self.log(f"[{index+1}/{total}] Position: Row {row}, Col {col}")
                
                # Move stage (skip first position)
                if movement != 'start':
                    self.log(f"  → Moving {movement}")
                    if not self.controller.move_stage(movement):
                        raise RuntimeError(f"Failed to move {movement}")
                
                # Capture sequence
                self.log(f"  → Capturing image...")
                if not self.controller.execute_capture_sequence():
                    raise RuntimeError("Capture sequence failed")
                
                images_captured += 1
                
            # Completed
            elapsed = time.time() - start_time
            self.log("=== AUTOMATION COMPLETED ===")
            self.log(f"Images captured: {images_captured}")
            self.log(f"Time: {elapsed/60:.1f} minutes")
            
            self.status_label.config(text="✓ Completed!", fg="#27ae60")
            messagebox.showinfo("Complete", f"Successfully captured {images_captured} images!")
            
        except Exception as e:
            self.log(f"ERROR: {e}")
            self.status_label.config(text="✗ Error occurred", fg="#e74c3c")
            messagebox.showerror("Error", f"Automation failed:\n{e}")
        
        finally:
            self.automation_running = False
            self.start_button.config(state="normal")
            self.stop_button.config(state="disabled")
    
    def stop_automation(self):
        """Request automation stop"""
        if self.automation_running:
            self.stop_requested = True
            self.log("Stop requested - will stop after current image...")
            self.stop_button.config(state="disabled")


class CalibrationWindow:
    """Calibration dialog for finding button positions"""
    
    def __init__(self, parent):
        self.parent = parent
        self.window = tk.Toplevel(parent.root)
        self.window.title("Button Calibration")
        self.window.geometry("500x600")
        self.window.resizable(False, False)
        self.window.grab_set()  # Make modal
        
        self.calibration_data = {}
        self.setup_ui()
    
    def setup_ui(self):
        """Build calibration UI"""
        # Title
        title = tk.Label(
            self.window,
            text="Button Calibration",
            font=("Arial", 16, "bold"),
            fg="#2c3e50"
        )
        title.pack(pady=20)
        
        # Instructions
        instructions = tk.Label(
            self.window,
            text="Click each button below, then click on the corresponding\n"
                 "button in the Bz-x800 Viewer window.\n\n"
                 "The position will be captured automatically.",
            font=("Arial", 10),
            fg="#7f8c8d",
            justify="center"
        )
        instructions.pack(pady=10)
        
        # Calibration buttons frame
        buttons_frame = tk.Frame(self.window)
        buttons_frame.pack(pady=30)
        
        # OK button calibration
        self.create_calibration_button(
            buttons_frame,
            "1. OK Button",
            "Click here, then click the OK button in the save dialog",
            "ok_button",
            0
        )
        
        # Live Image button calibration
        self.create_calibration_button(
            buttons_frame,
            "2. Live Image Button",
            "Click here, then click the Live Image button",
            "live_image_button",
            1
        )
        
        # Status display
        self.status_frame = tk.LabelFrame(
            self.window,
            text="Calibration Status",
            font=("Arial", 10, "bold"),
            padx=20,
            pady=15
        )
        self.status_frame.pack(padx=20, pady=20, fill="both", expand=True)
        
        self.ok_status = tk.Label(self.status_frame, text="✗ OK Button: Not calibrated", fg="#e74c3c", anchor="w")
        self.ok_status.pack(fill="x", pady=5)
        
        self.live_status = tk.Label(self.status_frame, text="✗ Live Image Button: Not calibrated", fg="#e74c3c", anchor="w")
        self.live_status.pack(fill="x", pady=5)
        
        # Update status if already calibrated
        if self.parent.config.get('ok_button'):
            pos = self.parent.config['ok_button']
            self.ok_status.config(text=f"✓ OK Button: ({pos[0]}, {pos[1]})", fg="#27ae60")
        
        if self.parent.config.get('live_image_button'):
            pos = self.parent.config['live_image_button']
            self.live_status.config(text=f"✓ Live Image Button: ({pos[0]}, {pos[1]})", fg="#27ae60")
        
        # Save button
        save_button = tk.Button(
            self.window,
            text="Save and Close",
            font=("Arial", 11, "bold"),
            bg="#27ae60",
            fg="white",
            padx=30,
            pady=10,
            command=self.save_and_close,
            cursor="hand2"
        )
        save_button.pack(pady=20)
    
    def create_calibration_button(self, parent, title, description, key, row):
        """Create a calibration button"""
        frame = tk.Frame(parent)
        frame.pack(pady=10, fill="x")
        
        button = tk.Button(
            frame,
            text=title,
            font=("Arial", 11, "bold"),
            bg="#3498db",
            fg="white",
            padx=20,
            pady=15,
            width=20,
            command=lambda: self.start_position_capture(key),
            cursor="hand2"
        )
        button.pack()
        
        desc_label = tk.Label(frame, text=description, font=("Arial", 9), fg="#7f8c8d")
        desc_label.pack(pady=5)
    
    def start_position_capture(self, key):
        """Start capturing mouse position"""
        messagebox.showinfo(
            "Ready to Capture",
            f"Click OK, then click on the {key.replace('_', ' ')} in the Viewer window.\n\n"
            "You have 5 seconds."
        )
        
        # Wait briefly then capture
        self.window.after(100, lambda: self.capture_position(key))
    
    def capture_position(self, key):
        """Capture mouse position after delay"""
        import pyautogui
        
        # Countdown
        for i in range(5, 0, -1):
            self.window.title(f"Calibration - Click in {i}...")
            self.window.update()
            time.sleep(1)
        
        # Capture position
        pos = pyautogui.position()
        self.calibration_data[key] = [pos.x, pos.y]
        
        self.window.title("Button Calibration")
        
        # Update status
        if key == 'ok_button':
            self.ok_status.config(text=f"✓ OK Button: ({pos.x}, {pos.y})", fg="#27ae60")
        elif key == 'live_image_button':
            self.live_status.config(text=f"✓ Live Image Button: ({pos.x}, {pos.y})", fg="#27ae60")
        
        messagebox.showinfo("Success", f"Position captured: ({pos.x}, {pos.y})")
    
    def save_and_close(self):
        """Save calibration and close window"""
        if not self.calibration_data.get('ok_button') and not self.parent.config.get('ok_button'):
            messagebox.showerror("Incomplete", "Please calibrate the OK button.")
            return
        
        if not self.calibration_data.get('live_image_button') and not self.parent.config.get('live_image_button'):
            messagebox.showerror("Incomplete", "Please calibrate the Live Image button.")
            return
        
        # Update parent config
        for key, value in self.calibration_data.items():
            self.parent.config[key] = value
        
        self.parent.save_config()
        
        messagebox.showinfo("Saved", "Calibration saved successfully!")
        self.window.destroy()


def main():
    """Entry point"""
    root = tk.Tk()
    app = MicroscopeAutomationApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
