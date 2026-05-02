import json
import gradio as gr

from .graph_app import graph


def extract_answer(tool_result):
    if isinstance(tool_result, dict):
        if "answer" in tool_result:
            return tool_result["answer"]
        return json.dumps(tool_result, indent=2, ensure_ascii=False, default=str)

    return str(tool_result)


def run_agent(query: str, knowledge_dir: str, thread_id: str):
    config = {
        "configurable": {
            "thread_id": thread_id
        }
    }

    result = graph.invoke(
        {
            "user_query": query,
            "knowledge_dir": knowledge_dir,
        },
        config=config,
    )

    final_output = result.get("final_output", {})
    selected_tool = final_output.get("selected_tool")
    route_result = final_output.get("route_result", {})
    tool_result = final_output.get("tool_result", {})
    history = final_output.get("history", [])
    error = final_output.get("error")

    answer = extract_answer(tool_result)

    return (
        selected_tool or "",
        answer,
        json.dumps(route_result, indent=2, ensure_ascii=False, default=str),
        json.dumps(history, indent=2, ensure_ascii=False, default=str),
        error or "",
    )


with gr.Blocks(title="LangGraph Agent Demo") as demo:
    gr.Markdown("# LangGraph 多工具研究助手")
    gr.Markdown("支持知识库问答、文档总结、文档对比、模糊请求澄清和多轮记忆。")

    with gr.Row():
        query_input = gr.Textbox(
            label="用户问题",
            placeholder="例如：请总结 engineering.md 的核心内容",
            lines=3,
        )

    with gr.Row():
        knowledge_dir_input = gr.Textbox(label="知识库目录", value="knowledge")
        thread_id_input = gr.Textbox(label="Thread ID", value="gradio-demo")

    submit_btn = gr.Button("运行 Agent")

    selected_tool_output = gr.Textbox(label="选中的工具")
    answer_output = gr.Textbox(label="工具输出 / 最终回答", lines=10)
    route_output = gr.Textbox(label="路由结果", lines=10)
    history_output = gr.Textbox(label="最近记忆", lines=10)
    error_output = gr.Textbox(label="错误信息")

    submit_btn.click(
        fn=run_agent,
        inputs=[query_input, knowledge_dir_input, thread_id_input],
        outputs=[
            selected_tool_output,
            answer_output,
            route_output,
            history_output,
            error_output,
        ],
    )


if __name__ == "__main__":
    demo.launch(server_name="127.0.0.1", server_port=7861)
