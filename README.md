# Bz-x800 Microscope Automation

Automated grid-based image capture for the Bz-x800 microscope. Simple GUI application for lab users.

## Features

- **Serpentine grid scanning** for efficient capture
- **Simple GUI** - no command line needed
- **One-time calibration** - just click on buttons
- **Real-time progress tracking** with live logs
- **Safe abort** - stop button or move mouse to corner

## Quick Start

### 1. Install Python
- Download Python 3.8+ from [python.org](https://www.python.org/downloads/)
- **Important**: Check "Add Python to PATH" during installation

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Run
```bash
python main.py
```

### 4. First-Time Setup
- Click "⚙ Calibrate"
- Follow the on-screen instructions
- Calibration is saved and only needed once

## Usage

Every session:

1. Open Bz-x800 Viewer software
2. Position microscope at **TOP-LEFT** corner of tissue
3. Set focus manually (maintained during capture)
4. Run the automation program
5. Enter grid dimensions (width × height)
6. Click START
7. Wait for completion

## How It Works

**Automation sequence:**
1. Waits for capture (manual or automated)
2. Clicks "OK" button in save dialog
3. Clicks "Live Image" button to return to live view
4. Moves stage with arrow keys (→ or ↓)
5. Repeats in serpentine pattern

**Serpentine Pattern:**
```
Start → → → →
            ↓
      ← ← ← ←
↓
→ → → → End
```

## Configuration

Settings are stored in `config.json` (auto-generated):

```json
{
  "ok_button": [x, y],          // Button positions (calibrated)
  "live_image_button": [x, y],
  "capture_delay": 1.0,         // Seconds to wait after capture
  "ok_delay": 0.8,              // Seconds after clicking OK
  "live_delay": 0.5,            // Seconds after clicking Live Image
  "arrow_delay": 0.3            // Seconds after stage movement
}
```

Adjust delays if automation is too fast/slow for your system.

## Requirements

- Windows 10/11
- Python 3.8 or higher
- Bz-x800 Viewer software installed
- ~50 MB disk space

## Troubleshooting

| Problem | Solution |
|---------|----------|
| "Button positions not calibrated" | Click ⚙ Calibrate and follow wizard |
| Clicks miss buttons | Re-run calibration |
| Stage doesn't move | Ensure Viewer window is focused |
| Automation too fast/slow | Edit delays in config.json |

## Building Standalone Executable

To create a standalone .exe (no Python needed on target computer):

```bash
pip install pyinstaller
pyinstaller --onefile --windowed --name "Microscope_Automation" main.py
```

Find the .exe in `dist/Microscope_Automation.exe`

## License

MIT License - Free to use and modify

## Author

Ryan - UCLA Undergraduate Researcher
