# LangGraph Agent 架构说明

## 整体流程

```mermaid
flowchart TD
    A[用户输入] --> B[Router 路由节点]
    B --> C{选择工具}
    C -->|rag_qa| D[RAG 知识库问答]
    C -->|summarize_doc| E[文档总结工具]
    C -->|compare_docs| F[文档对比工具]
    C -->|clarify| G[澄清节点]
    D --> H[Finalize 汇总输出]
    E --> H
    F --> H
    G --> H
    H --> I[更新 History]
    I --> J[返回结果]



核心模块说明
1. Router 节点

Router 节点负责理解用户请求，并判断应该调用哪个工具。
它不会直接回答问题，而是输出结构化路由结果。

可选工具包括：

rag_qa
summarize_doc
compare_docs
clarify
2. 工具节点

不同工具节点负责不同任务：

rag_qa：基于知识库检索和生成答案
summarize_doc：总结指定文档
compare_docs：比较两个文档
clarify：当用户请求不完整时，要求用户补充信息
3. State 状态

系统使用 LangGraph 的 state 保存当前执行过程中的信息，包括：

用户问题
当前知识库目录
路由结果
选中的工具
工具参数
工具执行结果
历史记忆
错误信息
4. Memory 记忆机制

系统通过 thread_id 区分不同对话线程。
同一个 thread_id 下，系统可以保留最近几轮历史，从而理解“它”“刚才那个文档”等指代。

5. Clarify 澄清节点

当用户请求缺少必要信息时，系统不会盲目猜测，而是进入澄清节点。
例如：

“请总结那个文档”
“请比较这两个文档”

这类请求会触发系统询问用户具体文件名。







