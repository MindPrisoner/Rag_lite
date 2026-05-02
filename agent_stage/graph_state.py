from typing import TypedDict, Optional, Any


class AgentState(TypedDict, total=False):
    user_query: str
    knowledge_dir: str

    history: list[dict]

    route_result: dict
    selected_tool: str
    tool_args: dict

    tool_result: Any
    final_output: dict

    error: Optional[str]
