"""
Configuration settings for PT Sheet Auto-Filler
"""

import os
from pathlib import Path

# Project paths
PROJECT_ROOT = Path(__file__).parent
TEMPLATES_DIR = PROJECT_ROOT / "templates"
OUTPUT_DIR = PROJECT_ROOT / "output"
IMAGES_DIR = PROJECT_ROOT / "images"

# Create directories if they don't exist
TEMPLATES_DIR.mkdir(exist_ok=True)
OUTPUT_DIR.mkdir(exist_ok=True)
IMAGES_DIR.mkdir(exist_ok=True)

# OCR Settings
TESSERACT_PATH = r"C:\Program Files\Tesseract-OCR\tesseract.exe"  # Windows path
# For Mac: /usr/local/bin/tesseract
# For Linux: /usr/bin/tesseract

# Excel Settings
EXCEL_TEMPLATE_FILE = TEMPLATES_DIR / "PT_Sheet_Template.xlsx"
OUTPUT_FILE_PREFIX = "FILLED_PT_"

# Image Processing Settings
IMAGE_RESIZE_FACTOR = 1.5  # Increase OCR accuracy
IMAGE_THRESHOLD = 150  # For binary image processing

# Data Extraction Settings
CONFIDENCE_THRESHOLD = 0.7  # Minimum confidence for extracted data
VERIFY_DUPLICATES = True

# Logging
LOG_LEVEL = "INFO"
LOG_FILE = PROJECT_ROOT / "app.log"

# Diamond Detection Settings
DIAMOND_MIN_AREA = 50  # Minimum pixels for diamond detection
DIAMOND_COLOR_RANGE = {
    'lower': (100, 100, 100),  # BGR color range for diamonds
    'upper': (255, 255, 255)
}

print(f"✅ Configuration loaded")
print(f"   Project Root: {PROJECT_ROOT}")
print(f"   Templates Dir: {TEMPLATES_DIR}")
print(f"   Output Dir: {OUTPUT_DIR}")
print(f"   Images Dir: {IMAGES_DIR}")
