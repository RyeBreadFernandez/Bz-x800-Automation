# Bz-x800 Microscope Automation - Deployment Guide

## Overview

This is a standalone GUI application for automating grid-based image capture on the Bz-x800 microscope. Designed for non-technical lab users.

## Architecture

```
bz_automation/
├── main.py                    # GUI application (tkinter)
├── core/
│   ├── gui_automation.py      # PyAutoGUI automation
│   └── grid_navigator.py      # Grid path logic
├── config.json                # Runtime config (created on first run)
├── START.bat                  # Simple launcher
└── build.bat                  # Build standalone .exe
```

## Deployment Options

### Option 1: Standalone Executable (Recommended for Lab)

**Build the .exe once, distribute to all users:**

```bash
# On development machine:
pip install -r requirements.txt
python build.bat

# This creates: dist/Microscope_Automation.exe
```

**Distribute:**
- Copy `Microscope_Automation.exe` to lab computer
- Users double-click to run
- No Python installation needed
- Config saved next to .exe

### Option 2: Python Script (Development/Testing)

**Requirements:**
- Python 3.8+
- Dependencies in requirements.txt

**Run:**
```bash
pip install -r requirements.txt
python main.py
```

Or use the launcher:
```bash
START.bat   # Windows
```

## Configuration

### Calibration Data (config.json)

Created automatically on first calibration:

```json
{
  "ok_button": [1234, 567],          // X, Y pixel position
  "live_image_button": [1234, 890],
  "capture_delay": 1.0,              // Seconds to wait after capture
  "ok_delay": 0.8,                   // Seconds to wait after OK click
  "live_delay": 0.5,                 // Seconds to wait after Live Image
  "arrow_delay": 0.3                 // Seconds to wait after stage move
}
```

### Tuning Delays

If automation is too fast/slow:
- Increase delays for slower computers
- Decrease for faster response
- Typical range: 0.3 - 2.0 seconds

## User Workflow

1. **First Time Setup** (5 minutes):
   - Run program
   - Click "Calibrate"
   - Click each button as prompted
   - Positions saved permanently

2. **Every Session** (30 seconds):
   - Open Viewer software
   - Position microscope at top-left
   - Run program
   - Enter grid size
   - Click START

## Technical Details

### GUI Framework
- **tkinter**: Built-in with Python, no extra dependencies
- **Threading**: Automation runs in background thread
- **Modal dialogs**: For calibration workflow

### Automation
- **PyAutoGUI**: Simulates mouse clicks and keyboard
- **Failsafe**: Move mouse to corner to abort
- **Serpentine path**: Minimizes stage movement

### Error Handling
- Validates grid inputs
- Checks calibration status
- Graceful stop on Ctrl+C or stop button
- All errors shown in GUI

## Building for Distribution

### Creating the .exe

```bash
# Install PyInstaller
pip install pyinstaller

# Build
pyinstaller --onefile --windowed --name "Microscope_Automation" main.py

# Output: dist/Microscope_Automation.exe
```

### Testing the .exe

1. Copy .exe to clean machine (no Python)
2. Run it
3. Calibrate
4. Test with 2×2 grid
5. Verify all captures work

### File Size

- Typical .exe size: ~15-20 MB
- Includes Python interpreter + dependencies
- Single file, no installation needed

## Troubleshooting

### Common Issues

**"Button positions not calibrated"**
- Solution: Run calibration wizard

**Clicks miss the buttons**
- Cause: Screen resolution changed or buttons moved
- Solution: Re-run calibration

**Stage doesn't move**
- Cause: Viewer window not focused
- Solution: Click on Viewer window before starting

**Automation too fast/slow**
- Solution: Edit delays in config.json

### Debug Mode

To see detailed logs, run from command line:
```bash
python main.py
```

Console will show all operations in real-time.

## Maintenance

### Updating the Application

1. Modify source code
2. Test with `python main.py`
3. Rebuild: `python build.bat`
4. Distribute new .exe

### Version Control

Recommended Git workflow:
```bash
git add main.py core/
git commit -m "Description of changes"
git tag v1.0.0
```

## Security Notes

- No network access required
- No sensitive data stored
- Config file contains only GUI coordinates
- Safe for lab environment

## Future Enhancements

Potential additions:
- [ ] Variable overlap percentage
- [ ] Auto-focus verification
- [ ] Multi-channel support
- [ ] Integrated image stitching
- [ ] Session resume after interruption
- [ ] Export capture log to CSV

## Support

For lab users:
- Refer to USER_GUIDE.md
- Contact lab IT support

For developers:
- Check this README
- Review code comments
- Test on target hardware
