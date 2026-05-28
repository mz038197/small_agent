# WG-20: SkillsLoader and System Prompt Injection

## Goal

Load local skill cards and inject an active skills summary into the system prompt.

## Prerequisite

WG-19 is complete. Long-term memory can be read and injected.

## Allowed Files

- `main.py`

## Forbidden

- Do not add image handling.
- Do not create `agent_core.py`.
- Do not replace the student's persona or nick.

## Required Changes

- Add `SkillEntry`.
- Add `split_frontmatter()`.
- Add `SkillsLoader`.
- Add `build_skills_summary()`.
- Add `SKILLS_LOADER = SkillsLoader(WORKSPACE)` or equivalent.
- Update `build_system_prompt()` so it combines:
  - `get_identity()`;
  - long-term memory block;
  - active skill bodies under `# Active Skills`;
  - available skills summary from `build_skills_summary()`.

## Preserve

- Student nick/persona from `get_identity()`.
- Existing long-term memory injection.
- Existing tools and ReAct loop.

## Verification

- `SkillsLoader`, `SKILLS_LOADER`, and `build_system_prompt` exist.
- System prompt still includes the student's identity.
- `build_system_prompt()` actually includes active skills and available skills summary when skills are present.
- Missing or empty skills directories should return an empty list/summary instead of crashing.
- Missing skills directory should not crash the agent.

## Return To Router

After WG-20 passes verification:

1. Report the completed WG briefly.
2. Ask exactly: `WG-20 已完成。要繼續下一題嗎？`
3. If the student says yes, return to `references/wg_milestone_checklist.md`, recompute `next_wg`, then read only the next routed card.
4. Do not preload future cards.
5. Do not continue automatically without explicit confirmation.

## Handoff Card

```text
mode: WG-20 direct-or-guided
allowed_files: main.py
source: starter_main_wg21.py WG-20 SkillsLoader and system prompt blocks
preserve: nick, persona text, memory block, existing tools
forbidden: image handling, agent_core.py, replacing get_identity wholesale
verify: SkillsLoader loads safely; build_system_prompt includes identity + memory + active skills + skills summary
after_verify: ask "WG-20 已完成。要繼續下一題嗎？"; if yes, rescan and route; read only one next card
```
