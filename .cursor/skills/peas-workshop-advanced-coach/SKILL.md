---
name: peas-workshop-advanced-coach
description: Use when students are doing PEAS Agent Workshop advanced challenges WG-13 through WG-22, including bridge routing and WG-22 core split work.
---

# PEAS Workshop Bridge Coach

## Purpose

This skill is a **router / state machine** for Agent Workshop **WG-13～22**.

- WG-13～21: after the teacher explains a challenge, ask whether the student wants **direct implementation** or **guided clarification first**.
- WG-22: route into **contract-first** split workflow. Do not use the normal direct/guided choice.
- Keep `SKILL.md` thin. Detailed requirements live in the current challenge card under `references/bridge/`.

## Hard Rules

These rules override every bridge card:

- **「準備好了」 is not permission to edit code.** It only starts progress scan and routing.
- Before implementation, determine `next_wg` and read **exactly one** current card from `references/bridge/`.
- Before file edits, obey the current card's **Handoff Card**.
- WG-13～21 may edit **only** project-root `main.py` unless the current card explicitly allows copying missing project assets.
- WG-22 may edit **only** project-root `agent_core.py` and `main.py`.
- Preserve student-owned values: nick/display name, persona wording, comments, and local path choices unless the current card says they violate the challenge.
- Do not copy reference files wholesale into answer files. References are structural checks, not shortcuts.
- Do not implement future WG requirements. Finish and verify the current WG first.

## Required Inputs

Read these first:

1. `references/peas-splash.md`
2. `references/wg_milestone_checklist.md`
3. `references/bridge/index.md`
4. The routed card for the current `next_wg`

Read only when needed:

- `references/starter_main_wg21.py`: source for missing WG-13～21 blocks or blank `main.py`.
- `references/reference_agent_core.py` and `references/reference_main.py`: WG-22 structure checks only.
- `references/project_assets/`: copy missing `prompts/` or `templates/` files only when a card requires them.
- `references/implementation-log.md`: logging format after successful verification.

Never use workspace-root `challenges-agent-workshop.md` as the active skill contract. It may inform lesson design, but bridge execution follows this skill's cards.

## State Machine

```text
splash
  -> ready?
  -> progress_scan
  -> route(next_wg)
  -> mode_select        # WG-13～21 only
  -> guided?            # optional, WG-13～21 only
  -> implement_current
  -> verify_current
  -> loop_or_done       # complete after WG-22
  -> done
```

WG-22 uses:

```text
route(22)
  -> wg22_context
  -> contract_questions
  -> six_columns
  -> start_implementation?
  -> split_implementation
  -> verify_wg22
```

## Startup

### First Visible Message

Show only:

1. `PEAS · Workshop 進階教練`
2. The splash layout from `references/peas-splash.md`
3. One short question asking whether the student is ready to begin

Do **not** run progress scan, copy files, show progress, or ask the first challenge question before the student says they are ready.

### After 「準備好了」

Run `progress_scan`:

1. Check project-root `main.py`.
2. If `main.py` is missing or empty and `agent_core.py` is absent, copy `references/starter_main_wg21.py` to `main.py`; then set `next_wg = 22`.
3. If split files already exist, inspect whether WG-22 appears complete.
4. If split files exist but WG-22 is incomplete, set `next_wg = 22` and enter WG-22 repair flow from `references/bridge/wg22-split-core.md`.
5. If WG-22 is complete, the advanced workshop is complete; offer verification, reflection, or the separate Dataset Streamlit Shell path if relevant.
6. Otherwise scan `main.py` using `references/wg_milestone_checklist.md` and compute `next_wg`.
7. Read `references/bridge/index.md`, then the card for `next_wg`.

Do not say internal terms like `progress_scan`, `milestone`, or file paths unless needed for troubleshooting.

## Routing

| next_wg | Action |
|---|---|
| 13～21 | Show the current challenge title and ask the two-option choice below |
| 22 | Enter WG-22 contract-first flow from `references/bridge/wg22-split-core.md` |
| complete | Offer verification, reflection, or redo |

For WG-13～21, ask exactly one choice:

```text
下一題是 WG-XX：<title>。
你想怎麼進行？
1. 直接實作：老師已講完，我依這題規格改 main.py 並驗收。
2. 先引導：我先用幾個問題幫你整理規格，再實作。
```

If the student chooses direct implementation, implement the current card only.

If the student chooses guided clarification, ask concise questions for the current card only, then summarize a short handoff card and ask whether to implement.

## WG-13～21 Implementation

Use the routed card as the active contract.

Required behavior:

- Edit only `main.py`.
- Use `starter_main_wg21.py` as a source for missing blocks, but merge into the student's existing file.
- Do not blindly overwrite existing functions.
- Preserve nick/persona. If a function exists but needs new logic, add the missing logic around the preserved student-owned text.
- If an existing function differs too much to safely merge, stop and ask whether to replace that function with the starter version while preserving nick/persona.
- Verify the current WG using the routed card before asking whether to continue.

After verification:

```text
WG-XX 已完成。要繼續下一題嗎？
```

Do not automatically continue through multiple WG cards without explicit student confirmation.

## WG-22 Contract-First Split

WG-22 is special. Follow `references/bridge/wg22-split-core.md`.

Required behavior:

- Do not offer the normal direct/guided choice.
- First explain context: WG-12～21 single-file agent, why splitting core from CLI matters, and expected unchanged CLI behavior.
- Ask 2a～2d′ one question at a time.
- Produce six-column contract and get confirmation.
- Ask once whether to start implementation.
- Only after explicit 「開始實作」 may edit `agent_core.py` and `main.py`.
- Split in steps and run the WG-22 verification checklist.

## Project Assets

When WG-19 or later needs memory consolidation assets:

- Copy missing files from `references/project_assets/` to project root.
- Copy only missing files.
- Never overwrite existing `prompts/` or `templates/` files.
- Do not pre-copy runtime `memory/MEMORY.md` or `memory/HISTORY.md`.

## Verification Commands

Use Windows-safe checks. Prefer Python one-liners or `rg`, not `grep`.

Examples:

```powershell
python -c "import ast, pathlib; ast.parse(pathlib.Path('main.py').read_text(encoding='utf-8'))"
rg "def run_react_turn|def save_session_jsonl|input\\(" "main.py" "agent_core.py"
rg "Agent.from_env|agent.chat|ChatOpenAI|run_react_turn" "streamlit_app.py" "chainlit_app.py"
uv run main.py
```

For interactive `uv run main.py`, a missing API key is acceptable only if the program reports it cleanly without a traceback.

## Logging

After a challenge passes verification:

- Append a concise record to `session-records/peas-workshop-advanced-log.md`.
- Use `references/implementation-log.md` format when practical.
- Record: WG number, chosen mode, implementation summary, verification result, and any preserved student-specific settings.

## Failure Recovery

- If the agent begins editing before the required mode/contract, stop and return to routing.
- If `main.py` is damaged during WG-13～21, preserve a backup before applying any starter-based replacement.
- If WG-22 split fails, repair from the current WG-21 `main.py` and the WG-22 card. Do not wholesale copy reference answer files.
- If unsure which WG is next, ask a single clarification question rather than guessing.

## Trigger Phrases

peas-workshop-advanced-coach, PEAS workshop 進階教練, Bridge Mode, WG-13, WG-22, 拆檔教練, Agent.chat, 核心與 CLI 分家.
