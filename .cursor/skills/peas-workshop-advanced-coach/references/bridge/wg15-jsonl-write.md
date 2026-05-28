# WG-15: Write Conversation Turns to JSONL

## Goal

Persist each completed conversation turn to a JSONL session file without writing `SystemMessage`.

## Prerequisite

WG-14 is complete. The agent has a working ReAct loop and tools.

## Allowed Files

- `main.py`

## Forbidden

- Do not load old sessions yet; that belongs to WG-16.
- Do not add token trimming or memory consolidation.
- Do not create `agent_core.py`.
- Do not persist system prompt content.

## Required Changes

- Add metadata helpers such as `_default_metadata()`.
- Add serialization helpers:
  - `_serialize_tool_calls`
  - `_message_to_jsonl_line`
- Add `save_session_jsonl()`.
- Update `run_react_turn()` so it returns `final_text` plus the full `turn_messages` list, matching starter behavior:
  - assistant messages;
  - tool messages;
  - the history user placeholder / current user message as appropriate.
- After each completed turn, save:
  - first-line metadata if needed;
  - user message;
  - assistant/tool messages from the turn.
- Extend in-memory `history` with `turn_messages` after each turn.
- Keep system prompt generated at runtime, not written into JSONL.

## Preserve

- Existing tools and ReAct loop behavior.
- Student nick/persona.
- Existing session file name if the student already chose one safely.

## Verification

- `save_session_jsonl` and `_message_to_jsonl_line` exist.
- `run_react_turn()` returns `final_text, turn_messages` or an equivalent pair that preserves assistant/tool messages.
- Running a turn writes a JSONL file.
- The JSONL file does not include serialized `SystemMessage`.

## Return To Router

After WG-15 passes verification:

1. Report the completed WG briefly.
2. Ask exactly: `WG-15 已完成。要繼續下一題嗎？`
3. If the student says yes, return to `references/wg_milestone_checklist.md`, recompute `next_wg`, then read only the next routed card.
4. Do not preload future cards.
5. Do not continue automatically without explicit confirmation.

## Handoff Card

```text
mode: WG-15 direct-or-guided
allowed_files: main.py
source: starter_main_wg21.py WG-15 JSONL write helpers
preserve: nick, tools, ReAct loop, session filename if present
forbidden: load_session_jsonl, token budget, memory, agent_core.py
verify: JSONL write helpers exist; turn_messages are saved; system messages are not persisted
after_verify: ask "WG-15 已完成。要繼續下一題嗎？"; if yes, rescan and route; read only one next card
```
