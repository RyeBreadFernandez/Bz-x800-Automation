# Setup Instructions for Lab Computer

## For Lab IT / Installer

Follow these steps to set up the microscope automation on the lab computer.

---

## Method 1: Standalone Executable (EASIEST)

**Best for**: Lab computers without Python, non-technical users

### Steps:

1. **Get the executable** (one of these):
   - Option A: Download the pre-built `Microscope_Automation.exe`
   - Option B: Build it yourself (see "Building the Executable" below)

2. **Copy to lab computer**:
   - Create a folder: `C:\MicroscopeAutomation\`
   - Copy `Microscope_Automation.exe` into it

3. **Create desktop shortcut** (optional):
   - Right-click on `Microscope_Automation.exe`
   - Send to → Desktop (create shortcut)
   - Rename to "Microscope Automation"

4. **First-time setup**:
   - Double-click to run
   - Follow calibration wizard
   - Done!

**✅ Advantages**:
- No Python installation needed
- Single file
- Works on any Windows computer
- Users just double-click to run

---

## Method 2: Python Script

**Best for**: Development, testing, or computers with Python

### Requirements:
- Windows 10 or 11
- Python 3.8 or higher
- Internet connection (for initial setup)

### Steps:

1. **Install Python** (if not already installed):
   - Download from: https://www.python.org/downloads/
   - **CRITICAL**: Check "Add Python to PATH" during installation
   - Verify: Open Command Prompt, type `python --version`

2. **Copy program files to lab computer**:
   ```
   C:\MicroscopeAutomation\
   ├── main.py
   ├── START.bat
   ├── requirements.txt
   ├── core\
   │   ├── __init__.py
   │   ├── gui_automation.py
   │   └── grid_navigator.py
   └── USER_GUIDE.md
   ```

3. **Run first time**:
   - Double-click `START.bat`
   - It will auto-install dependencies
   - Program will start

4. **Create desktop shortcut** (optional):
   - Right-click `START.bat` → Send to → Desktop (create shortcut)
   - Rename to "Microscope Automation"

**✅ Advantages**:
- Easy to update (just replace main.py)
- Can debug if issues arise
- Full Python environment available

---

## Building the Executable (For Developers)

If you need to build the .exe yourself:

### On a Windows Machine:

1. **Install Python 3.8+** with PATH

2. **Open Command Prompt** in the project folder

3. **Run build script**:
   ```bash
   build.bat
   ```

4. **Find the executable**:
   - Location: `dist\Microscope_Automation.exe`
   - Size: ~15-20 MB
   - Copy this file to lab computers

### Manual Build (if build.bat doesn't work):

```bash
pip install pyinstaller pyautogui
pyinstaller --onefile --windowed --name "Microscope_Automation" main.py
```

---

## Testing the Installation

### Quick Test (2×2 grid):

1. Open Bz-x800 Viewer
2. Navigate to capture screen
3. Run the automation program
4. Click "⚙ Calibrate" (first time only)
5. Enter: Width `2`, Height `2`
6. Click START
7. Verify 4 images are captured

### Full Test (real grid):

1. Position actual tissue sample
2. Enter real grid dimensions
3. Run full automation
4. Verify all images captured correctly

---

## Configuration

### Default Settings

The program creates `config.json` on first run:

```json
{
  "ok_button": null,
  "live_image_button": null,
  "capture_delay": 1.0,
  "ok_delay": 0.8,
  "live_delay": 0.5,
  "arrow_delay": 0.3
}
```

### Location of config.json:

- **Executable**: Same folder as .exe
- **Python script**: Same folder as main.py

### Adjusting Speed:

If automation is too fast/slow, edit the delay values:
- **Increase** for slower computers
- **Decrease** for faster response
- Typical range: 0.3 - 2.0 seconds

---

## User Training

### Give users:
1. `USER_GUIDE.md` - Simple instructions
2. Desktop shortcut to program
3. 5-minute walkthrough of calibration

### Key points to teach:
- Always position microscope at TOP-LEFT
- Calibration only needed once
- Don't touch computer during capture
- How to stop if needed

---

## Troubleshooting

### "Python not found" error
- Solution: Install Python with PATH checked
- Or use the standalone .exe instead

### "Button positions not calibrated"
- Solution: Run calibration wizard
- Takes 2 minutes

### Program clicks wrong spots
- Cause: Screen resolution changed
- Solution: Re-run calibration

### Microscope doesn't move
- Cause: Viewer window not focused
- Solution: Click Viewer before starting

---

## File Locations

### User-facing files:
- `Microscope_Automation.exe` → Only file needed!
- `USER_GUIDE.md` → Instructions for users

### Technical files (keep for reference):
- `README.md` → Developer documentation
- `main.py` → Source code
- `core/` → Program modules
- `requirements.txt` → Python dependencies
- `build.bat` → Build script

---

## Security & Permissions

### Required permissions:
- Read/write in installation folder (for config.json)
- Mouse/keyboard control (for automation)
- No network access needed
- No admin rights needed

### Firewall:
- No special rules needed
- Program doesn't access network

---

## Support

### For Users:
- Refer to USER_GUIDE.md
- Contact lab IT support

### For IT Support:
- Refer to README.md (technical docs)
- Check config.json for settings
- Re-run calibration if issues

### For Developers:
- Review source code (main.py, core/)
- Test on actual microscope
- Use Python script version for debugging

---

## Quick Reference

### Installation Time:
- Executable method: **2 minutes**
- Python method: **10 minutes**

### Disk Space:
- Executable: **~20 MB**
- Python method: **~200 MB** (Python + dependencies)

### Internet Required:
- Executable: **No**
- Python method: **Yes** (first-time setup only)

---

## Success Checklist

- [ ] Program installed on lab computer
- [ ] Desktop shortcut created (optional)
- [ ] Calibration completed successfully
- [ ] Test capture (2×2 grid) works
- [ ] User trained on basic operation
- [ ] USER_GUIDE.md provided to users

**✅ Setup complete!**
