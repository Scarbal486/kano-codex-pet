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

Status: Approved

- The user approved the four cardinal anchors and the final coherent 16-direction candidate on 2026-08-01.
- Approved source: `work/runs/kano--scarbal486-v2/decoded/look-directions-16-built-in-edit-v2.png`.
- Both complete 8-pose rows came from the same 2 x 8 generation. The rows were split only at the pure-green separator and registered at scale `0.6`; no cell patching, mirroring, candidate mixing, or post-generation enlargement was used.
- Row 9 contains `000` through `157.5`; row 10 contains `180` through `337.5`, in clockwise 22.5-degree increments.
- Automatic continuity QA reports `ok: true` and `reviewRequired: true`. The user reviewed and accepted the labeled QA sheet and the 10 FPS loop; `reviewRequired` is retained as an automatic warning, not rewritten as an automatic pass.
- The critical row boundary `157.5 -> 180` measures 2560 differing pixels, 0.71 px center shift, and 1.042 area ratio. The loop boundary `337.5 -> 000` measures 2821 differing pixels, 4.47 px center shift, and 1.111 area ratio.
- Alpha-hole warnings were visually reviewed as the natural gaps around the forked antlers and hair contours, with no visible torso or costume hole.
- Repository QA outputs: `assets/look-directions.png` and `assets/previews/look-directions.gif`.
- Formal jobs `look-cardinals`, `look-row-9`, and `look-row-10` are marked `complete` in the ignored production manifest.

## Validation

Status: Passed

- The single authorized chroma-despill pass completed with `ok: true`, preserved alpha, changed 130752 pixels, and rejected 0 pixels. No second despill pass was run.
- Final package atlas: `dist/spritesheet.webp`, lossless animated WebP RGBA, 1536 x 2288, 8 columns x 11 rows, 192 x 208 cells, Codex Pet v2. The file is 2550320 bytes and contains 6 animation frames, each with a 100 ms duration, at 10 FPS with infinite loop value `0`.
- Deterministic animation validation passed with 0 errors, 0 warnings, and 0 transparent-RGB residue pixels. At animation phase `p`, idle columns 0 through 5 all decode to approved idle source cell `p`; neutral and unused cells and every non-idle row remain pixel-identical to the approved static atlas.
- All six decoded phases independently passed `validate_atlas.py --require-v2`: each is 1536 x 2288 with 0 errors, 0 warnings, and 0 transparent-RGB residue pixels.
- Manifest: `dist/pet.json`; validation report: `dist/validation.json`; final visual audit sheet: `assets/contact-sheet.png`.
- SHA-256 `dist/pet.json`: `CBCEDA7DDE77A114440C5CE572CEAFEF1E822E84C18C12A422642BEA77C2F686`.
- SHA-256 `dist/spritesheet.webp`: `0E4D65565AD672FAA9D91262E4BE3A9B11524EE4F31AFF9FE1C17DB9E79F5296`.
- SHA-256 `dist/validation.json`: `BB1F32D503A62AB808DC27E77DCE3CB2130BDF815E1B6ECA0AA1AD243ABE8F13`.

## Runtime smoke test

Status: Selection, load, render, idle-loop, and caret-driven look checks passed; exhaustive live state sweep not performed

- Installed to `C:\Users\W\.codex\pets\kano--scarbal486` on 2026-08-01. Installed `pet.json` and `spritesheet.webp` hashes exactly match `dist/`.
- Tested application: Codex `26.721.11231.0` on Windows.
- Settings -> Pets discovered `鹿乃 / Kano` without an application restart. The custom preview was nonblank, correctly scaled, and free of an opaque green background.
- `鹿乃 / Kano` was selected successfully; the built-in `Codex` entry returned to an available state. Invoking `Wake pet` created a visible 408 x 400 Codex auxiliary window.
- Runtime accessibility identified the rendered node as `鹿乃 / Kano 宠物` with a 113 x 122 on-screen bound, matching the configured 112 px mascot width. The rendered character was complete, not clipped, and had no pure-green pixels.
- A 5.318-second runtime sample at approximately 10 Hz captured 50 window frames, 5 distinct pet frames, and 4 idle transitions. The observed transition intervals match Codex's fixed idle pacing.
- Codex `26.721.11231.0` deliberately multiplies the idle-row dwell times by 6: `[1680, 660, 660, 840, 840, 1920] ms`. The slow idle impression is therefore host playback policy, not missing atlas frames or the 10 FPS direction-review GIF.
- After unlocking Windows, a 16-point ordinary-mouse ring around the pet left the renderer on idle frames. Current Codex runtime code confirms that this is the expected input model: ordinary overlay pointer events drive drag and interaction behavior, while look frames consume `avatar-overlay-computer-use-cursor-changed` or a notification reply editor's `caretPoint`.
- Merely opening an empty reply editor initializes `caretPoint` to `null`; the first capture from that state matched `idle-0`, so it is retained as a negative control rather than look evidence.
- With the reply draft still empty, an `End` selection event caused the editor's `onSelect` path to publish a caret point. A fresh 113 x 122 capture then matched look direction `315` from final atlas row 10, column 6: on 4,413 high-alpha pixels, RGB MAE was `5.359`, median absolute channel error was `0`, and the 90th percentile was `9`. The runner-up `337.5` measured MAE `28.143`; the best idle frame measured MAE `48.959`.
- The reply editor was closed immediately after capture, its toggle returned to `Off`, and no text was entered or submitted. This proves the installed package responds through one formal caret-look path; it does not claim that all 16 directions were individually triggered in computer-use mode or that every non-idle state was swept live.
- Ignored evidence remains under `work/runs/kano--scarbal486-v2/qa/`, including settings, pet-window, frame-sampling, runtime-code, unlocked ordinary-mouse, and caret-look captures. The machine-readable caret result is `runtime-look-unlocked/runtime-look-input-qa.json`.

### Smooth idle follow-up

Status: 10 FPS idle playback and animated-package caret look passed on 2026-08-02

- Root cause: Codex `26.721.11231.0` multiplies the six host idle durations by 6, producing `[1680, 660, 660, 840, 840, 1920] ms`. `pet.json` has no timing field. The Kano-only animated atlas advances the approved idle art independently at 100 ms per phase without modifying Codex resources or another pet.
- Installed path: `C:\Users\W\.codex\pets\kano--scarbal486\spritesheet.webp`. Its SHA-256 equals `dist/spritesheet.webp` (`0E4D65565AD672FAA9D91262E4BE3A9B11524EE4F31AFF9FE1C17DB9E79F5296`); installed and packaged `pet.json` remain byte-identical at `CBCEDA7DDE77A114440C5CE572CEAFEF1E822E84C18C12A422642BEA77C2F686`.
- Primary runtime sample: 70 captures over 3445 ms at an average 49.928 ms sampling interval. All six phases appeared in strict sequential order across 34 transitions. Complete measured dwell intervals were 92-114 ms, with 100.061 ms mean and 100 ms median. Best-match RGB MAE was 6.072-7.274 and no capture contained a pure-green pixel. No old 660-1920 ms stall occurred.
- Visual inspection of the six-phase runtime contact sheet found the antlers, head, cape, and feet complete and unclipped in every phase. The accessibility node remained 113 x 122 and the auxiliary Codex window remained 408 x 400.
- Reload persistence sample: after restoring the static A/B control, reinstalling the exact dynamic package, closing the pet window, refreshing Pets, and waking Kano again, 45 captures over 2198 ms contained all six phases in sequential order across 22 transitions. The measured dwell range was 47-154 ms under capture jitter, with 100.095 ms mean; no 660 ms stall or pure-green pixel appeared.
- A fresh dynamic-package caret test used UI Automation to toggle the current notification's reply editor `On`, verified its empty `Edit` control held keyboard focus, and sent one `End` selection event. The pre-event frame matched idle; all 19 post-event captures matched look direction `337.5` from final atlas row 10, column 7. The representative frame compared 4,379 high-alpha pixels at RGB MAE `6.152`, median absolute channel error `0`, and 90th percentile `11`; the best idle control measured MAE `56.106`, a 9.120x separation.
- The reply editor was closed immediately after the burst, its toggle returned to `Off`, its control disappeared, and draft length was `0` both before and after. No text was entered and no message was submitted. At capture time the installed atlas and manifest were byte-identical to `dist`, with SHA-256 `0E4D65565AD672FAA9D91262E4BE3A9B11524EE4F31AFF9FE1C17DB9E79F5296` and `CBCEDA7DDE77A114440C5CE572CEAFEF1E822E84C18C12A422642BEA77C2F686`.
- A post-look idle sample then captured 70 frames over 3459 ms with the reply toggle still `Off` and the pet node still 113 x 122. All six phases appeared in strict sequential order across 35 transitions; complete dwell intervals were 78-118 ms with a 99.912 ms mean. Best-match RGB MAE was 6.040-7.269, no 660 ms stall occurred, and all captures contained 0 pure-green pixels. Visual review of its six-phase contact sheet again found the character complete and unclipped.
- Ignored evidence is under `work/runs/kano--scarbal486-v2/qa/smooth-idle/runtime/`, including the static backup, primary, post-reload, and post-look timing captures, the six-phase runtime contact sheets, A/B caret controls, the fresh 20-frame dynamic live-look burst, `dynamic-live-look-qa.json`, and `idle-after-live-look-qa.json`.

## Release

Status: Not started
