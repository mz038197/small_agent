# WG-18: Messages Sent to the Model

## Goal

Repair and centralize the transcript sent to the model so loaded history, trimmed past messages, and current-turn messages are assembled consistently.

## Prerequisite

WG-17 is complete. Budget helpers and boundary tracking exist.

## Allowed Files

- `main.py`

## Forbidden

- Do not add long-term memory consolidation yet.
- Do not add image handling yet.
- Do not create `agent_core.py`.

## Required Changes

- Add `messages_for_model()` or equivalent central adapter.
- Add `_known_tool_call_ids()` or equivalent helper to identify valid tool call IDs before each position.
- Ensure tool-call/tool-result pairing remains valid:
  - remove orphan `ToolMessage` entries whose `tool_call_id` has no prior assistant tool call;
  - preserve matching assistant tool calls and tool results;
  - do not mutate the original `history` / JSONL-bound list in place.
- Ensure `run_react_turn()` uses the central adapter when sending messages.
- Preserve current user turn plus selected past context.

## Preserve

- Existing ReAct loop.
- Existing JSONL load/save.
- Student nick/persona.

## Verification

- `messages_for_model` exists.
- `_known_tool_call_ids` or equivalent tool-call ID tracking exists.
- Model input excludes invalid tool result leftovers.
- The adapter returns a new list or safe copy; it does not corrupt the persisted history.
- ReAct tool calls still work after the adapter is introduced.

## Return To Router

After WG-18 passes verification:

1. Report the completed WG briefly.
2. Ask exactly: `WG-18 已完成。要繼續下一題嗎？`
3. If the student says yes, return to `references/wg_milestone_checklist.md`, recompute `next_wg`, then read only the next routed card.
4. Do not preload future cards.
5. Do not continue automatically without explicit confirmation.

## Handoff Card

```text
mode: WG-18 direct-or-guided
allowed_files: main.py
source: starter_main_wg21.py WG-18 model-message adapter
preserve: nick, JSONL, budget helpers, ReAct loop
forbidden: memory consolidation, skills, image handling, agent_core.py
verify: messages_for_model and tool-call ID repair exist; adapter does not mutate JSONL history
after_verify: ask "WG-18 已完成。要繼續下一題嗎？"; if yes, rescan and route; read only one next card
```
