"""RAG evaluation using RAGAS."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from datasets import Dataset
from ragas import evaluate
from ragas.metrics import (
    faithfulness,
    answer_relevancy,
    context_precision,
    context_recall,
)
from src.retrieval.vector_store import VectorStore
from src.retrieval.retriever import Retriever
from src.generation.llm_chain import LLMChain
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def create_evaluation_dataset() -> Dataset:
    """Create a sample evaluation dataset."""
    # Sample Q&A pairs (replace with your actual evaluation data)
    eval_data = {
        "question": [
            "What is the recommended maintenance interval for SGT-800 turbines?",
            "How do I troubleshoot vibration issues in gas turbines?",
            "What are the safety precautions for turbine inspection?",
        ],
        "ground_truth": [
            "The recommended maintenance interval for SGT-800 turbines is 25,000 operating hours or 5 years, whichever comes first.",
            "Vibration issues can be troubleshooted by checking alignment, bearing condition, and rotor balance.",
            "Safety precautions include lockout/tagout procedures, PPE requirements, and confined space entry permits.",
        ],
    }
    return Dataset.from_dict(eval_data)


def run_evaluation():
    """Run RAG evaluation."""
    logger.info("Loading vector store...")
    vector_store = VectorStore()
    vector_store.load("./vector_store")
    
    retriever = Retriever(vector_store)
    llm_chain = LLMChain(retriever)
    
    # Load evaluation dataset
    eval_dataset = create_evaluation_dataset()
    
    # Generate answers and contexts
    logger.info("Generating answers...")
    answers = []
    contexts = []
    
    for question in eval_dataset["question"]:
        result = llm_chain.generate_answer(question, k=5)
        answers.append(result["answer"])
        
        # Format context for evaluation
        docs = retriever.retrieve(question, k=5)
        context_text = retriever.format_context(docs)
        contexts.append([context_text])
    
    # Create evaluation dataset
    eval_data = {
        "question": eval_dataset["question"],
        "answer": answers,
        "contexts": contexts,
        "ground_truth": eval_dataset["ground_truth"],
    }
    dataset = Dataset.from_dict(eval_data)
    
    # Run evaluation
    logger.info("Running RAGAS evaluation...")
    result = evaluate(
        dataset,
        metrics=[
            faithfulness,
            answer_relevancy,
            context_precision,
            context_recall,
        ],
    )
    
    # Print results
    logger.info("\n=== Evaluation Results ===")
    for metric, score in result.items():
        logger.info(f"{metric}: {score:.4f}")
    
    # Save results
    result_df = result.to_pandas()
    result_df.to_csv("./evaluation_results.csv", index=False)
    logger.info("\nResults saved to evaluation_results.csv")


if __name__ == "__main__":
    run_evaluation()
