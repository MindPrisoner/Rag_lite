import argparse
import json

from .graph_app import graph


def print_short_output(result: dict):
    final_output = result.get("final_output", {})
    selected_tool = final_output.get("selected_tool")
    tool_result = final_output.get("tool_result", {})

    print("\n=== 本轮工具 ===")
    print(selected_tool)

    print("\n=== 本轮输出 ===")
    if isinstance(tool_result, dict) and "answer" in tool_result:
        print(tool_result["answer"])
    else:
        print(json.dumps(tool_result, indent=2, ensure_ascii=False, default=str))

    print("\n=== 最近记忆 ===")
    history = final_output.get("history", [])
    print(json.dumps(history, indent=2, ensure_ascii=False, default=str))


def main():
    parser = argparse.ArgumentParser(description="LangGraph 多轮记忆 CLI")
    parser.add_argument("--dir", default="knowledge", help="知识库目录")
    parser.add_argument("--thread-id", default="demo", help="对话线程 ID")
    args = parser.parse_args()

    config = {
        "configurable": {
            "thread_id": args.thread_id
        }
    }

    print("LangGraph 多轮记忆 CLI 已启动")
    print("输入 exit / quit 退出")
    print(f"当前 thread_id = {args.thread_id}")

    while True:
        user_query = input("\n你：").strip()

        if user_query.lower() in {"exit", "quit"}:
            print("已退出")
            break

        if not user_query:
            continue

        result = graph.invoke(
            {
                "user_query": user_query,
                "knowledge_dir": args.dir,
            },
            config=config,
        )

        print_short_output(result)


if __name__ == "__main__":
    main()
