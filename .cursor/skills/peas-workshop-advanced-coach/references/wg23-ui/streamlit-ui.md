# WG-23 Streamlit UI

## Goal

Build a Streamlit chat UI shell around `agent_core.Agent`.

Streamlit is synchronous, so it can update the UI directly inside a normal `on_token` callback.

## Allowed Files

- `streamlit_app.py`
- A project-local upload folder such as `uploads/` or `assets/uploads/`

## Forbidden

- Do not modify `agent_core.py`.
- Do not modify `main.py`.
- Do not import or instantiate `ChatOpenAI`.
- Do not copy ReAct, tools, JSONL, memory, or image-message logic into Streamlit.
- Do not convert uploaded images to base64 for the prompt.
- Do not pass absolute paths to `image_path`.

## Required Changes

- Create `streamlit_app.py`.
- Import:
  - `contextlib`
  - `io`
  - `Path`
  - `streamlit as st`
  - `Agent` from `agent_core`
- Initialize one agent in `st.session_state`:
  - `st.session_state.agent = Agent.from_env()`
  - catch `RuntimeError` and show `st.error(...)`
- Use `st.chat_message` to display chat history.
- Use `st.chat_input` for text.
- Use `st.file_uploader` for optional image input.
- Save uploaded images into a project-local folder.
- Pass a relative path string as `image_path`.
- Stream assistant text using `on_token`.
- Wrap `agent.chat(...)` with `contextlib.redirect_stdout(io.StringIO())` and `redirect_stderr(...)` so core print output does not break the UI.

## Streaming Pattern

Use this synchronous callback shape:

```python
answer_parts: list[str] = []
placeholder = st.empty()

def on_token(token: str) -> None:
    answer_parts.append(token)
    placeholder.markdown("".join(answer_parts))

with contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()):
    final_text = agent.chat(user_text, image_path=image_rel, on_token=on_token)
```

## Image Upload Pattern

Use a relative project path:

```python
upload_dir = Path("uploads")
upload_dir.mkdir(exist_ok=True)

image_rel = None
uploaded = st.file_uploader("上傳圖片", type=["png", "jpg", "jpeg", "webp"])
if uploaded is not None:
    safe_name = Path(uploaded.name).name
    image_path = upload_dir / safe_name
    image_path.write_bytes(uploaded.getbuffer())
    image_rel = str(image_path)
```

## Creative Space

Students may customize:

- Product title and description
- Page icon and layout
- Welcome message
- Example prompts
- Sidebar controls
- Image preview and helper text
- Assistant persona presentation

## Verification

- `streamlit_app.py` exists.
- `from agent_core import Agent` exists.
- `Agent.from_env()` is used.
- `agent.chat(..., on_token=...)` is used.
- There is no `ChatOpenAI`.
- There is no `run_react_turn`.
- There is no `save_session_jsonl`.
- Uploaded images are saved under a relative project path.
- `image_path=image_rel` is passed to `agent.chat` when an image is uploaded.
- Streaming text appears incrementally.

Run:

```powershell
uv run streamlit run streamlit_app.py
```

## Return To Router

After the Streamlit UI passes verification:

1. Report the completed WG briefly.
2. Ask exactly: `WG-23 已完成。要檢查、重做，還是整理你的作品說明？`
3. If the student asks for review or redo, return to `references/wg_milestone_checklist.md`, recompute `next_wg`, then read only the routed WG-23 UI card.
4. Do not preload unrelated future cards.
5. Do not start another implementation without explicit confirmation.

## Handoff Card

```text
mode: WG-23 Streamlit UI
allowed_files: streamlit_app.py; uploads/ or assets/uploads/ only
source: agent_core.Agent API; this Streamlit card
preserve: agent_core.py, main.py, student's product idea
must_do: Agent.from_env, st.chat_input, st.chat_message, st.file_uploader, agent.chat(on_token=...), relative image_path, redirect_stdout/stderr
forbidden: ChatOpenAI, run_react_turn, JSONL/memory logic, base64 image prompt, absolute image_path
verify: streamlit app starts; streaming and image upload work through Agent.chat
after_verify: ask "WG-23 已完成。要檢查、重做，還是整理你的作品說明？"; if continuing, rescan and route; read only one card
```
