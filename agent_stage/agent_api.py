from typing import Any
from fastapi import FastAPI
from pydantic import BaseModel, Field

from .graph_app import graph


class AgentRequest(BaseModel):
    query: str
    knowledge_dir: str = "knowledge"
    thread_id: str = "agent-api-default"


class AgentResponse(BaseModel):
    thread_id: str
    selected_tool: str | None = None
    route_result: dict[str, Any] | None = None
    tool_result: Any = None
    history: list[dict[str, Any]] = Field(default_factory=list)
    error: str | None = None
    final_output: dict[str, Any] = Field(default_factory=dict)


app = FastAPI(title="LangGraph Agent API")


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/agent/query", response_model=AgentResponse)
def agent_query(req: AgentRequest):
    config = {
        "configurable": {
            "thread_id": req.thread_id
        }
    }

    result = graph.invoke(
        {
            "user_query": req.query,
            "knowledge_dir": req.knowledge_dir,
        },
        config=config,
    )

    final_output = result.get("final_output", {})

    return {
        "thread_id": req.thread_id,
        "selected_tool": final_output.get("selected_tool"),
        "route_result": final_output.get("route_result"),
        "tool_result": final_output.get("tool_result"),
        "history": final_output.get("history", []),
        "error": final_output.get("error"),
        "final_output": final_output,
    }
