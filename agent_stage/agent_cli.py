import argparse
import json

from .graph_app import graph


def main():
    parser = argparse.ArgumentParser(description="LangGraph 版多工具研究助手")
    parser.add_argument("--query", required=True, help="用户任务描述")
    parser.add_argument("--dir", default="knowledge", help="知识库目录")
    parser.add_argument(
        "--thread-id",
        default="agent-cli-default",
        help="LangGraph 对话线程 ID，用于 checkpointer 保存状态",
    )
    args = parser.parse_args()

    config = {
        "configurable": {
            "thread_id": args.thread_id
        }
    }

    result = graph.invoke(
        {
            "user_query": args.query,
            "knowledge_dir": args.dir,
        },
        config=config,
    )

    print("=== 最终 State ===")
    print(json.dumps(result, indent=2, ensure_ascii=False, default=str))
    print()

    print("=== 最终输出 ===")
    print(json.dumps(result.get("final_output", {}), indent=2, ensure_ascii=False, default=str))


if __name__ == "__main__":
    main()
