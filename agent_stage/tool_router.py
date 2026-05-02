from pathlib import Path

from generator import call_llm
from .prompts import ROUTER_SYSTEM_PROMPT
from .route_schema import validate_route


def list_knowledge_files(knowledge_dir: str = "knowledge") -> list[str]:
    root = Path(knowledge_dir)
    if not root.exists():
        return []
    return sorted([p.name for p in root.glob("*") if p.suffix.lower() in {".md", ".txt"}])


def format_history(history: list[dict] | None, max_turns: int = 5) -> str:
    if not history:
        return "暂无历史对话"

    recent = history[-max_turns:]
    lines = []

    for i, item in enumerate(recent, 1):
        lines.append(
            f"{i}. 用户问题: {item.get('user_query')}\n"
            f"   使用工具: {item.get('selected_tool')}\n"
            f"   工具参数: {item.get('tool_args')}\n"
            f"   结果摘要: {item.get('summary')}"
        )

    return "\n".join(lines)


def route_task(user_query: str, knowledge_dir: str = "knowledge", history: list[dict] | None = None) -> dict:
    files = list_knowledge_files(knowledge_dir)
    files_text = "\n".join([f"- {name}" for name in files])
    history_text = format_history(history)

    user_prompt = f"""
当前知识库目录下有这些文件：
{files_text}

最近对话历史：
{history_text}

用户当前请求：
{user_query}

请为这个请求选择最合适的工具，并生成 JSON。

注意：
1. 如果用户说“它”“这个文档”“刚才那个”，请结合最近对话历史判断指代对象
2. 如果历史中也无法判断指代对象，请选择 clarify
3. 不要编造文件名，只能使用当前知识库目录里的文件
""".strip()

    raw_output = call_llm(
        system_prompt=ROUTER_SYSTEM_PROMPT,
        user_prompt=user_prompt,
        timeout=60,
        max_retries=3,
    )

    return validate_route(raw_output, available_files=files)
