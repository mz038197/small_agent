# Bridge Cards Index

Use this file after `readiness_scan` determines the next unfinished workshop challenge.

## Routing

| next_wg | Card | Default mode |
|---|---|---|
| 13 | `wg13-react-tools.md` | Ask: direct implementation or guided clarification |
| 14 | `wg14-workspace-tools.md` | Ask: direct implementation or guided clarification |
| 15 | `wg15-jsonl-write.md` | Ask: direct implementation or guided clarification |
| 16 | `wg16-jsonl-load.md` | Ask: direct implementation or guided clarification |
| 17 | `wg17-budget-trim.md` | Ask: direct implementation or guided clarification |
| 18 | `wg18-messages-for-model.md` | Ask: direct implementation or guided clarification |
| 19 | `wg19-memory-merge.md` | Ask: direct implementation or guided clarification |
| 20 | `wg20-skills.md` | Ask: direct implementation or guided clarification |
| 21 | `wg21-image.md` | Ask: direct implementation or guided clarification |
| 22 | `wg22-split-core.md` | Contract-first flow; do not offer normal direct implementation |

## Universal Bridge Rules

- Read only the card for the current `next_wg` before implementation.
- WG-13 through WG-21 modify only project-root `main.py`.
- WG-22 may modify only project-root `agent_core.py` and `main.py`.
- Preserve student-owned values: nick/display name, persona wording, comments, and local path choices unless they conflict with the current card.
- Do not implement future WG requirements. Finish and verify the current WG first, then ask whether to continue.
- Before any file edit, form the card's handoff card internally and obey its allowed files, forbidden changes, and verification items.

## Student-Facing Choice

For WG-13 through WG-21, ask one concise choice:

```text
下一題是 WG-XX：<title>。
你想怎麼進行？
1. 直接實作：老師已講完，我依這題規格改 main.py 並驗收。
2. 先引導：我先用幾個問題幫你整理規格，再實作。
```

For WG-22, use the WG-22 card. It must start with contract alignment rather than the normal direct/guided choice.
