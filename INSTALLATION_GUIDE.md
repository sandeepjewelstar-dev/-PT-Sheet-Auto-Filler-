# 🚀 PT Sheet Auto-Filler - Complete Installation & Setup Guide

## **Your Software Location**
```
C:\Users\Admin\Documents\-PT-Sheet-Auto-Filler--main\-PT-Sheet-Auto-Filler--main
```

---

## **STEP 1: Verify Files Are Present**

Navigate to your folder and check if these files exist:

✅ `main.py` - Main application (run this to start)
✅ `config.py` - Configuration settings
✅ `ocr_extractor.py` - OCR module
✅ `excel_writer.py` - Excel filling module
✅ `validator.py` - Data validation module
✅ `requirements.txt` - Python dependencies
✅ `README.md` - Documentation

If any files are missing, download them from:
https://github.com/sandeepjewelstar-dev/-PT-Sheet-Auto-Filler-

---

## **STEP 2: Install Python (if not already installed)**

### **Check if Python is installed:**
1. Open Command Prompt (press `Win + R`, type `cmd`, press Enter)
2. Type this command:
   ```
   python --version
   ```
3. If you see a version number (e.g., Python 3.9.0), skip to **STEP 3**
4. If you get an error, download Python from: https://www.python.org/downloads/
   - **Important:** Check "Add Python to PATH" during installation ✅

---

## **STEP 3: Install Python Dependencies**

### **Method A: Automatic Installation (Recommended)**

1. **Open Command Prompt in your project folder:**
   - Navigate to: `C:\Users\Admin\Documents\-PT-Sheet-Auto-Filler--main\-PT-Sheet-Auto-Filler--main`
   - Right-click in empty space → "Open Command Prompt here"

2. **Run this command:**
   ```
   pip install -r requirements.txt
   ```

   This installs all required packages:
   - openpyxl (for Excel)
   - opencv-python (for image processing)
   - pytesseract (for OCR)
   - pillow (for image handling)
   - numpy & pandas (for data processing)

3. **Wait for installation to complete** (2-5 minutes)

### **Method B: Manual Installation**

If Method A doesn't work, run these commands one by one:

```
pip install openpyxl==3.9.0
pip install opencv-python==4.7.0.72
pip install pytesseract==0.3.10
pip install pillow==9.5.0
pip install numpy==1.24.3
pip install pandas==2.0.3
```

---

## **STEP 4: Install Tesseract OCR (Required for OCR)**

### **Windows Installation:**

1. Download Tesseract installer from:
   https://github.com/UB-Mannheim/tesseract/wiki

2. Download the latest version (e.g., `tesseract-ocr-w64-setup-v5.x.exe`)

3. Run the installer:
   - Click "Next" through all screens
   - **Important:** Note the installation path (default: `C:\Program Files\Tesseract-OCR`)
   - Complete installation

4. **Verify Tesseract installation:**
   ```
   tesseract --version
   ```

---

## **STEP 5: Create Required Folders**

Your software needs these folders to work:

```
C:\Users\Admin\Documents\-PT-Sheet-Auto-Filler--main\-PT-Sheet-Auto-Filler--main\
├── templates/              ← Place your Excel template here
├── images/                 ← Place CAD images here
├── output/                 ← Filled Excel files will be saved here
```

**Create these folders:**

1. Open File Explorer
2. Navigate to your project folder
3. Right-click → New → Folder
4. Create folder named: `templates`
5. Create folder named: `images`
6. Create folder named: `output`

---

## **STEP 6: Add Your Excel Template**

1. **Copy your Excel PT sheet** to the `templates` folder:
   - Path: `C:\Users\Admin\Documents\-PT-Sheet-Auto-Filler--main\-PT-Sheet-Auto-Filler--main\templates\`
   - File name: `PT_Sheet_Template.xlsx` (important: exact name)

2. **If you don't have a template yet:**
   - Run: `python create_excel_template.py`
   - This will generate a blank template

---

## **STEP 7: START THE APPLICATION**

### **Method A: Double-Click (Easiest)**

1. Open File Explorer
2. Navigate to: `C:\Users\Admin\Documents\-PT-Sheet-Auto-Filler--main\-PT-Sheet-Auto-Filler--main\`
3. **Double-click `main.py`**
4. The application window should open ✅

### **Method B: Command Prompt**

1. Open Command Prompt in your project folder
2. Type this command:
   ```
   python main.py
   ```
3. Press Enter
4. The application window should open ✅

### **Method C: Create a Shortcut (For easy future access)**

1. Right-click `main.py` → "Send to" → "Desktop (create shortcut)"
2. A shortcut will appear on your desktop
3. Double-click the shortcut to run the app anytime ✅

---

## **STEP 8: Using the Application**

Once the application opens:

```
╔════════════════════════════════════════════════════════════╗
║         💎 PT Sheet Auto-Filler v1.0                       ║
║  Automatic CAD Image to Excel PT Sheet Conversion          ║
╚════════════════════════════════════════════════════════════╝

Step 1: Select CAD Image
   └─ Click "Browse..." → Choose your CAD image (JPG, PNG, PDF)

Step 2: Select Excel Template  
   └─ Click "Browse..." → Choose PT_Sheet_Template.xlsx

Step 3: Process & Fill Excel
   └─ Click "⚡ Process & Fill Excel" button

Step 4: Wait for completion
   └─ Processing status shows in real-time
   └─ Filled Excel file automatically saved in output/ folder

✅ Done! Your filled PT sheet is ready to use!
```

---

## **Troubleshooting**

### **Problem 1: "Command 'python' is not recognized"**
- **Solution:** Python is not in PATH
- Re-install Python → Check "Add Python to PATH" ✅

### **Problem 2: "ModuleNotFoundError: No module named 'openpyxl'"**
- **Solution:** Dependencies not installed
- Run: `pip install -r requirements.txt`

### **Problem 3: "No module named 'pytesseract'"**
- **Solution:** Tesseract OCR not installed properly
- Download and install from: https://github.com/UB-Mannheim/tesseract/wiki

### **Problem 4: Application won't open**
- **Solution A:** Try opening via Command Prompt:
  ```
  python main.py
  ```
- **Solution B:** Check for error messages
- **Solution C:** Verify all Python files are in the correct folder

### **Problem 5: "No such file or directory: 'PT_Sheet_Template.xlsx'"**
- **Solution:** Excel template not found
- Ensure `PT_Sheet_Template.xlsx` is in the `templates/` folder

---

## **Quick Verification Checklist**

Before running the application, verify:

- [ ] Python 3.9+ installed (`python --version`)
- [ ] All Python packages installed (`pip list`)
- [ ] Tesseract OCR installed (`tesseract --version`)
- [ ] Folders exist: `templates/`, `images/`, `output/`
- [ ] `PT_Sheet_Template.xlsx` is in `templates/` folder
- [ ] All Python files present (main.py, config.py, etc.)
- [ ] Windows firewall allows Python (if prompted)

---

## **File Structure**

Your complete folder structure should look like:

```
C:\Users\Admin\Documents\-PT-Sheet-Auto-Filler--main\
└── -PT-Sheet-Auto-Filler--main\
    ├── main.py                          ← Run this to start app
    ├── config.py
    ├── ocr_extractor.py
    ├── excel_writer.py
    ├── validator.py
    ├── requirements.txt
    ├── README.md
    ├── templates/
    │   └── PT_Sheet_Template.xlsx       ← Your Excel template
    ├── images/
    │   └── sample_cad.jpg               ← Your CAD images
    └── output/
        └── FILLED_PT_*.xlsx             ← Generated files
```

---

## **Contact & Support**

If you face any issues:

1. Check the error message carefully
2. Run: `python main.py` in Command Prompt (you'll see detailed errors)
3. Verify all installation steps were completed
4. Check GitHub repository for updates

---

## **Next Steps**

1. ✅ Complete all installation steps above
2. ✅ Copy your Excel template to `templates/` folder
3. ✅ Copy your CAD images to `images/` folder
4. ✅ Run `python main.py`
5. ✅ Use the GUI to process images and fill Excel sheets

---

**🎉 Your PT Sheet Auto-Filler is ready to use!**

Start the application and begin automating your Excel filling process! 🚀
