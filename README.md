# RAG Lite Demo

一个轻量级的中文 RAG 原型项目，使用 **BM25 检索 + 大模型生成** 实现本地知识库问答，支持：

- CLI 问答
- FastAPI 接口调用
- Gradio 可视化页面
- 检索结果展示
- 来源引用
- 查询日志记录

## 项目特点

- 不依赖本地向量模型，不安装重型 `torch / sentence-transformers / faiss`
- 使用 `rank-bm25 + jieba` 搭建轻量检索原型
- 使用 OpenAI 兼容接口接入大模型生成
- 支持多文档知识库检索
- 回答时给出参考来源，便于调试和展示
- 自动记录查询日志，便于后续评估和优化

## 项目结构

```text
rag_lite/
├── knowledge/           # 本地知识库
├── logs/                # 查询日志
├── api.py               # FastAPI 接口
├── app_gradio.py        # Gradio 页面
├── cli.py               # 命令行入口
├── config.py            # 配置读取
├── loader.py            # 文档加载与分块
├── retriever.py         # BM25 检索
├── generator.py         # 大模型生成
├── pipeline.py          # 主流程
├── logger_utils.py      # 日志记录
├── schemas.py           # API 数据结构
└── README.md



环境准备
1. 创建 conda 环境
conda create -n llm python=3.11 -y
conda activate llm
2. 安装依赖
pip install -r requirements.txt
3. 配置环境变量

请先在你的 shell 环境中设置：

export DASHSCOPE_API_KEY="你的真实key"

然后准备 .env 文件，可参考 .env.example。

运行方式
方式 1：CLI
python cli.py --dir knowledge --query "为什么一个 RAG Demo 需要来源引用？"
方式 2：FastAPI
uvicorn api:app --reload

打开：

http://127.0.0.1:8000/docs
方式 3：Gradio
python app_gradio.py

打开：

http://127.0.0.1:7860
示例问题
一个基础的 RAG 系统通常包括哪些模块？
为什么一个 RAG Demo 需要来源引用？
为什么不能把 chunk 从单词中间切开？
当前实现

当前版本采用 BM25 检索 + LLM 生成，重点是先打通一个轻量、可展示、可服务化的 RAG 原型。

后续可继续升级为：

向量检索
混合检索
多轮对话记忆
查询日志分析
前端产品化
Docker 部署
注意事项
不要把真实 API Key 写入 .env
请确保 .env 已加入 .gitignore
日志目录默认不会上传到 GitHub
项目价值

这个项目适合作为：

LLM / RAG 学习项目
求职展示项目
AI 应用工程化练手项目
后续 LangChain / Agent 系统的基础模块




## LangGraph 多工具 Agent

在 RAG Lite 的基础上，本项目进一步实现了 LangGraph 多工具工作流，支持：

- RAG 知识库问答
- 单文档总结
- 双文档对比
- 模糊请求澄清
- 多轮短期记忆
- FastAPI 接口
- Gradio 页面展示

### 运行 Agent CLI

```bash
python -m agent_stage.agent_cli --dir knowledge --query "RAG 的核心流程是什么？"



运行多轮记忆 CLI
python -m agent_stage.memory_cli --dir knowledge --thread-id demo
运行 Agent API
uvicorn agent_stage.agent_api:app --reload

访问：

http://127.0.0.1:8000/docs
运行 Agent Gradio 页面
python -m agent_stage.agent_gradio

访问：

http://127.0.0.1:7861
Agent 工作流
用户请求
  ↓
Router 路由节点
  ↓
选择工具：rag_qa / summarize_doc / compare_docs / clarify
  ↓
执行工具
  ↓
Finalize 汇总输出
  ↓
更新历史记忆
