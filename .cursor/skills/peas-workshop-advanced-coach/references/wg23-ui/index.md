# WG-23: UI Shell for Your Agent

## Goal

Turn the completed WG-22 `agent_core.Agent` into a personal chat UI product.

This is **not** a rewrite of the agent. It is a UI shell around the existing core.

Core wiring is fixed; product experience is creative.

## Prerequisite

- WG-22 is complete.
- Project root has `agent_core.py`.
- `from agent_core import Agent` works.
- Thin CLI `main.py` still works.

## Student Choice

Ask one concise choice:

```text
接下來要把你的 Agent 做成 UI 產品。
你想用哪個框架？

1. Streamlit：同步 UI，適合快速做原型
2. Chainlit：聊天產品感更強，但串流需要 async adapter
```

Then read exactly one implementation card:

- Streamlit -> `references/wg23-ui/streamlit-ui.md`
- Chainlit -> `references/wg23-ui/chainlit-ui.md`

## Creative Freedom

Students may customize:

- Product name
- Theme / role / welcome message
- Layout and colors
- Example prompts and quick actions
- Image upload UX and preview text
- Upload folder name inside the project
- Whether the product is a study coach, image explainer, travel helper, recipe assistant, game NPC, etc.

## Non-Negotiable Wiring Rules

- UI must `from agent_core import Agent`.
- UI must initialize with `Agent.from_env()`.
- UI must call `agent.chat(..., on_token=...)`.
- Image uploads must be saved inside the project and passed as a **relative** `image_path`.
- UI must not import or instantiate `ChatOpenAI`.
- UI must not copy or call:
  - `run_react_turn`
  - `save_session_jsonl`
  - `load_session_jsonl`
  - `ensure_budget_before_react`
  - `messages_for_model`
- UI must not implement ReAct, tools, JSONL, memory, or multimodal message construction.
- UI must not convert uploaded images to base64 for the prompt.

## Important: `on_token` and `await`

`Agent.chat()` is a synchronous function. It calls `on_token(token)` directly.

Therefore:

- Streamlit can use a normal synchronous `def on_token(token): ...`.
- Chainlit must not pass `async def on_token(...)` directly to `Agent.chat()`, because `Agent.chat()` will not `await` it.
- Chainlit must use an async adapter / queue so synchronous tokens are bridged into `await msg.stream_token(token)`.

## Common Verification

- UI file exists.
- UI imports `Agent`.
- UI calls `Agent.from_env()`.
- UI calls `agent.chat(..., on_token=...)`.
- UI has no `ChatOpenAI`.
- UI has no `run_react_turn`.
- UI has no `save_session_jsonl`.
- UI has no `ensure_budget_before_react`.
- Uploaded image path passed to `Agent.chat` is relative.
- Streaming displays tokens.
- Missing API key is shown as a UI error, not a traceback.

## Return To Router

After WG-23 passes verification:

1. Report the completed WG briefly.
2. Ask exactly: `WG-23 已完成。要檢查、重做，還是整理你的作品說明？`
3. If the student asks for review or redo, return to `references/wg_milestone_checklist.md`, recompute `next_wg`, then read only the routed WG-23 UI card.
4. Do not preload unrelated future cards.
5. Do not start another implementation without explicit confirmation.

## Handoff Card

```text
mode: WG-23 UI shell
allowed_files: selected UI file; project-local upload folder only
source: agent_core.Agent API from WG-22; selected WG-23 UI card
preserve: agent_core.py, main.py, JSONL/memory/session behavior, student's product idea
must_do: import Agent, Agent.from_env(), agent.chat(..., on_token=...), image upload -> relative image_path
forbidden: direct OpenAI call, ReAct/JSONL/memory logic in UI, base64 image prompt in UI, async on_token passed directly to sync Agent.chat
verify: UI starts; streaming works; image_path is passed to Agent.chat; no forbidden core logic in UI
after_verify: ask "WG-23 已完成。要檢查、重做，還是整理你的作品說明？"; if continuing, rescan and route; read only one card
```
