from pydantic import BaseModel
from datetime import datetime

class FileArtifactBase(BaseModel):
    product_id: int
    file_type: str
    file_path: str

class FileArtifactCreate(FileArtifactBase):
    pass

class FileArtifactRead(FileArtifactBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True