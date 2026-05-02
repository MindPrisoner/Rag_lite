import time
from loader import load_knowledge_dir
from retriever import build_bm25, retrieve
from generator import call_llm
from logger_utils import append_query_log, now_iso
from career_prompts import get_career_prompt


def run_career_rag(mode: str, query: str, knowledge_dir: str = "career_knowledge"):
    start_time = time.time()

    chunks = load_knowledge_dir(knowledge_dir)
    bm25 = build_bm25(chunks)
    retrieved = retrieve(query, bm25, chunks)

    answer_status = "success"
    error = None

    try:
        system_prompt, user_prompt = get_career_prompt(mode, query, retrieved)
        answer = call_llm(system_prompt, user_prompt, timeout=60, max_retries=3)
    except Exception as e:
        answer = f"[生成失败] {type(e).__name__}: {e}"
        answer_status = "failed"
        error = str(e)

    elapsed_ms = int((time.time() - start_time) * 1000)
    timestamp = now_iso()

    result = {
        "mode": mode,
        "query": query,
        "retrieved": retrieved,
        "answer": answer,
        "answer_status": answer_status,
        "error": error,
        "elapsed_ms": elapsed_ms,
        "timestamp": timestamp,
    }

    log_record = {
        "timestamp": timestamp,
        "mode": mode,
        "query": query,
        "answer_status": answer_status,
        "error": error,
        "elapsed_ms": elapsed_ms,
        "retrieved": [
            {
                "rank": item["rank"],
                "score": item["score"],
                "source": item["source"],
                "chunk_id": item["chunk_id"],
            }
            for item in retrieved
        ],
    }
    append_query_log(log_record)

    return result
