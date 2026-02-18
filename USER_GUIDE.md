# Bz-x800 Microscope Automation
## Simple Guide for Lab Users

---

## 🚀 QUICK START (First Time)

### Option 1: Use the .exe file (EASIEST - No Python needed)
1. Copy `Microscope_Automation.exe` to your computer
2. Double-click it to run
3. Done!

### Option 2: Run from Python
1. Install Python from https://www.python.org/downloads/
   - **IMPORTANT**: Check "Add Python to PATH" during installation
2. Double-click `START.bat`
3. Wait for setup to complete
4. Done!

---

## 📋 HOW TO USE

### Every Session:

1. **Open the microscope software** (Bz-x800 Viewer)

2. **Set up your microscope**:
   - Position at TOP-LEFT corner of tissue
   - Focus on the sample
   - Check save folder is set

3. **First time only**: Click "⚙ Calibrate" button
   - Click "1. OK Button" → Click OK button in Viewer
   - Click "2. Live Image Button" → Click Live Image in Viewer
   - Click "Save and Close"
   - **You only need to do this ONCE!**

4. **Enter grid size**:
   - Width: How many images across?
   - Height: How many images down?
   - Example: 5 wide × 8 tall = 40 images total

5. **Click "START AUTOMATION"**

6. **Let it run!**
   - Progress bar shows how many images done
   - Log shows each capture
   - Don't touch the computer during capture

7. **All done!**
   - Images saved in Viewer's save folder
   - Ready for stitching!

---

## ⚠️ IMPORTANT TIPS

### Before Starting:
- ✅ Microscope at TOP-LEFT corner
- ✅ Focus is correct
- ✅ Save folder is set in Viewer
- ✅ Viewer window is on screen (not minimized)

### During Capture:
- ❌ Don't move the mouse
- ❌ Don't click anything
- ❌ Don't minimize windows
- ✅ If you need to stop, click "STOP" button

### If Something Goes Wrong:
- Click "STOP" button
- Check the microscope position
- Re-run calibration if buttons moved
- Try a small grid first (2×2) to test

---

## 🔧 TROUBLESHOOTING

| Problem | Solution |
|---------|----------|
| "Button positions not calibrated" | Click "⚙ Calibrate" and follow steps |
| Program doesn't click the right spots | Run calibration again |
| Microscope doesn't move | Make sure Viewer window is focused |
| Capture seems to skip positions | Increase delays (see Advanced Settings) |
| Python error when starting | Make sure Python is installed with PATH |

---

## 🎯 EXAMPLE

**Scenario**: You want to capture a 5×8 grid

1. Position microscope at top-left of tissue
2. Enter Width: `5`
3. Enter Height: `8`
4. You'll see "Total images: 40"
5. Click START AUTOMATION
6. Wait ~5-10 minutes (depending on your settings)
7. Done! 40 images ready for stitching

---

## 📁 FILE LOCATIONS

- **Images**: Saved where Viewer is configured to save
- **Config**: `config.json` (stores button positions)
- **This program**: Can be anywhere on your computer

---

## 🆘 GET HELP

If you have problems:
1. Check the log output in the program
2. Try calibrating again
3. Test with a 2×2 grid first
4. Make sure Viewer is the active window

---

## ⚙️ ADVANCED SETTINGS

If captures are too fast/slow, edit `config.json`:

```json
{
  "capture_delay": 1.0,   ← Time after capture trigger
  "ok_delay": 0.8,        ← Time after clicking OK
  "live_delay": 0.5,      ← Time after clicking Live Image
  "arrow_delay": 0.3      ← Time after moving stage
}
```

Increase these numbers if things are going too fast.

---

## ✨ That's It!

This program automates the tedious work of capturing grid images.
You focus on the science, let the computer do the clicking!
