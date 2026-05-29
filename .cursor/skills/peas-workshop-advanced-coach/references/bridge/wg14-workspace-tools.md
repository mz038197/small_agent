# WG-14: Workspace File and Shell Tools

## Goal

Give the agent safe workspace tools for reading, writing, editing, listing files, and running commands.

## Prerequisite

WG-13 is complete: `run_react_turn`, `TOOLS`, and tool binding patterns are available or can be extended.

## Allowed Files

- `main.py`

## Forbidden

- Do not add JSONL persistence.
- Do not add memory consolidation or skills.
- Do not create `agent_core.py`.
- Do not loosen workspace path safety.

## Required Changes

- Add `WORKSPACE = Path.cwd().resolve()` or preserve the student's equivalent.
- Add `resolve_workspace_path()`.
- Add tools:
  - `read_file`
  - `write_file`
  - `edit_file`
  - `list_dir`
  - `exec` / `exec_workspace`
- Add an `exec_workspace` guard for Windows shell compatibility:
  - reject commands containing heredoc syntax such as `<<` or `python - <<'PY'` when running on Windows;
  - return a clear error telling the agent to use `write_file` to create a `.py` script, then run `uv run python <script.py>`.
- Decode captured process output with a UTF-8 / system encoding / CP950 fallback so Windows shell errors do not become mojibake.
- Add or update `TOOLS` so all WG-13 and WG-14 tools are included.
- Add `_run_bound_tool()` if missing.
- Ensure `run_react_turn()` can execute tool calls and return `ToolMessage` results.

## Preserve

- Existing `get_identity()` persona and nick.
- Existing `add_numbers` behavior.
- Student workspace constants if already safe.

## Verification

- `main.py` parses successfully.
- `resolve_workspace_path`, file tools, `exec_workspace`, `TOOLS`, and `_run_bound_tool` exist.
- Path resolution rejects attempts outside the workspace.
- On Windows, `exec_workspace("python - <<'PY'")` returns a clear heredoc error instead of passing the command to the shell.
- Windows shell output decoding uses fallback encodings to avoid mojibake where possible.

## Return To Router

After WG-14 passes verification:

1. Report the completed WG briefly.
2. Ask exactly: `WG-14 已完成。要繼續下一題嗎？`
3. If the student says yes, return to `references/wg_milestone_checklist.md`, recompute `next_wg`, then read only the next routed card.
4. Do not preload future cards.
5. Do not continue automatically without explicit confirmation.

## Handoff Card

```text
mode: WG-14 direct-or-guided
allowed_files: main.py
source: starter_main_wg21.py WG-14 blocks, merged into current main.py
preserve: nick, WG-13 ReAct loop, safe existing workspace paths
forbidden: JSONL, memory, skills, agent_core.py
verify: workspace tools exist; path safety preserved; heredoc guard exists; output decode fallback exists; main.py parses
after_verify: ask "WG-14 已完成。要繼續下一題嗎？"; if yes, rescan and route; read only one next card
```
