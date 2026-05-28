# WG-17: Token Budget and Consolidation Boundary

## Goal

Estimate message cost with character length and decide which old conversation chunk can be trimmed when the prompt is too large.

## Prerequisite

WG-16 is complete. The program can load and save session JSONL.

## Allowed Files

- `main.py`

## Forbidden

- Do not perform long-term memory consolidation yet; that belongs to WG-19.
- Do not rewrite JSONL schema.
- Do not create `agent_core.py`.

## Required Changes

- Add `get_token_budget()`.
- Add `estimate_message_tokens()`.
- Add `message_cost()`.
- Add `pick_consolidation_boundary()`.
- Track `last_consolidated` or equivalent boundary state.
- Use the budget decision to identify old messages that can be excluded from `past`.

## Preserve

- Existing JSONL behavior.
- Student nick/persona.
- Current tool and ReAct behavior.

## Verification

- Required WG-17 functions exist.
- Boundary selection never cuts through invalid tool-call pairs.
- When under budget, history is sent normally.
- When over budget, old eligible messages can be excluded from the current model input.

## Return To Router

After WG-17 passes verification:

1. Report the completed WG briefly.
2. Ask exactly: `WG-17 已完成。要繼續下一題嗎？`
3. If the student says yes, return to `references/wg_milestone_checklist.md`, recompute `next_wg`, then read only the next routed card.
4. Do not preload future cards.
5. Do not continue automatically without explicit confirmation.

## Handoff Card

```text
mode: WG-17 direct-or-guided
allowed_files: main.py
source: starter_main_wg21.py WG-17 budget helpers
preserve: nick, JSONL behavior, ReAct/tool flow
forbidden: memory consolidation, skills, image handling, agent_core.py
verify: budget helpers exist; boundary logic is safe around tool messages
after_verify: ask "WG-17 已完成。要繼續下一題嗎？"; if yes, rescan and route; read only one next card
```
