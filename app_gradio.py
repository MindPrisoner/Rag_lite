import gradio as gr
from pipeline import run_rag


def format_sources(retrieved: list[dict]) -> str:
    if not retrieved:
        return "无"
    lines = []
    for item in retrieved:
        lines.append(
            f"- source={item['source']} | chunk={item['chunk_id']} | score={item['score']:.4f}"
        )
    return "\n".join(lines)


def format_retrieved_text(retrieved: list[dict]) -> str:
    if not retrieved:
        return "无检索结果"
    parts = []
    for item in retrieved:
        parts.append(
            f"[片段{item['rank']}] source={item['source']} chunk={item['chunk_id']} score={item['score']:.4f}\n{item['text']}"
        )
    return "\n\n".join(parts)


def rag_query(query: str, knowledge_dir: str):
    result = run_rag(query=query, knowledge_dir=knowledge_dir)

    return (
        result["answer"],
        result["answer_status"],
        result["error"] or "",
        str(result["elapsed_ms"]),
        result["timestamp"],
        format_sources(result["retrieved"]),
        format_retrieved_text(result["retrieved"]),
    )


with gr.Blocks(title="RAG Lite Demo") as demo:
    gr.Markdown("# RAG Lite Demo")
    gr.Markdown("输入问题，查看答案、来源和检索命中片段。")

    with gr.Row():
        query_input = gr.Textbox(label="问题", placeholder="请输入你的问题")
        knowledge_dir_input = gr.Textbox(label="知识库目录", value="knowledge")

    submit_btn = gr.Button("查询")

    answer_output = gr.Textbox(label="最终答案", lines=8)
    status_output = gr.Textbox(label="生成状态")
    error_output = gr.Textbox(label="错误信息")
    elapsed_output = gr.Textbox(label="耗时(ms)")
    timestamp_output = gr.Textbox(label="时间戳")
    sources_output = gr.Textbox(label="参考来源", lines=5)
    retrieved_output = gr.Textbox(label="检索结果详情", lines=16)

    submit_btn.click(
        fn=rag_query,
        inputs=[query_input, knowledge_dir_input],
        outputs=[
            answer_output,
            status_output,
            error_output,
            elapsed_output,
            timestamp_output,
            sources_output,
            retrieved_output,
        ],
    )

if __name__ == "__main__":
    demo.launch(server_name="127.0.0.1", server_port=7860)
