# 项目：RAG Lite Demo

## 项目目标
构建一个轻量级中文 RAG 原型项目，在不依赖本地重型向量模型的情况下，完成多文档知识库问答、来源引用、FastAPI 接口、Gradio 页面和查询日志。

## 核心实现
- 多文档知识库加载
- 按段落优先分块
- BM25 + jieba 检索
- OpenAI 兼容接口生成答案
- source / chunk_id 元信息保留
- 查询日志记录
- FastAPI 接口
- Gradio 演示页面

## 我做过的优化
- 修复固定长度切分导致的片段断裂问题
- 给生成阶段加入 timeout、重试和失败兜底
- 将真实 API Key 移到系统环境变量，避免误传 GitHub
- 补齐 README、.gitignore、.env.example、启动脚本

## 项目价值
- 适合求职展示
- 能说明我会搭建完整 LLM 应用链路
- 能体现我会做技术取舍、服务化和工程规范
