from pydantic import BaseModel


class MatchRequest(BaseModel):
    job_description: str