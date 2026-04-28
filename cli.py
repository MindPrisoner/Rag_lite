import argparse
from pipeline import run_rag


def main():
    parser = argparse.ArgumentParser(description="RAG CLI（多文档 + 来源引用）")
    parser.add_argument("--dir", default="knowledge", help="知识库目录路径")
    parser.add_argument("--query", required=True, help="用户问题")
    args = parser.parse_args()

    result = run_rag(query=args.query, knowledge_dir=args.dir)

    print("=== 问题 ===")
    print(result["query"])
    print()

    print("=== 检索结果 ===")
    for item in result["retrieved"]:
        print(
            f"[片段{item['rank']}] source={item['source']} chunk={item['chunk_id']} score={item['score']:.4f}"
        )
        print(item["text"])
        print()

    print("=== 生成状态 ===")
    print(result["answer_status"])
    print()

    print("=== 最终答案 ===")
    print(result["answer"])


if __name__ == "__main__":
    main()
