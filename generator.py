import time
from openai import OpenAI, APITimeoutError
from config import API_KEY, BASE_URL, MODEL_NAME

client = OpenAI(
    api_key=API_KEY,
    base_url=BASE_URL,
)

SYSTEM_PROMPT = """
你是一个严谨的 RAG 问答助手。
请优先依据给定参考资料回答，不要脱离资料自由发挥。
如果资料不足以回答，请明确说“根据当前资料无法确定”。
回答要简洁、清晰，并在最后列出参考来源。
"""


def build_context_text(contexts: list[dict], max_chars: int = 1200) -> str:
    parts = []
    total_len = 0

    for item in contexts:
        piece = f"[片段{item['rank']}] source={item['source']} chunk={item['chunk_id']}\n{item['text']}\n\n"
        if total_len + len(piece) > max_chars:
            break
        parts.append(piece)
        total_len += len(piece)

    return "".join(parts).strip()


def generate_answer(query: str, contexts: list[dict], timeout: int = 60, max_retries: int = 3) -> str:
    context_text = build_context_text(contexts, max_chars=1200)

    user_prompt = f"""
参考资料：
{context_text}

用户问题：
{query}

请根据参考资料回答问题。
要求：
1. 优先使用参考资料中的信息
2. 如果资料不足，不要编造
3. 回答尽量简洁
4. 最后用“参考来源：...”列出你主要使用的 source 和 chunk_id
"""

    last_error = None

    for attempt in range(1, max_retries + 1):
        try:
            response = client.chat.completions.create(
                model=MODEL_NAME,
                messages=[
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {"role": "user", "content": user_prompt},
                ],
                temperature=0.2,
                timeout=timeout,
            )
            return response.choices[0].message.content.strip()

        except APITimeoutError as e:
            last_error = e
            if attempt < max_retries:
                sleep_seconds = attempt * 2
                print(f"[WARN] 第 {attempt} 次生成超时，{sleep_seconds} 秒后重试...")
                time.sleep(sleep_seconds)
            else:
                break

        except Exception as e:
            last_error = e
            break

    raise RuntimeError(f"生成阶段失败: {type(last_error).__name__}: {last_error}") from last_error
