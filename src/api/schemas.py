"""Pydantic schemas for API requests and responses."""
from pydantic import BaseModel, Field
from typing import List, Optional


class QueryRequest(BaseModel):
    """Request schema for /ask endpoint."""
    question: str = Field(..., max_length=1000, description="User question")
    equipment_tag: Optional[str] = Field(None, description="Equipment identifier")
    top_k: int = Field(default=5, ge=1, le=20, description="Number of sources to retrieve")


class Citation(BaseModel):
    """Citation schema."""
    doc_id: str
    file_name: str
    page: int
    chunk_id: str


class AnswerResponse(BaseModel):
    """Response schema for /ask endpoint."""
    answer: str
    citations: List[str]
    sources: List[Citation]
    question: str


class HealthResponse(BaseModel):
    """Health check response."""
    status: str
    version: str
    vector_store_loaded: bool
