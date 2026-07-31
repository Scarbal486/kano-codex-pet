# Production Log

## Inputs

Status: Production run prepared

- Upstream repository: `https://github.com/legeling/awesome-codex-pet`
- Pinned commit: `f303c7bf3c620807ddd3f20277f5aa09232c2b73`
- Skill path: `.agents/skills/hatch-pet-v2`
- Local staged skill: `work/upstream/hatch-pet-v2`
- Python: `C:\Users\W\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe`
- Retrieval: Git clone over HTTP/1.1 could not reach `github.com:443`; the same pinned tree was fetched through the authenticated GitHub API.
- Upstream tests: 28 tests passed with `-X utf8` on 2026-07-31. The UTF-8 mode is required because the Windows default encoding is CP936.
- Run directory: `work/runs/kano--scarbal486-v2`
- Atlas contract: 8 columns x 11 rows, 192 x 208 cells, 1536 x 2288 final size.
- Selected chroma key: `#00FF00`
- Selected local references: `微笑.gif`, `早上好.gif`, `这就去.gif`, `阿里嘎多.gif`, `我看不懂.gif`, `拜托了.gif`, `打游戏中.gif`, `原来如此.gif`, `好气啊.gif`, `发光.gif`
- Prepared visual jobs: canonical base, nine standard rows, four-cardinal anchors, look row 9, and look row 10. Only the canonical base is initially ready.

## Canonical model

Status: Approved

- Approved candidate: A, confirmed by the user on 2026-07-31.
- Source bytes: `work/runs/kano--scarbal486-v2/decoded/base-built-in.png`
- Canonical runtime copy: `work/runs/kano--scarbal486-v2/decoded/base.png`
- Canonical reference copy: `work/runs/kano--scarbal486-v2/references/canonical-base.png`
- Repository model sheet: `assets/model-sheet.png`
- QA: identity, bow side, antlers, scarf, dotted green clothing, deep-blue eyes, and 192 x 208 readability reviewed and approved. Background variation remains assigned to the deterministic chroma pipeline.

## Standard rows

Status: All nine standard rows approved

- User-approved processing rule: a selected multi-pose grid may be reordered deterministically in reading order when every pose comes from the same generation. Reordering does not redraw, mirror, rescale, or mix candidates.
- `idle`: 6 frames from `decoded/idle-shoubanhua-wide-v2.png`; final strip `decoded/idle.png`; `components` extraction; zero QA errors or warnings.
- `running-right`: 8 frames from `decoded/running-right-shoubanhua-wide-v2.png`; deterministically reordered to `decoded/running-right.png`; `components` extraction; zero QA errors or warnings; all frame hashes are distinct.
- `running-left`: 8 frames from `decoded/running-left-built-in-grid.png`; deterministically reordered to `decoded/running-left.png`; generated independently and never mirrored; `components` extraction; zero QA errors or warnings; all frame hashes are distinct.
- `waving`: 4 frames from `decoded/waving-built-in.png`; final strip `decoded/waving.png`; `components` extraction; zero QA errors or warnings.
- `jumping`: 5 frames from `decoded/jumping-built-in.png`; final strip `decoded/jumping.png`; `stable-slots` extraction intentionally preserves the generated jump height. Manual review confirmed the crouch, ascent, apex, descent, and landing remain stable and unclipped.
- Built-in image results for `running-left`, `waving`, and `jumping` were decoded directly from the `payload.result` Base64 bytes in `C:\Users\W\.codex\sessions\2026\07\31\rollout-2026-07-31T14-40-24-019fb6e7-1377-73e3-8bc3-5f30cbbf6bee.jsonl`; no screenshot reconstruction was used.
- Rejected candidates remain only in the ignored run directory. In particular, the first two Shoubanhua left-running grids were rejected for wrong-direction poses, missing frames, and overlap.
- Approved previews: `assets/previews/idle.gif`, `running-right.gif`, `running-left.gif`, `waving.gif`, and `jumping.gif`.
- `failed`: 8 frames from `decoded/failed-built-in.png`; confusion, attached tears, drooping posture, and a deflated crouch; `components` extraction; zero QA errors or warnings.
- `waiting`: 6 frames from `decoded/waiting-built-in.png`; hands-together asking motion and expectant gaze remain distinct from idle; `components` extraction; zero QA errors or warnings.
- `running`: 6 frames from `decoded/running-built-in.png`; seated active-task loop with one consistent pink handheld device and no locomotion; `components` extraction; zero QA errors or warnings.
- `review`: 6 frames from `decoded/review-built-in.png`; forward lean, side-to-side gaze, narrowed eyes, head tilt, and understanding reset without added props; `components` extraction; zero QA errors or warnings.
- The four Task 6 built-in results were decoded directly from `payload.result` Base64 at JSONL lines 2502, 2541, 2561, and 2582 respectively. All four first-pass rows passed, so the Shoubanhua fallback was not used.
- Additional approved previews: `assets/previews/failed.gif`, `waiting.gif`, `running.gif`, and `review.gif`.
- Combined standard-row QA: all nine rows were extracted together and inspected with zero errors. Eight rows use component extraction; `jumping` uses the approved stable-slot override to preserve vertical travel and retains one expected warning.
- Intermediate atlas: 1536 x 1872 RGBA WebP at `work/runs/kano--scarbal486-v2/final/spritesheet.webp`. It is QA-only and is not copied to `dist/`.
- Contact-sheet verdict: all frame counts, directions, state semantics, identity traits, safe padding, scale continuity, and animation loops passed manual review. The final combined-run previews replace the earlier incremental copies under `assets/previews/`.

## Look directions

Status: Not started

## Validation

Status: Not started

## Runtime smoke test

Status: Not started

## Release

Status: Not started
