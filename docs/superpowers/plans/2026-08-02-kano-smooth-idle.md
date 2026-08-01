# Kano Smooth Idle Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Replace Kano's static runtime atlas with a verified six-frame lossless animated WebP that renders the approved idle loop at 10 FPS while preserving every non-idle pixel.

**Architecture:** A single Python CLI reads the approved static Pet v2 atlas, constructs six full-atlas animation phases, and duplicates the current approved idle cell across host-selected idle columns 0-5. It parses RIFF animation metadata and compares decoded pixels before atomically replacing the destination; focused `unittest` coverage establishes the behavior before implementation.

**Tech Stack:** Python 3.13, Pillow 12.2, `unittest`, RIFF/WebP container parsing, existing `hatch-pet-v2` atlas validator, Windows UI Automation runtime sampling.

---

### Task 1: Build And Validate Animated Idle Atlases

**Files:**
- Create: `tests/test_build_smooth_idle_atlas.py`
- Create: `scripts/build_smooth_idle_atlas.py`

- [ ] **Step 1: Write the failing tests**

Create `tests/test_build_smooth_idle_atlas.py` with one shared synthetic `1536 x 2288` RGBA atlas and tests that import:

```python
from scripts.build_smooth_idle_atlas import (
    AtlasError,
    build_smooth_idle_atlas,
    inspect_animated_webp,
)
```

The successful-build test must assert six decoded frames, loop `0`, six `100 ms` RIFF durations, phase `p` copied into idle columns 0-5, and pixel equality outside those six cells. Separate tests must assert rejection of wrong dimensions and animated input without creating the requested output.

- [ ] **Step 2: Run the tests and verify RED**

Run:

```powershell
$python = 'C:\Users\W\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe'
& $python -X utf8 -m unittest tests.test_build_smooth_idle_atlas -v
```

Expected: FAIL because `scripts.build_smooth_idle_atlas` does not exist.

- [ ] **Step 3: Implement the smallest builder/validator**

Create `scripts/build_smooth_idle_atlas.py` with these public interfaces:

```python
class AtlasError(ValueError):
    pass

def inspect_animated_webp(path: Path) -> dict[str, object]:
    """Return VP8X animation flag, ANIM loop count, and ANMF durations."""

def build_smooth_idle_atlas(
    source_path: Path,
    output_path: Path,
    report_path: Path | None = None,
) -> dict[str, object]:
    """Build, validate, and atomically install one six-phase 10 FPS atlas."""
```

Use constants `1536 x 2288`, cells `192 x 208`, six idle phases, and `100 ms`. Reject animated or wrong-size sources. Build each phase from `source.copy()`, paste source idle cell `phase` into row 0 columns 0-5 without a mask, save lossless animated WebP to a sibling temporary file, then validate:

```python
metadata["animation"] is True
metadata["loop"] == 0
metadata["durations_ms"] == [100] * 6
decoded_frame_count == 6
```

For every decoded phase, require the six idle cells to equal source idle cell `phase`, row 0 columns 6-7 to equal the source, rows 1-10 to equal the source, and transparent pixels to have zero RGB residue. Replace `output_path` only after all assertions pass. The CLI accepts `SOURCE OUTPUT --report REPORT` and exits nonzero with `AtlasError` text on invalid input.

- [ ] **Step 4: Run focused tests and verify GREEN**

Run:

```powershell
$env:PYTHONUTF8 = '1'
& $python -X utf8 -m unittest tests.test_build_smooth_idle_atlas -v
```

Expected: all focused tests pass with no errors.

- [ ] **Step 5: Run the existing regression suite**

Run:

```powershell
& $python -X utf8 -m unittest discover -s 'work\upstream\hatch-pet-v2\tests' -p 'test_*.py' -v
```

Expected: `Ran 28 tests` and `OK`.

- [ ] **Step 6: Commit the tested tooling**

```powershell
git add scripts/build_smooth_idle_atlas.py tests/test_build_smooth_idle_atlas.py
git commit -m "feat: build smooth Kano idle atlases"
```

### Task 2: Build And Package Kano's Animated Atlas

**Files:**
- Modify: `dist/spritesheet.webp`
- Modify: `dist/validation.json`
- Use ignored: `work/runs/kano--scarbal486-v2/final/spritesheet-extended.webp`
- Create ignored: `work/runs/kano--scarbal486-v2/qa/smooth-idle/`

- [ ] **Step 1: Resolve and verify the approved static source**

Compare the current tracked static package against the ignored post-despill production atlas. If their decoded RGBA pixels differ, use the current committed `dist/spritesheet.webp` as the source and save its exact bytes under ignored QA before replacement. Record source SHA-256 either way.

- [ ] **Step 2: Build to an ignored candidate first**

```powershell
& $python -X utf8 scripts/build_smooth_idle_atlas.py `
  <approved-static-source> `
  work/runs/kano--scarbal486-v2/qa/smooth-idle/spritesheet-animated.webp `
  --report work/runs/kano--scarbal486-v2/qa/smooth-idle/animation-validation.json
```

Expected: `ok: true`, six frames, `[100, 100, 100, 100, 100, 100]`, loop `0`, and preserved non-idle pixels.

- [ ] **Step 3: Validate every decoded animation phase**

Extract all six decoded phases to ignored PNG files. Run `work/upstream/hatch-pet-v2/scripts/validate_atlas.py --require-v2` against each phase with chroma key `#00FF00`.

Expected for every phase: `ok: true`, `1536 x 2288`, errors `0`, warnings `0`, and transparent RGB residue `0`.

- [ ] **Step 4: Replace the repository package atomically**

Run the builder again with the same approved static source and `dist/spritesheet.webp` as the destination, writing `dist/validation.json`. Confirm `dist/pet.json` is byte-identical to its pre-build SHA-256.

- [ ] **Step 5: Commit the verified package**

```powershell
git add dist/spritesheet.webp dist/validation.json
git commit -m "feat: smooth Kano idle playback"
```

### Task 3: Install And Perform Runtime Acceptance

**Files:**
- Copy to: `C:\Users\W\.codex\pets\kano--scarbal486\spritesheet.webp`
- Modify: `README.md`
- Modify: `docs/production-log.md`
- Create ignored: `work/runs/kano--scarbal486-v2/qa/smooth-idle/runtime/`

- [ ] **Step 1: Back up and install the exact candidate**

Save the currently installed static atlas under ignored QA. Copy `dist/spritesheet.webp` into Kano's install directory only, leaving `pet.json` unchanged. Verify source/install SHA-256 equality for both runtime files.

- [ ] **Step 2: Reload Kano without modifying Codex resources**

Use Settings -> Pets refresh or close/wake the pet as needed. Do not patch `app.asar`, bundled JavaScript, executables, settings for other pets, or another pet package.

- [ ] **Step 3: Capture and measure idle playback**

Capture the `鹿乃 / Kano 宠物` UI Automation node at approximately 20 Hz for at least three seconds. Match each capture against the six approved idle cells at the rendered `113 x 122` size and record timestamps, best phase, and MAE.

Expected: all six phases appear; consecutive phase transitions cluster near `100 ms`; no `660-1920 ms` stall remains; every rendered frame is nonblank, unclipped, and free of pure-green pixels.

- [ ] **Step 4: Regression-check look behavior and restart persistence**

Trigger the already verified empty-reply `End` caret path and confirm its capture still matches a look row. Close and wake Kano once, then repeat a shorter idle sample. If either check fails, restore the installed static backup and stop without claiming success.

- [ ] **Step 5: Update documentation**

Update README and the production log with the animated atlas SHA-256, file size, exact container metadata, phase timing sample, look regression result, Codex version, install path, and the fact that only Kano changed.

- [ ] **Step 6: Run completion verification and commit**

Run focused tests, upstream `28/28`, all six phase validators, manifest parsing, installed hashes, `git diff --check`, and `git status --short`. Then commit only documentation changes:

```powershell
git add README.md docs/production-log.md
git commit -m "docs: verify smooth Kano idle playback"
```

Do not push or create a release.
