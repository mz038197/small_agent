# WG-19: Long-Term Memory Consolidation

## Goal

When the conversation exceeds the budget, consolidate old conversation chunks into long-term memory files and read that memory back into the system prompt.

## Prerequisite

WG-18 is complete. Model-message assembly and budget boundary logic exist.

## Allowed Files

- `main.py`
- Project assets may be copied if missing:
  - `prompts/memory_merge.md`
  - `templates/memory/MEMORY.md`

## Forbidden

- Do not overwrite existing `prompts/` or `templates/` files.
- Do not add SkillsLoader yet.
- Do not create `agent_core.py`.

## Required Changes

- Add memory path helpers and file helpers:
  - `read_memory_md`
  - `write_memory_md`
  - `append_history_log`
  - `load_memory_merge_prompt`
  - `is_default_memory_template`
- Add consolidation helpers such as `_consolidate_pack`.
- Add `memory_block_for_system()`.
- Add `ensure_budget_before_react()` and call it before each ReAct turn.
- Update `last_consolidated` after successful consolidation.
- Update `build_system_prompt()` so each turn reads `memory_block_for_system()` and appends the `## Long-term Memory` block when present.

## Preserve

- Existing budget and `messages_for_model` behavior.
- Student nick/persona.
- Existing project assets if present.

## Verification

- `ensure_budget_before_react`, `load_memory_merge_prompt`, and `read_memory_md` exist.
- Missing `prompts/` or `templates/` are copied from `project_assets` only if absent.
- `build_system_prompt()` includes `memory_block_for_system()` output when memory exists and is not the default template.
- Under budget, no consolidation is required.
- Over budget, consolidation can update memory and preserve a valid current turn.

## Return To Router

After WG-19 passes verification:

1. Report the completed WG briefly.
2. Ask exactly: `WG-19 已完成。要繼續下一題嗎？`
3. If the student says yes, return to `references/wg_milestone_checklist.md`, recompute `next_wg`, then read only the next routed card.
4. Do not preload future cards.
5. Do not continue automatically without explicit confirmation.

## Handoff Card

```text
mode: WG-19 direct-or-guided
allowed_files: main.py; missing project_assets targets only
source: starter_main_wg21.py WG-19 memory helpers and project_assets
preserve: nick, existing prompts/templates, budget logic
forbidden: overwrite project assets, skills, image handling, agent_core.py
verify: memory helpers exist; ensure_budget_before_react is called before ReAct; build_system_prompt reads memory_block_for_system
after_verify: ask "WG-19 已完成。要繼續下一題嗎？"; if yes, rescan and route; read only one next card
```
