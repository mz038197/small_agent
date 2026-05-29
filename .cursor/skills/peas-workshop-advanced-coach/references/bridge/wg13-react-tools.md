# WG-13: 工具呼叫與 ReAct 迴圈

## Goal

Add the minimal LangChain tool-calling loop so the agent can call tools instead of answering everything directly.

## Prerequisite

Project-root `main.py` has WG-12 style system/history separation.

## Allowed Files

- `main.py`

## Forbidden

- Do not add file or shell tools yet; those belong to WG-14.
- Do not add JSONL persistence; that belongs to WG-15.
- Do not create `agent_core.py`; that belongs to WG-22.
- Do not overwrite the student's `nick` or persona wording.

## Required Changes

- Add `get_identity()` by upgrading the WG-12 identity prompt:
  - Keep the student's existing `nick` / display name.
  - Replace or expand the old short `system_text` so it includes only the WG-13 identity text:
    - `你是課堂程式助教，並請使用繁體中文。`
    - `【解題方式】`
    - `write_file`
    - `exec`
    - `uv run python`
    - `【依賴管理】`
    - `uv add <套件名>`
    - `不要用 pip install`
  - Return `f"{system_text}\n\n【本場次顯示名稱】{nick}"`.
- Add `get_runtime_environment()` as a separate runtime section:
  - Keep environment and platform restrictions out of `get_identity()`.
  - Include `【執行環境】`.
  - Detect Windows vs Unix-like at runtime instead of hard-coding the operating system.
  - On Windows, include `Windows`, the detected shell name when available, `【平台限制】`, `禁止使用 heredoc`, and `python - <<'PY'`.
  - Tell the agent to use `write_file` to create a `.py` script, then run `uv run python <script.py>` for multi-line Python.
- Add `add_numbers` as a LangChain `@tool`.
- Add `TOOLS = [add_numbers]` for WG-13; WG-14 will extend this list with file/shell tools.
- Bind tools to the chat model.
- Add `_stream_model_response()` or equivalent streaming accumulator.
- Add `run_react_turn()` with the ReAct loop:
  - send system + history + current user message;
  - stream assistant text;
  - execute requested tools;
  - append `ToolMessage`;
  - repeat until no tool calls remain.

## Preserve

- Student display name / nick in `get_identity()`.
- The WG-12 identity intent, but **not** the old one-line `system_text` if it lacks `【解題方式】` and `【依賴管理】`.
- Existing import style unless a new import is required.

## Verification

- `main.py` parses successfully.
- `get_identity`, `get_runtime_environment`, `add_numbers`, `TOOLS`, `_stream_model_response`, and `run_react_turn` exist.
- `get_identity()` includes `【解題方式】`, `write_file`, `exec`, `uv run python`, `【依賴管理】`, `uv add`, and `不要用 pip install`, but does not include environment-specific restrictions.
- `get_runtime_environment()` includes `【執行環境】`; on Windows it includes `Windows`, `【平台限制】`, `禁止使用 heredoc`, and `python - <<'PY'`.
- Pure arithmetic should use `add_numbers` instead of mental math.

## Return To Router

After WG-13 passes verification:

1. Report the completed WG briefly.
2. Ask exactly: `WG-13 已完成。要繼續下一題嗎？`
3. If the student says yes, return to `references/wg_milestone_checklist.md`, recompute `next_wg`, then read only the next routed card.
4. Do not preload future cards.
5. Do not continue automatically without explicit confirmation.

## Handoff Card

```text
mode: WG-13 direct-or-guided
allowed_files: main.py
source: starter_main_wg21.py WG-13 blocks, merged into current main.py
preserve: student nick/display name and existing WG-12 structure
must_include: get_identity, get_runtime_environment, TOOLS = [add_numbers], 解題方式, write_file, exec, uv run python, 依賴管理, uv add, no pip install, runtime 執行環境, Windows runtime heredoc restriction
forbidden: file/shell tools, JSONL, token budget, agent_core.py
verify: required WG-13 symbols exist including TOOLS; get_identity contains standard WG-13 identity text; get_runtime_environment contains platform section; main.py parses
after_verify: ask "WG-13 已完成。要繼續下一題嗎？"; if yes, rescan and route; read only one next card
```
