# Kano Codex Pet Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Produce, validate, install, and privately release a Codex Pet v2 package for 鹿乃 that matches the supplied single-frame sticker references and contains real animation in every runtime state.

**Architecture:** Keep the 32 source GIFs local and untracked. Use the pinned `hatch-pet-v2` scripts from `awesome-codex-pet` for run preparation, deterministic frame extraction, atlas assembly, previews, and validation; use reference-grounded `imagegen` for visual jobs and the user-authorized Shoubanhua path only for bounded full-row retries when identity or style fails. Commit only approved model art, QA media, documentation, and the two-file runtime package.

**Tech Stack:** PowerShell 7, bundled Python 3 with Pillow, Git/GitHub CLI, Codex built-in `imagegen`, optional AstrBot Shoubanhua generator, upstream `hatch-pet-v2` scripts pinned to `f303c7bf3c620807ddd3f20277f5aa09232c2b73`.

---

## File Map

- Create `README.md`: private project overview, install steps, previews, and non-official status.
- Create `NOTICE.md`: rights and attribution boundary without granting an unverified asset license.
- Create `config/pet-request.json`: stable pet identity and runtime manifest values.
- Create `config/hatch-pet-v2.lock.json`: pinned upstream repository, commit, and skill path.
- Create `docs/style-guide.md`: approved identity, palette, invariants, and forbidden drift.
- Create `docs/sources-and-rights.md`: source URLs, local-reference policy, and public-release gate.
- Create `docs/production-log.md`: selected references, chroma key, approved generation outputs, validation summary, and runtime smoke-test result.
- Create `assets/model-sheet.png`: approved canonical full-body identity reference.
- Create `assets/contact-sheet.png`: final 11-row contact sheet.
- Create `assets/look-directions.png`: final neutral plus 16-direction QA sheet.
- Create `assets/previews/*.gif`: approved state motion previews.
- Create `dist/pet.json`: Codex Pet v2 manifest.
- Create `dist/spritesheet.webp`: validated 1536×2288 v2 atlas.
- Create `dist/validation.json`: deterministic validation result copied from the production run.
- Use ignored `work/upstream/hatch-pet-v2/`: pinned upstream scripts, references, and tests.
- Use ignored `work/runs/kano--scarbal486-v2/`: prompts, generated row strips, decoded frames, intermediate atlases, and QA JSON.

## Fixed Runtime Values

```powershell
$python = 'C:\Users\W\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe'
$skill = (Join-Path $PWD 'work\upstream\hatch-pet-v2')
$run = (Join-Path $PWD 'work\runs\kano--scarbal486-v2')
$petInstall = (Join-Path $env:USERPROFILE '.codex\pets\kano--scarbal486')
```

The visual source files remain at the project root. Every root-level `*.gif`, `work/`, `.superpowers/`, and generated scratch directory must stay ignored.

### Task 1: Add Production Metadata And Rights Boundaries

**Files:**
- Create: `README.md`
- Create: `NOTICE.md`
- Create: `config/pet-request.json`
- Create: `config/hatch-pet-v2.lock.json`
- Create: `docs/style-guide.md`
- Create: `docs/sources-and-rights.md`
- Create: `docs/production-log.md`

- [ ] **Step 1: Write the stable pet request**

Create `config/pet-request.json` with exactly:

```json
{
  "id": "kano--scarbal486",
  "displayName": "鹿乃 / Kano",
  "description": "A fan-made Codex pet based on Kano's classic antler-girl avatar.",
  "spriteVersionNumber": 2,
  "spritesheetPath": "spritesheet.webp",
  "stylePreset": "sticker",
  "characterVersion": "Kano unmarked classic antler-girl avatar",
  "runtimePackage": ["pet.json", "spritesheet.webp"]
}
```

- [ ] **Step 2: Pin the upstream tooling**

Create `config/hatch-pet-v2.lock.json` with exactly:

```json
{
  "repository": "https://github.com/legeling/awesome-codex-pet",
  "commit": "f303c7bf3c620807ddd3f20277f5aa09232c2b73",
  "skillPath": ".agents/skills/hatch-pet-v2"
}
```

- [ ] **Step 3: Write the public-facing and rights documents**

`README.md` must contain these sections: `About`, `Preview`, `Install`, `Package`, `Development`, `Sources and rights`, and `Non-official project`. State that the repository is private during production and that installable files are under `dist/`.

`NOTICE.md` must contain this text:

```markdown
# Notice

This is an unofficial, fan-made Codex pet project. It is not affiliated with or endorsed by Kano, her management, OpenAI, or the creators and distributors of the reference stickers.

The original reference images are kept locally for private production and are not distributed in this repository. Character names, likenesses, and other third-party rights remain with their respective owners. No license to redistribute the character assets is granted until a separate source-and-rights review is completed.
```

`docs/sources-and-rights.md` must record the two Moegirl pages, the `awesome-codex-pet` repository, the local-only 32-image reference set, and the rule that public visibility or gallery submission requires a new rights review.

`docs/style-guide.md` must copy the approved identity, eight-color palette, required invariants, and full-row rejection rules from the design specification without adding another avatar era.

Initialize `docs/production-log.md` with the headings `Inputs`, `Canonical model`, `Standard rows`, `Look directions`, `Validation`, `Runtime smoke test`, and `Release`. Use `Not started` as explicit status text rather than an ambiguous blank.

- [ ] **Step 4: Verify metadata parses and references stay ignored**

Run:

```powershell
Get-Content -Raw 'config\pet-request.json' | ConvertFrom-Json | Format-List
Get-Content -Raw 'config\hatch-pet-v2.lock.json' | ConvertFrom-Json | Format-List
git status --short --ignored --untracked-files=all
```

Expected: both JSON files parse; all 32 root GIFs and `.superpowers/` appear with `!!`; no root GIF appears as staged or untracked.

- [ ] **Step 5: Commit the production metadata**

```powershell
git add README.md NOTICE.md config docs/style-guide.md docs/sources-and-rights.md docs/production-log.md
git commit -m "chore: scaffold Kano pet production metadata"
```

### Task 2: Stage And Verify The Pinned Hatch Tooling

**Files:**
- Use ignored: `work/upstream/hatch-pet-v2/**`
- Modify: `docs/production-log.md`

- [ ] **Step 1: Try the narrow Git checkout with HTTP/1.1**

Run:

```powershell
New-Item -ItemType Directory -Force 'work\upstream' | Out-Null
git -c http.version=HTTP/1.1 clone --filter=blob:none --sparse --no-checkout https://github.com/legeling/awesome-codex-pet.git 'work\upstream\awesome-codex-pet'
git -C 'work\upstream\awesome-codex-pet' sparse-checkout set '.agents/skills/hatch-pet-v2'
git -C 'work\upstream\awesome-codex-pet' checkout --detach f303c7bf3c620807ddd3f20277f5aa09232c2b73
Copy-Item -Recurse -Force 'work\upstream\awesome-codex-pet\.agents\skills\hatch-pet-v2' 'work\upstream\hatch-pet-v2'
```

Expected: `git -C work/upstream/awesome-codex-pet rev-parse HEAD` prints `f303c7bf3c620807ddd3f20277f5aa09232c2b73`.

- [ ] **Step 2: Use the API fallback only if the clone transport fails**

Run this PowerShell block after removing only the incomplete `work\upstream\awesome-codex-pet` directory and verifying that resolved path remains under `work\upstream`:

```powershell
$repo = 'legeling/awesome-codex-pet'
$ref = 'f303c7bf3c620807ddd3f20277f5aa09232c2b73'
$prefix = '.agents/skills/hatch-pet-v2/'
$target = (Join-Path $PWD 'work\upstream\hatch-pet-v2')
New-Item -ItemType Directory -Force $target | Out-Null
$tree = gh api "repos/$repo/git/trees/$ref`?recursive=1" | ConvertFrom-Json
foreach ($item in $tree.tree | Where-Object { $_.type -eq 'blob' -and $_.path.StartsWith($prefix) }) {
  $relative = $item.path.Substring($prefix.Length)
  $destination = Join-Path $target $relative
  New-Item -ItemType Directory -Force (Split-Path $destination) | Out-Null
  $content = gh api -H 'Accept: application/vnd.github.raw+json' "repos/$repo/contents/$($item.path)?ref=$ref"
  [System.IO.File]::WriteAllText($destination, ($content -join "`n") + "`n", [System.Text.UTF8Encoding]::new($false))
}
```

Expected: `work/upstream/hatch-pet-v2/scripts/validate_atlas.py`, `references/animation-rows.md`, and all upstream tests exist.

- [ ] **Step 3: Run the upstream test suite**

```powershell
& $python -m unittest discover -s "$skill\tests" -p 'test_*.py' -v
```

Expected: exit code 0 and the suite ends with `OK`. Do not continue with visual generation if the pinned tooling tests fail.

- [ ] **Step 4: Record the tool verification**

Update `docs/production-log.md` under `Inputs` with the pinned commit, exact Python path, and upstream test result.

```powershell
git add docs/production-log.md
git commit -m "chore: verify pinned hatch pet tooling"
```

### Task 3: Prepare The V2 Production Run

**Files:**
- Use ignored: `work/runs/kano--scarbal486-v2/**`
- Modify: `docs/production-log.md`

- [ ] **Step 1: Run the preparation script with representative references**

```powershell
& $python "$skill\scripts\prepare_pet_run.py" `
  --pet-name 'Kano' `
  --pet-id 'kano--scarbal486' `
  --display-name '鹿乃 / Kano' `
  --description 'A fan-made Codex pet based on Kano''s classic antler-girl avatar.' `
  --reference "$PWD\微笑.gif" `
  --reference "$PWD\早上好.gif" `
  --reference "$PWD\这就去.gif" `
  --reference "$PWD\阿里嘎多.gif" `
  --reference "$PWD\我看不懂.gif" `
  --reference "$PWD\拜托了.gif" `
  --reference "$PWD\打游戏中.gif" `
  --reference "$PWD\原来如此.gif" `
  --reference "$PWD\好气啊.gif" `
  --reference "$PWD\发光.gif" `
  --output-dir $run `
  --pet-notes 'Kano classic antler-girl: rounded brown bob with straight bangs, small cream antlers, coral bow fixed on her right side, red scarf, green dress with white dots, cream undershirt, large deep-blue eyes, warm cute healing personality with slight playful mischief.' `
  --style-preset 'sticker' `
  --style-notes 'Match the supplied 300x300 sticker drawings exactly: rounded blue-violet outline, flat colors, minimal soft shading, oversized head, tiny body, no pixel art, no 3D, no painterly texture, no realistic anatomy.' `
  --chroma-key 'auto' `
  --force
```

Expected: output JSON has `ok: true`, `ready_jobs` contains only `base`, and the run contains `pet_request.json`, `imagegen-jobs.json`, prompt files, and layout guides.

- [ ] **Step 2: Verify the generated contract**

```powershell
$request = Get-Content -Raw "$run\pet_request.json" | ConvertFrom-Json
$jobs = Get-Content -Raw "$run\imagegen-jobs.json" | ConvertFrom-Json
$request.atlas
$jobs.jobs | Select-Object id,kind,status,depends_on,output_path | Format-Table -AutoSize
```

Expected: atlas is 8×11 with 192×208 cells; jobs include `base`, nine standard rows, `look-cardinals`, `look-row-9`, and `look-row-10`; all row jobs depend on the canonical base.

- [ ] **Step 3: Record the selected chroma key and input set**

Write the actual `$request.chroma_key.hex` and the ten selected filenames under `Inputs` in `docs/production-log.md`.

```powershell
git add docs/production-log.md
git commit -m "chore: prepare Kano v2 production run"
```

### Task 4: Generate And Approve The Canonical Character Model

**Files:**
- Create: `assets/model-sheet.png`
- Use ignored: `work/runs/kano--scarbal486-v2/decoded/base.png`
- Modify: `docs/production-log.md`

- [ ] **Step 1: Load the identity references for built-in generation**

Open these local images with `view_image` so they are visible to the built-in image generator: `微笑.gif`, `早上好.gif`, `打游戏中.gif`, `这就去.gif`, `拜托了.gif`, and `我看不懂.gif`.

- [ ] **Step 2: Generate one canonical full-body model with `imagegen`**

Use the exact contents of `$run\prompts\base-pet.md` as the authoritative prompt. Reinforce only these approved invariants: bow stays on the character's right side; outfit is red scarf plus green white-dot dress; non-pixel rounded sticker style; one centered full-body character; perfectly flat generated chroma background; no text, scene, floor, shadow, detached marks, extra props, or alternate avatar era.

Copy the selected generated result to `$run\decoded\base.png`, then copy the same bytes to `$run\references\canonical-base.png`.

- [ ] **Step 3: Use Shoubanhua only if the built-in result fails identity or style**

Do not call Shoubanhua merely for a second aesthetic variant. If the built-in result fails the approved identity gate, run one bounded attempt with the current valid runtime model and the same references:

```powershell
$basePrompt = Get-Content -Raw "$run\prompts\base-pet.md"
& 'D:\AstrBot\.venv\Scripts\python.exe' -B 'C:\Users\W\.codex\skills\generating-with-shoubanhua\scripts\shoubanhua_generate.py' `
  --prompt $basePrompt `
  --out "$run\decoded\base-shoubanhua.png" `
  --image "$PWD\微笑.gif" `
  --image "$PWD\早上好.gif" `
  --image "$PWD\打游戏中.gif" `
  --image "$PWD\这就去.gif"
```

Expected: exit code 0, a non-empty decodable image, and no AstrBot configuration or model routing change. On non-zero exit, stop and report the redacted error verbatim; do not switch models or channels automatically.

- [ ] **Step 4: Validate and obtain explicit visual approval**

Decode the selected base with Pillow and verify non-zero dimensions. Display it at original size and at a 192×208 pet-size preview. Reject it for any identity drift listed in `docs/style-guide.md`. Ask the user to approve the canonical model before row generation.

- [ ] **Step 5: Persist the approved model**

Copy the approved canonical image to `assets/model-sheet.png`. Update the `base` job in `imagegen-jobs.json` to `complete`, record its selected source and QA note, and update `docs/production-log.md` under `Canonical model`.

```powershell
New-Item -ItemType Directory -Force 'assets' | Out-Null
Copy-Item "$run\decoded\base.png" 'assets\model-sheet.png'
$jobsPath = Join-Path $run 'imagegen-jobs.json'
$manifest = Get-Content -Raw $jobsPath | ConvertFrom-Json
$job = $manifest.jobs | Where-Object id -eq 'base'
$job.status = 'complete'
$job | Add-Member -NotePropertyName source_path -NotePropertyValue 'decoded/base.png' -Force
$job | Add-Member -NotePropertyName qa_note -NotePropertyValue 'Canonical model approved against the local Kano sticker references at full size and 192x208 preview size.' -Force
$job | Add-Member -NotePropertyName completed_at -NotePropertyValue ([DateTime]::UtcNow.ToString('o')) -Force
[System.IO.File]::WriteAllText($jobsPath, (($manifest | ConvertTo-Json -Depth 30) + "`n"), [System.Text.UTF8Encoding]::new($false))
git add assets/model-sheet.png docs/production-log.md
git commit -m "feat: approve Kano character master"
```

### Task 5: Produce Locomotion, Idle, Greeting, And Jump Rows

**Files:**
- Create: `assets/previews/idle.gif`
- Create: `assets/previews/running-right.gif`
- Create: `assets/previews/running-left.gif`
- Create: `assets/previews/waving.gif`
- Create: `assets/previews/jumping.gif`
- Modify: `docs/production-log.md`
- Use ignored: `work/runs/kano--scarbal486-v2/decoded/*.png`

- [ ] **Step 1: Generate `idle` as one coherent six-pose strip**

Use `prompts/rows/idle.md`, the canonical base, `微笑.gif`, and the generated idle layout guide. Require subtle breathing, one blink, and slight scarf motion; reject six effectively identical cells.

- [ ] **Step 2: Generate both directional movement rows independently**

Generate `running-right` and `running-left` as separate eight-pose strips using `这就去.gif`. Do not mirror because the bow and hair silhouette are asymmetric. Right must face and travel screen-right; left must face and travel screen-left; both need alternating cadence and scarf follow-through.

- [ ] **Step 3: Generate greeting and jump rows**

Generate `waving` from `早上好.gif` as four poses and `jumping` from `阿里嘎多.gif` as five poses. Do not include wave marks, ground shadows, dust, or detached effects.

- [ ] **Step 4: Run incremental extraction and deterministic QA after each row**

For each ID in `idle`, `running-right`, `running-left`, `waving`, and `jumping`, run:

```powershell
$id = 'idle'
$rowQa = Join-Path $run "qa\rows\$id"
& $python "$skill\scripts\extract_strip_frames.py" --decoded-dir "$run\decoded" --output-dir "$rowQa\frames" --states $id --method auto
& $python "$skill\scripts\inspect_frames.py" --frames-root "$rowQa\frames" --json-out "$rowQa\review.json" --states $id
& $python "$skill\scripts\render_animation_previews.py" --frames-root "$rowQa\frames" --output-dir "$rowQa\previews"
```

Repeat with the actual ID. Expected: `review.json` has no errors, the exact row frame count is present, and the preview loop has no clipping, size pop, reversed cadence, static repetition, or identity drift.

- [ ] **Step 5: Apply the bounded Shoubanhua row fallback only where required**

When a complete row fails visual identity or style after the built-in attempt, run Shoubanhua once with that row's prompt, canonical base, state reference, and layout guide. Use this exact mapping and command, changing `$id` only to the failed row:

```powershell
$stateRefs = @{
  'idle' = "$PWD\微笑.gif"
  'running-right' = "$PWD\这就去.gif"
  'running-left' = "$PWD\这就去.gif"
  'waving' = "$PWD\早上好.gif"
  'jumping' = "$PWD\阿里嘎多.gif"
}
$id = 'idle'
$rowPrompt = Get-Content -Raw "$run\prompts\rows\$id.md"
$candidate = "$run\decoded\$id-shoubanhua.png"
& 'D:\AstrBot\.venv\Scripts\python.exe' -B 'C:\Users\W\.codex\skills\generating-with-shoubanhua\scripts\shoubanhua_generate.py' `
  --prompt $rowPrompt `
  --out $candidate `
  --image "$run\references\canonical-base.png" `
  --image $stateRefs[$id] `
  --image "$run\references\layout-guides\$id.png"
```

Save the candidate separately, inspect it, then copy it over `decoded/$id.png` only after it passes. Never patch one cell into a row assembled from another generation. A non-zero call stops the row and is reported verbatim with credentials redacted.

- [ ] **Step 6: Copy approved previews and commit**

Copy the five approved GIFs to `assets/previews/`, update their jobs to `complete`, and record their QA notes in `docs/production-log.md`.

```powershell
New-Item -ItemType Directory -Force 'assets\previews' | Out-Null
$ids = 'idle','running-right','running-left','waving','jumping'
$jobsPath = Join-Path $run 'imagegen-jobs.json'
$manifest = Get-Content -Raw $jobsPath | ConvertFrom-Json
foreach ($id in $ids) {
  Copy-Item "$run\qa\rows\$id\previews\$id.gif" "assets\previews\$id.gif"
  $job = $manifest.jobs | Where-Object id -eq $id
  $job.status = 'complete'
  $job | Add-Member -NotePropertyName source_path -NotePropertyValue "decoded/$id.png" -Force
  $job | Add-Member -NotePropertyName qa_note -NotePropertyValue 'Exact frame count, deterministic row inspection, motion preview, and identity review passed.' -Force
  $job | Add-Member -NotePropertyName completed_at -NotePropertyValue ([DateTime]::UtcNow.ToString('o')) -Force
}
[System.IO.File]::WriteAllText($jobsPath, (($manifest | ConvertTo-Json -Depth 30) + "`n"), [System.Text.UTF8Encoding]::new($false))
git add assets/previews docs/production-log.md
git commit -m "feat: add Kano idle movement and greeting animations"
```

### Task 6: Produce Failure, Waiting, Working, And Review Rows

**Files:**
- Create: `assets/previews/failed.gif`
- Create: `assets/previews/waiting.gif`
- Create: `assets/previews/running.gif`
- Create: `assets/previews/review.gif`
- Modify: `docs/production-log.md`

- [ ] **Step 1: Generate `failed` and `waiting`**

Generate `failed` as eight poses grounded by `我看不懂.gif` and `好气啊.gif`: confusion, teary eyes, and a small deflated settle; no floating punctuation or detached tear drops. Generate `waiting` as six poses grounded by `拜托了.gif`: hands together, upward expectant gaze, gentle asking motion clearly distinct from idle.

- [ ] **Step 2: Generate `running` as active work, not locomotion**

Generate six poses grounded by `打游戏中.gif`: seated, focused operation of the same pink handheld device, purposeful hand movement and slight body bob. No literal foot-running, code UI, floating icons, or new workstation.

- [ ] **Step 3: Generate `review` as focused inspection**

Generate six poses grounded by `原来如此.gif`: slight forward lean, eyes checking side to side, head tilt, then a small understanding expression. Do not add paper, magnifying glass, punctuation, or UI.

- [ ] **Step 4: Run the same incremental extraction, inspection, and preview commands**

Run this block once per row, changing `$id` to `failed`, `waiting`, `running`, and `review`:

```powershell
$id = 'failed'
$rowQa = Join-Path $run "qa\rows\$id"
& $python "$skill\scripts\extract_strip_frames.py" --decoded-dir "$run\decoded" --output-dir "$rowQa\frames" --states $id --method auto
& $python "$skill\scripts\inspect_frames.py" --frames-root "$rowQa\frames" --json-out "$rowQa\review.json" --states $id
& $python "$skill\scripts\render_animation_previews.py" --frames-root "$rowQa\frames" --output-dir "$rowQa\previews"
```

Reject any row with wrong semantics, static copies, detached effects, identity drift, clipping, or size pop.

- [ ] **Step 5: Use the bounded Shoubanhua full-row fallback when needed**

Use this exact mapping and command, changing `$id` only to the failed row:

```powershell
$stateRefs = @{
  'failed' = "$PWD\我看不懂.gif"
  'waiting' = "$PWD\拜托了.gif"
  'running' = "$PWD\打游戏中.gif"
  'review' = "$PWD\原来如此.gif"
}
$id = 'failed'
$rowPrompt = Get-Content -Raw "$run\prompts\rows\$id.md"
$candidate = "$run\decoded\$id-shoubanhua.png"
& 'D:\AstrBot\.venv\Scripts\python.exe' -B 'C:\Users\W\.codex\skills\generating-with-shoubanhua\scripts\shoubanhua_generate.py' `
  --prompt $rowPrompt `
  --out $candidate `
  --image "$run\references\canonical-base.png" `
  --image $stateRefs[$id] `
  --image "$run\references\layout-guides\$id.png"
```

Inspect the result before replacing `decoded/$id.png`. A non-zero call stops the row; no automatic model or channel switch is allowed.

- [ ] **Step 6: Copy approved previews and commit**

```powershell
New-Item -ItemType Directory -Force 'assets\previews' | Out-Null
$ids = 'failed','waiting','running','review'
$jobsPath = Join-Path $run 'imagegen-jobs.json'
$manifest = Get-Content -Raw $jobsPath | ConvertFrom-Json
foreach ($id in $ids) {
  Copy-Item "$run\qa\rows\$id\previews\$id.gif" "assets\previews\$id.gif"
  $job = $manifest.jobs | Where-Object id -eq $id
  $job.status = 'complete'
  $job | Add-Member -NotePropertyName source_path -NotePropertyValue "decoded/$id.png" -Force
  $job | Add-Member -NotePropertyName qa_note -NotePropertyValue 'Exact frame count, deterministic row inspection, state-semantics review, motion preview, and identity review passed.' -Force
  $job | Add-Member -NotePropertyName completed_at -NotePropertyValue ([DateTime]::UtcNow.ToString('o')) -Force
}
[System.IO.File]::WriteAllText($jobsPath, (($manifest | ConvertTo-Json -Depth 30) + "`n"), [System.Text.UTF8Encoding]::new($false))
git add assets/previews docs/production-log.md
git commit -m "feat: add Kano task state animations"
```

### Task 7: Assemble And Review The Standard 8×9 Intermediate

**Files:**
- Create temporarily: `work/runs/kano--scarbal486-v2/final/spritesheet.webp`
- Create temporarily: `work/runs/kano--scarbal486-v2/qa/contact-sheet.png`
- Update: `assets/previews/*.gif`
- Modify: `docs/production-log.md`

- [ ] **Step 1: Extract all approved standard rows together**

```powershell
& $python "$skill\scripts\extract_strip_frames.py" --decoded-dir "$run\decoded" --output-dir "$run\frames" --states all --method auto
& $python "$skill\scripts\inspect_frames.py" --frames-root "$run\frames" --json-out "$run\qa\review.json" --states all
```

Expected: `qa/review.json` has no errors and every row has the exact v2 standard frame count.

- [ ] **Step 2: Compose the intermediate atlas and QA media**

```powershell
& $python "$skill\scripts\compose_atlas.py" --frames-root "$run\frames" --output "$run\final\spritesheet.png" --webp-output "$run\final\spritesheet.webp"
& $python "$skill\scripts\make_contact_sheet.py" "$run\final\spritesheet.webp" --output "$run\qa\contact-sheet.png"
& $python "$skill\scripts\render_animation_previews.py" --frames-root "$run\frames" --output-dir "$run\qa\previews"
```

Expected: intermediate atlas is 1536×1872 and is never copied into `dist/`.

- [ ] **Step 3: Review the standard contact sheet and all nine loops**

Display `qa/contact-sheet.png` and all nine preview GIFs. If per-frame fit caused scale or baseline pop while the source strip was stable, rerun extraction with `--method stable-slots`, then repeat inspection, composition, and preview rendering. Do not use `stable-slots` merely to hide bad generated poses.

- [ ] **Step 4: Record standard-row approval and commit the final previews**

Copy the final nine previews to `assets/previews/`, record the standard contact-sheet verdict in `docs/production-log.md`, and commit.

```powershell
git add assets/previews docs/production-log.md
git commit -m "feat: approve Kano standard animation atlas"
```

### Task 8: Produce And Validate The 16 Look Directions

**Files:**
- Create: `assets/look-directions.png`
- Create: `assets/previews/look-directions.gif`
- Modify: `docs/production-log.md`
- Use ignored: `work/runs/kano--scarbal486-v2/qa/look-mechanics.md`

- [ ] **Step 1: Write the pet-specific look mechanics**

Create `$run\qa\look-mechanics.md` with these rules: eyes lead the direction, followed by a small face/head turn; the torso remains upright; antlers follow head perspective without changing count or length; the bow remains attached to the character's right side; scarf movement is secondary; no whole-sprite rotation; 000° is unmistakably up and not neutral.

- [ ] **Step 2: Generate and extract the four cardinal anchors**

Generate one coherent four-pose strip in order 000° up, 090° screen-right, 180° down, 270° screen-left using the canonical base and `look-cardinals` layout guide.

```powershell
$chroma = (Get-Content -Raw "$run\pet_request.json" | ConvertFrom-Json).chroma_key.hex
& $python "$skill\scripts\extract_cardinal_anchors.py" --strip "$run\decoded\look-cardinals.png" --output-dir "$run\decoded\look-cardinals" --json-out "$run\qa\look-cardinals.json" --chroma-key $chroma
& $python "$skill\scripts\compose_cardinal_anchor_strip.py" --anchors-dir "$run\decoded\look-cardinals" --output "$run\decoded\look-anchors-approved.png"
```

Expected: all four complete poses fit with no clipping and their direction is visually unambiguous. Obtain explicit user approval before generating intermediate directions.

- [ ] **Step 3: Generate and register row 9**

Generate one coherent eight-pose `look-row-9` strip in order 000°, 022.5°, 045°, 067.5°, 090°, 112.5°, 135°, 157.5°. Attach the approved cardinal strip, canonical base, full references, and row layout guide.

```powershell
& $python "$skill\scripts\assemble_extended_atlas.py" `
  --base-atlas "$run\final\spritesheet.webp" `
  --look-row-9 "$run\decoded\look-row-9.png" `
  --neutral-cell "$run\frames\idle\00.png" `
  --chroma-key $chroma `
  --chroma-threshold 96 `
  --registered-row-output "$run\qa\look-row-9-registered.png" `
  --registration-manifest-output "$run\qa\look-row-9-registration.json"
```

Expected: pose-group registration succeeds, all eight groups remain in order, and near-edge checks pass.

- [ ] **Step 4: Generate row 10 only after row 9 passes**

Generate one coherent eight-pose `look-row-10` strip in order 180°, 202.5°, 225°, 247.5°, 270°, 292.5°, 315°, 337.5°. Attach the approved cardinals, canonical base, row 9 continuity evidence, full references, and row layout guide.

- [ ] **Step 5: Assemble the full v2 atlas**

```powershell
& $python "$skill\scripts\assemble_extended_atlas.py" `
  --base-atlas "$run\final\spritesheet.webp" `
  --registered-row-9 "$run\qa\look-row-9-registered.png" `
  --row-9-registration "$run\qa\look-row-9-registration.json" `
  --look-row-10 "$run\decoded\look-row-10.png" `
  --neutral-cell "$run\frames\idle\00.png" `
  --chroma-key $chroma `
  --chroma-threshold 96 `
  --output "$run\final\spritesheet-extended.png" `
  --webp-output "$run\final\spritesheet-extended.webp" `
  --manifest-output "$run\final\spritesheet-extended.json"
```

- [ ] **Step 6: Generate direction QA evidence**

```powershell
& $python "$skill\scripts\make_direction_qa_sheet.py" "$run\final\spritesheet-extended.webp" --output "$run\qa\look-directions.png"
& $python "$skill\scripts\measure_direction_continuity.py" "$run\final\spritesheet-extended.webp" --json-out "$run\qa\look-continuity.json"
```

Inspect all 16 labeled directions at normal pet size. Record `pass`, `warning`, or `fail` plus observed horizontal and vertical evidence for every direction in `$run\qa\direction-semantics.json`. Cardinals may not be ambiguous. Because this execution does not assume delegated workers, explicit user inspection is the independent acceptance gate.

- [ ] **Step 7: Repair only complete look rows**

If one direction fails, strengthen the corresponding row prompt and regenerate the entire eight-pose row. Never replace one final direction cell. Re-run registration, assembly, direction QA, continuity measurement, and user inspection.

- [ ] **Step 8: Persist direction QA media and commit**

Copy `qa/look-directions.png` to `assets/look-directions.png`, render/copy the ordered direction loop to `assets/previews/look-directions.gif`, update `docs/production-log.md`, and commit.

```powershell
git add assets/look-directions.png assets/previews/look-directions.gif docs/production-log.md
git commit -m "feat: add Kano look directions"
```

### Task 9: Clean, Validate, And Package The Final Pet

**Files:**
- Create: `dist/pet.json`
- Create: `dist/spritesheet.webp`
- Create: `dist/validation.json`
- Create: `assets/contact-sheet.png`
- Modify: `docs/production-log.md`

- [ ] **Step 1: Run the single authorized chroma cleanup pass**

```powershell
& $python "$skill\scripts\despill_chroma_edges.py" `
  "$run\final\spritesheet-extended.png" `
  --output "$run\final\spritesheet-extended.png" `
  --webp-output "$run\final\spritesheet-extended.webp" `
  --chroma-key $chroma `
  --json-out "$run\qa\chroma-despill-extended.json"
```

Expected: report has `ok: true`. Do not run a second despill pass or regenerate visual rows for perceived fringe after this deterministic pass succeeds.

- [ ] **Step 2: Validate the v2 atlas**

```powershell
& $python "$skill\scripts\validate_atlas.py" `
  "$run\final\spritesheet-extended.webp" `
  --json-out "$run\final\validation-extended.json" `
  --chroma-key $chroma `
  --require-v2
```

Expected: exit code 0; dimensions 1536×2288; 8×11 cells; used cells non-empty; unused standard cells transparent; no chroma leak or fringe failure.

- [ ] **Step 3: Create the final contact sheet**

```powershell
& $python "$skill\scripts\make_contact_sheet.py" "$run\final\spritesheet-extended.webp" --output "$run\qa\contact-sheet-extended.png"
```

Display this sheet with the nine state previews and direction sheet. Any remaining identity drift blocks packaging even if deterministic validation passes.

- [ ] **Step 4: Write the exact runtime manifest**

Create `dist/pet.json` with exactly:

```json
{
  "id": "kano--scarbal486",
  "displayName": "鹿乃 / Kano",
  "description": "A fan-made Codex pet based on Kano's classic antler-girl avatar.",
  "spriteVersionNumber": 2,
  "spritesheetPath": "spritesheet.webp"
}
```

- [ ] **Step 5: Copy only validated outputs into the repository**

```powershell
New-Item -ItemType Directory -Force 'dist','assets' | Out-Null
Copy-Item "$run\final\spritesheet-extended.webp" 'dist\spritesheet.webp'
Copy-Item "$run\final\validation-extended.json" 'dist\validation.json'
Copy-Item "$run\qa\contact-sheet-extended.png" 'assets\contact-sheet.png'
```

- [ ] **Step 6: Re-run validation on the committed destination**

```powershell
& $python "$skill\scripts\validate_atlas.py" 'dist\spritesheet.webp' --json-out 'dist\validation.json' --chroma-key $chroma --require-v2
Get-Content -Raw 'dist\pet.json' | ConvertFrom-Json | Format-List
```

Expected: validation passes from `dist/`, not only from the ignored run folder.

- [ ] **Step 7: Record validation and commit the package**

Update `docs/production-log.md` with the despill result, validation result, atlas dimensions, and final SHA-256 values.

```powershell
Get-FileHash -Algorithm SHA256 'dist\pet.json','dist\spritesheet.webp' | Format-Table -AutoSize
git add dist assets/contact-sheet.png docs/production-log.md
git commit -m "feat: package Kano Codex pet v2"
```

### Task 10: Install And Verify In The Codex App

**Files:**
- Copy to: `%USERPROFILE%\.codex\pets\kano--scarbal486\pet.json`
- Copy to: `%USERPROFILE%\.codex\pets\kano--scarbal486\spritesheet.webp`
- Modify: `README.md`
- Modify: `docs/production-log.md`

- [ ] **Step 1: Stage the exact runtime package**

```powershell
New-Item -ItemType Directory -Force $petInstall | Out-Null
Copy-Item 'dist\pet.json' (Join-Path $petInstall 'pet.json')
Copy-Item 'dist\spritesheet.webp' (Join-Path $petInstall 'spritesheet.webp')
```

- [ ] **Step 2: Verify installed bytes match the repository package**

```powershell
Get-FileHash -Algorithm SHA256 'dist\pet.json',(Join-Path $petInstall 'pet.json')
Get-FileHash -Algorithm SHA256 'dist\spritesheet.webp',(Join-Path $petInstall 'spritesheet.webp')
```

Expected: each source/destination pair has identical SHA-256.

- [ ] **Step 3: Perform the real Codex runtime smoke test**

Refresh or restart Codex only as needed for custom-pet discovery. Select `鹿乃 / Kano` in Settings → Pets. Trigger or observe idle, movement, greeting, jump, failed, waiting, running-task, review, and pointer-look behavior. Capture a normal-size screenshot or short recording showing the pet rendered in Codex.

Expected: no blank pet, wrong scale, opaque key background, clipped frame, swapped bow side, reversed movement, or non-playing row.

- [ ] **Step 4: Update documentation and commit**

Add the tested install path and selection steps to `README.md`. Record the tested Codex version/date and runtime observations in `docs/production-log.md`.

```powershell
git add README.md docs/production-log.md
git commit -m "docs: verify Kano pet installation"
```

### Task 11: Final User Acceptance And Private Release

**Files:**
- Final review: `assets/contact-sheet.png`
- Final review: `assets/look-directions.png`
- Final review: `assets/previews/*.gif`
- Final package: `dist/pet.json`
- Final package: `dist/spritesheet.webp`

- [ ] **Step 1: Run repository and package verification**

```powershell
git status --short
git ls-files '*.gif'
& $python "$skill\scripts\validate_atlas.py" 'dist\spritesheet.webp' --json-out 'dist\validation.json' --chroma-key $chroma --require-v2
gh repo view Scarbal486/kano-codex-pet --json visibility,defaultBranchRef,url
```

Expected: clean worktree; tracked GIFs exist only under `assets/previews/`; validation passes; repository remains `PRIVATE`; default branch is `main`.

- [ ] **Step 2: Present the complete visual evidence to the user**

Show the final contact sheet, all state GIFs, look-direction sheet, and Codex runtime screenshot. Ask for explicit final approval. Any visible mismatch returns to the smallest failed complete row; do not create a release from a rejected atlas.

- [ ] **Step 3: Push the approved commits**

```powershell
git -c http.version=HTTP/1.1 push origin main
```

Expected: `origin/main` matches local `main`.

- [ ] **Step 4: Create the private release archive**

Create a ZIP containing only `pet.json` and `spritesheet.webp`, then publish a private-repository GitHub release:

```powershell
Compress-Archive -Path 'dist\pet.json','dist\spritesheet.webp' -DestinationPath 'dist\kano-codex-pet-v1.0.0.zip' -Force
gh release create v1.0.0 'dist\kano-codex-pet-v1.0.0.zip' --repo Scarbal486/kano-codex-pet --title 'Kano Codex Pet v1.0.0' --notes 'Private first release. Includes the Codex Pet v2 manifest and validated spritesheet.'
```

Expected: release `v1.0.0` exists and the archive contains exactly the two runtime files.

- [ ] **Step 5: Record release evidence**

Update `docs/production-log.md` with the release URL and final package hashes, commit, and push:

```powershell
git add docs/production-log.md
git commit -m "release: record Kano pet v1.0.0"
git -c http.version=HTTP/1.1 push origin main
```
