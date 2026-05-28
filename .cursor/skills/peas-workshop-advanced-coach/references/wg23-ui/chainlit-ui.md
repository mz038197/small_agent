# WG-23 Chainlit UI

## Goal

Build a Chainlit chat UI shell around `agent_core.Agent`.

Chainlit display APIs are async, while `Agent.chat()` is synchronous. Use an async adapter / queue to bridge `on_token` into `await msg.stream_token(...)`.

## Allowed Files

- `chainlit_app.py`
- A project-local upload folder such as `uploads/` or `assets/uploads/`

## Forbidden

- Do not modify `agent_core.py`.
- Do not modify `main.py`.
- Do not import or instantiate `ChatOpenAI`.
- Do not copy ReAct, tools, JSONL, memory, or image-message logic into Chainlit.
- Do not convert uploaded images to base64 for the prompt.
- Do not pass absolute paths to `image_path`.
- Do not pass `async def on_token(...)` directly into synchronous `Agent.chat()`.

## Required Changes

- Create `chainlit_app.py`.
- Import:
  - `asyncio`
  - `contextlib`
  - `io`
  - `Path`
  - `chainlit as cl`
  - `Agent` from `agent_core`
- Use `@cl.on_chat_start` to initialize `Agent.from_env()`.
- Store the agent with `cl.user_session.set("agent", agent)`.
- Use `@cl.on_message` to receive messages.
- Retrieve the agent with `cl.user_session.get("agent")`.
- Create `cl.Message(content="")` and stream tokens into it.
- Extract image/file uploads from `message.elements`, save them under a project-local folder, and pass a relative path as `image_path`.
- Wrap the synchronous agent call with `contextlib.redirect_stdout(...)` and `redirect_stderr(...)`.

## Async Adapter Pattern

Use this shape. The exact helper name may change, but the architecture must remain:

```python
async def run_agent_with_streaming(agent, text: str, msg: cl.Message, image_path: str | None = None) -> str:
    loop = asyncio.get_running_loop()
    queue: asyncio.Queue[str | None] = asyncio.Queue()

    def on_token(token: str) -> None:
        loop.call_soon_threadsafe(queue.put_nowait, token)

    def run_agent() -> str:
        try:
            with contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()):
                return agent.chat(text, image_path=image_path, on_token=on_token)
        finally:
            loop.call_soon_threadsafe(queue.put_nowait, None)

    async def drain() -> None:
        while True:
            token = await queue.get()
            if token is None:
                break
            await msg.stream_token(token)

    result, _ = await asyncio.gather(asyncio.to_thread(run_agent), drain())
    return result
```

Why this is required:

- `Agent.chat()` is synchronous and calls `on_token(token)`.
- `msg.stream_token(token)` is async and must be awaited.
- The queue lets synchronous tokens cross into Chainlit's async event loop safely.

## Image Upload Pattern

Use project-relative paths:

```python
def save_first_image_element(elements) -> str | None:
    upload_dir = Path("uploads")
    upload_dir.mkdir(exist_ok=True)
    for element in elements or []:
        path = getattr(element, "path", None)
        name = getattr(element, "name", None) or "upload"
        mime = getattr(element, "mime", "") or ""
        if path and mime.startswith("image/"):
            suffix = Path(name).suffix or Path(path).suffix
            target = upload_dir / f"chainlit_upload{suffix}"
            target.write_bytes(Path(path).read_bytes())
            return str(target)
    return None
```

The implementation may improve naming, but it must return a relative path inside the project.

## Creative Space

Students may customize:

- App name and welcome message
- `cl.Message` text
- Starter questions
- Product role and examples
- Image preview / response phrasing
- Upload folder naming

## Verification

- `chainlit_app.py` exists.
- `from agent_core import Agent` exists.
- `Agent.from_env()` is used in `@cl.on_chat_start`.
- `agent.chat(..., on_token=...)` is used.
- `asyncio.to_thread` or an equivalent adapter is used for synchronous `Agent.chat`.
- `await msg.stream_token(token)` is called from an async drain/handler, not directly inside a sync callback.
- There is no `ChatOpenAI`.
- There is no `run_react_turn`.
- There is no `save_session_jsonl`.
- Uploaded images are saved under a relative project path.
- `image_path=image_rel` is passed to `agent.chat` when an image is uploaded.

Run:

```powershell
uv run chainlit run chainlit_app.py
```

## Return To Router

After the Chainlit UI passes verification:

1. Report the completed WG briefly.
2. Ask exactly: `WG-23 已完成。要檢查、重做，還是整理你的作品說明？`
3. If the student asks for review or redo, return to `references/wg_milestone_checklist.md`, recompute `next_wg`, then read only the routed WG-23 UI card.
4. Do not preload unrelated future cards.
5. Do not start another implementation without explicit confirmation.

## Handoff Card

```text
mode: WG-23 Chainlit UI
allowed_files: chainlit_app.py; uploads/ or assets/uploads/ only
source: agent_core.Agent API; this Chainlit card
preserve: agent_core.py, main.py, student's product idea
must_do: Agent.from_env in on_chat_start, cl.user_session, on_message, async queue adapter, agent.chat(on_token=...), relative image_path
forbidden: ChatOpenAI, run_react_turn, JSONL/memory logic, base64 image prompt, absolute image_path, async on_token passed directly to Agent.chat
verify: chainlit app starts; streaming works through queue adapter; image upload passes image_path to Agent.chat
after_verify: ask "WG-23 已完成。要檢查、重做，還是整理你的作品說明？"; if continuing, rescan and route; read only one card
```
