def build_context_text(contexts: list[dict], max_chars: int = 1400) -> str:
    parts = []
    total_len = 0

    for item in contexts:
        piece = f"[片段{item['rank']}] source={item['source']} chunk={item['chunk_id']}\n{item['text']}\n\n"
        if total_len + len(piece) > max_chars:
            break
        parts.append(piece)
        total_len += len(piece)

    return "".join(parts).strip()


def get_career_prompt(mode: str, query: str, contexts: list[dict]):
    context_text = build_context_text(contexts)

    system_prompt = """
你是一名严谨的 AI 求职助手。
你必须优先依据给定资料回答，不要脱离资料自由发挥。
如果资料不足，请明确说明“根据当前资料无法完全确定”。
回答要专业、直接、适合求职场景。
""".strip()

    if mode == "fit":
        user_prompt = f"""
参考资料：
{context_text}

用户请求：
{query}

请输出以下结构：
1. 岗位匹配亮点
2. 当前能力短板
3. 简历应强调的内容
4. 两周补强计划
5. 参考来源

要求：
- 结合候选人资料和目标岗位资料
- 内容具体，不要空话
- 最后列出参考来源
""".strip()

    elif mode == "mock":
        user_prompt = f"""
参考资料：
{context_text}

用户请求：
{query}

请输出以下结构：
1. 高频问题 1~5
2. 每题考察点
3. 每题参考回答（简洁版）
4. 面试官可能继续追问什么
5. 参考来源

要求：
- 问题尽量贴近 AI 应用工程 / RAG / 项目落地场景
- 回答要像候选人真实可说出口的话
- 最后列出参考来源
""".strip()

    elif mode == "project":
        user_prompt = f"""
参考资料：
{context_text}

用户请求：
{query}

请输出以下结构：
1. 30 秒项目讲解
2. 1 分钟项目讲解
3. 项目亮点
4. 技术取舍说明
5. 可能追问与回答要点
6. 参考来源

要求：
- 适合面试场景
- 强调工程实现、问题处理、展示价值
- 最后列出参考来源
""".strip()

    else:
        raise ValueError(f"不支持的 mode: {mode}")

    return system_prompt, user_prompt
