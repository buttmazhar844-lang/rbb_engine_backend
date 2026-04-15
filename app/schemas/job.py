from pydantic import BaseModel
from datetime import datetime

class JobBase(BaseModel):
    job_type: str
    status: str | None = None

class JobRead(JobBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True
