import os
from pathlib import Path
from typing import Dict, Any
import json
from app.core.config import settings
from app.utils.logger import logger

class StorageManager:
    """
    Manages file storage for products and generated assets.
    Ensures directory structure exists and provides path utilities.
    """
    
    def __init__(self):
        self.base_path = Path(settings.storage_path)
    
    def ensure_directories(self) -> None:
        """Create base storage directories if they don't exist"""
        self.base_path.mkdir(parents=True, exist_ok=True)
    
    def get_product_path(self, product_id: int) -> Path:
        """Get storage path for a specific product"""
        product_path = self.base_path / f"product_{product_id}"
        product_path.mkdir(parents=True, exist_ok=True)
        return product_path
    
    def save_json_file(self, product_id: int, file_type: str, data: Dict[Any, Any]) -> Path:
        """Save JSON file for product (raw.json, final.json, metadata.json)"""
        product_path = self.get_product_path(product_id)
        file_path = product_path / f"{file_type}.json"
        
        with open(file_path, 'w') as f:
            json.dump(data, f, indent=2)
        
        logger.info(f"Saved {file_type}.json for product {product_id}")
        return file_path
    
    def prepare_zip_structure(self, product_id: int) -> Path:
        """Prepare directory structure for ZIP bundle (no compression yet)"""
        product_path = self.get_product_path(product_id)
        zip_dir = product_path / "bundle"
        zip_dir.mkdir(exist_ok=True)
        
        # Create subdirectories for organized bundle
        (zip_dir / "json").mkdir(exist_ok=True)
        (zip_dir / "pdf").mkdir(exist_ok=True)
        (zip_dir / "thumbnails").mkdir(exist_ok=True)
        
        logger.info(f"Prepared ZIP structure for product {product_id}")
        return zip_dir
    
    def create_stub_files(self, product_id: int) -> Dict[str, Path]:
        """Create stub JSON files with placeholder content"""
        stub_data = {
            "raw": {"product_id": product_id, "status": "stub", "type": "raw_data"},
            "final": {"product_id": product_id, "status": "stub", "type": "final_output"},
            "metadata": {"product_id": product_id, "created_by": "stub_generator", "version": "1.0"}
        }
        
        file_paths = {}
        for file_type, data in stub_data.items():
            file_paths[file_type] = self.save_json_file(product_id, file_type, data)
        
        return file_paths

storage_manager = StorageManager()
