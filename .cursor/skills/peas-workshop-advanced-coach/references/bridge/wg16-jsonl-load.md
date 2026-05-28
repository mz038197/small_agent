# WG-16: Load Session JSONL on Startup

## Goal

Restore conversation history from the JSONL session file when the CLI starts.

## Prerequisite

WG-15 is complete. JSONL writing exists and excludes system messages.

## Allowed Files

- `main.py`

## Forbidden

- Do not add token trimming.
- Do not add memory consolidation.
- Do not create `agent_core.py`.
- Do not crash on malformed JSONL rows.

## Required Changes

- Add `_row_to_message()` or equivalent parser.
- Add `load_session_jsonl(path)`.
- On startup, load persisted history and metadata if the file exists.
- Skip malformed rows with a warning rather than crashing.
- Continue writing new turns via WG-15 behavior.

## Preserve

- Student nick/persona.
- Existing JSONL schema and session file path.
- Existing ReAct/tool behavior.

## Verification

- `load_session_jsonl` and `_row_to_message` exist.
- Starting with no session file begins with empty history.
- Starting with an existing file restores history.
- Malformed rows do not crash the program.

## Return To Router

After WG-16 passes verification:

1. Report the completed WG briefly.
2. Ask exactly: `WG-16 已完成。要繼續下一題嗎？`
3. If the student says yes, return to `references/wg_milestone_checklist.md`, recompute `next_wg`, then read only the next routed card.
4. Do not preload future cards.
5. Do not continue automatically without explicit confirmation.

## Handoff Card

```text
mode: WG-16 direct-or-guided
allowed_files: main.py
source: starter_main_wg21.py WG-16 load helpers
preserve: nick, JSONL filename/schema, WG-15 save behavior
forbidden: token budget, memory, skills, agent_core.py
verify: load_session_jsonl exists; cold start restores history safely
after_verify: ask "WG-16 已完成。要繼續下一題嗎？"; if yes, rescan and route; read only one next card
```
