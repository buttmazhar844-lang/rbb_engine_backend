from sqlalchemy import Column, Integer, String, DateTime, Index, Enum
from sqlalchemy.sql import func
from app.db.session import Base
from app.core.enums import Locale, FileType

class FileArtifact(Base):
    """Files associated with products (raw.json, final.json, metadata.json, zip bundles)"""
    __tablename__ = "file_artifacts"

    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, nullable=False, index=True)  # References Product.id
    locale = Column(Enum(Locale), nullable=False, default=Locale.US, index=True)
    file_type = Column(Enum(FileType), nullable=False, index=True)
    file_path = Column(String, nullable=False)  # Relative path to file in storage
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    __table_args__ = (
        Index('ix_file_artifacts_product_type', 'product_id', 'file_type'),
        Index('ix_file_artifacts_locale', 'locale'),
    )