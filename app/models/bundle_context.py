from sqlalchemy import Column, Integer, String, DateTime, Text
from sqlalchemy.sql import func
from app.db.session import Base

class BundleContext(Base):
    """Stores the latest anchor reading passage context for a standard.
    Overwritten each time a new Anchor Reading Passage is generated for that standard.
    """
    __tablename__ = "bundle_contexts"

    id = Column(Integer, primary_key=True, index=True)
    standard_id = Column(Integer, nullable=False, unique=True, index=True)
    passage_title = Column(String(200), nullable=False)
    passage_topic = Column(String(500), nullable=False)   # main_theme
    key_vocabulary = Column(Text, nullable=True)           # comma-separated terms
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
