import argparse
from career_pipeline import run_career_rag


def main():
    parser = argparse.ArgumentParser(description="求职场景 RAG CLI")
    parser.add_argument("--mode", required=True, choices=["fit", "mock", "project"], help="求职模式")
    parser.add_argument("--dir", default="career_knowledge", help="求职知识库目录")
    parser.add_argument("--query", required=True, help="用户问题")
    args = parser.parse_args()

    result = run_career_rag(mode=args.mode, query=args.query, knowledge_dir=args.dir)

    print("=== 模式 ===")
    print(result["mode"])
    print()

    print("=== 问题 ===")
    print(result["query"])
    print()

    print("=== 检索结果 ===")
    for item in result["retrieved"]:
        print(f"[片段{item['rank']}] source={item['source']} chunk={item['chunk_id']} score={item['score']:.4f}")
        print(item["text"])
        print()

    print("=== 生成状态 ===")
    print(result["answer_status"])
    print()

    print("=== 最终输出 ===")
    print(result["answer"])


if __name__ == "__main__":
    main()
