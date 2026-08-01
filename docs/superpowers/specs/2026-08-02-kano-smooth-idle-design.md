# Kano Smooth Idle Design

## Goal

Make only the installed `鹿乃 / Kano` pet's idle animation play at a steady 10 FPS without changing the approved artwork, Codex application files, built-in pets, other custom pets, or non-idle behavior.

## Confirmed Cause

Codex `26.721.11231.0` owns standard animation timing. Its renderer defines the six idle durations as `280, 110, 110, 140, 140, 320 ms`, then multiplies each duration by `6`. The resulting runtime dwell times are `1680, 660, 660, 840, 840, 1920 ms`. The custom-pet manifest supports the atlas path and sprite version but has no timing field, so changing `pet.json` cannot correct the pacing.

## Selected Approach

Package a lossless animated WebP for Kano while retaining the existing Pet v2 atlas contract.

The output contains six WebP animation frames at `100 ms` each with infinite looping. In WebP animation frame `p`, row 0 columns `0` through `5` each contain approved idle source cell `p`. Therefore, whichever idle column Codex's slow scheduler currently selects, the displayed cell follows the WebP animation phase at 10 FPS.

All other atlas cells are copied from the decoded approved static atlas without pixel changes in every WebP animation frame:

- Row 0 column 6 remains the neutral cell.
- Row 0 column 7 remains transparent.
- Rows 1 through 8 retain every standard non-idle state.
- Rows 9 and 10 retain all 16 look directions.

This changes only Kano because only Kano's installed `spritesheet.webp` becomes animated. No Codex resource, executable, JavaScript bundle, preference, or other pet package is modified.

## Repository Changes

Create one focused builder/validator script under `scripts/`. It accepts the approved static atlas, emits the animated atlas, and writes a machine-readable report. The implementation uses Pillow already available in the pinned workspace runtime and directly parses the WebP RIFF animation chunks for timing verification because Pillow 12.2.0 does not expose the first frame's duration through `Image.info`.

Add focused unit tests under `tests/` using a small synthetic RGBA atlas. Tests must establish the following behavior before production code is written:

1. Output is an animated WebP with six frames, infinite looping, and six `100 ms` `ANMF` durations.
2. At animation phase `p`, idle columns 0 through 5 equal source idle cell `p` after decoding.
3. Row 0 columns 6 and 7 and rows 1 through 10 equal the source in every phase.
4. Wrong source dimensions and non-static source atlases are rejected without overwriting output.
5. The report records dimensions, frame count, duration, loop count, and pixel-preservation results.

The approved static atlas remains preserved in the ignored production run directory. `dist/spritesheet.webp` becomes the verified animated artifact; `dist/pet.json` remains structurally unchanged. `dist/validation.json`, `README.md`, and `docs/production-log.md` are updated to identify and audit the animated package.

## Encoding Rules

- Decode the approved `1536 x 2288` RGBA static atlas once.
- Construct six full-size RGBA frames in memory.
- Use lossless WebP animation encoding so unchanged cells decode byte-for-byte equal to the approved source pixels.
- Set durations to exactly `[100, 100, 100, 100, 100, 100]` milliseconds and loop count to `0` (infinite).
- Do not resize, interpolate, redraw, mirror, reorder, despill, or otherwise alter any source cell.
- Write to a temporary sibling path, validate it completely, then replace the requested destination only after validation succeeds.

## Validation

Automated validation has three layers:

1. Run the new focused unit tests through `unittest` and retain the existing upstream `28/28` test suite.
2. Run the existing Pet v2 atlas validator against every decoded WebP animation frame, not only frame zero. Every phase must remain `1536 x 2288` RGBA with zero errors, zero warnings, and zero transparent-RGB residue.
3. Run the dynamic validator to verify RIFF `VP8X` animation flags, `ANIM` infinite loop metadata, six `ANMF` chunks, exact `100 ms` durations, phase-correct idle cells, and pixel-identical non-idle regions.

After installing, source and installed SHA-256 hashes must match for both runtime files.

## Runtime Acceptance

Refresh or restart Codex only as required to reload Kano, then select and wake the pet. Capture the `113 x 122` pet node at approximately 20 Hz for at least three seconds while it is idle.

Acceptance requires:

- all six approved idle phases appear;
- measured phase transitions are approximately `100 ms`, allowing normal screen-capture scheduling jitter;
- no old `660-1920 ms` stalls remain during the sample;
- the pet is not blank, clipped, green-backed, or visibly corrupted;
- one caret-driven look capture still matches a look row rather than an idle phase;
- closing and reopening the pet does not change the result.

If Chromium does not animate the WebP atlas as a CSS background, or pauses it in this overlay, the experiment fails cleanly: restore the currently installed static atlas from the repository commit or verified backup, record the failed runtime result, and do not patch Codex itself under this design.

## Delivery Boundary

Commit the tested builder, tests, updated runtime artifact, validation report, and documentation locally. Do not push, publish a release, modify the Codex installation package, or change another pet.
