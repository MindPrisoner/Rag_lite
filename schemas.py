from typing import List, Optional, Literal
from pydantic import BaseModel


class RetrievedChunk(BaseModel):
    rank: int
    score: float
    source: str
    chunk_id: int
    text: str


class QueryRequest(BaseModel):
    query: str
    knowledge_dir: str = "knowledge"


class QueryResponse(BaseModel):
    query: str
    retrieved: List[RetrievedChunk]
    answer: str
    answer_status: Literal["success", "failed"]
    error: Optional[str] = None
    elapsed_ms: int
    timestamp: str
