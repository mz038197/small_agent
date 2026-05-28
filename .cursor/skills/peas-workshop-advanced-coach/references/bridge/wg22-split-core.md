# WG-22: Split Agent Core from CLI

## Goal

Move WG-12～21 execution logic from single-file `main.py` into `agent_core.py`, expose `class Agent`, and leave `main.py` as a thin CLI shell.

## Prerequisite

WG-21 is complete in project-root `main.py`.

## Allowed Files

- `agent_core.py`
- `main.py`

## Forbidden

- Do not offer the normal WG-13～21 direct/guided choice.
- Do not implement before contract alignment and six-column confirmation.
- Do not copy `reference_agent_core.py` or `reference_main.py` wholesale into the answer files.
- Do not rewrite ReAct/JSONL/memory logic from scratch.
- Do not leave `input()` in `agent_core.py`.
- Do not leave `run_react_turn`, `save_session_jsonl`, or `ensure_budget_before_react` in thin `main.py`.

## Student-Facing Flow

1. Show WG-22 progress and context: completed single-file agent, current single-file pain, goal of core/CLI split.
2. Ask one 2a question about expected user-facing behavior after the split.
3. Continue 2b～2d′ one question at a time.
4. Convert confirmed answers into the six-column contract.
5. Ask once whether to start implementation.
6. Implement only after the student explicitly says "開始實作" or equivalent.

## Required API

- `Agent.from_env()`
  - calls `load_dotenv()`;
  - checks `OPENAI_API_KEY`;
  - accepts optional `session_path`;
  - otherwise reads `os.getenv("SESSION_JSONL_PATH", "session.jsonl")`;
  - loads JSONL history;
  - creates `ChatOpenAI(model="gpt-5.4-mini", temperature=0.2)`;
  - binds `TOOLS`;
  - restores `last_consolidated`.
- `Agent.chat(user_text, *, image_path=None, on_token=None) -> str`
  - rejects absolute/out-of-project `image_path` through the existing WG-21 path resolver behavior;
  - runs memory budget/consolidation;
  - runs ReAct;
  - saves JSONL;
  - extends in-memory history;
  - returns final assistant text;
  - supports WG-21 image path;
  - supports optional `on_token` callback: assistant text tokens go to callback and are not printed a second time when callback is provided.

## Split Steps

| Step | Work | Verification before next step |
|---|---|---|
| 1 | Create `agent_core.py` and migrate WG-13～16 helpers from current `main.py`. | `python -c "import agent_core"` succeeds; WG-13～16 symbols exist in `agent_core.py`. |
| 2 | Migrate WG-17～21 helpers, including image helpers and memory/skills. | `run_react_turn`, `messages_for_model`, `ensure_budget_before_react`, `SkillsLoader`, and `build_human_message_for_current_turn` exist in `agent_core.py`. |
| 3 | Add `class Agent` with `from_env()` and `chat(...)`. | `python -c "from agent_core import Agent"` succeeds; `Agent.from_env` and `Agent.chat` exist with the required API. |
| 4 | Replace `main.py` with a thin CLI that catches `RuntimeError`, handles quit commands, parses `/image`, and calls `agent.chat(...)`. | `main.py` has no `def run_react_turn`, `def save_session_jsonl`, or `def ensure_budget_before_react`; `agent_core.py` has no `input(`. |
| 5 | Run final checklist. | `uv run main.py` starts; missing key is reported without traceback; behavior remains equivalent to WG-21 starter. |

## Preserve

- Student nick/persona and approved path choices.
- Existing session file behavior unless the contract says otherwise.
- CLI user experience from the WG-21 single-file version.

## Verification

- `from agent_core import Agent` works.
- `Agent.from_env()` uses `load_dotenv`, `OPENAI_API_KEY`, `SESSION_JSONL_PATH` defaulting to `session.jsonl`, `gpt-5.4-mini`, and `TOOLS`.
- `Agent.chat(...)` returns final text and supports `image_path` plus `on_token`.
- With `on_token` provided, assistant text tokens are emitted through the callback and not printed a second time.
- `agent_core.py` has no `input(`.
- `main.py` has no `def run_react_turn`, `def save_session_jsonl`, or `def ensure_budget_before_react`.
- `main.py` calls `agent.chat(...)` for each turn.
- `uv run main.py` starts; missing key is reported without traceback.
- Tool calls, JSONL load/save, memory consolidation, skills, and `/image` behavior remain equivalent to WG-21.

## Return To Router

After WG-22 passes verification:

1. Report the completed WG briefly.
2. Ask exactly: `WG-22 已完成。要繼續下一題嗎？`
3. If the student says yes, return to `references/wg_milestone_checklist.md`, recompute `next_wg`, then read only the next routed card.
4. Do not preload future cards.
5. Do not continue automatically without explicit confirmation.

## Handoff Card

```text
mode: WG-22 contract-first split
allowed_files: agent_core.py, main.py
source: current WG-21 main.py / starter_main_wg21.py behavior as logic source; reference_agent_core.py/reference_main.py as structural checks only
preserve: nick, persona, session path choices, CLI behavior
forbidden: direct implementation before contract, wholesale reference copy, rewriting core logic, input() in core, alternate model name
verify: Agent API exists; gpt-5.4-mini; SESSION_JSONL_PATH default session.jsonl; on_token behavior; thin main; no core loop in main; uv run main.py smoke test
after_verify: ask "WG-22 已完成。要繼續下一題嗎？"; if yes, rescan and route; read only one next card
```
