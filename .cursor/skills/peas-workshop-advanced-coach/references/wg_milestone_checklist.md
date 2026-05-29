# Bridge Progress Scan: WG-12～22

Use this file to determine the next unfinished workshop challenge before routing to a bridge card.

## Scan Target

- Before WG-22 split: scan project-root `main.py`.
- After split starts or completes: scan `agent_core.py` for core symbols and `main.py` for thin CLI behavior.
- If `main.py` is missing or empty and `agent_core.py` is absent, the skill may copy `starter_main_wg21.py` to `main.py` and route to WG-22.

## How To Compute `next_wg`

1. Check rows in order.
2. A WG is complete when all required symbols / behaviors for that row are present.
3. `next_wg = first incomplete WG`.
4. If WG-13～21 are complete and no split is complete, `next_wg = 22`.
5. If WG-22 checks pass, the advanced workshop is complete; offer verification, reflection, or the separate Dataset Streamlit Shell path if relevant.

## Milestones

| WG | Title | Completion Signals |
|---|---|---|
| 12 | system/history separation | System prompt is built at runtime; history exists; serialized session does not depend on storing `SystemMessage` |
| 13 | tool calling and ReAct loop | `get_identity`, `add_numbers`, `_stream_model_response`, `run_react_turn` |
| 14 | workspace tools | `WORKSPACE`, `resolve_workspace_path`, `TOOLS`, `_run_bound_tool`, file tools, `exec_workspace` |
| 15 | JSONL write | `_message_to_jsonl_line`, `save_session_jsonl`; main loop writes after each turn |
| 16 | JSONL load | `_row_to_message`, `load_session_jsonl`; startup restores history when file exists |
| 17 | budget trimming | `get_token_budget`, `estimate_message_tokens`, `message_cost`, `pick_consolidation_boundary` |
| 18 | model transcript adapter | `messages_for_model` and safe model input repair for tool-call transcripts |
| 19 | memory consolidation | `read_memory_md`, `load_memory_merge_prompt`, `memory_block_for_system`, `ensure_budget_before_react` |
| 20 | SkillsLoader | `SkillEntry`, `SkillsLoader`, `SKILLS_LOADER`, `build_skills_summary`, `build_system_prompt` includes skills |
| 21 | image input | `PROJECT_ROOT`, `resolve_project_image_path`, `build_human_message_for_current_turn`, JSONL `image_path`, CLI `/image` or `pending_image` |
| 22 | core/CLI split | `agent_core.py` exports `Agent`; `Agent.from_env`; `Agent.chat`; `agent_core.py` has no `input(`; thin `main.py` calls `agent.chat` and has no core loop definitions |

## Preservation Rules

When a WG-13～21 card edits `main.py`:

- Preserve student nick / display name.
- Preserve persona wording unless the current WG requires a minimal addition.
- Preserve local path choices such as session filename when compatible.
- Do not overwrite whole existing functions when a small merge is enough.
- If a merge is ambiguous, ask before replacing a function with starter-derived content.

## Routing Examples

- Highest complete WG is 12 -> `next_wg = 13`, read `bridge/wg13-react-tools.md`.
- Highest complete WG is 20 -> `next_wg = 21`, read `bridge/wg21-image.md`.
- WG-21 complete and no `Agent` split -> `next_wg = 22`, read `bridge/wg22-split-core.md`.
- WG-22 complete -> offer verification, reflection, or the separate Dataset Streamlit Shell path.
