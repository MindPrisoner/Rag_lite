import traceback

from .tool_router import route_task
from .tools import tool_rag_qa, tool_summarize_doc, tool_compare_docs
from .graph_state import AgentState


def router_node(state: AgentState) -> dict:
    user_query = state["user_query"]
    knowledge_dir = state.get("knowledge_dir", "knowledge")
    history = state.get("history", [])

    route_result = route_task(
        user_query=user_query,
        knowledge_dir=knowledge_dir,
        history=history,
    )

    return {
        "route_result": route_result,
        "selected_tool": route_result["tool_name"],
        "tool_args": route_result.get("arguments", {}),
    }


def rag_qa_node(state: AgentState) -> dict:
    knowledge_dir = state.get("knowledge_dir", "knowledge")
    tool_args = state.get("tool_args", {})
    query = tool_args["query"]

    result = tool_rag_qa(query=query, knowledge_dir=knowledge_dir)
    return {"tool_result": result}


def summarize_doc_node(state: AgentState) -> dict:
    knowledge_dir = state.get("knowledge_dir", "knowledge")
    tool_args = state.get("tool_args", {})
    file_name = tool_args["file_name"]

    result = tool_summarize_doc(file_name=file_name, knowledge_dir=knowledge_dir)
    return {"tool_result": result}


def compare_docs_node(state: AgentState) -> dict:
    knowledge_dir = state.get("knowledge_dir", "knowledge")
    tool_args = state.get("tool_args", {})
    file_a = tool_args["file_a"]
    file_b = tool_args["file_b"]

    result = tool_compare_docs(file_a=file_a, file_b=file_b, knowledge_dir=knowledge_dir)
    return {"tool_result": result}


def clarify_node(state: AgentState) -> dict:
    tool_args = state.get("tool_args", {})
    message = tool_args.get("message", "你的请求信息不够完整，请补充更多细节。")

    return {
        "tool_result": {
            "answer": message
        }
    }


def build_history_summary(state: AgentState) -> str:
    selected_tool = state.get("selected_tool")
    tool_args = state.get("tool_args", {})
    tool_result = state.get("tool_result", {})

    if selected_tool == "rag_qa":
        answer = tool_result.get("answer", "") if isinstance(tool_result, dict) else ""
        return f"完成了一次知识库问答，答案摘要：{answer[:120]}"

    if selected_tool == "summarize_doc":
        file_name = tool_args.get("file_name", "")
        return f"总结了文档 {file_name}"

    if selected_tool == "compare_docs":
        file_a = tool_args.get("file_a", "")
        file_b = tool_args.get("file_b", "")
        return f"比较了文档 {file_a} 和 {file_b}"

    if selected_tool == "clarify":
        return "向用户请求补充信息"

    return "完成了一次任务"


def finalize_node(state: AgentState) -> dict:
    history = state.get("history", [])

    new_history_item = {
        "user_query": state.get("user_query"),
        "selected_tool": state.get("selected_tool"),
        "tool_args": state.get("tool_args"),
        "summary": build_history_summary(state),
    }

    updated_history = history + [new_history_item]

    return {
        "history": updated_history,
        "final_output": {
            "user_query": state.get("user_query"),
            "selected_tool": state.get("selected_tool"),
            "route_result": state.get("route_result"),
            "tool_result": state.get("tool_result"),
            "history": updated_history[-5:],
            "error": state.get("error"),
        }
    }


def error_wrapper(node_fn):
    def wrapped(state: AgentState) -> dict:
        try:
            return node_fn(state)
        except Exception as e:
            return {
                "error": f"{type(e).__name__}: {e}",
                "tool_result": {
                    "traceback": traceback.format_exc()
                }
            }
    return wrapped
