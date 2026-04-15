# Import all models here for Alembic to detect them
from app.db.session import Base
from app.models.product import Product
from app.models.job import Job
from app.models.standard import Standard
from app.models.generation_job import GenerationJob
from app.models.file_artifact import FileArtifact
