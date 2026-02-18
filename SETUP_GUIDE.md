# COMPLETE SETUP GUIDE

## PART 1: GitHub Setup (First Time)

### Step 1: Install Git

1. **Download Git:**
   - Go to: https://git-scm.com/download/win
   - Download and install
   - Use default settings

2. **Verify installation:**
   ```bash
   git --version
   ```

### Step 2: Create GitHub Account (if needed)

1. Go to: https://github.com
2. Sign up (free)
3. Verify your email

### Step 3: Create Repository

1. **On GitHub.com:**
   - Click the "+" icon (top right)
   - Click "New repository"
   - Repository name: `bz-microscope-automation`
   - Description: "Automated grid capture for Bz-x800 microscope"
   - Public or Private (your choice)
   - ✅ Check "Add a README file"
   - Click "Create repository"

2. **Copy the repository URL:**
   - Click the green "Code" button
   - Copy the HTTPS URL (looks like: `https://github.com/YOUR_USERNAME/bz-microscope-automation.git`)

### Step 4: Upload Your Code

**Open Command Prompt in the `bz_automation` folder:**

```bash
# Initialize git (first time only)
git init

# Add all files
git add .

# Commit
git commit -m "Initial commit: Microscope automation application"

# Connect to GitHub
git remote add origin https://github.com/YOUR_USERNAME/bz-microscope-automation.git

# Push to GitHub
git push -u origin main
```

**If you get an error about "main" vs "master":**
```bash
git branch -M main
git push -u origin main
```

**If asked for credentials:**
- Username: Your GitHub username
- Password: Use a Personal Access Token (not your password)
  - Get token at: https://github.com/settings/tokens
  - Click "Generate new token (classic)"
  - Give it a name, check "repo" scope
  - Copy the token and use it as password

---

## PART 2: Running on Your Machine

### Step 1: Install Python

1. **Download Python:**
   - Go to: https://www.python.org/downloads/
   - Download Python 3.10 or newer
   - **IMPORTANT:** Check "Add Python to PATH" during installation

2. **Verify:**
   ```bash
   python --version
   ```

### Step 2: Get the Code

**If you uploaded to GitHub:**
```bash
# Clone your repository
cd C:\
git clone https://github.com/YOUR_USERNAME/bz-microscope-automation.git
cd bz-microscope-automation
```

**If working locally:**
```bash
# Just navigate to the folder
cd path\to\bz_automation
```

### Step 3: Test the Application

```bash
# Install dependencies
pip install -r requirements.txt

# Run the application
python main.py
```

**The GUI should open!**

### Step 4: Build the .exe (Optional)

```bash
# Build standalone executable
python build.bat

# Or manually:
pip install pyinstaller
pyinstaller --onefile --windowed --name "MicroscopeAutomation" --add-data "core;core" main.py
```

**Result:** `dist\MicroscopeAutomation.exe`

---

## PART 3: Deploy to Lab Computer

### Method A: Copy the .exe

1. **On your computer:**
   - Build the .exe (see Step 4 above)
   - Find: `dist\MicroscopeAutomation.exe`

2. **Copy to lab computer:**
   - USB drive
   - Network share
   - Email (if small enough)

3. **On lab computer:**
   - No Python needed!
   - Just double-click the .exe

### Method B: Clone from GitHub

1. **On lab computer:**
   ```bash
   # Install Git (if needed)
   # Install Python (if needed)
   
   # Clone repository
   git clone https://github.com/YOUR_USERNAME/bz-microscope-automation.git
   cd bz-microscope-automation
   
   # Install and run
   pip install -r requirements.txt
   python main.py
   ```

---

## PART 4: Making Updates

### When you fix bugs or add features:

1. **Edit the code** (main.py, etc.)

2. **Test it:**
   ```bash
   python main.py
   ```

3. **Commit to GitHub:**
   ```bash
   git add .
   git commit -m "Description of what you changed"
   git push
   ```

4. **Rebuild .exe (if distributing):**
   ```bash
   python build.bat
   ```

5. **Deploy to lab:**
   - Copy new .exe to lab computer
   - Or on lab computer: `git pull` to get updates

---

## QUICK REFERENCE

### First Time Setup:
```bash
# 1. Install Python
# 2. Navigate to folder
cd bz_automation

# 3. Upload to GitHub
git init
git add .
git commit -m "Initial commit"
git remote add origin https://github.com/YOUR_USERNAME/REPO_NAME.git
git push -u origin main

# 4. Test locally
pip install -r requirements.txt
python main.py

# 5. Build .exe
python build.bat
```

### Daily Development:
```bash
# Make changes...

# Test
python main.py

# Commit
git add .
git commit -m "What you changed"
git push
```

### Deploying to Lab:
```bash
# Option 1: Copy dist/MicroscopeAutomation.exe
# Option 2: git clone on lab computer
```

---

## Troubleshooting

### "git not found"
- Install Git from git-scm.com
- Restart Command Prompt

### "Python not found"
- Install Python from python.org
- Check "Add to PATH" during install
- Restart Command Prompt

### "Permission denied" on GitHub push
- Use Personal Access Token instead of password
- Get at: https://github.com/settings/tokens

### Build fails
```bash
# Update PyInstaller
pip install --upgrade pyinstaller

# Try again
python build.bat
```

### .exe doesn't run on other computer
- Make sure you used `--onefile` flag
- Test on computer without Python
- Check Windows Defender settings

---

## File Structure Explained

```
bz_automation/
├── main.py                  # Main application (all GUI + automation)
├── core/
│   ├── __init__.py         # Makes core a Python package
│   └── grid_navigator.py   # Grid path generation
├── requirements.txt         # Python dependencies
├── run.bat                  # Quick test script
├── build.bat               # Build .exe script
├── README.md               # Project documentation
└── config.json             # Created on first run (calibration data)
```

---

## Success Checklist

- [ ] Git installed
- [ ] Python installed
- [ ] Code uploaded to GitHub
- [ ] Tested locally with `python main.py`
- [ ] .exe built successfully
- [ ] .exe tested on your computer
- [ ] .exe deployed to lab computer
- [ ] Calibration completed on lab computer
- [ ] Test capture (2×2 grid) successful

**You're done!**
