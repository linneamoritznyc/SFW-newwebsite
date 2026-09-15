# Green pairings, current against proposed

Extends the Current Green / Proposed Green comparison with the rest of the palette. Built
15 September 2026.

- **Current Green** is `--green-legacy` **#59A66C**, which `docs/brand-guide.html` labels
  "Decorative only, fails contrast".
- **Proposed Green** is `--green` **#156826**, Food Web Green, "Buttons, links, eyebrows".

Nothing here is a new colour. Every swatch is a token already in `css/site.css` section 1, with the
name and the role taken word for word from `docs/brand-guide.html`. To add another pairing, add its
token to `build/make-sheets.py`; do not pick a colour by eye.

## The three sheets

| File | What it is |
| :-- | :-- |
| `pairings-current-set.png` | The eight pairings already in the deck, 3840 x 2160. |
| `pairings-twelve-more.png` | Twelve more palette colours in the same test, same proportions, 3840 x 2160. |
| `pairings-reference.png` | All nineteen with name, hex, token, role and both contrast ratios. |

Rebuild: `python3 "Color Pairings/build/make-sheets.py"` then `node "Color Pairings/build/render.js"`,
both from the repository root.

## The twelve added

Moss `--moss`, Ground `--ground`, Scope `--scope`, Olive `--olive`, Living Green `--living`,
Glow `--glow`, Membrane Violet `--membrane`, Specimen Case `--panel-green`, Paper `--paper`,
Ink `--ink`, Ink Soft `--ink-soft`, Ink Faint `--ink-faint`.

That is every colour in the brand guide. Nothing is left untested.

## One swatch in the original is not a brand colour

The eighth pairing on the current slide is a pale blue, roughly #D4ECFB by eye. It is not in
`css/site.css` and not in the brand guide, so it has no name and no documented role. I replaced it
with **Paper #FFFFFF**, which is the one background the green actually has to survive on every page.
If that blue is meant to stay, it needs a token, a name and a role like every other colour. If it was
only ever a tint of Education Blue, say so and it can be derived properly instead of sampled.

## What the contrast numbers say

Contrast of each green against the colour beside it, current then proposed.

| Colour | Hex | Current | Proposed |
| :-- | :-- | --: | --: |
| Paper | #FFFFFF | 2.96 | **6.91** |
| Organic Cream | #F4F1EA | 2.62 | **6.12** |
| Specimen Case | #E6EADC | 2.42 | **5.65** |
| Glow | #DBE6A7 | 2.24 | **5.23** |
| Sage | #A7B097 | 1.31 | **3.06** |
| Living Green | #A2AE77 | 1.25 | **2.91** |
| Harvest Gold | #C9A227 | 1.22 | **2.86** |
| Tan | #C89B7B | 1.19 | **2.77** |
| Membrane Violet | #9E8FC2 | 1.01 | **2.36** |
| Education Blue | #3780B8 | 1.44 | **1.63** |
| Ink Faint | #6A665C | 1.93 | 1.21 |
| Olive | #5F6A3C | 1.96 | 1.19 |
| Legacy Purple | #6B4C7A | 2.41 | 1.03 |
| Soil Brown | #4F3433 | 3.79 | 1.62 |
| Scope | #3C3841 | 3.87 | 1.66 |
| Moss | #22371F | 4.34 | 1.86 |
| Ink | #333130 | 4.37 | 1.87 |
| Ink Soft | #4A463F | 3.17 | 1.36 |
| Ground | #231F1D | 5.52 | 2.37 |

**The case for the change is the top of that table.** Current Green on the white page is 2.96 to 1.
The threshold for normal body text is 4.5 to 1, so a green link or a green eyebrow in the current
colour fails, which is exactly what the brand guide already says about it. Food Web Green is 6.91 to
1 on white and 6.12 on Organic Cream: it passes as text, as a link, and as a button label everywhere
the page is light. Every pale pairing roughly doubles.

**Three things the deeper green does not fix, and one it makes worse.**

1. **Do not set Food Web Green as type or a hairline directly on the dark colours.** Against Ground,
   Moss, Scope and Ink it lands between 1.7 and 2.4 to 1, where Current Green was 3.9 to 5.5. The
   green is not used as text on dark grounds anywhere on the site today, so nothing breaks, but the
   dark footer and the overlay menu need white or Sage, not green. `site.css` already does this, with
   Sage documented for hover on dark. Worth writing into the guide as a rule rather than leaving it to
   memory.
2. **Legacy Purple is the one to watch, at 1.03 to 1.** Food Web Green and Legacy Purple have all but
   identical luminance. Side by side they read as two colours to most people and as one flat shape in
   greyscale, in a black-and-white photocopy, and to some colour-blind readers. If the two ever touch,
   they need a rule or a gap between them. This matters for the trifold, where Legacy Purple frames
   the panel two QR code and Food Web Green frames the panel six one; they are on different panels, so
   nothing touches, but it is worth knowing before anyone puts them next to each other.
3. **Olive at 1.19 and Ink Faint at 1.21 have the same problem.** Olive is documented for line accents
   and icon strokes, so an olive rule drawn on a Food Web Green field will not be visible. Use white or
   Glow on green instead.
4. **Education Blue barely moves, 1.44 to 1.63.** Green and blue at this depth sit very close. They
   work as adjacent fields, as in the sheets, but a blue label on a green ground would not read either
   way. Not caused by the change; it was already true.

## Worth deciding

- The pale blue in the current slide: name it and give it a role, or drop it.
- Whether the "never green type on Ground, Moss, Scope or Ink" rule goes into `docs/brand-guide.html`
  alongside the four restrictions already there (cream is a shape, Legacy Purple is restricted,
  Green Legacy is decorative, Harvest Gold is for Donate).
- The gold on the current slide reads a little warmer than `--gold` #C9A227. These sheets use the
  token value. Worth checking whether the deck has drifted from it.
- Whether Green Legacy #59A66C stays in the palette at all once Food Web Green takes the working
  role. It is still listed as a decorative colour; if nothing uses it, it can come out.
