# User Guide - Bz-x800 Microscope Automation

## Quick Start

### First Time Only

1. **Install Python**
   - Download from python.org
   - Check "Add Python to PATH" when installing

2. **Install the program**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run it**
   ```bash
   python main.py
   ```

4. **Calibrate buttons** (takes 2 minutes)
   - Click "⚙ Calibrate"
   - Follow the on-screen instructions
   - Done! (Never needed again)

---

## Every Session

### 1. Prepare Microscope
- Open Bz-x800 Viewer
- Position microscope at **TOP-LEFT** corner
- Set focus
- Check save folder is configured

### 2. Run Automation
```bash
python main.py
```

### 3. Enter Grid Size
- Width: How many images across? (e.g., 5)
- Height: How many images down? (e.g., 8)
- Total shows automatically (e.g., 40 images)

### 4. Start
- Click "START"
- Confirm you're ready
- Walk away
- Come back when done!

---

## What It Does

1. Waits for image capture
2. Clicks "OK" in save dialog
3. Clicks "Live Image" to return to view
4. Moves stage with arrow keys
5. Repeats in serpentine pattern

```
Path Example:
→ → → →
      ↓
← ← ← ←
↓
→ → → →
```

---

## Troubleshooting

**"Button positions not calibrated"**
- Click ⚙ Calibrate and follow wizard

**Clicks miss the buttons**
- Run calibration again

**Stage doesn't move**
- Make sure Viewer window is active

**Too fast or too slow**
- Edit `config.json` and adjust delays

---

## Tips

- Test with 2×2 grid first
- Don't touch computer during capture
- Click STOP if you need to abort
- Focus stays locked during capture
- Images save where Viewer is configured

---

That's it! Simple automated microscope imaging.
