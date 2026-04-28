import re
from pathlib import Path
from config import CHUNK_SIZE


def load_text(file_path: str) -> str:
    return Path(file_path).read_text(encoding="utf-8")


def normalize_text(text: str) -> str:
    text = text.replace("\r\n", "\n")
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()


def paragraph_split(text: str) -> list[str]:
    text = normalize_text(text)
    paragraphs = [p.strip() for p in re.split(r"\n\s*\n", text) if p.strip()]
    return paragraphs


def chunk_paragraphs(paragraphs: list[str], source: str, chunk_size: int = CHUNK_SIZE) -> list[dict]:
    chunks = []
    current = []
    current_len = 0
    chunk_id = 0

    for para in paragraphs:
        para_len = len(para)

        if current and current_len + para_len + 2 > chunk_size:
            chunk_text = "\n\n".join(current).strip()
            chunks.append({
                "source": source,
                "chunk_id": chunk_id,
                "text": chunk_text
            })
            chunk_id += 1
            current = [para]
            current_len = para_len
        else:
            current.append(para)
            current_len += para_len + 2

    if current:
        chunk_text = "\n\n".join(current).strip()
        chunks.append({
            "source": source,
            "chunk_id": chunk_id,
            "text": chunk_text
        })

    return chunks


def load_knowledge_dir(knowledge_dir: str) -> list[dict]:
    root = Path(knowledge_dir)
    if not root.exists():
        raise FileNotFoundError(f"知识库目录不存在: {knowledge_dir}")

    all_chunks = []
    for path in sorted(root.glob("*")):
        if path.suffix.lower() not in {".md", ".txt"}:
            continue

        text = load_text(str(path))
        paragraphs = paragraph_split(text)
        chunks = chunk_paragraphs(paragraphs, source=path.name)
        all_chunks.extend(chunks)

    if not all_chunks:
        raise ValueError("知识库目录中没有可用的 txt/md 文档")

    return all_chunks
