import json
from typing import Any, Literal

from pydantic import BaseModel, Field, ValidationError


class RouteResult(BaseModel):
    tool_name: Literal["rag_qa", "summarize_doc", "compare_docs", "clarify"]
    reason: str
    arguments: dict[str, Any] = Field(default_factory=dict)


def safe_json_loads(text: str) -> dict:
    text = text.strip()

    if text.startswith("```"):
        text = text.strip("`")
        text = text.replace("json", "", 1).strip()

    return json.loads(text)


def make_clarify_route(reason: str, message: str) -> dict:
    return {
        "tool_name": "clarify",
        "reason": reason,
        "arguments": {
            "message": message
        }
    }


def validate_route(raw_output: str, available_files: list[str]) -> dict:
    try:
        data = safe_json_loads(raw_output)
        route = RouteResult(**data)
    except (json.JSONDecodeError, ValidationError) as e:
        return make_clarify_route(
            reason="路由结果解析或校验失败",
            message=f"我没有正确理解你的任务，请重新说明。错误信息：{type(e).__name__}"
        )

    tool_name = route.tool_name
    args = route.arguments

    if tool_name == "rag_qa":
        if not args.get("query"):
            return make_clarify_route(
                reason="rag_qa 缺少 query 参数",
                message="你想问知识库什么问题？请补充完整问题。"
            )

    if tool_name == "summarize_doc":
        file_name = args.get("file_name")
        if not file_name:
            return make_clarify_route(
                reason="summarize_doc 缺少 file_name 参数",
                message=f"你想总结哪个文档？当前可用文档有：{available_files}"
            )
        if file_name not in available_files:
            return make_clarify_route(
                reason="summarize_doc 指定了不存在的文件",
                message=f"找不到 {file_name}。当前可用文档有：{available_files}"
            )

    if tool_name == "compare_docs":
        file_a = args.get("file_a")
        file_b = args.get("file_b")

        if not file_a or not file_b:
            return make_clarify_route(
                reason="compare_docs 缺少 file_a 或 file_b",
                message=f"你想比较哪两个文档？当前可用文档有：{available_files}"
            )

        missing = [name for name in [file_a, file_b] if name not in available_files]
        if missing:
            return make_clarify_route(
                reason="compare_docs 指定了不存在的文件",
                message=f"找不到这些文件：{missing}。当前可用文档有：{available_files}"
            )

    return route.model_dump()
