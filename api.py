from fastapi import FastAPI
from pipeline import run_rag
from schemas import QueryRequest, QueryResponse

app = FastAPI(title="RAG Lite API")


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/query", response_model=QueryResponse)
def query_rag(req: QueryRequest):
    result = run_rag(query=req.query, knowledge_dir=req.knowledge_dir)
    return result
