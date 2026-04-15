from typing import List, Optional
from sqlalchemy.orm import Session, Query
from app.models.product import Product
from app.schemas.product import ProductCreate
from app.core.enums import Locale, CurriculumBoard, TemplateType, ProductStatus

class ProductRepository:
    def __init__(self, db: Session):
        self.db = db
        self.model = Product

    def create(self, product_data: ProductCreate) -> Product:
        """Create new product"""
        db_product = Product(**product_data.model_dump())
        self.db.add(db_product)
        self.db.commit()
        self.db.refresh(db_product)
        return db_product

    def get_by_id(self, product_id: int) -> Optional[Product]:
        """Get product by ID"""
        return self.db.query(Product).filter(Product.id == product_id).first()

    def get_all(
        self,
        status: Optional[ProductStatus] = None,
        template_type: Optional[TemplateType] = None,
        generation_job_id: Optional[int] = None,
        standard_id: Optional[int] = None,
        curriculum_board: Optional[CurriculumBoard] = None,
        grade_level: Optional[int] = None,
        locale: Optional[Locale] = None
    ) -> Query:
        """Get all products with optional filters"""
        query = self.db.query(Product)
        
        if status:
            query = query.filter(Product.status == status)
        if template_type:
            query = query.filter(Product.template_type == template_type)
        if generation_job_id:
            query = query.filter(Product.generation_job_id == generation_job_id)
        if standard_id:
            query = query.filter(Product.standard_id == standard_id)
        if curriculum_board:
            query = query.filter(Product.curriculum_board == curriculum_board)
        if grade_level:
            query = query.filter(Product.grade_level == grade_level)
        if locale:
            query = query.filter(Product.locale == locale)
            
        return query.order_by(Product.created_at.desc())

    def list_by_job(self, generation_job_id: int) -> List[Product]:
        """Get all products for a specific generation job"""
        return self.db.query(Product).filter(
            Product.generation_job_id == generation_job_id
        ).order_by(Product.created_at.desc()).all()
    
    def update_status(self, product_id: int, status: ProductStatus) -> Product:
        """Update product status"""
        product = self.get_by_id(product_id)
        if product:
            product.status = status
            self.db.commit()
            self.db.refresh(product)
        return product

    def delete(self, product_id: int) -> None:
        """Delete a product by ID"""
        product = self.get_by_id(product_id)
        if product:
            self.db.delete(product)
            self.db.commit()