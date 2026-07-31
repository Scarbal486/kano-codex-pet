# Kano Pet Style Guide

## Approved identity

Use only Kano's classic unmarked antler-girl avatar:

- Rounded brown bob with straight bangs.
- Two small light-colored antlers.
- Coral bow fixed to the character's right side. Turning must preserve the real wearing side instead of mirroring it.
- Long red scarf.
- Green clothing with white dots and a light undershirt.
- Large deep-blue eyes, soft blush, and a rounded face.
- Oversized head, tiny body, and short limbs.

Do not mix in the Hanayori Kano or Kano Mahoro avatar eras.

## Palette

| Use | Color |
| --- | --- |
| Hair | `#BD8068` |
| Scarf | `#EB435C` |
| Green clothing | `#AAD67C` |
| Skin | `#FFEBD3` |
| Bow and blush | `#ED8C87` |
| Antlers and light highlights | `#FFFCEF` |
| Deep eye color | `#013251` |
| Blue-violet outline | `#343363` |

## Required invariants

- Use rounded, stable, thick blue-violet outlines.
- Use flat colors with only minimal soft shading.
- Keep expressions exaggerated but cute, without realistic anatomy or complex illustration rendering.
- Express actions through pose, expression, and silhouette changes rather than text or floating effects.
- Keep face shape, bangs, eye color, antlers, bow side, scarf, dotted clothing, proportions, line width, and rendering consistent across every row.
- Produce real frame-to-frame motion; repeated static frames do not pass review.
- Draw left-facing movement independently so asymmetric accessories remain on their correct side.

## Full-row rejection rules

Reject and regenerate the complete row if any frame:

- Changes to pink hair, twin tails, or a Hanayori school uniform.
- Swaps the bow side or changes antler count, length, or shape.
- Drifts in face shape, bangs, eye color, scarf, or dotted clothing.
- Becomes pixel art, 3D, oil-painted, plastic-toy-like, or realistic.
- Uses visibly different line width, proportions, or rendering from other rows.
- Contains detached text, punctuation, UI, speed lines, ground shadows, or floating effects.
- Is clipped, contains identity drift, or causes obvious scale or baseline popping.

A failed cell is not patched into an otherwise generated row. The entire coherent row must be regenerated.
