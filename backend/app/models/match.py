from pydantic import BaseModel

class Match(BaseModel):
    resume_id: int
    job_id: int