"""FastAPI application entry point."""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.api.routes import router, vector_store
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)

# Create FastAPI app
app = FastAPI(
    title="TurboAssist AI",
    description="RAG-powered technical knowledge assistant for turbomachinery maintenance",
    version="1.0.0",
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routes
app.include_router(router)


@app.on_event("startup")
async def startup_event():
    """Load vector store on startup."""
    try:
        vector_store.load("./vector_store")
        logger.info("Vector store loaded successfully")
    except Exception as e:
        logger.warning(f"Could not load vector store: {e}")
        logger.info("Please run ingestion script first: python scripts/ingest_data.py")


@app.get("/")
async def root():
    """Root endpoint."""
    return {
        "message": "TurboAssist AI API",
        "docs": "/docs",
        "health": "/health",
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
