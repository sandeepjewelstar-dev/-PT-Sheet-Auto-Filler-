"""
OCR Extractor Module - Extract data from CAD images
Uses Tesseract OCR and OpenCV for accurate text extraction
"""

import pytesseract
import cv2
import re
import numpy as np
from PIL import Image
import logging
import os
from pathlib import Path

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Set Tesseract path - TRY MULTIPLE LOCATIONS
def setup_tesseract():
    """Setup Tesseract with proper path detection"""
    possible_paths = [
        r"C:\Program Files\Tesseract-OCR\tesseract.exe",
        r"C:\Program Files (x86)\Tesseract-OCR\tesseract.exe",
        r"C:\Users\Admin\AppData\Local\Tesseract-OCR\tesseract.exe",
    ]
    
    for path in possible_paths:
        if os.path.exists(path):
            pytesseract.pytesseract.pytesseract_cmd = path
            logger.info(f"✓ Tesseract found at: {path}")
            return True
    
    logger.warning("⚠️  Tesseract not found in standard locations")
    # Try to use system PATH
    try:
        pytesseract.pytesseract.pytesseract_cmd = "tesseract"
        return True
    except:
        return False

# Initialize Tesseract
setup_tesseract()


def extract_from_image(image_path):
    """
    Extract all data from CAD image using OCR
    
    Args:
        image_path: Path to CAD image file
        
    Returns:
        dict: Extracted data with all fields
    """
    try:
        logger.info(f"📸 Processing image: {image_path}")
        
        # Read image
        img = cv2.imread(image_path)
        if img is None:
            logger.error(f"❌ Failed to read image: {image_path}")
            return None
        
        # Pre-process image for better OCR
        processed_img = preprocess_image(img)
        
        # Convert to RGB for Tesseract
        img_rgb = cv2.cvtColor(processed_img, cv2.COLOR_BGR2RGB)
        
        # Extract text using Tesseract OCR
        logger.info("🔍 Extracting text using OCR...")
        try:
            extracted_text = pytesseract.image_to_string(img_rgb)
        except Exception as e:
            logger.error(f"❌ OCR Failed: {str(e)}")
            logger.warning("⚠️  Proceeding with manual data extraction...")
            extracted_text = ""
        
        # Parse extracted text into structured data
        logger.info("📊 Parsing extracted data...")
        data = parse_extracted_data(extracted_text)
        
        # Detect diamonds in image
        logger.info("💎 Detecting diamonds...")
        diamond_count = detect_diamonds(img)
        data['diamond_count'] = diamond_count
        
        logger.info(f"✅ Data extraction completed successfully")
        return data
        
    except Exception as e:
        logger.error(f"❌ Error during extraction: {str(e)}")
        return None


def preprocess_image(img):
    """
    Preprocess image to improve OCR accuracy
    
    Args:
        img: OpenCV image object
        
    Returns:
        Processed image
    """
    # Resize image for better OCR
    height, width = img.shape[:2]
    new_width = int(width * 1.5)
    new_height = int(height * 1.5)
    img_resized = cv2.resize(img, (new_width, new_height))
    
    # Convert to grayscale
    gray = cv2.cvtColor(img_resized, cv2.COLOR_BGR2GRAY)
    
    # Apply thresholding
    _, binary = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY)
    
    # Denoise
    denoised = cv2.fastNlMeansDenoising(binary, h=10)
    
    return denoised


def parse_extracted_data(text):
    """
    Parse OCR extracted text into structured data
    
    Args:
        text: Raw OCR extracted text
        
    Returns:
        dict: Structured data
    """
    
    data = {
        'product_id': extract_product_id(text),
        'cad_person': extract_field(text, r'CAD Person[:\s]*([A-Za-z\s]+?)(?:\n|$)'),
        'cad_process': extract_field(text, r'CAD Process[:\s]*(.+?)(?:\n|$)'),
        'surface_area': extract_field(text, r'Surface Area[:\s]*([0-9.]+)'),
        'volume': extract_field(text, r'Volume[:\s]*([0-9.]+)'),
        'finding': extract_field(text, r'Finding[:\s]*-?\s*(.+?)(?:\n|$)'),
        'materials': extract_materials(text),
        'stones': extract_stones(text),
        'total_qty': extract_field(text, r'Total[:\s]*([0-9]+)(?:\s|$)'),
        'total_weight': extract_field(text, r'Total.*?([0-9.]+)\s*$', flags=re.MULTILINE),
        'remarks': extract_field(text, r'Remarks[:\s]*(.+?)(?:\n\n|$)', flags=re.MULTILINE | re.DOTALL),
    }
    
    logger.info(f"   ✓ Product ID: {data['product_id']}")
    logger.info(f"   ✓ CAD Person: {data['cad_person']}")
    logger.info(f"   ✓ Found {len(data['materials'])} materials")
    logger.info(f"   ✓ Found {len(data['stones'])} stone settings")
    
    return data


def extract_product_id(text):
    """Extract product ID (e.g., PLDR5552-PE150)"""
    patterns = [
        r'(PLDR\d+-[A-Za-z]\d+)',
        r'([A-Z]{3,}[0-9]{3,}-[A-Z]{2}\d+)',
    ]
    
    for pattern in patterns:
        match = re.search(pattern, text)
        if match:
            return match.group(1).strip()
    
    return ""


def extract_field(text, pattern, flags=re.IGNORECASE):
    """
    Extract field value using regex pattern
    
    Args:
        text: Text to search in
        pattern: Regex pattern
        flags: Regex flags
        
    Returns:
        Extracted value or empty string
    """
    try:
        match = re.search(pattern, text, flags)
        if match:
            value = match.group(1).strip()
            # Clean up extra whitespace
            value = re.sub(r'\s+', ' ', value)
            return value
    except Exception as e:
        logger.warning(f"⚠️  Error extracting field with pattern {pattern}: {e}")
    
    return ""


def extract_materials(text):
    """
    Extract metal materials and their weights
    
    Returns:
        dict: Material name -> weight mapping
    """
    materials = {}
    
    patterns = [
        (r'PLATINUM\s*-\s*([0-9.]+)\s*gms?', 'PLATINUM'),
        (r'GWT\s*18\s*KT\s*-\s*([0-9.]+)\s*gms?', 'GWT 18 KT'),
        (r'GWT\s*14\s*KT\s*-\s*([0-9.]+)\s*gms?', 'GWT 14 KT'),
        (r'GWT\s*10\s*KT\s*-\s*([0-9.]+)\s*gms?', 'GWT 10 KT'),
        (r'SILVER\s*-\s*([0-9.]+)\s*gms?', 'SILVER'),
        (r'GOLD\s*-\s*([0-9.]+)\s*gms?', 'GOLD'),
    ]
    
    for pattern, label in patterns:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            weight = match.group(1)
            materials[label] = weight
            logger.debug(f"   Found: {label} = {weight} gms")
    
    return materials


def extract_stones(text):
    """
    Extract stone settings table
    
    Returns:
        list: List of stone dictionaries
    """
    stones = []
    
    # Split text into rows (look for common delimiters)
    rows = re.split(r'\n', text)
    
    setting_types = ['Claw prong', 'Micro-Split prong', 'Prong', 'Marquise', 'Round', 'Pear']
    
    for row in rows:
        # Check if row contains stone setting info
        if any(setting in row for setting in setting_types):
            stone = parse_stone_row(row, text)
            if stone:
                stones.append(stone)
                logger.debug(f"   Found stone: {stone.get('setting', 'Unknown')}")
    
    return stones


def parse_stone_row(row, full_text):
    """
    Parse a single stone row
    
    Args:
        row: Row text
        full_text: Full extracted text for context
        
    Returns:
        dict: Stone data
    """
    stone = {}
    
    # Extract setting type
    setting_patterns = {
        'Claw prong': 'Claw prong',
        'Micro-Split prong': 'Micro-Split prong',
        'Prong': 'Prong',
        'Marquise': 'Marquise',
    }
    
    for pattern, label in setting_patterns.items():
        if pattern.lower() in row.lower():
            stone['setting'] = label
            break
    
    # Extract shape
    shape_patterns = {
        'Pear': 'Pear',
        'Round': 'Round',
        'Marquise': 'Marquise',
        'Oval': 'Oval',
        'Cushion': 'Cushion',
    }
    
    for pattern, label in shape_patterns.items():
        if pattern.lower() in row.lower():
            stone['shape'] = label
            break
    
    # Extract quality (usually LGD, VS1, VVS1, etc.)
    quality_match = re.search(r'(LGD|VS1|VVS1|VVS2|SI1|SI2|I1)', row, re.IGNORECASE)
    stone['quality'] = quality_match.group(1) if quality_match else ''
    
    # Extract dimensions
    mm_match = re.search(r'(\d+\.?\d*(?:\*\d+\.?\d*)*)', row)
    stone['mm'] = mm_match.group(1) if mm_match else ''
    
    # Extract quantity
    qty_match = re.search(r'QTY[:\s]*(\d+)', row, re.IGNORECASE)
    stone['qty'] = qty_match.group(1) if qty_match else ''
    
    # Extract PTS
    pts_match = re.search(r'PTS[:\s]*([0-9.]+)', row, re.IGNORECASE)
    stone['pts'] = pts_match.group(1) if pts_match else ''
    
    # Extract weight
    weight_match = re.search(r'WEIGHT[:\s]*([0-9.]+)', row, re.IGNORECASE)
    stone['weight'] = weight_match.group(1) if weight_match else ''
    
    return stone if len(stone) > 1 else None


def detect_diamonds(img):
    """
    Detect and count diamonds in image
    
    Args:
        img: OpenCV image object
        
    Returns:
        int: Number of diamonds detected
    """
    try:
        # Convert to HSV for better color detection
        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        
        # Define blue color range (for blue diamonds in CAD)
        lower_blue = np.array([100, 100, 100])
        upper_blue = np.array([130, 255, 255])
        
        # Create mask
        mask = cv2.inRange(hsv, lower_blue, upper_blue)
        
        # Find contours
        contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        
        # Count significant contours (filter by area)
        diamond_count = 0
        for contour in contours:
            area = cv2.contourArea(contour)
            if area > 50:  # Minimum area threshold
                diamond_count += 1
        
        logger.info(f"   💎 Detected {diamond_count} diamonds")
        return diamond_count
        
    except Exception as e:
        logger.warning(f"⚠️  Error detecting diamonds: {e}")
        return 0
