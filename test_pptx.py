#!/usr/bin/env python3
"""
Test script for PPTX processor - Product 4
"""
import sys
import json
from pathlib import Path

# Add app to path
sys.path.insert(0, str(Path(__file__).parent))

from app.services.pptx_processor import pptx_processor
from app.utils.storage import storage_manager

def test_product_4():
    """Test PPTX generation with product 4 data"""
    
    # Load product 4 data
    product_id = 4
    product_path = Path("rbb-drive/product_4")
    
    # Load raw.json
    with open(product_path / "raw.json", 'r') as f:
        content_data = json.load(f)
    
    # Use metadata from the database export
    product_metadata = {
        'grade_level': '6',
        'ela_standard_code': 'RL.7.2',
        'ela_standard_type': 'RI',
        'curriculum_board': 'COMMON_CORE',
        'worldview_flag': 'NEUTRAL'
    }
    
    print("Testing PPTX generation with Product 4...")
    print(f"Product ID: {product_id}")
    print(f"Title: {content_data.get('title')}")
    print(f"Grade: {product_metadata.get('grade_level')}")
    print(f"Standard: {product_metadata.get('ela_standard_code')}")
    
    try:
        # Generate PPTX
        output_path = pptx_processor.fill_anchor_reading_passage(
            content_data=content_data,
            product_metadata=product_metadata,
            product_id=product_id
        )
        
        print(f"\n✓ SUCCESS: PPTX generated at: {output_path}")
        print(f"✓ File exists: {output_path.exists()}")
        print(f"✓ File size: {output_path.stat().st_size} bytes")
        
        return True
        
    except Exception as e:
        print(f"\n✗ FAILED: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_product_4()
    sys.exit(0 if success else 1)
