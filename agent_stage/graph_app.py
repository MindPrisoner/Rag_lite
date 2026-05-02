from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.memory import InMemorySaver

from .graph_state import AgentState
from .graph_nodes import (
    router_node,
    rag_qa_node,
    summarize_doc_node,
    compare_docs_node,
    clarify_node,
    finalize_node,
    error_wrapper,
)


def route_by_tool(state: AgentState) -> str:
    selected_tool = state.get("selected_tool")

    if selected_tool == "rag_qa":
        return "rag_qa"

    if selected_tool == "summarize_doc":
        return "summarize_doc"

    if selected_tool == "compare_docs":
        return "compare_docs"

    if selected_tool == "clarify":
        return "clarify"

    return "finalize"


def build_graph():
    graph_builder = StateGraph(AgentState)

    graph_builder.add_node("router", error_wrapper(router_node))
    graph_builder.add_node("rag_qa", error_wrapper(rag_qa_node))
    graph_builder.add_node("summarize_doc", error_wrapper(summarize_doc_node))
    graph_builder.add_node("compare_docs", error_wrapper(compare_docs_node))
    graph_builder.add_node("clarify", error_wrapper(clarify_node))
    graph_builder.add_node("finalize", error_wrapper(finalize_node))

    graph_builder.add_edge(START, "router")

    graph_builder.add_conditional_edges(
        "router",
        route_by_tool,
        {
            "rag_qa": "rag_qa",
            "summarize_doc": "summarize_doc",
            "compare_docs": "compare_docs",
            "clarify": "clarify",
            "finalize": "finalize",
        },
    )

    graph_builder.add_edge("rag_qa", "finalize")
    graph_builder.add_edge("summarize_doc", "finalize")
    graph_builder.add_edge("compare_docs", "finalize")
    graph_builder.add_edge("clarify", "finalize")
    graph_builder.add_edge("finalize", END)

    checkpointer = InMemorySaver()
    return graph_builder.compile(checkpointer=checkpointer)


graph = build_graph()
