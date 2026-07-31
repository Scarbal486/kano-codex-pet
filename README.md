# Kano Codex Pet

## About

This repository contains an unofficial, fan-made Codex Pet v2 based on Kano's classic antler-girl avatar. The visual target is the rounded chibi sticker style shown by the local production references.

The repository remains private during production. It must not be made public until a separate source-and-rights review is complete.

## Preview

Approved contact sheets, direction checks, and animation previews will be added under `assets/` as production passes visual review.

## Install

The installable files are under `dist/`. Copy `pet.json` and `spritesheet.webp` to:

```text
%USERPROFILE%\.codex\pets\kano--scarbal486\
```

Then refresh or restart Codex and select `鹿乃 / Kano` in Settings -> Pets.

## Package

The runtime package contains only:

- `dist/pet.json`
- `dist/spritesheet.webp`

`dist/validation.json` records deterministic atlas validation and is not required at runtime.

## Development

The pet targets Codex Pet v2: an 8 x 11 atlas with 192 x 208 cells, for a final size of 1536 x 2288. Local reference stickers and intermediate production files are intentionally excluded from Git.

## Sources and rights

See `docs/sources-and-rights.md` and `NOTICE.md`. The original sticker references remain local and are not distributed by this repository.

## Non-official project

This project is not affiliated with or endorsed by Kano, her management, OpenAI, or the creators and distributors of the reference stickers.
