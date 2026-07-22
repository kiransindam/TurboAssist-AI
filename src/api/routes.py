"""API route definitions."""
from fastapi import APIRouter, HTTPException, Depends
from src.api.schemas import QueryRequest, AnswerResponse, HealthResponse, Citation
from src.generation.llm_chain import LLMChain
from src.retrieval.vector_store import VectorStore
from src.retrieval.retriever import Retriever
import logging

logger = logging.getLogger(__name__)

router = APIRouter()

# Global instances (in production, use dependency injection)
vector_store = VectorStore()
retriever = Retriever(vector_store)
llm_chain = LLMChain(retriever)


@router.post("/ask", response_model=AnswerResponse)
async def ask_question(request: QueryRequest):
    """
    Answer a technical question using RAG.
    
    - **question**: The user's question
    - **equipment_tag**: Optional equipment identifier
    - **top_k**: Number of source documents to retrieve
    
    Returns a citation-backed answer.
    """
    try:
        result = llm_chain.generate_answer(
            question=request.question,
            k=request.top_k,
        )
        
        return AnswerResponse(
            answer=result["answer"],
            citations=result["citations"],
            sources=[Citation(**source) for source in result["sources"]],
            question=request.question,
        )
        
    except Exception as e:
        logger.error(f"Error processing question: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint."""
    return HealthResponse(
        status="healthy",
        version="1.0.0",
        vector_store_loaded=vector_store.vectorstore is not None,
    )
