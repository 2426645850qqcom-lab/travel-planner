# TripForge

> 5 个 AI Agent 同时开工，3 秒出一份旅行计划。

---

## 它是什么？

你告诉 TripForge 想去哪、待几天、花多少钱，它启动一组 AI Agent 分别去搜景点、查天气、找酒店，最后汇总成一份可以跟着走的行程表。不用自己翻小红书、高德、携程来回切换。

**Form 模式**适合快速出结果，填表 30 秒 → 等几秒 → 出计划。
**Chat 模式**适合没有明确想法的时候，像聊天一样慢慢把需求说明白，AI 追问、补全、纠错。

规划完的行程有地图、有预算拆解、有每日时间线，可以导出 PDF 带走。

---

## 怎么搭起来

### 你需要的钥匙

| 去哪申请 | 用来干嘛 |
|----------|----------|
| [DeepSeek 开放平台](https://platform.deepseek.com) | 让 AI 能"思考"，生成行程 |
| [高德开放平台](https://lbs.amap.com) | 搜景点、查天气、找酒店 |

> 高德要申请两次：Web 服务 Key 给后端用，JS API Key 给前端地图用。

### 后端

```bash
cd backend
pip install -r requirements.txt
cp .env.example .env   # 然后把 Key 填进去
python run.py           # 跑在 8000 端口
```

### 前端

```bash
cd frontend
npm install
cp .env.example .env   # 填前端用的高德 Key
npm run dev             # 跑在 5173 端口
```

打开浏览器就是首页，填表或聊天都行。

---

## 里面长什么样

整个系统可以理解成一条流水线：

```
你说"想去杭州玩两天"
        │
        ▼
┌──────────────────┐
│   POI Agent      │  ← 分析你的偏好，搜出最匹配的 20 个景点
└──────┬───────────┘
        ▼
┌──────────────────┐
│   Weather Agent  │  ← 查目的地这几天的天气
└──────┬───────────┘
        ▼
┌──────────────────┐
│   Hotel Agent    │  ← 按你选的住宿档位找酒店
└──────┬───────────┘
        ▼
┌──────────────────┐
│   Planner Agent  │  ← 把上面的信息拼成完整行程 JSON
└──────┬───────────┘
        ▼
┌──────────────────┐
│   Human Review   │  ← 你看了不满意可以打回去重做
└──────────────────┘
```

五个 Agent 是按顺序跑的，但每个 Agent 内部都在并行干活。前端用 SSE 流式接收进度，所以你能看到实时的 Agent 状态切换。

这整个编排逻辑写在 **LangGraph** 的状态图里，LLM 端可以切 DeepSeek 或 OpenAI，地图数据来自高德 API。

---

## 技术选型

**后端：** FastAPI · LangChain · LangGraph · Pydantic v2 · ChromaDB · SSE

**前端：** Vue 3 · TypeScript · Pinia · Element Plus · 高德 JS API

**外部：** DeepSeek / OpenAI · 高德地图 · LangSmith（可选，监控 Agent）

---

## 项目结构

```
travel-planner/
├── backend/
│   └── app/
│       ├── agents/      # LangGraph 状态图 + 5 个 Agent 节点
│       ├── api/         # FastAPI 路由（trip / chat / map / config）
│       ├── core/        # 配置、LLM 工厂、对话记忆
│       ├── models/      # Pydantic 数据模型
│       └── services/    # 高德 API 封装、向量存储
└── frontend/
    └── src/
        ├── views/       # Home（表单）/ Chat（对话）/ Result（结果+地图）
        ├── stores/      # Pinia 状态
        └── services/    # Axios API 调用
```

---

## 注意事项

- **别把 `.env` 传上去** —— 里面是你的 API Key，.gitignore 已经拦住了
- 高德 Web 服务 Key 和 JS API Key 是两把不同的钥匙，别混用
- DeepSeek 调用会扣费，不过很便宜，规划一次大概几分钱
- 预算数字是 AI 估算的，实际花销以现场为准
- `saved_results/` 里的 JSON 是你每次规划的存档，定期清理不会丢东西

---

## 路线图

- [ ] 接入更多 LLM（Claude、通义千问）
- [ ] 行程分享链接
- [ ] 用户系统 + 历史记录
- [ ] 移动端 PWA 适配
- [ ] 景点实拍图 + 评价聚合

---

建这个项目是为了练手 LangGraph 的多 Agent 编排，如果你有想法或发现了 bug，欢迎提 Issue 或者直接 PR。
