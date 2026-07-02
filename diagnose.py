"""
Diagnostic Script - Debug OCR and Image Processing Issues
Run this to identify what's causing the extraction failure
"""

import sys
import os
from pathlib import Path

print("="*60)
print("PT SHEET AUTO-FILLER - DIAGNOSTIC SCRIPT")
print("="*60)
print()

# Check Python version
print("1. Python Version:")
print(f"   Version: {sys.version}")
print(f"   Executable: {sys.executable}")
print()

# Check installed packages
print("2. Checking Required Packages:")
packages = ['openpyxl', 'cv2', 'pytesseract', 'PIL', 'numpy', 'pandas']

for package in packages:
    try:
        if package == 'cv2':
            import cv2
            print(f"   ✓ opencv-python: {cv2.__version__}")
        elif package == 'PIL':
            from PIL import Image
            print(f"   ✓ Pillow: {Image.__version__}")
        else:
            mod = __import__(package)
            if hasattr(mod, '__version__'):
                print(f"   ✓ {package}: {mod.__version__}")
            else:
                print(f"   ✓ {package}: installed")
    except Exception as e:
        print(f"   ✗ {package}: NOT installed - {str(e)}")
print()

# Check Tesseract
print("3. Tesseract OCR:")
try:
    import pytesseract
    print(f"   ✓ pytesseract installed")
    
    # Try to find Tesseract executable
    import subprocess
    result = subprocess.run(['tesseract', '--version'], capture_output=True, text=True)
    if result.returncode == 0:
        lines = result.stdout.split('\n')
        print(f"   ✓ Tesseract found: {lines[0]}")
    else:
        print(f"   ✗ Tesseract executable not found in PATH")
        print(f"   Try setting path manually in config.py")
except Exception as e:
    print(f"   ✗ Error: {str(e)}")
print()

# Check config
print("4. Configuration:")
try:
    from config import (
        TESSERACT_PATH, TEMPLATES_DIR, OUTPUT_DIR, 
        IMAGES_DIR, IMAGE_RESIZE_FACTOR, IMAGE_THRESHOLD
    )
    print(f"   Tesseract Path: {TESSERACT_PATH}")
    print(f"   Templates Dir: {TEMPLATES_DIR}")
    print(f"   Output Dir: {OUTPUT_DIR}")
    print(f"   Images Dir: {IMAGES_DIR}")
    print(f"   Image Resize Factor: {IMAGE_RESIZE_FACTOR}")
    print(f"   Image Threshold: {IMAGE_THRESHOLD}")
    print()
    
    # Check if path exists
    if Path(TESSERACT_PATH).exists():
        print(f"   ✓ Tesseract path exists: {TESSERACT_PATH}")
    else:
        print(f"   ✗ Tesseract path NOT found: {TESSERACT_PATH}")
        print(f"   This is likely the problem!")
except Exception as e:
    print(f"   ✗ Error loading config: {str(e)}")
print()

# Check directories
print("5. Required Directories:")
dirs = ['templates', 'images', 'output']
for d in dirs:
    dir_path = Path(d)
    if dir_path.exists():
        files = list(dir_path.glob('*'))
        print(f"   ✓ {d}/: exists ({len(files)} items)")
        if files and len(files) <= 5:
            for f in files:
                print(f"      - {f.name}")
    else:
        print(f"   ✗ {d}/: NOT found - creating...")
        dir_path.mkdir(exist_ok=True)
print()

# Test image processing
print("6. Testing Image Processing:")
try:
    import cv2
    import numpy as np
    
    # Create a test image
    test_img = np.ones((100, 100, 3), dtype=np.uint8) * 255
    print(f"   ✓ Can create test images")
    
    # Try to read an image
    if Path('images').exists():
        image_files = list(Path('images').glob('*.jpg')) + list(Path('images').glob('*.png'))
        if image_files:
            test_file = str(image_files[0])
            img = cv2.imread(test_file)
            if img is not None:
                print(f"   ✓ Can read images: {image_files[0].name}")
                print(f"      Shape: {img.shape}")
            else:
                print(f"   ✗ Failed to read image: {image_files[0].name}")
        else:
            print(f"   ⚠ No image files found in images/ folder")
except Exception as e:
    print(f"   ✗ Error: {str(e)}")
print()

# Test OCR
print("7. Testing OCR:")
try:
    import pytesseract
    from PIL import Image
    import os
    
    # Set Tesseract path
    from config import TESSERACT_PATH
    pytesseract.pytesseract.pytesseract_cmd = TESSERACT_PATH
    
    # Create a simple test image
    img = Image.new('RGB', (100, 100), color='white')
    text = pytesseract.image_to_string(img)
    print(f"   ✓ OCR works (Tesseract responding)")
    
except FileNotFoundError as e:
    print(f"   ✗ Tesseract not found: {str(e)}")
    print(f"   Solution: Update TESSERACT_PATH in config.py")
except Exception as e:
    print(f"   ✗ OCR Error: {str(e)}")
print()

# Test actual extraction
print("8. Testing Data Extraction:")
try:
    image_files = list(Path('images').glob('*.jpg')) + list(Path('images').glob('*.png'))
    
    if image_files:
        test_file = str(image_files[0])
        print(f"   Testing with: {image_files[0].name}")
        
        from ocr_extractor import extract_from_image
        result = extract_from_image(test_file)
        
        if result:
            print(f"   ✓ Extraction successful!")
            print(f"   Product ID: {result.get('product_id', 'N/A')}")
            print(f"   CAD Person: {result.get('cad_person', 'N/A')}")
            print(f"   Materials found: {len(result.get('materials', {}))}")
        else:
            print(f"   ✗ Extraction returned None")
    else:
        print(f"   ⚠ No images found to test")
        
except Exception as e:
    print(f"   ✗ Extraction failed: {str(e)}")
    import traceback
    traceback.print_exc()

print()
print("="*60)
print("DIAGNOSTIC COMPLETE")
print("="*60)
print()
print("NEXT STEPS:")
print("1. Check for any ✗ marks above")
print("2. If Tesseract path is wrong, update config.py")
print("3. Ensure images are in images/ folder")
print("4. Run: python main.py")
