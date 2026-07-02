"""
Validator Module - Validate extracted data for accuracy
"""

import re
import logging
from typing import Dict, List, Tuple

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def validate_data(data: Dict) -> Tuple[bool, List[str]]:
    """
    Validate extracted data
    
    Args:
        data: Dictionary with extracted data
        
    Returns:
        Tuple: (is_valid: bool, errors: List[str])
    """
    errors = []
    
    logger.info("🔍 Validating extracted data...")
    
    # Check required fields
    errors.extend(validate_required_fields(data))
    
    # Validate numeric fields
    errors.extend(validate_numeric_fields(data))
    
    # Validate material data
    errors.extend(validate_materials(data))
    
    # Validate stone data
    errors.extend(validate_stones(data))
    
    # Validate totals
    errors.extend(validate_totals(data))
    
    is_valid = len(errors) == 0
    
    if is_valid:
        logger.info("✅ Data validation passed - all fields are valid!")
    else:
        logger.warning(f"❌ Data validation failed with {len(errors)} error(s)")
        for i, error in enumerate(errors, 1):
            logger.warning(f"   {i}. {error}")
    
    return is_valid, errors


def validate_required_fields(data: Dict) -> List[str]:
    """Validate that required fields are present"""
    errors = []
    
    required_fields = [
        'product_id',
        'cad_person',
        'surface_area',
        'volume',
    ]
    
    for field in required_fields:
        if not data.get(field):
            errors.append(f"Missing required field: '{field}'")
    
    if not data.get('materials'):
        errors.append("No materials data found")
    
    if not data.get('stones'):
        errors.append("No stone settings data found")
    
    return errors


def validate_numeric_fields(data: Dict) -> List[str]:
    """Validate numeric fields are valid numbers"""
    errors = []
    
    numeric_fields = {
        'surface_area': 'Surface Area',
        'volume': 'Volume',
        'total_qty': 'Total Quantity',
        'total_weight': 'Total Weight',
        'diamond_count': 'Diamond Count',
    }
    
    for field, label in numeric_fields.items():
        value = data.get(field)
        if value and not is_valid_number(value):
            errors.append(f"Invalid numeric value for {label}: '{value}'")
    
    return errors


def validate_materials(data: Dict) -> List[str]:
    """Validate materials section"""
    errors = []
    
    materials = data.get('materials', {})
    
    if not materials:
        return errors
    
    if len(materials) < 2:
        errors.append(f"Expected at least 3 materials, found {len(materials)}")
    
    # Validate each material weight is numeric
    for material, weight in materials.items():
        if not is_valid_number(weight):
            errors.append(f"Invalid weight for material '{material}': '{weight}'")
        elif float(weight) <= 0:
            errors.append(f"Material '{material}' weight must be positive: {weight}")
    
    return errors


def validate_stones(data: Dict) -> List[str]:
    """Validate stone settings"""
    errors = []
    
    stones = data.get('stones', [])
    
    if not stones:
        errors.append("No stone settings data found")
        return errors
    
    if len(stones) < 1:
        errors.append("Expected at least 1 stone setting")
    
    # Validate each stone
    for idx, stone in enumerate(stones, 1):
        stone_errors = validate_stone(stone, idx)
        errors.extend(stone_errors)
    
    return errors


def validate_stone(stone: Dict, index: int) -> List[str]:
    """Validate individual stone"""
    errors = []
    
    # Check required fields
    if not stone.get('setting'):
        errors.append(f"Stone {index}: Missing setting type")
    
    if not stone.get('shape'):
        errors.append(f"Stone {index}: Missing shape")
    
    if not stone.get('qty'):
        errors.append(f"Stone {index}: Missing quantity")
    elif not is_valid_number(stone.get('qty')):
        errors.append(f"Stone {index}: Invalid quantity '{stone.get('qty')}'")
    
    # Validate quality
    quality = stone.get('quality', '')
    if quality:
        valid_qualities = ['LGD', 'VS1', 'VVS1', 'VVS2', 'SI1', 'SI2', 'I1']
        if quality not in valid_qualities:
            errors.append(f"Stone {index}: Invalid quality '{quality}'")
    
    # Validate dimensions
    if stone.get('mm'):
        if not is_valid_dimensions(stone.get('mm')):
            errors.append(f"Stone {index}: Invalid dimensions '{stone.get('mm')}'")
    
    # Validate weights and PTS
    for field in ['weight', 'pts']:
        value = stone.get(field)
        if value and not is_valid_number(value):
            errors.append(f"Stone {index}: Invalid {field} '{value}'")
    
    return errors


def validate_totals(data: Dict) -> List[str]:
    """Validate total calculations"""
    errors = []
    
    total_qty = data.get('total_qty')
    stones = data.get('stones', [])
    
    if total_qty and stones:
        # Calculate expected quantity
        calculated_qty = sum(
            int(stone.get('qty', 0)) 
            for stone in stones 
            if is_valid_number(stone.get('qty', '0'))
        )
        
        try:
            total_qty_int = int(total_qty)
            if total_qty_int != calculated_qty:
                errors.append(
                    f"Total quantity mismatch: "
                    f"declared {total_qty_int}, calculated {calculated_qty}"
                )
        except ValueError:
            errors.append(f"Invalid total quantity: '{total_qty}'")
    
    return errors


def is_valid_number(value) -> bool:
    """Check if value is a valid number"""
    if not value:
        return False
    
    try:
        float(str(value).replace(',', ''))
        return True
    except (ValueError, TypeError):
        return False


def is_valid_dimensions(dimensions_str: str) -> bool:
    """
    Check if dimensions string is valid
    Valid formats: 1.5, 9.98*6.44, 9.98*6.44*4.05
    """
    if not dimensions_str:
        return False
    
    # Pattern: numbers separated by * or x
    pattern = r'^(\d+\.?\d*)(\*(\d+\.?\d*))*$'
    return bool(re.match(pattern, str(dimensions_str)))


def generate_validation_report(data: Dict) -> str:
    """
    Generate a detailed validation report
    
    Args:
        data: Extracted data
        
    Returns:
        str: Formatted validation report
    """
    is_valid, errors = validate_data(data)
    
    report = f"""
{'='*60}
DATA VALIDATION REPORT
{'='*60}

Status: {'✅ PASSED' if is_valid else '❌ FAILED'}

Extracted Data Summary:
{'='*60}
Product ID:       {data.get('product_id', 'N/A')}
CAD Person:       {data.get('cad_person', 'N/A')}
Surface Area:     {data.get('surface_area', 'N/A')}
Volume:           {data.get('volume', 'N/A')}
Finding:          {data.get('finding', 'N/A')}

Materials Found:  {len(data.get('materials', {}))}
Stones Found:     {len(data.get('stones', []))}
Total Quantity:   {data.get('total_qty', 'N/A')}
Total Weight:     {data.get('total_weight', 'N/A')}
Diamonds Detect:  {data.get('diamond_count', 'N/A')}

{'='*60}
"""
    
    if errors:
        report += "ERRORS & WARNINGS:\n"
        report += "="*60 + "\n"
        for i, error in enumerate(errors, 1):
            report += f"{i}. {error}\n"
    
    report += "="*60 + "\n"
    
    return report
