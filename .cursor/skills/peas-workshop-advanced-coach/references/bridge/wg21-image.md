# WG-21: Image Input and JSONL Image Path

## Goal

Support one image attachment per current user turn, store only its relative `image_path` in JSONL, and rebuild loaded history without re-sending old images.

## Prerequisite

WG-20 is complete. Skills and memory are integrated into the system prompt.

## Allowed Files

- `main.py`

## Forbidden

- Do not create `agent_core.py`.
- Do not store base64 image data in JSONL.
- Do not re-send historical images to the model.
- Do not accept absolute image paths.

## Required Changes

- Add `PROJECT_ROOT`.
- Add image helpers:
  - `guess_media_type`
  - `image_bytes_to_data_url`
  - `resolve_project_image_path`
- Add history/user helpers:
  - `history_human_placeholder`
  - `human_fields_for_jsonl`
  - `load_user_row_to_history_human`
  - `build_human_message_for_current_turn`
- Add model-send helpers for images:
  - `_human_text_length`
  - `_human_to_text_only_for_model`
  - `_keep_image_only_on_current_human`
- Update JSONL serialization/loading so user rows can store `image_path`.
- Update CLI `main()` with `/image` and `pending_image` behavior.

## Preserve

- Student nick/persona.
- Existing JSONL schema fields; only extend as needed.
- Existing tools, memory, and skills behavior.

## Verification

- `resolve_project_image_path` and `build_human_message_for_current_turn` exist.
- `/image relative/path.png` selects an image for the next text turn.
- `/image path question` sends image + text in one turn.
- JSONL stores relative `image_path`, not base64.
- Loaded history uses placeholders/text only; only current turn includes image content.

## Return To Router

After WG-21 passes verification:

1. Report the completed WG briefly.
2. Ask exactly: `WG-21 已完成。要繼續下一題嗎？`
3. If the student says yes, return to `references/wg_milestone_checklist.md`, recompute `next_wg`, then read only the next routed card.
4. Do not preload future cards.
5. Do not continue automatically without explicit confirmation.

## Handoff Card

```text
mode: WG-21 direct-or-guided
allowed_files: main.py
source: starter_main_wg21.py WG-21 image helpers and CLI parsing
preserve: nick, JSONL history, memory, skills, session path
forbidden: agent_core.py, absolute paths, base64 in JSONL, historical image re-send
verify: image helpers exist; /image CLI works; JSONL stores image_path only
after_verify: ask "WG-21 已完成。要繼續下一題嗎？"; if yes, rescan and route; read only one next card
```
