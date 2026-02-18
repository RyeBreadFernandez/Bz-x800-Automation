# GUI Application Overview

## Main Window

```
╔══════════════════════════════════════════════════════════╗
║                                                          ║
║        Bz-x800 Microscope Automation                     ║
║                                                          ║
╠══════════════════════════════════════════════════════════╣
║                                                          ║
║  ┌─────────────────────────────────────────────────┐    ║
║  │ Instructions                                    │    ║
║  │                                                 │    ║
║  │ 1. Open Bz-x800 Viewer software                │    ║
║  │ 2. Position microscope at TOP-LEFT corner      │    ║
║  │ 3. Set focus (stays focused during capture)    │    ║
║  │ 4. Make sure save folder is configured         │    ║
║  │                                                 │    ║
║  └─────────────────────────────────────────────────┘    ║
║                                                          ║
║  ┌─────────────────────────────────────────────────┐    ║
║  │ Grid Size                                       │    ║
║  │                                                 │    ║
║  │  Width (images across):  [    5    ]           │    ║
║  │                                                 │    ║
║  │  Height (images down):   [    8    ]           │    ║
║  │                                                 │    ║
║  │           Total images: 40                      │    ║
║  │                                                 │    ║
║  └─────────────────────────────────────────────────┘    ║
║                                                          ║
║  ┌─────────────────────────────────────────────────┐    ║
║  │ Progress                                        │    ║
║  │                                                 │    ║
║  │  Status: Capturing: Row 2, Col 3               │    ║
║  │                                                 │    ║
║  │  [████████████░░░░░░░░░░░░░░░] 45%             │    ║
║  │                                                 │    ║
║  │  18 / 40 images                                │    ║
║  │                                                 │    ║
║  │  ┌──────────────────────────────────────────┐  │    ║
║  │  │ [12:34:56] Image 18 captured             │  │    ║
║  │  │ [12:34:55] Moving right                  │  │    ║
║  │  │ [12:34:54] Image 17 captured             │  │    ║
║  │  │ [12:34:53] Moving right                  │  │    ║
║  │  └──────────────────────────────────────────┘  │    ║
║  │                                                 │    ║
║  └─────────────────────────────────────────────────┘    ║
║                                                          ║
║  ┌────────────────┐  ┌──────────┐  ┌──────────────┐   ║
║  │ START          │  │  STOP    │  │ ⚙ Calibrate  │   ║
║  │ AUTOMATION     │  │          │  │              │   ║
║  └────────────────┘  └──────────┘  └──────────────┘   ║
║                                                          ║
╚══════════════════════════════════════════════════════════╝
```

## Calibration Window

```
╔══════════════════════════════════════════════════════════╗
║                                                          ║
║              Button Calibration                          ║
║                                                          ║
╠══════════════════════════════════════════════════════════╣
║                                                          ║
║  Click each button below, then click on the             ║
║  corresponding button in the Bz-x800 Viewer window.     ║
║                                                          ║
║  The position will be captured automatically.           ║
║                                                          ║
║  ┌──────────────────────────────────────────────────┐   ║
║  │                                                  │   ║
║  │         [  1. OK Button  ]                       │   ║
║  │                                                  │   ║
║  │  Click here, then click the OK button           │   ║
║  │  in the save dialog                              │   ║
║  │                                                  │   ║
║  └──────────────────────────────────────────────────┘   ║
║                                                          ║
║  ┌──────────────────────────────────────────────────┐   ║
║  │                                                  │   ║
║  │    [  2. Live Image Button  ]                    │   ║
║  │                                                  │   ║
║  │  Click here, then click the Live Image button   │   ║
║  │                                                  │   ║
║  └──────────────────────────────────────────────────┘   ║
║                                                          ║
║  ┌─────────────────────────────────────────────────┐    ║
║  │ Calibration Status                              │    ║
║  │                                                 │    ║
║  │  ✓ OK Button: (1234, 567)                      │    ║
║  │  ✓ Live Image Button: (1234, 890)              │    ║
║  │                                                 │    ║
║  └─────────────────────────────────────────────────┘    ║
║                                                          ║
║              [  Save and Close  ]                        ║
║                                                          ║
╚══════════════════════════════════════════════════════════╝
```

## Key Features

### User-Friendly Design:
- ✅ Big, clear buttons
- ✅ Simple input fields
- ✅ Visual progress bar
- ✅ Real-time log output
- ✅ Automatic total calculation
- ✅ Clear instructions on every screen

### Non-Technical Operation:
- ✅ No command line needed
- ✅ No code editing
- ✅ Visual calibration wizard
- ✅ Helpful error messages
- ✅ Can't proceed without required info

### Safety Features:
- ✅ Stop button always accessible
- ✅ Confirms before starting
- ✅ Validates all inputs
- ✅ Shows progress in real-time
- ✅ Graceful error handling

### Professional Polish:
- ✅ Color-coded status messages
- ✅ Timestamped logs
- ✅ Progress percentage
- ✅ Estimated time remaining
- ✅ Clean, modern interface
