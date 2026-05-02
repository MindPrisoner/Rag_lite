from pathlib import Path

from pipeline import run_rag
from generator import call_llm
from loader import load_text


def tool_rag_qa(query: str, knowledge_dir: str = "knowledge"):
    return run_rag(query=query, knowledge_dir=knowledge_dir)


def tool_summarize_doc(file_name: str, knowledge_dir: str = "knowledge"):
    file_path = Path(knowledge_dir) / file_name
    if not file_path.exists():
        raise FileNotFoundError(f"文件不存在: {file_path}")

    text = load_text(str(file_path))

    system_prompt = """
你是一个严谨的文档总结助手。
请根据给定文档内容输出简洁总结。
""".strip()

    user_prompt = f"""
请总结下面文档内容，输出以下结构：
1. 文档主题
2. 3~5 条核心要点
3. 这份文档最适合回答什么类型的问题

文档内容：
{text[:2500]}
""".strip()

    answer = call_llm(system_prompt, user_prompt, timeout=60, max_retries=3)

    return {
        "tool_name": "summarize_doc",
        "file_name": file_name,
        "answer": answer,
    }


def tool_compare_docs(file_a: str, file_b: str, knowledge_dir: str = "knowledge"):
    path_a = Path(knowledge_dir) / file_a
    path_b = Path(knowledge_dir) / file_b

    if not path_a.exists():
        raise FileNotFoundError(f"文件不存在: {path_a}")
    if not path_b.exists():
        raise FileNotFoundError(f"文件不存在: {path_b}")

    text_a = load_text(str(path_a))
    text_b = load_text(str(path_b))

    system_prompt = """
你是一个严谨的文档比较助手。
请比较两个文档的主题、重点、差异和适用场景。
""".strip()

    user_prompt = f"""
请比较下面两个文档，输出以下结构：
1. 文档 A 主题
2. 文档 B 主题
3. 共同点
4. 不同点
5. 分别适合回答什么问题

文档 A（{file_a}）：
{text_a[:1800]}

文档 B（{file_b}）：
{text_b[:1800]}
""".strip()

    answer = call_llm(system_prompt, user_prompt, timeout=60, max_retries=3)

    return {
        "tool_name": "compare_docs",
        "file_a": file_a,
        "file_b": file_b,
        "answer": answer,
    }
